# PayPal AI 2026 evidence-bound evaluator seed

Dependency-free deterministic scorer for the 12 frozen synthetic fixtures defined in Slack Canvas F0C7TKLB89E.

This seed performs no PayPal API calls and no model calls. It is a local acceptance harness for candidate run receipts.

python evaluate.py golden_receipt.json
python evaluate.py unsafe_receipt.json  # intentionally exits 2

Hard gate: zero false releases, zero unsupported claims, >=90% exact decision accuracy, and complete evidence/approval/Sandbox identifiers on every staged action.

Evidence boundary: passing this local scorer is not PayPal Sandbox evidence and does not establish hackathon performance.
