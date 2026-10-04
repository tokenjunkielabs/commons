# Gradle through an existing cloud proxy

Use `gradle_env_proxy.py` when a cloud VM can fetch with curl or Git but the
Gradle wrapper's Java downloader fails with `Network is unreachable`. Java does
not automatically consume the shell's `HTTP_PROXY` / `HTTPS_PROXY` settings.
The helper translates those existing settings into JVM properties for the
wrapper launcher and the Gradle daemon, then runs the real project wrapper in
a POSIX cloud environment with Python 3.9 or newer.

```sh
python3 /path/to/commons/host/gradle_env_proxy.py --refresh-env-proxy --project /path/to/GmsCore -- --version
GRADLE_MICROG_VERSION_WITHOUT_GIT=1 python3 /path/to/commons/host/gradle_env_proxy.py --refresh-env-proxy --project /path/to/GmsCore -- :play-services-droidguard-core:assembleDebug
```

Cloud proxy endpoints can change between tool invocations. Read the environment
on every invocation; do not copy a proxy host or port from a prior command.
`--refresh-env-proxy` removes only inherited `GRADLE_OPTS` proxy host/port flags
for protocols configured in the current environment, then rebuilds those flags
from that environment. Other JVM options remain. Explicit wrapper arguments,
other JVM option variables and `gradle.properties` still take precedence. Omit
the flag when intentionally keeping proxy endpoint flags in `GRADLE_OPTS`.

Run the tasks required by the active bounty on its exact current source. Keep
the existing issue claim, integration branch and upstream submission owner.
This helper supplies network configuration; it does not provide Android SDK
packages, a JDK compiler, a device, attestation, or bounty acceptance.

## Behavior

- Uses lowercase proxy variables first, then uppercase equivalents. Each
  protocol keeps its own endpoint. An HTTP forward proxy also handles HTTPS
  destinations through the JVM's normal CONNECT behavior.
- Preserves explicit proxy properties from wrapper arguments, existing JVM
  option variables, and the project's/user's `gradle.properties`. If a caller
  supplies a proxy host or port, the helper leaves that endpoint alone.
- Translates `NO_PROXY` hostnames, domain suffixes, wildcard domains and literal
  IP addresses to `http.nonProxyHosts` (the JVM property also used for HTTPS).
  IPv4 CIDRs become bounded address-prefix lists: `172.16.0.0/12` becomes
  `172.16.*` through `172.31.*`. This is JVM hostname matching, not a DNS
  resolution rule. Loopback bypass remains. IPv6 subnets and port-specific
  bypasses produce a clear error before the wrapper runs. Explicit
  `-Dhttp.nonProxyHosts=...` takes precedence over automatic translation.
- Preserves other wrapper arguments and JVM options, returns the wrapper's exit
  code, and reports missing wrappers or invalid configuration with exit 2.
- Does not print proxy URLs or values, write credentials or project settings,
  change network policy, install software outside the wrapper's normal behavior,
  dispatch hosted CI, or schedule work. Authenticated proxy URLs must use an
  existing JVM authenticator rather than putting credentials in command options.

## Observed cloud use

On 2026-10-04, the exact GmsCore wrapper at
`3f10ba2b9ef6aa7a7806cf0547d70932bb4d3965` failed before downloading Gradle 8.13
with `java.net.SocketException: Network is unreachable`. curl reached that
distribution URL through the environment proxy. Applying the same environment
proxy as JVM settings completed the real Gradle distribution download and
`--version` with exit 0 on OpenJDK 17.0.20/Linux. This is a working wrapper
download and launch, not an Android application build or a device result.
The real project also completed Gradle `help` with dependency configuration and
exit 0 in 71 seconds using the same configured proxy. The helper's automatic
environment path and explicit-setting preservation were then exercised against
that installed wrapper; no test suite or hosted workflow was dispatched.

Reference: [Gradle networking](https://docs.gradle.org/current/userguide/networking.html)
and [JDK 17 networking properties](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/net/doc-files/net-properties.html).
