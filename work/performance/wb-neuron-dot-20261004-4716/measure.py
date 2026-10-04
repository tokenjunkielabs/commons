#!/usr/bin/env python3
"""Compare complete WB-RANGE neuron/archive CLIs on a pinned original GGUF.

Stdlib only. Each timed sample starts a fresh Python process. The model is
served only over loopback; warm samples must perform zero HTTP requests.
"""
from __future__ import annotations

import argparse
import hashlib
import http.server
import json
import os
from pathlib import Path
import platform
import re
import resource
import shutil
import statistics
import subprocess
import sys
import tempfile
import threading
import time


MODEL_SHA256 = "047bf46455a544931cff6fef14d7910154c56afbc23ab1c5e56a72e69912c04b"
MODEL_URL = "https://huggingface.co/ggml-org/tiny-llamas/resolve/def3e2dd70df35ecbf6403ea347de4c5977220c1/stories260K.gguf"


def identity(path: Path) -> dict:
    raw = path.read_bytes()
    return {"path": str(path), "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "git_blob_sha": hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()}


def event_summary(events: list[dict]) -> dict:
    encoded = json.dumps(events, sort_keys=True, separators=(",", ":")).encode()
    return {"requests": len(events), "body_bytes": sum(e["bytes"] for e in events),
            "ordered_requests_sha256": hashlib.sha256(encoded).hexdigest(),
            "statuses": sorted(set(e["status"] for e in events)),
            "first_requested_byte": min((e["begin"] for e in events), default=None),
            "last_requested_byte": max((e["end"] for e in events), default=None)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline-root", type=Path, required=True)
    parser.add_argument("--candidate-root", type=Path, required=True)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--pairs", type=int, default=9)
    parser.add_argument("--warmups", type=int, default=2, help="Excluded warmup runs per source")
    parser.add_argument("--timeout", type=float, default=60)
    args = parser.parse_args()
    if args.pairs < 1 or args.warmups < 0 or args.timeout <= 0:
        parser.error("pairs and timeout must be positive; warmups must be nonnegative")
    if args.output.exists():
        parser.error("output already exists; choose a new receipt path")

    roots = {"baseline": args.baseline_root.resolve(), "candidate": args.candidate_root.resolve()}
    sources = {label: {name: identity(root / "host" / name)
                       for name in ("wb_range.py", "wb_metrics.py")}
               for label, root in roots.items()}
    if sources["baseline"]["wb_range.py"]["sha256"] != sources["candidate"]["wb_range.py"]["sha256"]:
        raise ValueError("caller/transport source must be identical in this scoring comparison")
    model = args.model.resolve().read_bytes()
    if hashlib.sha256(model).hexdigest() != MODEL_SHA256 or len(model) != 1185376:
        raise ValueError("model bytes do not match the retained original stories260K identity")
    args.work_dir.mkdir(parents=True, exist_ok=True)
    run_dir = Path(tempfile.mkdtemp(prefix="neuron-dot-", dir=args.work_dir.resolve()))
    events: list[dict] = []

    class ModelHandler(http.server.BaseHTTPRequestHandler):
        def log_message(self, *_args):
            pass

        def do_GET(self):
            match = re.fullmatch(r"bytes=(\d+)-(\d+)", self.headers.get("Range", ""))
            if self.path != "/stories260K.gguf" or match is None:
                self.send_error(400)
                return
            begin, end = map(int, match.groups())
            if end < begin or end >= len(model):
                events.append({"begin": begin, "end": end, "status": 416, "bytes": 0})
                self.send_error(416)
                return
            payload = model[begin:end + 1]
            self.send_response(206)
            self.send_header("Content-Range", f"bytes {begin}-{end}/{len(model)}")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            events.append({"begin": begin, "end": end, "status": 206, "bytes": len(payload)})

    server = http.server.HTTPServer(("127.0.0.1", 0), ModelHandler)
    server_thread = threading.Thread(target=server.serve_forever, kwargs={"poll_interval": 0.05})
    server_thread.start()
    url = f"http://127.0.0.1:{server.server_port}/stories260K.gguf"
    reference: bytes | None = None
    rows = []
    report = {"schema": "wb-neuron-dot-measurement/v1", "status": "RUNNING",
              "model": {"path": str(args.model.resolve()), "bytes": len(model),
                        "sha256": MODEL_SHA256, "source": MODEL_URL},
              "sources": sources, "benchmark": identity(Path(__file__).resolve()),
              "environment": {"python": sys.version, "executable": sys.executable,
                              "platform": platform.platform(), "machine": platform.machine(),
                              "cpu_count": os.cpu_count(), "run_directory": str(run_dir)},
              "workload": {"operation": "metric neurons -> archive", "units": 512,
                           "vocab_sample": 1200, "pairs": args.pairs,
                           "warmups_per_source": args.warmups, "cold_pairs": 1},
              "limits": ["Warm timing includes fresh Python startup/imports, index and cache reads, decoding, metric scoring, archive writes, and stdout JSON.",
                         "Child CPU is user plus system CPU from RUSAGE_CHILDREN; it excludes the benchmark's loopback server and comparison work.",
                         "Cold means model-weight ranges absent from the application cache; the index and its header cache are prepared identically first.",
                         "Warm application caches and operating-system caches are not flushed. Shared-host scheduling can affect wall time.",
                         "The single cold pair is an observation, not a repeatable cold-latency estimate.",
                         "This inspects stored original-model weights. It performs no model inference, WAN timing, Android/device operation, or payment."],
              "runs": rows}

    def invoke(label: str, phase: str, pair: int, command: list[str]) -> tuple[dict, dict]:
        before_events = len(events)
        before_cpu = resource.getrusage(resource.RUSAGE_CHILDREN)
        started = time.perf_counter_ns()
        process = subprocess.run(command, capture_output=True, timeout=args.timeout)
        wall_ns = time.perf_counter_ns() - started
        after_cpu = resource.getrusage(resource.RUSAGE_CHILDREN)
        user = after_cpu.ru_utime - before_cpu.ru_utime
        system = after_cpu.ru_stime - before_cpu.ru_stime
        row = {"source": label, "phase": phase, "pair": pair, "command": command,
               "exit_code": process.returncode, "wall_ns": wall_ns,
               "child_user_cpu_seconds": user, "child_system_cpu_seconds": system,
               "child_cpu_seconds": user + system, "http": event_summary(events[before_events:]),
               "stdout_sha256": hashlib.sha256(process.stdout).hexdigest()}
        rows.append(row)
        if process.returncode:
            row["stderr"] = process.stderr.decode(errors="replace")
            raise RuntimeError(f"{label}/{phase}/{pair} exited {process.returncode}: {row['stderr']}")
        print(json.dumps({k: row[k] for k in ("source", "phase", "pair", "wall_ns", "child_cpu_seconds", "http")}), flush=True)
        return row, json.loads(process.stdout)

    def metric(label: str, phase: str, pair: int, work: Path, index: Path) -> None:
        nonlocal reference
        command = [sys.executable, "-B", str(roots[label] / "host/wb_range.py"),
                   "metric", str(index), "neurons", "--units", "512",
                   "--vocab-sample", "1200", "--work-dir", str(work)]
        row, output = invoke(label, phase, pair, command)
        manifest = json.loads((work / "archive/manifest.json").read_text())
        entry = next(e for e in manifest["entries"] if e["id"] == output["entry_id"])
        payload = (work / "archive" / entry["blob"]).read_bytes()
        digest = hashlib.sha256(payload).hexdigest()
        if digest != entry["sha256"] or len(payload) != entry["bytes"]:
            raise RuntimeError("archive payload does not match its native manifest")
        if json.loads(payload) != output["result"]:
            raise RuntimeError("archived metric differs from the complete CLI result")
        if reference is None:
            reference = payload
            report["reference_metric_result"] = json.loads(payload)
        if payload != reference:
            raise RuntimeError(f"complete archived payload differs for {label}/{phase}/{pair}")
        row["archive_payload"] = {"bytes": len(payload), "sha256": digest, "byte_equal": True}
        row["result_shape"] = {k: output["result"][k] for k in ("neurons", "vocab_rows_scanned", "tensor")}
        if phase in ("warmup", "warm") and row["http"]["requests"]:
            raise RuntimeError("expected warm metric execution to make zero HTTP requests")

    try:
        prepared = run_dir / "prepared-index"
        index = prepared / "wb_range_index.json"
        invoke("baseline", "index-setup", 0,
               [sys.executable, "-B", str(roots["baseline"] / "host/wb_range.py"),
                "index", url, "--work-dir", str(prepared)])
        report["frozen_index"] = identity(index)
        work_dirs = {label: run_dir / label for label in roots}
        for label, work in work_dirs.items():
            shutil.copytree(prepared / "cache", work / "cache")
            metric(label, "cold", 0, work, index)
        cold = [r for r in rows if r["phase"] == "cold"]
        if cold[0]["http"] != cold[1]["http"]:
            raise RuntimeError("cold metric HTTP request sequence or body counts changed")
        for phase, count in (("warmup", args.warmups), ("warm", args.pairs)):
            for pair in range(count):
                order = ("baseline", "candidate") if pair % 2 == 0 else ("candidate", "baseline")
                for label in order:
                    metric(label, phase, pair, work_dirs[label], index)
        for label, root in roots.items():
            for name, expected in sources[label].items():
                if identity(root / "host" / name) != expected:
                    raise RuntimeError(f"source changed during measurement: {label}/{name}")
        warm = [r for r in rows if r["phase"] == "warm"]
        summary = {}
        for field in ("wall_ns", "child_cpu_seconds"):
            medians = {label: statistics.median(r[field] for r in warm if r["source"] == label) for label in roots}
            pairs = [{label: next(r[field] for r in warm if r["source"] == label and r["pair"] == pair)
                      for label in roots} for pair in range(args.pairs)]
            summary[field] = {"medians": medians,
                              "candidate_reduction_percent": 100 * (1 - medians["candidate"] / medians["baseline"]),
                              "candidate_paired_wins": sum(p["candidate"] < p["baseline"] for p in pairs),
                              "pairs": pairs}
        report.update(status="PASS", warm_summary=summary,
                      all_archived_metric_payloads_byte_equal=True,
                      cold_http_sequence_and_bytes_equal=True, warm_http_requests=0)
        print(json.dumps({"status": report["status"], "warm_summary": summary}), flush=True)
    except BaseException as exc:
        report.update(status="FAILED", error=f"{type(exc).__name__}: {exc}")
        raise
    finally:
        server.shutdown()
        server.server_close()
        server_thread.join()
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
