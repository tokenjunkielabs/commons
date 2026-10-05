# Chronicle PR #105: qualified pod-label tag compatibility

This source continuation fixes a mismatch between the Kubernetes sidecar's pod metadata and Chronicle's default point validator. A qualified pod label contains a slash. The retained sidecar prefixes that original key with `pod_label_`, but the default validator excludes slashes from tag keys. With pod labels enabled, that invalid tag is added to every collected point and `WriteBatchContext` rejects the batch before writing it.

The supplied example's `app=demo-app` label does not trigger the mismatch. This is a static finding about the reusable sidecar with qualified label input, not a claim that the example cluster failed.

## Source and attribution

- Canonical contribution: https://github.com/josedab/chronicle/pull/105
- Original bounty discussion: https://github.com/josedab/chronicle/issues/99
- Related earlier contribution, kept separate: https://github.com/josedab/chronicle/pull/96
- Source repository and branch: `woahwhattheheck/chronicle`, `bounty-11-kubernetes-sidecar`.
- Immutable source head: `fcf682d72208aaac75e34b4a2bda37d14136a225`.
- Upstream base recorded in the parent qualification: `74f8afa4f8fc3b9dec137cafc6b82a0efd51d80f`.
- Original source: https://github.com/woahwhattheheck/chronicle/blob/fcf682d72208aaac75e34b4a2bda37d14136a225/k8s_sidecar.go
- Original `k8s_sidecar.go`: `b77e7def6c108bea5b40f109d8b57469c00cb84d`, 23,354 UTF-8 bytes.
- Continued source: `source/k8s_sidecar.go`, `f1de93bc9d61402750cb5f5fee1f332b3a168de0`, 25,097 bytes.
- Patch: `qualified-pod-labels.patch`, `3ec645077de380e1b79460aaa50e79c2ee14f67d`, 3,327 bytes.
- Original Apache 2.0 license: `LICENSE`, `87304d46b7ddd7d7370cb12c6b6984d8e2d8d337`, 10,771 bytes; copyright 2024 Chronicle Contributors.

The original Chronicle contributors and PR #105 retain their source and contribution credit. This packet supplies one additional source repair and documents its limits. The modified source carries a dated change notice. No source or contribution is attributed to the author of PR #96 merely because that earlier PR covers the same example category.

## Exact producer and consumer

| Retained source at the immutable head | Blob | Relevant behavior |
|---|---|---|
| `k8s_sidecar.go` | `b77e7def6c108bea5b40f109d8b57469c00cb84d` | Default `AddPodLabels=true`; loads Downward API labels; prefixes their keys before the batch write |
| `point_validator.go` | `737770c2ca0494b2bb8cef3957253a5062e8fb3b` | Default tag-key expression `^[a-zA-Z_][a-zA-Z0-9._\\-]*$`; maximum 128 bytes per key and 64 total tags |
| `feature_manager_accessors_extended.go` | `a790394cedbca9d6c67040d5395be626e222f2ee` | `PointValidator()` lazily creates the default validator |
| `db_core.go` | `7efa34e8ba56d483d28177da1b856c7f0942f3f7` | `Open` initializes the feature manager before returning a database |
| `db_write.go` | `9095c031cb203dea463f7d26c8ef74f8c3436a0f` | `WriteBatchContext` returns a validation error before the flush |
| `examples/kubernetes-sidecar/main.go` | `6b54e5934dc1b0f53c779bc4437820371f92e58a` | Uses the default sidecar configuration and this collection/write path |

Kubernetes' primary label documentation describes an optional DNS prefix, a slash separator, and a required name of at most 63 characters:
https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/

Root read that primary documentation during this qualification. Its grammar, together with the retained producer and validator, supports the repair. No actual pod, API server, metrics endpoint, or generated sample was queried.

## Behavior of the repair

1. No-slash keys keep the exact previous `pod_label_<original-key>` form.
2. Slash-containing keys must have a nonempty, lowercase DNS-subdomain-shaped prefix of at most 253 bytes and an alphanumeric-ended name of at most 63 bytes, with only alphanumerics, dot, underscore and hyphen internally. Extra slashes, empty components and invalid characters are rejected.
3. An admitted qualified key maps to `pod_label_q_` plus the lowercase 64-hex SHA-256 of its complete original key bytes. Values are unchanged.
4. The generated Chronicle key is 76 bytes. Its suffix after `pod_label_` is 66 bytes, so it cannot equal a valid unqualified Kubernetes name, whose maximum is 63. The digest is a bounded naming convention, not authentication or a mathematical claim that hash collisions are impossible.
5. The complete mapping is staged before adding metadata to any point. Every output key is bound to its original input key. A generated/literal or generated/generated collision returns an error instead of depending on Go map iteration order or overwriting another pod label.
6. The caller records that error through the existing `recordScrapeError` path and returns before `WriteBatch`. An invalid qualified key also follows this path.
7. Namespace, pod and node tags keep their existing behavior. Pod metadata still replaces same-named sample/extra tags, as the original code did.

`GetPodInfo()` returns a live pointer with mutable maps. Arbitrary caller-injected no-slash keys are therefore deliberately distinguished from valid Kubernetes names: their existing literal spelling remains unchanged, and the existing validator still decides whether they are acceptable. An injected literal name that collides with a generated qualified name is refused explicitly.

## Preserved limits

The 64-total-tag cap and all other point validation remain unchanged. This repair does not truncate tags or values, drop overflowing metadata, relax the global validator, change metric parsing, alter target-label semantics, implement discovery or remote write, or add synchronization around the live `PodInfo` map. A caller concurrently mutating that map remains outside this change.

Tag values over the default 256-byte threshold retain the validator's existing warning behavior. Invalid no-slash keys retain its existing error behavior. Qualified keys are length-bounded before hashing; the original source keys are not retained as new data tags.

The documented example's POST `/query` calls already match the production route and JSON request shape. Its split app/sidecar containers, explicit query bind address and described port/probe edits required for ConfigMap changes were coherent in this source inspection and are not changed.

## Evidence and delivery boundary

The complete PR #105 file list contained 30 paths. The immutable recursive tree returned 1,570 entries with `truncated:false` and no `AGENTS.md` path. The parent read the matching `CONTRIBUTING.md` blob `8ff89ad3ee99e1dfc122d5acfe8d30a90384e7b1`. Production sources were inspected statically; exact preimage, postimage and patch bytes are retained.

No Go compilation, gofmt, test, race test, lint, Docker build, Kubernetes rollout, network request to the example, metrics scrape or hardware/runtime acceptance was performed. Existing tests, workflows and historical acceptance records were neither executed nor rewritten. Prior contributor validation is not presented as validation of this continuation.

This Commons packet is an attributed source continuation, not an upstream submission or a claim of bounty eligibility, priority, maintainer approval or payment. The original bounty program's first-claimant and maintainer conditions remain unresolved, and its required executable checks remain unperformed here.

## Publication custody

Operation: `CHRONICLE-105-QUALIFIED-POD-LABELS-20261005-7CA6`.

The original activity recorded the stable Commons branch `work/chronicle105-qualified-pod-labels-20261005-7ca6` before any source write: https://tokenjunkielabs.slack.com/archives/C0BS7AZ4BSL/p1791218246185579 . The packet contains only the continued source, exact patch, this guide and the unchanged original license. Native publication requests, responses and progress are retained separately; any merge/readback receipt belongs to that original activity.
