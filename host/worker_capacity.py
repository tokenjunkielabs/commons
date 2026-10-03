#!/usr/bin/env python3
"""Print a read-only snapshot of memory limits and selected filesystem capacity."""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

SCHEMA = "commons.worker_capacity/v1"


def _now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _error(exc):
    return {"kind": type(exc).__name__, "errno": getattr(exc, "errno", None)}


def _nonnegative(raw):
    if not re.fullmatch(r"[0-9]+", raw):
        raise ValueError("expected a nonnegative kernel counter")
    return int(raw)


def _host_memory():
    result = {"source": "/proc/meminfo", "total_bytes": None, "available_bytes": None}
    try:
        wanted = {"MemTotal": "total_bytes", "MemAvailable": "available_bytes"}
        for line in Path(result["source"]).read_text(encoding="ascii").splitlines():
            key, _, raw = line.partition(":")
            if key in wanted:
                value, unit = raw.split()
                if unit != "kB":
                    raise ValueError("unexpected memory unit")
                result[wanted[key]] = _nonnegative(value) * 1024
        result["status"] = "ok" if all(result[key] is not None for key in wanted.values()) else "partial"
    except (OSError, UnicodeError, ValueError) as exc:
        result.update(status="unavailable", error=_error(exc))
    return result


def _unescape_mount(value):
    return re.sub(r"\\([0-7]{3})", lambda match: chr(int(match[1], 8)), value)


def _cgroup_location():
    membership = None
    for line in Path("/proc/self/cgroup").read_text(encoding="utf-8").splitlines():
        if line.startswith("0::"):
            membership = PurePosixPath(line[3:])
            break
    if membership is None:
        raise ValueError("no cgroup v2 membership")
    if not membership.is_absolute() or ".." in membership.parts:
        raise ValueError("unresolvable cgroup membership")
    candidates = []
    for line in Path("/proc/self/mountinfo").read_text(encoding="utf-8").splitlines():
        left, separator, right = line.partition(" - ")
        fields = left.split()
        if not separator or not right.startswith("cgroup2 ") or len(fields) < 5:
            continue
        root = PurePosixPath(_unescape_mount(fields[3]))
        mount = Path(_unescape_mount(fields[4]))
        if membership.is_relative_to(root):
            current = mount / str(membership.relative_to(root))
            candidates.append((len(root.parts), str(mount), mount, current))
    if not candidates:
        raise ValueError("no visible cgroup v2 mount matches membership")
    # A subtree mount is more specific than another view of the same hierarchy.
    _, _, mount, current = max(candidates, key=lambda item: item[:2])
    return mount, current, str(membership)


def _pairs(file):
    result = {}
    for line in file.read_text(encoding="ascii").splitlines():
        key, value = line.split()
        if key in result:
            raise ValueError("duplicate kernel counter")
        result[key] = _nonnegative(value)
    return result


def _cgroup_memory():
    result = {"status": "unavailable", "scope": "visible_cgroup_v2_ancestors",
              "levels": [], "smallest_observed_headroom_bytes": None}
    try:
        mount, current, membership = _cgroup_location()
    except (OSError, UnicodeError, ValueError) as exc:
        result["error"] = _error(exc)
        return result
    result.update(mountpoint=str(mount), membership=membership)
    finite_headrooms = []
    directory = current
    while True:
        row = {"directory": str(directory), "current_bytes": None,
               "max_bytes": None, "max_status": "unavailable",
               "high_bytes": None, "high_status": "unavailable",
               "headroom_bytes": None, "errors": {}}
        for filename, key in (("memory.current", "current"),
                              ("memory.max", "max"), ("memory.high", "high")):
            try:
                raw = (directory / filename).read_text(encoding="ascii").strip()
                if key != "current" and raw == "max":
                    row[key + "_status"] = "unlimited"
                else:
                    row[key + "_bytes"] = _nonnegative(raw)
                    if key != "current":
                        row[key + "_status"] = "finite"
            except (OSError, UnicodeError, ValueError) as exc:
                row["errors"][filename] = _error(exc)
        if row["current_bytes"] is not None and row["max_status"] == "finite":
            row["headroom_bytes"] = max(0, row["max_bytes"] - row["current_bytes"])
            row["over_limit_bytes"] = max(0, row["current_bytes"] - row["max_bytes"])
            finite_headrooms.append(row["headroom_bytes"])
        result["levels"].append(row)
        if directory == mount:
            break
        directory = directory.parent
    result["smallest_observed_headroom_bytes"] = min(finite_headrooms) if finite_headrooms else None
    result["status"] = "ok" if all(not row["errors"] for row in result["levels"]) else "partial"
    for filename, key in (("memory.events", "events"), ("memory.stat", "stat_bytes")):
        try:
            values = _pairs(current / filename)
            if key == "stat_bytes":
                values = {name: values[name] for name in
                          ("anon", "file", "shmem", "kernel", "inactive_file") if name in values}
            result[key] = values
        except (OSError, UnicodeError, ValueError) as exc:
            result[key] = None
            result.setdefault("errors", {})[filename] = _error(exc)
            result["status"] = "partial"
    return result


def _filesystem(value):
    result = {"requested_path": value, "available_bytes": None,
              "total_bytes": None, "inodes_available": None, "inodes_total": None}
    try:
        path = Path(value).expanduser().resolve(strict=True)
        usage = shutil.disk_usage(path)
        result.update(path=str(path), status="ok",
                      available_bytes=usage.free, total_bytes=usage.total)
        if hasattr(os, "statvfs"):
            stat = os.statvfs(path)
            result.update(inodes_available=stat.f_favail, inodes_total=stat.f_files)
            # Match statvfs's caller-available blocks, rather than reserved blocks.
            result["available_bytes"] = stat.f_bavail * stat.f_frsize
        else:
            result["inode_status"] = "unavailable"
    except (OSError, ValueError, RuntimeError) as exc:
        result.update(status="error", error=_error(exc))
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", action="append", help="existing file/directory; repeat for each output filesystem (default: current directory)")
    args = parser.parse_args(argv)
    started = _now()
    paths = args.path or ["."]
    report = {"schema": SCHEMA, "started_at": started, "host_memory": _host_memory(),
              "cgroup_memory": _cgroup_memory(),
              "filesystems": [_filesystem(value) for value in paths]}
    report["finished_at"] = _now()
    print(json.dumps(report, indent=2, ensure_ascii=True, allow_nan=False))
    return 2 if any(row["status"] == "error" for row in report["filesystems"]) else 0


if __name__ == "__main__":
    sys.exit(main())

