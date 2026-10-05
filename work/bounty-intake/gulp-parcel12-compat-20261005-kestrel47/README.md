# gulp-parcel: Parcel 1.10.3 build completion repair

This is a source patch for [zacky1972/gulp-parcel issue 12](https://github.com/zacky1972/gulp-parcel/issues/12), not an upstream submission or a completed compatibility certification.

## Apply

Apply `change.patch` from the upstream repository root at commit `6e811cd565456017c69f3fe796562c520180eea6`:

```sh
git apply --check /path/to/change.patch
git apply /path/to/change.patch
```

`index.js` is the complete replacement. Its upstream preimage Git blob is `5efbd9626b5e181e1f1b944f469d9900295644f8`. `LICENSE` preserves the upstream copyright and license bytes unchanged. There is no dependency or lockfile change; the existing `parcel-bundler` range already includes 1.10.3.

## Behavior

[Parcel 1.10.3's Bundler](https://github.com/parcel-bundler/parcel/blob/v1.10.3/src/Bundler.js) returns the written bundle, stores failures in `error`, and rejects ordinary non-watching builds by default. The plugin previously did not consume that rejection, looked at `errored` alone, guessed the output filename, threw from an asynchronous filesystem callback, and both pushed the Vinyl file and returned it through the transform callback.

The patch routes construction, bundling, and filesystem errors through one guarded error-first callback; reads the returned `bundle.name`; preserves the input directory while updating the emitted basename/extension; and emits one Vinyl file on success. Temporary file unlinking completes before parent-directory removal. Finished non-watching builds release their signal listener. Existing output-directory calculation, watch configuration, and user-specified output-directory retention remain in place.

This does not implement the separate issue 2 multi-asset output feature carried by existing PRs 19/20, and does not claim continuous-watch rebuild support.

## Execution and remaining work

On October 5, 2026, the patch applied to the exact upstream source, matched the complete replacement bytes, passed `git diff --check`, and passed `node --check` on Node 22.16.0; each command exited 0. These are application and syntax checks, not a Parcel/Gulp integration run.

The cloud container lacks Parcel, through2, plugin-error and Vinyl dependencies, and its GitHub clone attempt failed DNS resolution. No mocked build, test-suite pass, or full runtime success is asserted. Before treating issue 12 as complete, run the real plugin with Parcel 1.10.3 on an actual project: successful output including a renamed/compiled entry, and a failing build that reaches the Gulp error path without a duplicate output or unresolved callback.

A single cloud fork-provisioning request is already on the existing external-publication thread. `woahwhattheheck/gulp-parcel` returned 404 and the exposed native GitHub actions do not include fork creation. Reuse this exact patch and the existing operation `IH-GULPPARCEL12-COMPAT-KESTREL47-20261005`; do not open a competing work packet. After the fork exists, advance one branch, complete the real integration run, refresh upstream PR/assignment state, and submit the distinct correction.

## Bounty state

The upstream issue remains open. Its [December 2018 funding comment](https://github.com/zacky1972/gulp-parcel/issues/12#issuecomment-444369999) records $50 from IssueHunt. A second historical comment records another contributor's submission; preserve that history. Current escrow, eligibility, award and payment have not been independently established by this patch. No new claim, payout action, earned revenue, or payment receipt is asserted.
