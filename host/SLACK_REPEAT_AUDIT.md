# Slack repeat audit

`host/slack_repeat_audit.py` is a read-only diagnostic for separating repeated
Slack observations from distinct repeated sends. It never sends, edits, deletes,
suppresses, acknowledges, retries, or schedules Slack work.

## Why this exists

The recovered diagnostic was built after TITAN coordination showed clusters of
nearly identical rendered updates with distinct Slack timestamps. Identical text
alone is not enough to decide whether the cause was concurrent agents, a sender
retry, pagination overlap, or delivery-layer behavior.

Use this tool to preserve the evidence boundary before changing sender logic.

## Usage

Python 3.10+; no third-party packages or network access are required.

```bash
python host/slack_repeat_audit.py \
  --input /path/to/slack-messages.json \
  --window-seconds 2 \
  --output /tmp/slack-repeat-report.json
```

Input may be an array of Slack-style message objects or an object with a
`messages` array and optional default `channel`. Keep Slack timestamps as
strings.

```json
{
  "channel": "C123ABC",
  "messages": [
    {"user": "U123ABC", "ts": "1788826406.369419", "text": "Example update"},
    {"user": "U123ABC", "ts": "1788826406.890359", "text": "Example update"}
  ]
}
```

## Interpretation

The audit groups only compatible observations: channel, author, thread context,
subtype, content, supplied rich payloads/metadata, and edited state must agree.
It preserves distinct message IDs and reports repeated reads of the same ID
separately. Conflicting snapshots of one message ID are excluded from duplicate
send groups.

Reports omit message bodies by default, retain content hashes and source
timestamps, and use windows anchored to the first message rather than extending
a cluster indefinitely.

A repeat group is **evidence, not a root-cause verdict**. Before changing retry
or publication behavior, correlate the returned Slack timestamps with the
swarm's send operation IDs, attempt records, and connector message receipts:

- different operation IDs usually indicate independent publication attempts;
- one operation with multiple attempts and distinct Slack timestamps supports a
  retry/delivery investigation;
- one Slack timestamp observed multiple times is a read/pagination concern, not
  an independent send.

Do not add automatic suppression from text equality alone.

## Provenance

This is the byte-identical recovered CLI from
`woahwhattheheck/commons-ship-enforcer` operation
`DOT-SWARM-RECOVERY-20261004-SLACK-AUDIT`, recovery commit
`fb5219f06fb4a8c152f20a0c3c3175d868924b6b`. Original source authorship was
not recovered, so no individual author attribution is asserted here.

The retained recovery record contains the original 26-passing-test log and
bounded TITAN fixture. Those tests were not transplanted or rerun as part of
this Commons integration. The fixture was a transcription of connector-rendered
messages, not a raw Slack API capture, and did not establish sender root cause.
