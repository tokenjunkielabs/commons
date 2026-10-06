# Alexa+ MCP demo video script

Target duration: 2:40-2:55. Hard stop before 3:00.

## 0:00-0:20 — What the project is

On screen:
- web Alexa+ simulator;
- small architecture inset showing simulator -> agent -> Streamable HTTP MCP -> durable local workflow services.

Narration:
"Continuity MCP is a stateful workflow copilot. Instead of wrapping one API call, it coordinates several steps, preserves context across sessions, and recovers safely from timeouts or restarts."

Show the exact MCP protocol/version string and current git revision in a small footer.

## 0:20-0:55 — Clean orchestration

Prompt:
"Help me prepare for demo day. Create a checklist, a short milestone timeline, and a summary I can ask for later."

Show:
- tool activity condensed to readable events;
- tasks + timeline + note appear;
- workflow status reaches COMPLETED;
- evidence panel shows zero retries and zero duplicate side effects.

Do not linger on logs.

## 0:55-1:35 — Failure recovery

Enable the deterministic one-shot timeout injection.

Run the fixed timeout fixture.

Show:
- first mutating call times out;
- bounded retry uses the same operation id;
- exactly one side effect exists;
- workflow status records RECOVERED -> COMPLETED;
- evidence panel exposes retry_count=1 rather than hiding it.

Narration:
"The retry is visible and bounded. Idempotency is what prevents a timeout from duplicating a real-world action."

## 1:35-2:10 — Restart and resume

Start the restart fixture.

After one committed step:
- terminate/restart the server;
- reopen the simulator;
- ask "Continue where we left off."

Show:
- persisted workflow is rediscovered;
- committed work is not replayed;
- remaining work completes;
- resumed=true appears in the receipt.

Narration:
"The workflow state lives beyond the conversation process, so a later session can continue rather than start over."

## 2:10-2:35 — Benchmarks

Open the exact benchmark summary for this revision.

Show:
- case count;
- completion rate;
- injected-failure recovery rate;
- restart/resume success rate;
- duplicate-side-effect cases;
- retry-budget violations;
- p50/p95 latency.

Only state measured values that exist in the exact result artifact.

## 2:35-2:50 — Competition fit

Show:
- self-hosted MCP server;
- MCP 2025-11-25+;
- Streamable HTTP;
- local setup command;
- repository review configuration.

Narration:
"The submission uses the Alexa+ self-hosted MCP path and our own simulator, so it does not depend on gated Alexa+ preview tooling."

## 2:50-2:55 — Finish

"Continuity MCP makes long, failure-prone workflows resumable, inspectable, and safe to retry."

## Recording constraints

- keep the final video under three minutes;
- show the project actually functioning;
- publish the final video only when the account owner authorizes submission work;
- use no copyrighted music or unlicensed third-party assets;
- keep private internal coordination and non-public data out of the recording;
- if a benchmark value is not tied to the exact demo revision, do not say it.
