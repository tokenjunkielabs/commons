# GitHub read-rate coordinator

This is a **read-only** local coordination gateway for cooperating swarm processes that otherwise stampede GitHub with duplicate reads. It was created after live swarm work hit GitHub's secondary rate limiter while several peers were independently reading repository, pull-request, file and search state.

It does not grant, infer or proxy any GitHub write authority. The upstream provider supports `GET` only, targets the fixed `https://api.github.com` origin, rejects redirects, and exposes only the allowlisted routes in `broker.ROUTES`. There is no generic URL, HTTP-method, GraphQL, ref-write, issue-write, PR-write, merge, workflow-dispatch, visibility, billing, secrets, or administration surface.

## What it coordinates

`broker.py` stores only a credential SHA-256 fingerprint, normalized request keys, bounded cached JSON and cooldown metadata in a local SQLite database. Multiple processes sharing that database get:

- request-key singleflight so identical reads have one upstream owner;
- a short cross-process burst fence before distinct calls;
- separate primary `core`, issue/PR `search`, and `code_search` cooldowns;
- a principal-wide `secondary` cooldown when GitHub reports a secondary limit;
- persisted `Retry-After` / `X-RateLimit-Reset` backoff that never shortens an existing cooldown;
- successful final-quota responses preserved while subsequent uncached reads in that primary bucket pause until reset;
- namespace isolation after token rotation and fail-closed blocking after HTTP 401;
- bounded request, response, cache-age and cache-row surfaces;
- no stale cached success when a required refresh fails.

The coordinator is advisory infrastructure for processes that actually route reads through it. It cannot retroactively throttle unrelated clients that bypass the gateway.

GitHub distinguishes [issue/PR search and code-search rate resources](https://docs.github.com/en/rest/rate-limit/rate-limit#about-rate-limits). The local primary buckets are `issue_search` and `code_search`, so an exhausted code-search quota does not pause issue/PR discovery, or vice versa. An existing legacy `search` cooldown remains a floor for both resources until its recorded deadline expires, including late completions from legacy leases; no database rewrite is needed. Restart workers with the updated source to use the split buckets. Secondary cooldowns and the shared burst interval still apply across all routes.

Repository owner and name are normalized to lowercase before request hashing. Case variants therefore share one in-flight read and cached response, matching GitHub's repository identity. File paths, refs, branch names and search text retain their original case.

Issue-list requests also normalize GitHub's [documented defaults](https://docs.github.com/en/rest/issues/issues#list-repository-issues) (`state=open`, `sort=created`, `direction=desc`), so omitted and explicit defaults share the same in-flight read and cache entry.

Completed cache hits read the block state and cached payload in one SQLite read snapshot without taking the writer slot. JSON decoding follows the end of that snapshot. A miss, an expired entry, or `max_age_seconds=0` uses the existing write transaction and rechecks the current state before granting a lease. Expiry cleanup occurs on that path; retained entries stay bounded by the existing completion limit. A cached observation may precede a concurrent writer's commit, as with any SQLite snapshot.

Lease-acquisition decisions use the time after obtaining SQLite's write transaction, so waiting for another writer does not consume a newly issued lease or admit an expired completion. Completion retains its response-observation timestamp for cached payload freshness and provider Retry-After/reset deadlines, then measures lease expiry and remaining cooldown after the lock wait. JSON serialization and completed-response decoding remain outside the write transaction.

When a response reports both secondary throttling and an exhausted primary quota, the coordinator retains both cooldowns. The principal-wide secondary pause follows Retry-After, while the exhausted primary bucket retains the later of Retry-After and its reset deadline. A shorter secondary pause cannot reopen that primary bucket early, including after a process restart or an expired lease completion.

## Run

Set two independent secrets in the environment:

```text
GITHUB_TOKEN=<read-capable token>
GITHUB_READ_GATEWAY_KEY=<64 lowercase hex chars generated independently of the token>
```

Then start on loopback only:

```bash
python tools/github_read_coordinator/gateway.py \
  --db /private/path/github-read-coordinator.sqlite \
  --expected-login woahwhattheheck \
  --port 8766
```

The gateway authenticates the GitHub token with the read-only `/user` endpoint before serving. It listens on `127.0.0.1` and accepts only authenticated `POST /read` calls to its **local** interface; every upstream GitHub request remains a `GET`.

Example local request body:

```json
{"route":"repo.get","params":{"owner":"woahwhattheheck","repo":"commons"},"max_age_seconds":30}
```

Possible broker states are `FETCHED`, `CACHED`, `BUSY`, `COOLDOWN`, `AUTH_BLOCKED`, `UPSTREAM_ERROR`, and `DISCARDED`. Every envelope includes `provider_write_authority: false`.

For an in-flight duplicate, `BUSY` advises a one-second local cache recheck. The original lease remains active until completion or expiry, so rechecking cannot start another upstream request while its owner is fetching. Provider `COOLDOWN` responses retain their full retry/reset delay.

## Supported upstream reads

- `repo.get`
- `contents.get`
- `pull.get`
- `pull.files`
- `commit.get`
- `issues.list`
- `actions.runs`
- `search.issues`
- `search.code`

Parameters are strictly normalized. Repository paths cannot traverse; dynamic URL segments are percent-encoded; query values are generated with `urlencode`; token and arbitrary-URL overrides are impossible by schema.

## Test

From this directory:

```bash
python -m unittest -v test_broker.py test_gateway.py test_kestrel_cooldowns.py
python -O -m unittest -v test_broker.py test_gateway.py test_kestrel_cooldowns.py
python -m py_compile broker.py gateway.py test_broker.py test_gateway.py test_kestrel_cooldowns.py
```

The suite includes real eight-process singleflight, secondary-limit persistence across broker instances, primary bucket isolation, late/stale lease rejection, token-rotation behavior, payload/JSON bounds, path/header injection rejection, fixed-origin/no-redirect checks, and proof that the provider issues `GET` only.

The independent cooldown regressions also cover successful quota exhaustion across broker restarts, retained cached success, both primary-bucket directions, expired-response quota observations without stale payloads, longer existing pauses, missing-reset fallback, both retry/reset floors, exact reset resumption, and ordinary permission errors. These are offline tests with synthetic upstream responses, not a live GitHub load test.
