# Native GitHub workflow artifact retrieval

Use this route when a cloud session needs an existing Actions artifact and its local shell cannot resolve or reach GitHub. It was exercised on October 5, 2026; it is not a proposal for new infrastructure.

## Minimal route

1. Use `GitHub.fetch_workflow_run_artifacts(repo_full_name, run_id)` to locate the required artifact and record its ID, expiry, digest when present, and source/workflow provenance. Reuse a known artifact instead of dispatching another build just to retrieve it.
2. Call `GitHub.download_workflow_artifact(repo_full_name, artifact_id, file_name)`. Its client follows GitHub's temporary redirect and returns a file reference for the ZIP bytes.
3. Use the exact mounted path provided with the tool result. In this harness these files were automatically mounted; neither a local-PC request nor a second materialization step was needed. Do not invent a sandbox path from a display name.
4. Confirm the ZIP digest against the retained artifact metadata, then inspect the relevant entries. A successful download does not establish that the workflow passed, that the evidence belongs to the current PR head, or that a bounty is accepted or paid.

For example, this exact call successfully retrieved the existing Chronicle acceptance record:

```json
{
  "repo_full_name": "woahwhattheheck/chronicle",
  "artifact_id": 11298288760,
  "file_name": "chronicle106-prior-acceptance.zip"
}
```

Observed result: 50,003 bytes, 36 ZIP entries, SHA-256 `83fe86c5f837e7b04a3692214647701e36ddddb5ef28a793675121be4e9db69d`, matching the existing example README. That record is for source `a991190eef51d555c1bcaa4dacc960256797120e`, run `37189161693`; it must not be relabeled as validation of later source changes. The hosted artifact has a finite retention period, so this historical ID is an example, not a permanent dependency.

## Discovery and failure handling

When the method is missing, rediscover the GitHub tool surface alongside useful work; it was exposed during this session's later discovery. A partial tool listing is not evidence that the whole connector is read-only. Invoke only a returned schema; do not manufacture an unavailable action name.

`GitHub.fetch` is for text resources and rejects binary payloads. Do not repeatedly feed it artifact ZIP URLs or retry shell DNS failures. The native download action is distinct from `download_user_content`, which is only for GitHub private image attachments and is not a repository/artifact downloader.

Respect provider cooldowns and reuse the canonical artifact/source owner. Do not dispatch duplicate runs, rotate accounts to evade a limit, publish credentials, or turn retrieval into a work pile for the owner's PC. If the native action itself fails, record that actual error and leave the evidence unavailable rather than claiming it was inspected.

Returned temporary signed URLs are transport credentials, not durable citations: do not copy them into Slack, PRs or documentation. Cite the ordinary workflow/artifact page and stable IDs. Keep private artifact contents within their authorized audience.

## Evidence

[Executed acceptance run](https://github.com/woahwhattheheck/chronicle/actions/runs/37189161693) · [Retained artifact](https://github.com/woahwhattheheck/chronicle/actions/runs/37189161693/artifacts/11298288760) · [Source-bound acceptance record](https://github.com/woahwhattheheck/chronicle/blob/3ec9685653eef096c1af075fecc12982cda77ce6/examples/docker-compose-monitoring/README.md)
