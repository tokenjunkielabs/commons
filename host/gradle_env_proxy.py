#!/usr/bin/env python3
"""Run a Gradle wrapper using the cloud environment's existing HTTP proxies."""

from __future__ import annotations

import argparse
import ipaddress
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys
from urllib.parse import urlsplit


def proxy_properties(environment: dict[str, str]) -> dict[str, str]:
    properties: dict[str, str] = {}
    for protocol in ("http", "https"):
        value = environment.get(f"{protocol}_proxy") or environment.get(f"{protocol.upper()}_PROXY")
        if not value:
            continue
        try:
            proxy = urlsplit(value if "://" in value else f"http://{value}")
            port = proxy.port if proxy.port is not None else 80
        except ValueError:
            raise ValueError(f"{protocol.upper()}_PROXY is not a valid proxy URL") from None
        if proxy.scheme != "http":
            raise ValueError(f"{protocol.upper()}_PROXY must name an HTTP forward proxy for the JVM")
        if proxy.username is not None or proxy.password is not None:
            raise ValueError(f"{protocol.upper()}_PROXY contains credentials; configure the JVM's existing proxy authenticator instead")
        if not proxy.hostname or proxy.path not in ("", "/") or proxy.query or proxy.fragment:
            raise ValueError(f"{protocol.upper()}_PROXY is not a host-and-port proxy URL")
        if port == 0:
            raise ValueError(f"{protocol.upper()}_PROXY must use a nonzero port")
        properties[f"{protocol}.proxyHost"] = proxy.hostname
        properties[f"{protocol}.proxyPort"] = str(port)

    bypass = environment.get("no_proxy") or environment.get("NO_PROXY")
    if properties and bypass:
        hosts: list[str] = ["localhost", "127.*", "[::1]"]
        for entry in bypass.split(","):
            host = entry.strip()
            if not host:
                continue
            if "/" in host:
                try:
                    network = ipaddress.ip_network(host, strict=False)
                except ValueError:
                    raise ValueError("NO_PROXY contains an invalid IP network") from None
                if network.version == 6 and network.num_addresses != 1:
                    raise ValueError("NO_PROXY contains an IPv6 subnet; supply explicit JVM nonProxyHosts for its address spellings")
                if network.version == 4 and network.num_addresses > 1:
                    # Split only to the next whole octet: /12 becomes sixteen
                    # address prefixes, never millions of individual addresses.
                    prefix = max(8, ((network.prefixlen + 7) // 8) * 8)
                    blocks = network.subnets(new_prefix=prefix) if prefix > network.prefixlen else (network,)
                    for block in blocks:
                        parts = str(block.network_address).split(".")
                        hosts.append(".".join(parts[:prefix // 8]) + (".*" if prefix < 32 else ""))
                    continue
                host = str(network.network_address)
            if host.startswith("."):
                hosts.extend((host[1:], f"*{host}"))
            elif host.startswith("*."):
                hosts.extend((host[2:], host))
            else:
                try:
                    address = ipaddress.ip_address(host.strip("[]"))
                except ValueError:
                    if ":" in host:
                        raise ValueError("NO_PROXY contains a port-specific rule the JVM cannot represent; use explicit JVM nonProxyHosts")
                    if "*" not in host:
                        hosts.append(f"*.{host}")
                else:
                    if address.version == 6:
                        host = f"[{address}]"
                hosts.append(host)
        properties["http.nonProxyHosts"] = "|".join(dict.fromkeys(hosts))
    return properties


def explicit_properties(environment: dict[str, str], project: Path, arguments: list[str]) -> set[str]:
    """Keep existing JVM settings, including project/user Gradle properties."""
    keys: set[str] = set()
    option_text = " ".join(environment.get(name, "") for name in
                           ("GRADLE_OPTS", "JAVA_OPTS", "JAVA_TOOL_OPTIONS", "JDK_JAVA_OPTIONS", "_JAVA_OPTIONS"))
    keys.update(re.findall(r"(?:^|\s)[\"']?-D([^\s=]+)=", option_text))
    keys.update(argument[2:].split("=", 1)[0] for argument in arguments if argument.startswith("-D"))
    user_home = Path(environment.get("GRADLE_USER_HOME", str(Path.home() / ".gradle")))
    for path in (project / "gradle.properties", user_home / "gradle.properties"):
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            keys.update(re.findall(r"(?m)^\s*systemProp\.([^\s:=]+)\s*[:=]", text))
    return keys


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=Path.cwd(), help="Gradle project directory (default: current directory)")
    parser.add_argument("--refresh-env-proxy", action="store_true", help="Replace inherited GRADLE_OPTS proxy endpoint flags with this invocation's environment")
    parser.add_argument("arguments", nargs=argparse.REMAINDER, help="Wrapper arguments after --")
    args = parser.parse_args()
    arguments = args.arguments[1:] if args.arguments[:1] == ["--"] else args.arguments
    project = args.project.resolve()
    wrapper = project / "gradlew"
    environment = os.environ.copy()
    try:
        if not wrapper.is_file():
            raise ValueError("The selected project does not contain a Gradle wrapper")
        if args.refresh_env_proxy:
            refresh_keys = {
                f"{protocol}.{part}"
                for protocol in ("http", "https")
                if environment.get(f"{protocol}_proxy") or environment.get(f"{protocol.upper()}_PROXY")
                for part in ("proxyHost", "proxyPort")
            }
            try:
                inherited = shlex.split(environment.get("GRADLE_OPTS", ""))
            except ValueError:
                raise ValueError("GRADLE_OPTS contains unmatched quoting") from None
            environment["GRADLE_OPTS"] = shlex.join(
                option for option in inherited
                if not (option.startswith("-D") and option[2:].split("=", 1)[0] in refresh_keys)
            )
        explicit = explicit_properties(environment, project, arguments)
        proxy_environment = environment.copy()
        # An explicit host/port pair belongs to the caller; do not mix it with
        # half of an environment proxy endpoint.
        for protocol in ("http", "https"):
            if any(f"{protocol}.{part}" in explicit for part in ("proxyHost", "proxyPort")):
                proxy_environment.pop(f"{protocol}_proxy", None)
                proxy_environment.pop(f"{protocol.upper()}_PROXY", None)
        if "http.nonProxyHosts" in explicit:
            proxy_environment.pop("no_proxy", None)
            proxy_environment.pop("NO_PROXY", None)
        properties = proxy_properties(proxy_environment)
        options = [f"-D{key}={value}" for key, value in properties.items()]
        # The launcher needs these before a distribution exists. CLI properties
        # also reach the Gradle daemon; caller-supplied options stay last.
        environment["GRADLE_OPTS"] = " ".join(filter(None, (shlex.join(options), environment.get("GRADLE_OPTS", ""))))
        print(f"Gradle environment proxy: {len(properties)} JVM properties applied; existing explicit settings preserved", file=sys.stderr, flush=True)
        command = [str(wrapper), *options, *arguments]
        result = subprocess.run(command, cwd=project, env=environment, check=False)
        return result.returncode if result.returncode >= 0 else 128 - result.returncode
    except (OSError, ValueError) as error:
        # Do not include proxy URLs or environment values in failure messages.
        if isinstance(error, OSError):
            print(f"Gradle environment proxy: process or file operation failed ({error.__class__.__name__}, errno={error.errno})", file=sys.stderr)
        else:
            print(f"Gradle environment proxy: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
