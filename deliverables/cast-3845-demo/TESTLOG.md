# TESTLOG — cast-3845-demo lane tooling

Build order: CAST-3845-REAL-RECEIVER-VIDEO-20261002-01
Ran: 2026-10-02 09:26 EDT (2026-10-02T13:26:37Z), stdlib Python 3 only, no network.

## Results

| Check | Command | Result |
|---|---|---|
| Byte-compile | `python3 -m py_compile make-manifest.py verify-manifest.py` | OK |
| Schema parses | `json.load` on `manifest-schema.json` | OK |
| Builder self-test | `python3 make-manifest.py --self-test` | PASS (4/4): synthetic STUB-NO-HARDWARE manifest builds and validates; stub+CAPTURED rejected; missing head_sha rejected; simulated receiver rejected |
| Verifier self-test | `python3 verify-manifest.py --self-test` | PASS: good stub manifest verifies; tampered video fails verification |

Notes:
- Self-tests use synthetic tmp bytes only; they exercise the tooling, not a real capture.
- `verify-manifest.py` imports the validator from `make-manifest.py` (single source of truth).
- No dependencies beyond the Python standard library.
