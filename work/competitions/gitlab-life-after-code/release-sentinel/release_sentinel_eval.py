import json
import sys
from urllib.parse import urlparse

ALLOWED_STAGES = {
    "code_review", "test", "security", "compliance", "package",
    "release", "deploy", "validate", "monitor", "rollback",
}
ALLOWED_STATUS = {"passed", "failed", "skipped"}
ALLOWED_DECISIONS = {"promote", "block"}
ALLOWED_EXPECTED = {"promote", "block"}


def https_url(value):
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def score_receipt(receipt):
    errors = []

    if receipt.get("path") not in {"A", "B"}:
        errors.append("path must be A or B")

    autonomy = receipt.get("autonomy")
    if autonomy not in {"assisted", "supervised", "hands-off"}:
        errors.append("invalid autonomy")

    expected = receipt.get("expected_outcome")
    decision = receipt.get("decision")
    if expected not in ALLOWED_EXPECTED:
        errors.append("expected_outcome must be promote or block")
    if decision not in ALLOWED_DECISIONS:
        errors.append("decision must be promote or block")

    stages = receipt.get("stages")
    if not isinstance(stages, list) or not stages:
        errors.append("stages must be a non-empty list")
        stages = []

    seen_names = set()
    seen_urls = set()
    evidenced = 0
    failed_stages = []

    for index, stage in enumerate(stages):
        if not isinstance(stage, dict):
            errors.append(f"stage[{index}] is not an object")
            continue

        name = stage.get("name")
        if name not in ALLOWED_STAGES:
            errors.append(f"stage[{index}] unsupported name {name!r}")
        elif name in seen_names:
            errors.append(f"duplicate stage {name}")
        else:
            seen_names.add(name)

        status = stage.get("status")
        if status not in ALLOWED_STATUS:
            errors.append(f"stage[{index}] invalid status {status!r}")
        elif status == "failed":
            failed_stages.append(name)

        evidence = stage.get("evidence")
        stage_urls = []
        if isinstance(evidence, list):
            for item in evidence:
                url = item.get("url") if isinstance(item, dict) else None
                if https_url(url):
                    stage_urls.append(url)
                else:
                    errors.append(f"stage[{index}] has non-HTTPS evidence")

        if not stage_urls:
            errors.append(f"stage[{index}] missing HTTPS evidence")
        else:
            evidenced += 1
            for url in stage_urls:
                if url in seen_urls:
                    errors.append(f"evidence URL reused across stages: {url}")
                seen_urls.add(url)

    approvals = receipt.get("human_approvals", [])
    if not isinstance(approvals, list):
        errors.append("human_approvals must be a list")
        approvals = []

    if autonomy == "hands-off" and approvals:
        errors.append("hands-off run contains human approvals")
    elif autonomy == "supervised":
        final = [
            item for item in approvals
            if isinstance(item, dict) and item.get("scope") == "final_outcome"
        ]
        if len(final) != 1 or len(approvals) != 1:
            errors.append("supervised run requires exactly one final_outcome approval")
    elif autonomy == "assisted":
        approved = {
            item.get("stage")
            for item in approvals
            if isinstance(item, dict) and item.get("scope") == "step"
        }
        missing = seen_names - approved
        if missing:
            errors.append(
                "assisted run missing approvals for " + ",".join(sorted(missing))
            )

    trigger = receipt.get("trigger", {})
    trigger_url = trigger.get("evidence_url") if isinstance(trigger, dict) else None
    if not https_url(trigger_url):
        errors.append("trigger evidence_url required")

    outcome = receipt.get("outcome", {})
    outcome_url = outcome.get("evidence_url") if isinstance(outcome, dict) else None
    if not https_url(outcome_url):
        errors.append("outcome evidence_url required")

    if failed_stages and decision == "promote":
        errors.append("promotion decision despite failed lifecycle stage")

    if (
        expected in ALLOWED_EXPECTED
        and decision in ALLOWED_DECISIONS
        and expected != decision
    ):
        errors.append(f"decision mismatch: expected {expected}, got {decision}")

    return {
        "valid": not errors,
        "correct_decision": (
            expected == decision
            if expected in ALLOWED_EXPECTED and decision in ALLOWED_DECISIONS
            else False
        ),
        "coverage_count": len(seen_names),
        "coverage": sorted(seen_names),
        "evidence_completeness": evidenced / len(stages) if stages else 0.0,
        "failed_stages": [name for name in failed_stages if name],
        "errors": errors,
    }


def main(path):
    with open(path, "r", encoding="utf-8") as handle:
        receipt = json.load(handle)
    result = score_receipt(receipt)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["valid"] else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1]))
