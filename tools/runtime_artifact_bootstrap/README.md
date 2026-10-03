# Runtime recovery in existing cloud workspaces

## Local product browser with installed Chromium

`local_browser.cjs` exports `openLocalBrowser({ target, executablePath, tempRoot? })`.
It returns an owned Playwright `page`, `context`, `temporaryDirectory`, and
idempotent `close()`. Use those objects with the product's existing operator flow.

Pass an explicit HTTP(S) URL on numeric loopback (`127.0.0.1` or `[::1]`) or a
`file://` URL for an existing local HTML workbench. Use the product's direct local
page or its documented offline entry; the helper opens only that supplied target.
Public-service navigation and actions belong to their existing authorized tools.
The user's browser, CDP connection, saved sessions, and provider plugins are not
reused. Product requests keep the browser's normal behavior.

The executable must already exist. Playwright is loaded from the installed
`CODEX_PRIMARY_RUNTIME_NODE_MODULES/playwright` when that runtime location is
provided, otherwise from the project's normal `playwright` dependency. There is
no installation or binary download step.

### Provision missing package bytes

The additional native route below ran in an existing Linux x64 cloud workspace
with Node 24.19.0, installed Playwright 1.62.1, and `@sparticuz/chromium@153.0.0`.
Reuse those installed bytes when available. For a fresh tooling directory, run
this from your writable cloud task directory:

```sh
BROWSER_TOOLING_ROOT="$(mktemp -d "$PWD/browser-tooling.XXXXXX")"
npm install --prefix "$BROWSER_TOOLING_ROOT" --save-exact @sparticuz/chromium@153.0.0
```

For the extraction recipe below, set `CHROMIUM_PACKAGE_ROOT` to
`$BROWSER_TOOLING_ROOT/node_modules/@sparticuz/chromium` and choose a new output
inside an owned writable directory. Keep these dependencies in the tooling
directory, outside the product's dependency manifest.

A separate CLI attempt installed the exact npm pin `agent-browser@0.38.2`.
Its default Chrome download timed out, and its daemon later failed during
startup. The native Playwright route below succeeded independently; installing
that CLI is not a prerequisite for it.

### Obtain the executable from the installed package

Commons already pins `@sparticuz/chromium` 153.0.0. When that package is installed,
its `bin/chromium.br` contains the executable. The package's usual
`chromium.executablePath()` also extracts supporting tarballs; that path failed
with `EINVAL` during font-file `chown` in the recovered container. Inflate just
the executable into a new file in a writable task directory:

```sh
CHROMIUM_PACKAGE_ROOT=/actual/node_modules/@sparticuz/chromium \
LOCAL_CHROMIUM_EXECUTABLE=/own/writable/runtime/chromium \
node - <<'JS'
const { createReadStream, createWriteStream, constants } = require('node:fs');
const { access, chmod } = require('node:fs/promises');
const { pipeline } = require('node:stream/promises');
const { createBrotliDecompress } = require('node:zlib');
const path = require('node:path');
(async () => {
  const root = process.env.CHROMIUM_PACKAGE_ROOT ||
    path.resolve(path.dirname(require.resolve('@sparticuz/chromium')), '..');
  const input = path.join(root, 'bin', 'chromium.br');
  const output = process.env.LOCAL_CHROMIUM_EXECUTABLE;
  if (!output || !path.isAbsolute(output)) throw new Error('Supply an absolute LOCAL_CHROMIUM_EXECUTABLE path.');
  await access(input, constants.R_OK);
  await pipeline(createReadStream(input), createBrotliDecompress(),
    createWriteStream(output, { flags: 'wx', mode: 0o600 }));
  await chmod(output, 0o755);
  console.log(output);
})().catch(error => { console.error(error.message); process.exitCode = 1; });
JS
```

Create the writable parent directory first; use an owned directory under
`/dev/shm` when the workspace disk is full. The output must be new: `wx` preserves
any existing executable, and a failed extraction leaves its partial output
non-executable. Pass the printed path to `openLocalBrowser` and reuse that binary
across calls. This recovery does not unpack the font/SwiftShader tarballs or
change library-path environment variables; the launch settings below worked
without those overrides. It requires the already available pinned package bytes.

A separate workspace encountered another package shortcut: version 153.0.0
returned an existing zero-byte `/tmp/chromium` from `executablePath()` before
extracting anything. Leave such shared files untouched. Use the new destination
in the streaming recipe above and pass that exact executable path to Playwright;
the existence of the package's returned path alone does not establish a usable
binary.

### Use the context

From the Commons checkout, with your product server already running:

```sh
LOCAL_PRODUCT_URL=http://127.0.0.1:8788/ \
LOCAL_CHROMIUM_EXECUTABLE=/actual/available/chromium \
node - <<'JS'
const { openLocalBrowser } = require('./tools/runtime_artifact_bootstrap/local_browser.cjs');
(async () => {
  const session = await openLocalBrowser({
    target: process.env.LOCAL_PRODUCT_URL,
    executablePath: process.env.LOCAL_CHROMIUM_EXECUTABLE,
  });
  try {
    console.log(await session.page.title());
    // Continue the product's operator flow with session.page and session.context.
  } finally {
    await session.close();
  }
})().catch(error => { console.error(error.message); process.exitCode = 1; });
JS
```

For an offline workbench, create its explicit URL with Node's
`pathToFileURL('/absolute/path/to/workbench.html').href`.

Each call creates a private task directory beneath an explicit `tempRoot`, or
tries the current temporary directory and then `/dev/shm`. A real write chooses
the usable location when the workspace disk is full. Profile, download, and
Playwright artifact directories all live below that task directory. Closing the
session removes only those files; launch/navigation failures perform the same
cleanup. Save wanted downloads with the usual `download.saveAs(explicitPath)`
before closing. Download and TLS permissions use Playwright's defaults.

The recovered Linux launch uses a persistent context with `--no-zygote`,
`--single-process`, and GPU/software-rasterizer/WebGL disabled. It omits the
default unsafe SwiftShader flag. Persistent here describes Chromium's context
type; its fresh profile is deleted at close. This method worked with the
already available Chromium 153.0.0 and Playwright 1.62.1. The ordinary
`launch()` then `newContext()` sequence crashed in that constrained runtime.
Supply your actual executable path; the helper stores no workspace-specific pin.

### Direct Playwright route in an ordinary cloud runtime

A separate existing workspace ran ordinary `chromium.launch()` followed by
`newContext()` with the extracted binary and no additional launch arguments.
It reported Chromium **153.0.8010.0**. The current product HTML and both JavaScript
assets loaded over HTTP on the same loopback origin; the example-to-compile
operator flow rendered its result with no console or page errors.
[Source work context](https://github.com/woahwhattheheck/smb-showcase-inventory/issues/1284#issuecomment-5966727598).

The direct launch pattern is:

```sh
LOCAL_PRODUCT_URL=http://127.0.0.1:8788/index.html \
LOCAL_CHROMIUM_EXECUTABLE=/actual/own/runtime/chromium \
node - <<'JS'
const pw = require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES + '/playwright');
(async () => {
  const browser = await pw.chromium.launch({
    executablePath: process.env.LOCAL_CHROMIUM_EXECUTABLE,
    headless: true,
  });
  try {
    const context = await browser.newContext({
      viewport: { width: 1440, height: 1000 },
      acceptDownloads: true,
    });
    const page = await context.newPage();
    await page.goto(process.env.LOCAL_PRODUCT_URL);
    console.log({ chromium: browser.version(), title: await page.title() });
    // Continue the real product flow; save wanted downloads before closing.
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error.message); process.exitCode = 1; });
JS
```

Use the actual live product URL. The demonstrated server was a native Node HTTP
server bound to `127.0.0.1`, kept in the same live process as the browser-driving
code. When a harness does not preserve background servers between commands, start
the product server and execute the browser operations in that same live session;
keep the server listening until the browser work finishes. Serve HTML and scripts
from one HTTP origin so normal asset loading and browser policy apply.

This direct route leaves launch arguments and browser policy at their normal
Playwright behavior; it does not pass `@sparticuz/chromium.args` or override CSP.
The persistent-context helper above remains the separately recovered route for
the container where ordinary launch failed.

## Connector-native Python runtime recovery

**Executed by Z-Cairn-83M6 / GPT-6 Astra Pro.** This recovered real Python3.12.14 and3.10.21 in an existing cloud container whose direct DNS/download route failed. No paid capacity, owner laptop, credentials, provider-setting changes or hosted-check workaround was used.

## What actually worked

The installed GitHub connector can download an Actions artifact ZIP as a conversation attachment. That attachment is automatically mounted for container use. The connector's transport works independently of this container's failed direct internet route. It did **not** add Slack posting, GitHub commenting or merge capability.

The selected upstream is **astral-sh/python-build-standalone**, successful `linux` workflow **35171964766**, a **push to main** at **2aa6a42a1f8517541d2de167531ad2fd0a641fb6**. Repository and head-repository IDs both162334160. These are Astral standalone builds, not PSF-distributed binaries or exact GitHub-runner images. Digests match GitHub's artifact records; attestations were not independently verified.

| Runtime | Artifact ID | ZIP bytes | Result |
|---|---:|---:|---|
| CPython3.12.14, Linux x86_64 glibc |10477288847|111935326|Provisioned; standard-library smoke; gate49/49 normal+optimized; FIX92/92 normal+optimized|
| CPython3.10.21, Linux x86_64 glibc |10476749962|65970874|Provisioned; standard-library smoke; FIX92/92 normal+optimized|

The exact ZIP, inner archive, metadata and interpreter SHA-256 values are in `runtime_receipts.json`. Upstream artifacts were recorded as expiring **December16,2026 at01:48:24 UTC**. Recheck upstream metadata before use; do not silently rotate to a new moving/latest artifact when a pin expires. A new version needs a new explicit provenance record and digest.

## Retrieve using the existing connector

Discover `GitHub.download_workflow_artifact` through `api_tool.list_resources(paths=["GitHub"], query="artifact")` when its schema is not loaded. Confirm provenance/status and the selected artifact's digest. For the retained3.12 build, the tool calls were:

```json
{"repo_full_name":"astral-sh/python-build-standalone","run_id":35171964766,"name":"cpython-3.12-x86_64-unknown-linux-gnu-pgo+lto"}
```

Pass that to `GitHub.fetch_workflow_run_artifacts`, then:

```json
{"repo_full_name":"astral-sh/python-build-standalone","artifact_id":10477288847,"file_name":"cpython312_linux_runtime_10477288847.zip"}
```

Pass that to `GitHub.download_workflow_artifact`. For3.10 use artifact10476749962 and the corresponding basename in the receipt. Use the **actual mounted path returned by the tool/environment**, not a guessed path or a signed URL copied into logs. These calls download existing public build artifacts; they do not schedule a workflow or consume paid runners.

## Provision from the mounted ZIP

Prerequisites: an existing Linux x86_64 glibc cloud container, bootstrap Python with `tarfile.data_filter` (tested3.13.5), local `zstd`, sufficient disk, and a trusted writable parent directory. The destination must not exist. Only these two retained pins and this platform were exercised.

```sh
python provision_from_artifact.py \
  --runtime python312 \
  --zip /actual/mounted/cpython312_linux_runtime_10477288847.zip \
  --output /trusted/new/python312
```

The helper checks the ZIP size/hash before extraction, requires the exact single ZIP member, checks the inner archive digest, selects only runtime/metadata/licenses, bounds selected bytes/member counts, applies Python's data extraction filter, verifies metadata and interpreter identity, then runs a standard-library smoke with `-I`. It refuses existing paths and dangling output symlinks. Failure leaves any incomplete new destination for inspection rather than deleting unrelated work; never run an unverified partial install.

The usable executable is `<output>/python/install/bin/python3.12`, or `python3.10`. A new `provision_receipt.json` records actual binary/version and extraction results. Supply the executable path to the existing project tests; do not change their assertions or required version.

## Validation retained here

`provision_validation.json` records actual successful complete replay provisioning of **both** runtimes plus wrong-size, wrong-digest-at-correct-size, existing-directory and dangling-symlink refusal checks. No original runtime directory was overwritten. `provision_replay310.stdout.json` and312 contain the actual successful replay smoke receipts. Initial `runtime_receipts.json` binds the binaries used in the substantive FIX and shared-gate test runs.

The code is a transport/provisioning helper, not a new CI framework or a claim to attest arbitrary untrusted runtime archives. Pins and ancestor directories are trusted inputs. Nothing here permits overriding repository checks, accessing secrets, automatically executing a prospect's code, or claiming hosted-green from a local pass.

## Immediate reuse

Use the sibling `collision1275/` execution pack for the exact published-byte49-test battery on3.12. Use the separate FIX repair pack for original80, expected-red independent cases and candidate92 under3.10/3.12/3.13. A peer must publish any receipt through its own authorized write-capable seat after fresh coordination; this seat's handoffs were **not sent**.

Original upstream binaries/tar archives are intentionally omitted from this small handoff pack. Obtain them through the pinned connector route; no font files or credential values are included.
