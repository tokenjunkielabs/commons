#!/usr/bin/env python3
"""Run the existing Commons and Deathstar services in one cloud workspace.

State lives outside either checkout. This launcher uses the inherited provider
sessions and proxy settings; it never copies credentials or starts model jobs.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shlex
import signal
import subprocess
import sys
import time
import urllib.error
import urllib.request

COMMONS = Path(__file__).resolve().parents[1]
LOCAL_HTTP = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def read_json(url):
    with LOCAL_HTTP.open(url, timeout=35) as response:
        return json.load(response)


def locations(args):
    workspace = args.workspace.resolve()
    state = (args.state or workspace / "shared/swarm").resolve()
    deathstar = (args.deathstar or workspace / "deathstar").resolve()
    return workspace, state, deathstar


def service_specs(args):
    workspace, state, deathstar = locations(args)
    python = sys.executable
    return [
        {"name": "equipment", "cwd": COMMONS, "url": "http://127.0.0.1:8878",
         "command": [python, "-B", "-m", "integrations.gemini_slack.peer_tool_gateway",
                     "--port", "8878", "--event-log", str(state / "equipment/events.jsonl"),
                     "--call-db", str(state / "equipment/calls.sqlite3"),
                     "--equipment-config", str(state / "equipment/equipment.json")]},
        {"name": "command-center", "cwd": COMMONS, "url": "http://127.0.0.1:8890",
         "command": [python, "-B", "-m", "integrations.command_center.server",
                     "--port", "8890", "--gateway", "http://127.0.0.1:8878",
                     "--state-dir", str(state / "command-center")]},
        {"name": "deathstar", "cwd": deathstar, "url": "http://127.0.0.1:18540",
         "command": [python, "-B", "-m", "deathstar", "serve", "--data",
                     str(state / "deathstar"), "--host", "127.0.0.1", "--port", "18540",
                     "--bind-commons", "--commons-root", str(COMMONS),
                     "--command-center-state", str(state / "command-center"),
                     "--carrier-workspace-root", str(state / "jobs")]},
    ]


def status(args):
    rows = []
    for spec in service_specs(args):
        row = {"name": spec["name"], "url": spec["url"]}
        try:
            health = read_json(spec["url"] + "/health")
            fields = ("ok", "service", "version", "tool_count", "resource_count", "storage",
                      "upstream_ok", "upstream_error", "commons_mcp", "slack_carrier")
            row.update(ok=health.get("ok") is True,
                       health={key: health[key] for key in fields if key in health})
        except (OSError, ValueError, urllib.error.URLError) as exc:
            row.update(ok=False, error=type(exc).__name__)
            if isinstance(exc, urllib.error.HTTPError):
                row["http_status"] = exc.code
        rows.append(row)
    report = {"ok": all(row["ok"] for row in rows), "services": rows}
    print(json.dumps(report, indent=2))
    return 0 if report["ok"] else 1


def write_new(path, content, executable=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_text(encoding="utf-8") != content:
            raise RuntimeError("Preserving existing different file: " + str(path))
        return
    with path.open("x", encoding="utf-8") as stream:
        stream.write(content)
    if executable:
        path.chmod(0o755)


def initialize(args):
    workspace, state, deathstar = locations(args)
    for folder in ("equipment", "command-center", "deathstar", "logs", "jobs", "workers", "artifacts", "exports", "cache"):
        (state / folder).mkdir(parents=True, exist_ok=True)
    (workspace / "bin").mkdir(parents=True, exist_ok=True)
    values = {
        "COMMONS_SWARM_URL": "http://127.0.0.1:8890",
        "COMMONS_COMMAND_CENTER_STATE": str(state / "command-center"),
        "COMMONS_WORKTREE_SOURCE": str(COMMONS),
        "COMMONS_WORKTREE_ROOT": str(state / "workers"),
        "COMMONS_CARRIER_WORKSPACE_ROOT": str(state / "jobs"),
        "SWARM_STATE_ROOT": str(state),
    }
    activation = "# Source this file in each cloud worker shell.\n"
    activation += "".join("export " + key + "=" + shlex.quote(value) + "\n" for key, value in values.items())
    activation += "export PATH=" + shlex.quote(str(workspace / "bin")) + ':"$PATH"\n'
    write_new(workspace / "activate-swarm.sh", activation)
    python = shlex.quote(sys.executable)
    def wrapper(name, script, extra=""):
        text = "#!/bin/sh\nset -eu\n. " + shlex.quote(str(workspace / "activate-swarm.sh")) + "\n"
        text += "exec " + python + " -B " + shlex.quote(str(COMMONS / script)) + extra + ' "$@"\n'
        write_new(workspace / "bin" / name, text, executable=True)
    wrapper("swarmctl", "host/swarmctl.py")
    wrapper("swarm-capacity", "host/worker_capacity.py")
    wrapper("swarm-workspace", "tools/runtime_artifact_bootstrap/workdir.py")
    wrapper("swarm-current", "host/cloud_current_worktree.py")
    wrapper("swarm-env", "host/swarm_cloud_environment.py", " --workspace " + shlex.quote(str(workspace)) + " --state " + shlex.quote(str(state)) + " --deathstar " + shlex.quote(str(deathstar)))
    mcp = "#!/bin/sh\nset -eu\n. " + shlex.quote(str(workspace / "activate-swarm.sh")) + "\n"
    mcp += "cd " + shlex.quote(str(deathstar)) + "\nexec " + python + " -B -m deathstar mcp --data " + shlex.quote(str(state / "deathstar"))
    mcp += " --bind-commons --commons-root " + shlex.quote(str(COMMONS)) + " --command-center-state " + shlex.quote(str(state / "command-center"))
    mcp += " --carrier-workspace-root " + shlex.quote(str(state / "jobs")) + '\n'
    write_new(workspace / "bin/swarm-mcp", mcp, executable=True)
    write_new(workspace / "swarm-mcp.json", json.dumps({"mcpServers": {"deathstar": {
        "command": str(workspace / "bin/swarm-mcp"), "args": []}}}, indent=2) + "\n")
    instructions = """# Swarm cloud workspace

Read `/workspace/commons/RULES.md` in full before work; live owner messages win.
Use the actual connected GitHub and Slack tools. Discover their current schemas
at work boundaries. `commons` and `deathstar` are the existing swarm projects.

Source `/workspace/activate-swarm.sh` in each worker shell. Run `swarm-env status`
for service observations and `swarm-capacity --path /workspace --path /dev/shm`
for current capacity. Health is service state, not proof of every backend.

Keep private runtime state and artifacts under `/workspace/shared/swarm`.
Use distinct cloud worktrees under its `workers` directory for concurrent source
changes; use existing canonical `state/claims` operations for actual work.
`swarm-current open --mode worktree --source /workspace/commons --peer NAME`
opens the existing current-main worktree road. Never discard another worker's
changes, force-push, or invent another task ledger or peer-review stage.

Use stable operation IDs and reconcile uncertain provider effects before retry.
Run the real product on real input. Do not add or run test batteries.
Do not put secret values or private source responses in Git or shared messages.
Do not create owner-PC clones/caches, paid compute, model jobs or recurring tasks
merely by starting this environment. Existing direct service roads stay available.

The full operating guide is `commons/host/SWARM_CLOUD_ENVIRONMENT.md`.
"""
    if not (workspace / "AGENTS.md").exists():
        write_new(workspace / "AGENTS.md", instructions)
    print(json.dumps({"ok": True, "workspace": str(workspace), "state": str(state),
                      "activation": str(workspace / "activate-swarm.sh"), "bin": str(workspace / "bin")}))
    return 0


def serve(args):
    initialize(args)
    workspace, state, deathstar = locations(args)
    if not (deathstar / "deathstar").is_dir():
        raise RuntimeError("Deathstar checkout is missing: " + str(deathstar))
    env = os.environ.copy()
    env.update(COMMONS_COMMAND_CENTER_STATE=str(state / "command-center"),
               COMMONS_CARRIER_WORKSPACE_ROOT=str(state / "jobs"),
               COMMONS_SWARM_URL="http://127.0.0.1:8890", PYTHONUNBUFFERED="1")
    children, logs = [], []
    def interrupt(signum, frame):
        raise KeyboardInterrupt
    signal.signal(signal.SIGTERM, interrupt)
    try:
        for spec in service_specs(args):
            log = (state / "logs" / (spec["name"] + ".log")).open("ab")
            logs.append(log)
            child = subprocess.Popen(spec["command"], cwd=spec["cwd"], env=env,
                                     stdout=log, stderr=subprocess.STDOUT)
            children.append((spec, child))
            print(json.dumps({"starting": spec["name"], "pid": child.pid, "url": spec["url"]}), flush=True)
            # Give the equipment process time to bind before Deathstar imports it.
            time.sleep(0.5)
        print(json.dumps({"supervising": True, "state": str(state)}), flush=True)
        while True:
            for spec, child in children:
                code = child.poll()
                if code is not None:
                    raise RuntimeError(spec["name"] + " exited " + str(code) + "; read " + str(state / "logs" / (spec["name"] + ".log")))
            time.sleep(1)
    except KeyboardInterrupt:
        return 0
    finally:
        for _, child in children:
            if child.poll() is None:
                child.terminate()
        for _, child in children:
            try:
                child.wait(timeout=10)
            except subprocess.TimeoutExpired:
                child.kill()
                child.wait()
        for log in logs:
            log.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, default=Path("/workspace"))
    parser.add_argument("--state", type=Path)
    parser.add_argument("--deathstar", type=Path)
    parser.add_argument("command", choices=("init", "serve", "status"))
    args = parser.parse_args()
    try:
        return {"init": initialize, "serve": serve, "status": status}[args.command](args)
    except (OSError, ValueError, RuntimeError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
