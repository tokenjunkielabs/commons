# Agenthon 2026 Track 1 baseline solver

Public-safe baseline carrier for the Agenthon 2026 Track 1 coding workflow.

## Contents

- `agent.py`: House-backed solve CLI using only bounded task context and local task data.
- `test_agent.py`: focused offline fake-House checks covering the two-call success path, one concrete repair path, and forbidden evaluation-material access.
- `Dockerfile`: Python 3.13 runtime carrier.
- `requirements.txt`: scientific/data dependencies available to generated solutions.

## Execution contract

```bash
python agent.py solve --task-dir /input --out /app/output
```

The solver uses the injected `MODEL_ENDPOINT`, `MODEL_NAME`, and `MODEL_TOKEN` variables and calls the House chat-completions endpoint. The normal path uses two House calls (plan + implementation); one additional repair call is permitted only after a concrete local compile/runtime failure.

The carrier explicitly excludes checks/reference/oracle/expected/reward material from task context and rejects generated programs that reference verifier material, network packages, or shell-spawn helpers.

## Evidence boundary

Recovered from Slack source bank `F0C6TQ4M15H` produced by GPT-5.6 Sol / Recovery-NDJSON-003x. The source bank reported 3/3 focused `unittest` checks and `py_compile` passing before publication. Slack Canvas transport represents leading indentation with non-breaking spaces, so publication normalizes those indentation characters to ordinary ASCII spaces; focused checks are rerun on the published branch before promotion.

No registration, CodaBench upload, official House execution, public-practice pass rate, or leaderboard score is claimed by this packet.
