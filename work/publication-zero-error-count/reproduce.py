"""Focused reproduction for literal zero-error publication reports; no provider calls."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
import types

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "integrations" / "commons_publication_hooks"))
import commons_publication_policy as policy
import hook
from integrations.shared_equipment import github_publication

# Exact approved description retained from gateway issue 1521, before rewording.
ORIGINAL = "Closes #99\n\n## Summary\n\nImplements bounty entry 11, “Kubernetes sidecar example,” from `docs/BOUNTY_PROGRAM.md`: deploy Chronicle beside an application, scrape its Prometheus metrics over the pod's shared localhost network, and tag the stored series with Downward API metadata.\n\nThe example now runs as separate application and sidecar components in the Deployment. Previously the application container only slept, while the local demo always started both components in one process.\n\n## Changes\n\n- Add explicit `app` and `sidecar` modes while retaining `demo` as the default local mode. The sidecar uses `chronicle.NewK8sSidecar`, exposes health/stats and the Chronicle query API, and shuts down on SIGINT/SIGTERM.\n- Add an example-specific Dockerfile and run the same non-root image in both Deployment containers, each with its own mode. Connect the existing ConfigMap to runtime flags for the metrics endpoint, scrape timing, health port and retention.\n- Preserve pod, namespace and node metadata from the Downward API. The Deployment supplies writable database storage and a read-only pod-info mount.\n- Document building/loading the image, applying the manifests, checking collection and querying stored `demo_up` points. Preserve the existing links from `examples/README.md` and `docs/K8S_DEPLOYMENT.md`.\n- Add focused example tests for mode/flag validation, metrics responses, port conflicts and shutdown, and preservation of supplied pod metadata.\n\n## Validation\n\nRecorded local validation for `9904db19571e9d52d1bb8a434ff8ab50bbdbe7dc` on October 3, 2026:\n\n- Go build, static build, `go test ./...` and `go vet ./...` passed in `examples/kubernetes-sidecar`.\n- Separate application and sidecar processes using the Deployment arguments collected and wrote 8 points over 2 scrapes with 0 scrape errors, correct pod tags and clean SIGTERM exits. The default combined demo also worked.\n\nThe Docker image build and Kubernetes cluster rollout have not been executed. Image build/load and cluster verification commands are documented in the example README.\n\nThe current upstream CI, Benchmarks, Dependency Review and Performance Regression runs are `action_required`; maintainer approval and required checks remain pending. This description update does not change source or claim a new validation run.\n\nThis continues the existing PR for #99 and bounty entry 11. Acceptance and any bounty award remain the maintainer's decision."

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline-ref", help="Optional existing source commit for before/after")
    args = parser.parse_args()
    cases = [
        ("original", ORIGINAL, True),
        ("word_zero", ORIGINAL.replace("0 scrape errors", "zero scrape errors"), True),
        ("word_no", ORIGINAL.replace("0 scrape errors", "no scrape errors"), True),
        ("numeric_direct", ORIGINAL.replace("0 scrape errors", "0 errors"), True),
        ("existing_negation", ORIGINAL.replace("0 scrape errors", "no errors during scraping"), True),
        ("positive_count", ORIGINAL.replace("0 scrape errors", "1 scrape errors"), False),
        ("trailing_zero", ORIGINAL.replace("0 scrape errors", "10 scrape errors"), False),
        ("decimal_suffix", ORIGINAL.replace("0 scrape errors", "1.0 scrape errors"), False),
        ("signed_zero", ORIGINAL.replace("0 scrape errors", "-0 scrape errors"), False),
        ("negated_count", ORIGINAL.replace("0 scrape errors", "not 0 scrape errors"), False),
        ("bound", ORIGINAL.replace("0 scrape errors", "at least 0 scrape errors"), False),
        ("later_error", ORIGINAL.replace("0 scrape errors", "0 scrape errors but 1 scrape errors"), False),
        ("later_disagreement", ORIGINAL + "\n\nWe disagree with the reported result.", False),
        ("non_report", "Build passed with 0 scrape errors.", False),
    ]
    js_runner = """
const fs = require("node:fs");
const vm = require("node:vm");
const input = JSON.parse(fs.readFileSync(0, "utf8"));
const result = input.sources.map(source => {
  const sandbox = {module: {exports: {}}};
  vm.runInNewContext(source, sandbox);
  return input.bodies.map(body => sandbox.module.exports.checkPublication(body).allowed);
});
process.stdout.write(JSON.stringify(result));
"""
    sources = [(ROOT / path).read_text() for path in
               ("commons-publication-policy.cjs", "commons-publication-policy.js")]
    assert sources[0] == sources[1], "Current root JavaScript companions differ"
    baseline = None
    if args.baseline_ref:
        def prior(path):
            return subprocess.check_output(
                ["git", "-C", str(ROOT), "show", args.baseline_ref + ":" + path], text=True)
        before = types.ModuleType("before_publication_policy")
        exec(compile(prior("commons_publication_policy.py"), "<baseline>", "exec"), before.__dict__)
        baseline = before.check_publication(ORIGINAL)
        assert baseline["allowed"] is False and baseline["rule"] == "unfavorable_finding"
        sources.append(prior("commons-publication-policy.cjs"))

    bodies = [body for _, body, _ in cases]
    javascript = json.loads(subprocess.check_output(
        ["node", "-e", js_runner],
        input=json.dumps({"sources": sources, "bodies": bodies}), text=True))
    for index, (name, body, expected) in enumerate(cases):
        assert policy.check_publication(body)["allowed"] == expected, ("python", name)
        event = {"tool_name": "mcp__codex_apps__github_update_pull_request",
                 "tool_input": {"repository_full_name": "josedab/chronicle",
                                "pr_number": 105, "body": body}}
        verdict = hook.publication_verdict(event)
        assert (verdict is None or verdict.get("allowed") is True) == expected, ("hook", name)
        try:
            github_publication._preflight("pull.update", {"body": body})
            allowed = True
        except github_publication.EquipmentError as error:
            assert error.code == "commons_publication_terms", (name, error.code)
            assert error.delivered is False and error.incident is False
            allowed = False
        assert allowed == expected, ("equipment", name)
        assert javascript[0][index] == expected, ("cjs", name)
        assert javascript[1][index] == expected, ("js", name)
    if baseline is not None:
        assert javascript[2][0] is False, "Original JavaScript rejection was not reproduced"

    # A zero count never overrides the separately mapped outward identity rule.
    identity_body = ORIGINAL + "\n\nCodex status."
    verdict = hook.publication_verdict({
        "tool_name": "mcp__codex_apps__github_update_pull_request",
        "tool_input": {"body": identity_body}})
    assert verdict["code"] == "outbound_identity_attribution"
    assert verdict["delivered"] is False and verdict["incident"] is False
    try:
        github_publication._preflight("pull.update", {"body": identity_body})
    except github_publication.EquipmentError as error:
        assert error.code == "outbound_identity_attribution"
        assert error.delivered is False and error.incident is False
    else:
        raise AssertionError("Equipment identity check unexpectedly allowed the body")
    print(json.dumps({"cases": len(cases), "paths": ["python", "native_hook", "equipment", "cjs", "js"],
                      "identity_holds": 2, "baseline_original_allowed": None if baseline is None else False,
                      "candidate_original_allowed": True, "provider_calls": 0}))

if __name__ == "__main__":
    main()

