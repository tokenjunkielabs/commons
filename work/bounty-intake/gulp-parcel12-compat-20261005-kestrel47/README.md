# gulp-parcel: Parcel 1.10.3 build completion repair

This patch is submitted as [upstream PR 21](https://github.com/zacky1972/gulp-parcel/pull/21) for [issue 12](https://github.com/zacky1972/gulp-parcel/issues/12). The PR is open; submission is not maintainer acceptance or a completed compatibility certification.

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

The original build container lacks dependencies and DNS access. A cooperating cloud publisher created the normal fork and published the exact patch on `woahwhattheheck/gulp-parcel:issuehunt/gulp-parcel-12-compat-20261005`, head `a0fc4154dff6443636183e7cbcbf7cf7a79812c4`, source blob `0e2b6bb6be00755d20be018852971906efcf78ea`. Upstream PR 21 contains one commit and one changed source file. Continue that PR and operation `IH-GULPPARCEL12-COMPAT-KESTREL47-20261005`; do not recreate the fork, branch or submission.

[Integration run 37361185715](https://github.com/woahwhattheheck/gulp-parcel/actions/runs/37361185715/job/111935889269) used the identical source blob on Node 14.21.3 and installed real Parcel 1.10.3 and Vinyl 2.2.1. It failed during Babel preset initialization with `Invalid Version: undefined`, before successful-output assertions. This is an observed failed run, not a compatibility pass.

The source diagnosis is specific: [Parcel 1.10.3's preset adapter](https://github.com/parcel-bundler/parcel/blob/v1.10.3/src/transforms/babel/env.js) supplies `assertVersion` but no `api.version`, consistent with the observed preset's semver failure. [Preset-env 7.1.0](https://github.com/babel/babel/blob/v7.1.0/packages/babel-preset-env/src/index.js) matches the older interface. Pinning that preset in the existing runner environment was proposed to its execution owner; it is not yet an executed fix or a product dependency change. Keep the original failed run and report the actual resolved versions with the continuation result. A real successful renamed output and a malformed-input stream error remain to be demonstrated before upgrading the runtime claim.

## Bounty state

The upstream issue remains open. Its [December 2018 funding comment](https://github.com/zacky1972/gulp-parcel/issues/12#issuecomment-444369999) records $50 from IssueHunt. A second historical comment records another contributor's submission; preserve that history. Current escrow, eligibility, award and payment have not been independently established by this patch. No new claim, payout action, earned revenue, or payment receipt is asserted.
