# Remove transient synchronization duplicates from generated Wear JARs

Use `remove_rsync_jar_duplicates.py` when D8 reports a duplicate class and one
archive entry includes a `.rsync-tmp` path component. The utility accepts named
generated JARs as positional arguments. It removes a temporary entry only when
its canonical counterpart exists and has identical bytes. An unmatched or
different entry stops that archive's repair before replacement. Retained entry
bytes are checked before the corrected archive replaces the original atomically.
Archive comments, retained entry timestamps and compression methods, entry order,
and file mode are preserved.

The companion `wear_rsync_jar_cleanup.init.gradle` targets only these producers:

- `:play-services-base:bundleLibRuntimeToJarDebug`
- `:play-services-base:bundleLibCompileToJarDebug`

It runs the sanitizer in `doLast`, after each producer finishes writing its
generated `classes.jar`. Pre-clean existing affected archives once before
launching Gradle, since `doLast` does not run for an up-to-date task. Keep
`--no-build-cache` to avoid restoring an archive without running the hook, and
`--no-configuration-cache` for this execution-time init script.

Retain the existing Java, Android SDK and Gradle environment. Set these checkout
paths and run from a POSIX shell with Python 3.9 or newer:

```sh
set -e
COMMONS_ROOT=/abs/commons
GMSCORE_ROOT=/abs/GmsCore
JAR_SANITIZER="$COMMONS_ROOT/host/remove_rsync_jar_duplicates.py"

python3 "$JAR_SANITIZER" \
  "$GMSCORE_ROOT/play-services-base/build/intermediates/runtime_library_classes_jar/debug/bundleLibRuntimeToJarDebug/classes.jar" \
  "$GMSCORE_ROOT/play-services-base/build/intermediates/compile_library_classes_jar/debug/bundleLibCompileToJarDebug/classes.jar"

python3 "$COMMONS_ROOT/host/gradle_env_proxy.py" \
  --project "$GMSCORE_ROOT" --refresh-env-proxy -- \
  --no-daemon --no-build-cache --no-configuration-cache \
  "-Dcommons.rsyncJarSanitizer=$JAR_SANITIZER" \
  --init-script "$COMMONS_ROOT/host/wear_rsync_jar_cleanup.init.gradle" \
  :play-services-core:assembleVtmDefaultDebug
```

The pre-clean command assumes both named archives already exist, as in the
observed incremental-build failure. On a fresh build, omit that command and
retain the init script. Supply the sanitizer's absolute path through
`commons.rsyncJarSanitizer`; Python runs as a child of the selected Gradle task
and a repair failure fails that task. An archive with no temporary entries is
left unchanged. Each archive is handled separately; a later failure does not
undo successful repairs of earlier arguments.

This repairs generated build artifacts without changing project source or
clearing caches. The hook was exercised with AGP 8.13.2 and Gradle 8.13; its two
task names and `output` property describe that observed Wear build. For another
producer, inspect its actual output contract before adapting the selection.
For proxy or forked-test-JVM configuration, see [Gradle through an existing
cloud proxy](GRADLE_ENV_PROXY.md).
