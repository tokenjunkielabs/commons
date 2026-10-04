# GGUF header field grouping measurement

The production indexer groups only fields whose complete adjacent extent is
known: a metadata key and its type, a tensor name and its rank, and an array
element type and count. It uses the existing grouped-read helper, including its
request limit and older split-cache behavior.

## Recorded result

On Python 3.12.14, Linux, and tmpfs, the complete native index command consumed
an authentic 14,152-byte header from the pinned stories260K.gguf source. The
loopback HTTP 206 server refused every byte beyond the retained header.

| Measurement | Baseline | Candidate |
| --- | ---: | ---: |
| Cold HTTP requests | 792 | 722 |
| Cold HTTP body bytes | 14,152 | 14,152 |
| Cold CLI median | 538.760 ms | 454.794 ms |
| Warm HTTP requests | 0 | 0 |
| Candidate using the baseline cache | — | 0 |

Three paired rounds alternated execution order. All nine complete CLI
invocations exited zero and produced the same parsed index after removing its
invocation timestamp: 48 tensors and 1,171,200 indexed tensor bytes. The first
actual metadata field also preserved its split reads at a 21-byte limit.

Raw samples, commands, versions and source hashes are in
[measurement.json](measurement.json). The exact executed program is
[measure_index.py](measure_index.py). Cold refers to a fresh application cache;
OS caches were not flushed. Timing includes CLI startup. These observations do
not measure WAN latency, tensor transfer or model inference.

## Reproduce the same comparison

From a checkout containing both Git blobs, use a fresh directory on Linux tmpfs.
This stages the two original source versions without changing the checkout or
running another worker's cached job:

```sh
WB_MEASURE_DIR=$(mktemp -d /dev/shm/wb-header-measure.XXXXXX)
mkdir -p "$WB_MEASURE_DIR/comparison/baseline/host" "$WB_MEASURE_DIR/comparison/candidate/host"
cp work/performance/wb-gguf-name-fields-20261004/measure_index.py "$WB_MEASURE_DIR/comparison/"
git cat-file blob 125612caacd6ef5b852028bee4680f7c5d1cd6cb > "$WB_MEASURE_DIR/comparison/baseline/host/wb_range.py"
git cat-file blob c2a208a5af3503e5fa94d80388b241f05c2e87a3 > "$WB_MEASURE_DIR/comparison/candidate/host/wb_range.py"
git cat-file blob e1fbb4aaf82c6965d377bfbdc8274f28f6a06071 > "$WB_MEASURE_DIR/comparison/baseline/host/wb_metrics.py"
cp "$WB_MEASURE_DIR/comparison/baseline/host/wb_metrics.py" "$WB_MEASURE_DIR/comparison/candidate/host/"
export WB_MEASURE_DIR
python - <<'PY'
import hashlib, os, pathlib, urllib.request
url = "https://huggingface.co/ggml-org/tiny-llamas/resolve/def3e2dd70df35ecbf6403ea347de4c5977220c1/stories260K.gguf"
request = urllib.request.Request(url, headers={"Range": "bytes=0-14151"})
with urllib.request.urlopen(request, timeout=30) as response:
    if response.status != 206 or response.headers.get("Content-Range") != "bytes 0-14151/1185376":
        raise SystemExit("source did not return the exact original header range")
    header = response.read(14153)
if len(header) != 14152 or hashlib.sha256(header).hexdigest() != "1b793503f1cebc379bc3a8101db035313e620203c1462a44a9e15e94993268b4":
    raise SystemExit("original header digest or length differs")
(pathlib.Path(os.environ["WB_MEASURE_DIR"]) / "stories260K.header").write_bytes(header)
PY
python -B "$WB_MEASURE_DIR/comparison/measure_index.py"
```

The header source is pinned to a model repository commit. Only that range was
newly acquired and hashed; the historical complete-model hash was not rechecked.
The script records a new result in its comparison directory and intentionally
requires a fresh `runs` directory.

