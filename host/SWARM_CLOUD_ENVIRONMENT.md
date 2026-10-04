# Shared swarm cloud environment

This setup runs the existing Commons equipment service, command center and
Deathstar workbench in the cloud workspace. Read [RULES.md](../RULES.md) and
[AGENTS.md](../AGENTS.md) before work; Bryce's live instructions take precedence.

## Start and use the environment

The checkouts are `/workspace/commons` and `/workspace/deathstar`. Private
runtime state belongs under `/workspace/shared/swarm`, outside both repositories.

Initialize the existing workspace:

```bash
python3 /workspace/commons/host/swarm_cloud_environment.py init \
  --workspace /workspace --state /workspace/shared/swarm
source /workspace/activate-swarm.sh
```

`init` installs the activation script and stable command wrappers. It writes
`/workspace/AGENTS.md` only when that file is absent; existing workspace
instructions remain in place. The activation script makes `/workspace/bin`
commands available to the current shell.

The activation script also sources existing private
`shared/swarm/toolchains/android.sh` and `languages.sh` files when present.
It captures the installed Node 24 binary directory as `SWARM_NODE24_BIN`
before those files run, and keeps Node 24 first on the default path. `init`
migrates only an exact copy of its previous generated activation template;
it preserves a differently edited activation file and reports the difference.

Start the real services under the VM's existing local Docker daemon:

```bash
swarm-env up
```

The command returns after the real endpoints respond. The owned container keeps
running after the command shell, execution session or conversation turn exits.
Repeated `up` reuses the current runtime. Changed inherited proxy, credential or
launcher configuration recreates only that runtime, retaining its private state.
No registry pull, paid service, scheduled job or model job is needed: a minimal
local image uses read-only mounts of this VM's installed toolchain and CA trust,
plus the writable cloud workspace and existing home credential facility. Service
temporary files and caches use the private state root. Inherited credential
values remain in the private runtime environment; they are not written to source,
command arguments, status responses or image layers.

Use any later worker shell to inspect the running endpoints:

```bash
source /workspace/activate-swarm.sh
swarm-env status
```

The equivalent direct command is
`python3 /workspace/commons/host/swarm_cloud_environment.py status --workspace /workspace --state /workspace/shared/swarm`.
Status reports actual endpoint responses; retain a failed response as a concrete
service condition and continue through available connected tools.

| Service | Local address | Purpose |
| --- | --- | --- |
| Commons shared equipment | `http://127.0.0.1:8878` | Existing shared tool catalog and equipment operations |
| Commons command center | `http://127.0.0.1:8890` | Existing work, coordination and observed runtime views |
| Deathstar | `http://127.0.0.1:18540` | Existing browser workbench, tools, workspaces and operation state |

These addresses are local to the VM. The runtime shares the VM's network
namespace to preserve the existing loopback-only service endpoints; remote
traffic still uses the inherited managed proxy and TLS trust. Docker restarts
the owned supervisor after a process failure and when the daemon restarts,
unless it was explicitly stopped. Ownership labels identify the exact workspace
and state root. Startup preserves unrelated containers and existing listeners.

Stop only this environment's managed services, keeping databases, logs,
worktrees, jobs and artifacts:

```bash
swarm-env down
```

`up` resumes the retained state. `serve` remains available as the original
foreground road when a retained supervisor session is wanted. Neither road
establishes survival after VM destruction; independent retained cloud storage
is still needed for that. Service startup is not provider operation completion.
`status` reports service responses separately from Docker lifecycle observations;
the direct foreground road remains usable when Docker is unavailable.

## Give workers useful, separate working space

Stable wrappers are `/workspace/bin/swarmctl`, `/workspace/bin/swarm-capacity`
and `/workspace/bin/swarm-workspace`.

`swarmctl status` reads the existing canonical task runtime, while `swarm-env`
controls this environment. `/workspace/swarm-mcp.json` connects an MCP client
to the real shared Deathstar STDIO server using `/workspace/bin/swarm-mcp`.
`swarm-current open --mode worktree --source /workspace/commons --peer NAME`
opens the existing isolated current-main source road in cloud storage.

```bash
swarm-capacity --path /workspace --path /dev/shm
swarm-workspace inspect --candidate /workspace/shared/swarm/jobs \
  --candidate /dev/shm --need-bytes 104857600
swarm-workspace create --candidate /workspace/shared/swarm/jobs \
  --candidate /dev/shm --need-bytes 104857600 --format path
```

Capacity observations are current measurements, not reservations. `/dev/shm`
consumes memory and is subject to cgroup headroom. Use each returned owned
directory for that worker's generated output and writable build state. Reuse
installed toolchain bytes when their relevant inputs match; preserve other
workers' directories, running jobs and completed execution results. The existing
[runtime bootstrap guide](../tools/runtime_artifact_bootstrap/README.md) covers
installed browsers, Android tools, workdir selection and per-invocation proxy
settings.

Keep logs, journals, local databases, private provider source, credential material
and recovery artifacts under `/workspace/shared/swarm`. Publish the actual source
change through the existing authorized repository road; private state does not
belong in commits, public dashboards or Slack posts. Use existing secure credential
facilities directly and preserve original operation IDs when recovering uncertain
provider writes.

## Use the roads that are actually available

Connected GitHub and Slack tools are separate from the local equipment service.
Inspect the current harness's complete deferred tool inventory and use discovered
native operations for authorized work. A reachable local catalog does not prove
that its GitHub, Slack, model or device backend is connected. Conversely, a local
equipment failure does not remove working connected GitHub/Slack tools or an
existing authenticated `gh` session.

Only a model or device backend that actually responds is usable. Catalog entries,
imported resources and service health describe discovery or local service state;
they do not establish a live model lane, phone, carrier, browser session or remote
device. Preserve provider errors and continue on an available road.

The existing [GitHub read coordinator](../tools/github_read_coordinator/README.md)
remains available for cooperating reads through an already configured shared
cache. This launcher does not start a new gateway on port 8766 or require a new
gateway credential. Native GitHub tools remain independently available.

Coordinate the exact operation and effective file scope through the existing
command-center/state/claims road. Preserve concurrent source changes and existing
owners, fetch before publishing, and never force-push. Run the real product on its
actual input, read its output and exit status, and complete the authorized work.
Telemetry remains passive; this environment adds no peer review, admission stage,
test suite or mock backend.

For service-specific operations, use the existing
[equipment guide](../integrations/shared_equipment/README.md),
[command-center guide](../integrations/command_center/README.md) and
`/workspace/deathstar/README.md`.

## Use the current workload's runtime

The October 4 work map covers current Android RCS/Wear/Cast and LocalDeviceAgent,
Fluxer Rust/WASM and Node, Chronicle Go, Java document tools, and Revert's pinned
Node 18 build. It comes from dated Slack workload searches and current owner
repository/PR reads. It is a selected workload map; it does not establish complete
Slack/DM/file coverage, every upstream issue, or every worker's live state.

Install or inspect the reusable compiler bytes explicitly:

```bash
python3 host/swarm_cloud_toolchains.py install
python3 host/swarm_cloud_languages.py install
source /workspace/activate-swarm.sh
```

These commands install free official runtime artifacts into private cloud state.
They retain version and digest provenance, preserve existing installations, and
reuse installed bytes. Service startup alone does not install compilers, start
model work, or repeat bounty builds. `inspect` on the Android provisioner and `status` on the language provisioner
report their local installations.

Select writable state for one worker before running a build:

```bash
eval "$(swarm-worker worker-01 --java 21 --node 24)"
# For LocalDeviceAgent or an existing JDK 17 build:
eval "$(swarm-worker worker-02 --java 17)"
# For Revert's existing Node 18 build:
eval "$(swarm-worker worker-03 --node 18)"
```

Each profile keeps Gradle, Cargo, Go, npm, uv, Android user state and temporary
files under `/workspace/shared/swarm/cache/workers/NAME`. Reusable JDKs, SDK and
compiler binaries remain shared. Source isolation still uses `swarm-current`;
the profile creates no claim, job assignment or alternative task ledger.

| Current source lane | Required runtime |
| --- | --- |
| GmsCore RCS/Wear/Cast | JDK 21 compiler, Android 35/build-tools 35.0.0, repository Gradle wrapper 8.13 |
| LocalDeviceAgent | JDK 17 compiler, project Android SDK/build tools, repository Gradle wrapper |
| Chronicle sidecar/FlightSQL | Go 1.24.4 toolchain named in `go.mod` |
| Fluxer | Node 24, project pnpm pin, Rust 1.98.1, WASM target and wasm-bindgen 0.2.128; project native build prerequisites |
| Revert Workable | Node 18.20.4, project Yarn 3.2.2; reuse the existing generated Fern artifact |
| UltimateAI document tools | JDK 21 plus Maven, LibreOffice Writer/Calc/Draw and Poppler when executing that product |

Read each current branch's own build files before running it. This environment
supplies reusable prerequisites, not a replacement for pinned source or an
accepted execution receipt. Use the existing Gradle proxy launcher with
`--refresh-env-proxy` and the system Java truststore as documented in
[GRADLE_ENV_PROXY.md](GRADLE_ENV_PROXY.md). Do not copy another invocation's proxy
endpoint or modify another worker's cache locks.

The installed system Chromium is available for actual local product work through
the existing Playwright runtime. Its usability does not establish an authenticated
provider session. Android SDK/adb does not establish a connected phone, SIM,
non-root receiver, Cast target or physical-device acceptance. A missing provider
binding remains a separate condition.

Canonical task state is retained coordination, not a census of live processes.
The October 4 read found six recoverable ACTIVE rows, including three whose
provider issues were already closed. Preserve their custody and observation
times; do not describe those rows as six running workers. Continue through the
current source, owner and provider response when selecting work. Reuse completed
source-bound builds, generated SDKs and artifacts; do not regenerate them solely
to populate an environment report.
