import hashlib
import http.server
import importlib.util
import json
import pathlib
import platform
import re
import shutil
import statistics
import struct
import subprocess
import sys
import threading
import time

ROOT = pathlib.Path(__file__).resolve().parent
HEADER_PATH = ROOT.parent / "stories260K.header"
HEADER = HEADER_PATH.read_bytes()
TOTAL = 1185376
EVENTS = []


class HeaderServer(http.server.BaseHTTPRequestHandler):
    def log_message(self, *_args):
        pass

    def do_GET(self):
        match = re.fullmatch(r"bytes=(\d+)-(\d+)", self.headers.get("Range", ""))
        if self.path != "/stories260K.gguf" or match is None:
            self.send_error(400)
            return
        begin, end = map(int, match.groups())
        if begin < 0 or end < begin or end >= len(HEADER):
            EVENTS.append({"begin": begin, "end": end, "status": 416, "bytes": 0})
            self.send_error(416, "Range exceeds the retained original header")
            return
        payload = HEADER[begin:end + 1]
        self.send_response(206)
        self.send_header("Content-Range", f"bytes {begin}-{end}/{TOTAL}")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)
        EVENTS.append({"begin": begin, "end": end, "status": 206, "bytes": len(payload)})


server = http.server.HTTPServer(("127.0.0.1", 0), HeaderServer)
threading.Thread(target=server.serve_forever, daemon=True).start()
url = f"http://127.0.0.1:{server.server_port}/stories260K.gguf"
run_root = ROOT / "runs"
run_root.mkdir(exist_ok=False)
rows = []
reference = None


def run(label, source, work):
    global reference
    stats_path = run_root / f"{label}.stats.json"
    command = [sys.executable, "-B", str(ROOT / source / "host/wb_range.py"),
               "index", url, "--work-dir", str(work), "--stats", str(stats_path)]
    before = len(EVENTS)
    started = time.perf_counter()
    process = subprocess.run(command, capture_output=True, text=True, timeout=60)
    wall = time.perf_counter() - started
    if process.returncode:
        raise RuntimeError(f"{label}: {process.returncode}: {process.stderr}")
    index = json.loads((work / "wb_range_index.json").read_text())
    index.pop("built_utc")
    canonical = json.dumps(index, sort_keys=True, separators=(",", ":"))
    if reference is None:
        reference = canonical
    if canonical != reference:
        raise RuntimeError(f"{label}: parsed index differs")
    events = EVENTS[before:]
    row = {"label": label, "source": source, "command": command,
           "exit_code": process.returncode, "stdout": process.stdout,
           "wall_seconds": wall, "stats": json.loads(stats_path.read_text()),
           "server_requests": len(events), "server_bytes": sum(e["bytes"] for e in events),
           "max_requested_byte": max((e["end"] for e in events), default=None),
           "normalized_index_sha256": hashlib.sha256(canonical.encode()).hexdigest()}
    rows.append(row)
    print(json.dumps({k: row[k] for k in ("label", "wall_seconds", "server_requests", "server_bytes")}), flush=True)


try:
    for round_number in range(3):
        order = ("baseline", "candidate") if round_number % 2 == 0 else ("candidate", "baseline")
        for source in order:
            run(f"{source}-cold-{round_number}", source, run_root / f"{source}-cold-{round_number}")
    run("baseline-warm", "baseline", run_root / "baseline-cold-0")
    run("candidate-warm", "candidate", run_root / "candidate-cold-0")
    upgrade = run_root / "candidate-upgrade"
    shutil.copytree(run_root / "baseline-cold-0", upgrade)
    run("candidate-upgrade", "candidate", upgrade)

    # Replay the first actual metadata key and following type under its exact
    # name-length limit, so the combined extent requires ordinary split reads.
    sys.path.insert(0, str(ROOT / "candidate/host"))
    key_length = struct.unpack("<Q", HEADER[24:32])[0]
    limits = []
    for source in ("baseline", "candidate"):
        spec = importlib.util.spec_from_file_location(f"wb_{source}", ROOT / source / "host/wb_range.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        reader = module.RangeReader(url, run_root / f"{source}-field-limit", limit=max(8, key_length))
        cursor = module._GgufCursor(reader)
        cursor.pos = 24
        before = len(EVENTS)
        value = (cursor.string(), cursor.unpack("<I")[0]) if source == "baseline" else cursor.string_with_u32()
        limits.append({"source": source, "limit": max(8, key_length), "value": value,
                       "requests": EVENTS[before:], "stats": reader.stats, "final_cursor": cursor.pos})
    if limits[0]["value"] != limits[1]["value"] or limits[0]["requests"] != limits[1]["requests"]:
        raise RuntimeError("Original metadata-field fallback differs")
    summary = {source: statistics.median(r["wall_seconds"] for r in rows
                                        if r["source"] == source and "-cold-" in r["label"])
               for source in ("baseline", "candidate")}
    result = {"operation": "WB-GGUF-NAME-FIELD-GROUPING-20261004-SABLE162F",
              "measurement": "Complete native CLI over retained original header via loopback HTTP206; no tensor bytes or model inference",
              "python": sys.version, "platform": platform.platform(), "filesystem": "tmpfs",
              "header": {"path": str(HEADER_PATH), "bytes": len(HEADER),
                         "sha256": hashlib.sha256(HEADER).hexdigest(), "original_total_bytes": TOTAL,
                         "source": "https://huggingface.co/ggml-org/tiny-llamas/resolve/def3e2dd70df35ecbf6403ea347de4c5977220c1/stories260K.gguf"},
              "sources": {}, "cold_median_wall_seconds": summary,
              "cold_wall_reduction_percent": 100 * (1 - summary["candidate"] / summary["baseline"]),
              "runs": rows, "actual_field_limit_replay": limits,
              "all_normalized_indexes_equal": True, "no_os_cache_flush": True,
              "cold_application_caches": True, "warmup_rounds": 0}
    for source in ("baseline", "candidate"):
        result["sources"][source] = {}
        for relative in ("host/wb_range.py", "host/wb_metrics.py"):
            raw = (ROOT / source / relative).read_bytes()
            result["sources"][source][relative] = {"sha256": hashlib.sha256(raw).hexdigest(),
                "git_blob_sha": hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()}
    (ROOT / "measurement.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"cold_medians": summary, "reduction_percent": result["cold_wall_reduction_percent"],
                      "field_limit": limits[1]["limit"], "field_value": limits[1]["value"]}), flush=True)
finally:
    server.shutdown()
    server.server_close()
