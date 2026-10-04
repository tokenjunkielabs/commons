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

Start the real services in a retained foreground execution session:

```bash
swarm-env serve
```

Use another shell to inspect the running endpoints:

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

These addresses are local to the VM. Services continue while their retained
foreground supervisor session and the VM remain alive. This setup does not
establish survival after VM termination. On recovery, reuse the retained private
state and run `serve`, then inspect `status`; service startup is not provider
operation completion.

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
