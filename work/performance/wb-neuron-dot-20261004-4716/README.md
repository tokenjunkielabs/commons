# Original-model neuron scoring performance

`neuron_cleanliness` now uses `sum(map(operator.mul, u, v))` for each
neuron/token dot product. This removes the per-product Python generator while
retaining the same multiplication order and built-in `sum`. Normalization,
bounded top-k selection, ties, nonfinite handling, and returned fields are
unchanged. The production change is one stdlib import and one scoring line.

## Complete CLI result — 4 October 2026

The actual `wb_range.py metric ... neurons` command inspected the original
`stories260K.gguf`: 172 directions from `blk.0.ffn_down.weight`, each 64 values
wide, against 512 vocabulary rows. Every sample started a fresh Python process
and included source imports, frozen-index/cache reads, decoding, scoring,
native archive publication, and stdout JSON.

One excluded warmup per source preceded three alternating warm-cache pairs.
All three pairs improved in both measures:

| Complete warm-cache command | Baseline median | Updated median | Reduction |
| --- | ---: | ---: | ---: |
| Elapsed wall time | 492.280 ms | 307.321 ms | 37.57% |
| Child process user + system CPU | 491.836 ms | 307.016 ms | 37.58% |

All ten metric/archive calls (two cold, two warmup, six timed warm) produced
the same complete **4,771-byte** archived metric payload, SHA-256
`4cd30b02532300275f0f7bc26263db93af3b7d87fffcf9a5673e023a4245d707`.
The runner reads each native archive manifest and payload, verifies their
size/digest, compares the payload to the complete CLI result, and compares
payload bytes across every invocation.

Each cold metric command made exactly **65 HTTP requests / 175,104 body bytes**,
with the same ordered range-request hash. The single cold pair measured
673.921 → 451.985 ms wall time; this is one observation, not a repeatable cold
latency estimate. Every warmup and timed warm invocation made **zero HTTP
requests**. The shared native index preparation was outside these metric
samples: 722 requests / 14,152 header bytes.

Measurements used Python 3.12.14 on Linux with files in tmpfs. CPU is obtained
from `RUSAGE_CHILDREN` and excludes the parent loopback server and comparisons.
The operating-system cache was not flushed. Shared-host scheduling causes
variation. This measures inspection of stored original-model weights; it does
not measure model inference, WAN transfer, or Android/device performance.

## Sources and model

| File | Baseline Git blob | Updated Git blob |
| --- | --- | --- |
| `host/wb_metrics.py` | `e1fbb4aaf82c6965d377bfbdc8274f28f6a06071` | `76453f22a6d51bcc978189590ccc3cac00ff8e12` |
| `host/wb_range.py` | `c2a208a5af3503e5fa94d80388b241f05c2e87a3` | identical |

The unchanged baseline blobs were confirmed on main
`e11e779eb5103886a95aacfcd5e4b7f40a1ea068` before the scoring change.
Full source SHA-256 values, commands, runtime, per-call counters, raw timing
samples, and the complete reference metric result are in `measurement.json`.

The [pinned original model](https://huggingface.co/ggml-org/tiny-llamas/resolve/def3e2dd70df35ecbf6403ea347de4c5977220c1/stories260K.gguf)
is 1,185,376 bytes, SHA-256
`047bf46455a544931cff6fef14d7910154c56afbc23ab1c5e56a72e69912c04b`.
The runner requires those exact bytes. Model weights are not embedded here.

## Replay

Use baseline and updated source directories containing `host/wb_range.py` and
`host/wb_metrics.py`, with the blob identities above. The runner needs only the
existing Python standard library on a POSIX host; it serves the supplied model
over an ephemeral loopback HTTP range endpoint and stops that server afterward.

```bash
python -B measure.py \
  --baseline-root /path/to/baseline \
  --candidate-root /path/to/updated \
  --model /path/to/stories260K.gguf \
  --work-dir /path/to/benchmark-runs \
  --output /path/to/new-measurement.json \
  --pairs 3 --warmups 1
```

Each invocation creates its own run directory and retains the index, range
caches, archives, and raw receipt. The output receipt path must be new. Warmup
and timing samples reuse each version's own cache, initialized from the same
prepared header cache. The script refuses differing caller/transport source
and detects source changes during the run.
