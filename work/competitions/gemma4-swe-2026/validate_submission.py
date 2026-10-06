#!/usr/bin/env python3
"""Offline preflight for Gemma 4 Developer Agent submission envelopes.

This validates the documented archive/sandbox/model constraints that can be
checked without Kaggle's compiler or evaluation harness. It intentionally does
not claim ADK schema/compiler equivalence.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass, field
import json
import os
from pathlib import Path, PurePosixPath
import stat
import sys
from typing import Any
import zipfile

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: python -m pip install pyyaml") from exc

REQUIRED_MODEL = "gemma-4-31b-it-qat-w4a16-ct"
MAX_UNPACKED_BYTES = 3 * 1024 * 1024 * 1024
ALLOWED_SUFFIXES = {".yaml", ".yml", ".md", ".txt", ".py", ".json", ".safetensors"}
STANDARD_TOP_LEVEL = {
    "agent.yaml", "eval_config.yaml", "configs", "prompts", "sub_agents",
    "adapters", "skills",
}


class IncludeRef(str):
    pass


class SubmissionLoader(yaml.SafeLoader):
    pass


def _include(loader: yaml.Loader, node: yaml.Node) -> IncludeRef:
    return IncludeRef(loader.construct_scalar(node))


SubmissionLoader.add_constructor("!include", _include)


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    files: list[str] = field(default_factory=list)
    unpacked_bytes: int = 0
    model_references: int = 0
    adapter_references: set[str] = field(default_factory=set)
    skill_names: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors

    def public(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "errors": self.errors,
            "warnings": self.warnings,
            "files": len(self.files),
            "unpacked_bytes": self.unpacked_bytes,
            "required_model": REQUIRED_MODEL,
            "model_references": self.model_references,
            "adapter_references": sorted(self.adapter_references),
            "skill_names": sorted(self.skill_names),
        }


def _safe_archive_name(name: str) -> str | None:
    if not name or "\x00" in name or "\\" in name:
        return None
    path = PurePosixPath(name)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        return None
    return str(path)


def _collect_directory(root: Path, report: Report) -> dict[str, bytes]:
    files: dict[str, bytes] = {}
    for current, dirs, filenames in os.walk(root, followlinks=False):
        current_path = Path(current)
        for dirname in list(dirs):
            path = current_path / dirname
            if path.is_symlink():
                report.errors.append(f"symlink is not allowed: {path.relative_to(root)}")
                dirs.remove(dirname)
        for filename in filenames:
            path = current_path / filename
            rel = path.relative_to(root).as_posix()
            if path.is_symlink():
                report.errors.append(f"symlink is not allowed: {rel}")
                continue
            data = path.read_bytes()
            files[rel] = data
            report.unpacked_bytes += len(data)
    return files


def _collect_zip(path: Path, report: Report) -> dict[str, bytes]:
    files: dict[str, bytes] = {}
    seen: set[str] = set()
    with zipfile.ZipFile(path) as archive:
        for info in archive.infolist():
            safe = _safe_archive_name(info.filename.rstrip("/"))
            if safe is None:
                report.errors.append(f"unsafe archive path: {info.filename!r}")
                continue
            if safe in seen:
                report.errors.append(f"duplicate archive path: {safe}")
                continue
            seen.add(safe)
            unix_mode = info.external_attr >> 16
            if unix_mode and stat.S_ISLNK(unix_mode):
                report.errors.append(f"symlink is not allowed: {safe}")
                continue
            if info.is_dir():
                continue
            if info.flag_bits & 0x1:
                report.errors.append(f"encrypted archive member is not allowed: {safe}")
                continue
            report.unpacked_bytes += info.file_size
            if report.unpacked_bytes >= MAX_UNPACKED_BYTES:
                report.errors.append("total unpacked size must be strictly less than 3 GiB")
                break
            files[safe] = archive.read(info)
    return files


def _parse_yaml(path: str, data: bytes, report: Report) -> Any | None:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        report.errors.append(f"{path}: YAML must be UTF-8")
        return None
    try:
        return yaml.load(text, Loader=SubmissionLoader)
    except yaml.YAMLError as exc:
        report.errors.append(f"{path}: invalid YAML: {exc}")
        return None


def _walk(node: Any):
    if isinstance(node, dict):
        yield node
        for value in node.values():
            yield from _walk(value)
    elif isinstance(node, list):
        for value in node:
            yield from _walk(value)


def _collect_includes(node: Any) -> list[IncludeRef]:
    refs: list[IncludeRef] = []
    if isinstance(node, IncludeRef):
        refs.append(node)
    elif isinstance(node, dict):
        for value in node.values():
            refs.extend(_collect_includes(value))
    elif isinstance(node, list):
        for value in node:
            refs.extend(_collect_includes(value))
    return refs


def _resolve_include(source: str, target: str) -> str | None:
    if not target or "\x00" in target or "\\" in target:
        return None
    source_dir = PurePosixPath(source).parent
    parts: list[str] = list(source_dir.parts)
    for part in PurePosixPath(target).parts:
        if part in {"", "."}:
            continue
        if part == "..":
            if not parts:
                return None
            parts.pop()
        else:
            parts.append(part)
    return "/".join(parts) if parts else None


def _validate_yaml_files(files: dict[str, bytes], report: Report) -> dict[str, Any]:
    parsed: dict[str, Any] = {}
    agent_files = [
        path
        for path in files
        if path == "agent.yaml"
        or (path.startswith("sub_agents/") and Path(path).suffix in {".yaml", ".yml"})
    ]
    for path in sorted({p for p in files if Path(p).suffix in {".yaml", ".yml"}}):
        node = _parse_yaml(path, files[path], report)
        if node is not None:
            parsed[path] = node
            for ref in _collect_includes(node):
                resolved = _resolve_include(path, str(ref))
                if resolved is None:
                    report.errors.append(f"{path}: !include escapes submission root: {ref}")
                elif resolved not in files:
                    report.errors.append(
                        f"{path}: !include target not found: {ref} -> {resolved}"
                    )

    for path in agent_files:
        node = parsed.get(path)
        if node is None:
            continue
        for mapping in _walk(node):
            if "model" in mapping:
                report.model_references += 1
                if mapping["model"] != REQUIRED_MODEL:
                    report.errors.append(
                        f"{path}: unsupported model {mapping['model']!r}; "
                        f"expected {REQUIRED_MODEL!r}"
                    )
            if "adapter" in mapping and mapping["adapter"] is not None:
                adapter = mapping["adapter"]
                if not isinstance(adapter, str) or not adapter.strip():
                    report.errors.append(f"{path}: adapter must be a non-empty string")
                else:
                    report.adapter_references.add(adapter)

    if report.model_references == 0:
        report.errors.append(
            "no model reference found in agent.yaml/sub_agents; "
            f"LLM agents must use {REQUIRED_MODEL}"
        )
    return parsed


def _validate_adapters(files: dict[str, bytes], report: Report) -> None:
    for adapter in sorted(report.adapter_references):
        prefix = f"adapters/{adapter}/"
        config = prefix + "adapter_config.json"
        weights = prefix + "adapter_model.safetensors"
        if config not in files:
            report.errors.append(f"adapter {adapter!r}: missing {config}")
        if weights not in files:
            report.errors.append(f"adapter {adapter!r}: missing {weights}")
        if config in files:
            try:
                payload = json.loads(files[config].decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                report.errors.append(f"{config}: invalid UTF-8 JSON: {exc}")
                continue
            if not isinstance(payload, dict):
                report.errors.append(f"{config}: expected a JSON object")


def _validate_skills(files: dict[str, bytes], report: Report) -> None:
    skill_dirs = sorted(
        {
            path.split("/", 2)[1]
            for path in files
            if path.startswith("skills/") and len(path.split("/")) >= 3
        }
    )
    for dirname in skill_dirs:
        manifest = f"skills/{dirname}/SKILL.md"
        if manifest not in files:
            report.errors.append(f"skill {dirname!r}: missing SKILL.md")
            continue
        try:
            text = files[manifest].decode("utf-8")
        except UnicodeDecodeError:
            report.errors.append(f"{manifest}: must be UTF-8")
            continue
        lines = text.splitlines()
        if not lines or lines[0].strip() != "---":
            report.errors.append(f"{manifest}: missing YAML frontmatter")
            continue
        try:
            end = next(i for i, line in enumerate(lines[1:], 1) if line.strip() == "---")
        except StopIteration:
            report.errors.append(f"{manifest}: unterminated YAML frontmatter")
            continue
        try:
            frontmatter = yaml.safe_load("\n".join(lines[1:end])) or {}
        except yaml.YAMLError as exc:
            report.errors.append(f"{manifest}: invalid frontmatter: {exc}")
            continue
        name = frontmatter.get("name") if isinstance(frontmatter, dict) else None
        if not isinstance(name, str) or not name.strip():
            report.errors.append(f"{manifest}: frontmatter requires non-empty name")
        else:
            report.skill_names.append(name.strip())


def validate(files: dict[str, bytes], report: Report) -> Report:
    report.files = sorted(files)

    if report.unpacked_bytes >= MAX_UNPACKED_BYTES:
        report.errors.append("total unpacked size must be strictly less than 3 GiB")
    if "agent.yaml" not in files:
        report.errors.append("agent.yaml must be at archive root")

    for path in sorted(files):
        suffix = Path(path).suffix.lower()
        if suffix not in ALLOWED_SUFFIXES:
            report.errors.append(f"unsupported file extension: {path}")
        top = path.split("/", 1)[0]
        if top not in STANDARD_TOP_LEVEL:
            warning = f"non-standard top-level entry retained for Kaggle compiler review: {top}"
            if warning not in report.warnings:
                report.warnings.append(warning)

    _validate_yaml_files(files, report)
    _validate_adapters(files, report)
    _validate_skills(files, report)
    return report


def validate_path(path: Path) -> Report:
    report = Report()
    if path.is_dir():
        files = _collect_directory(path, report)
    elif path.is_file() and path.suffix.lower() == ".zip":
        try:
            files = _collect_zip(path, report)
        except zipfile.BadZipFile as exc:
            report.errors.append(f"invalid zip archive: {exc}")
            files = {}
    else:
        report.errors.append("input must be a submission directory or .zip archive")
        files = {}
    return validate(files, report)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("submission", type=Path, help="submission directory or submission.zip")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = parser.parse_args(argv)

    report = validate_path(args.submission)
    if args.json:
        print(json.dumps(report.public(), indent=2, sort_keys=True))
    else:
        status = "PASS" if report.ok else "FAIL"
        print(f"{status}: {args.submission}")
        print(
            f"files={len(report.files)} unpacked_bytes={report.unpacked_bytes} "
            f"models={report.model_references} adapters={len(report.adapter_references)} "
            f"skills={len(report.skill_names)}"
        )
        for warning in report.warnings:
            print(f"WARNING: {warning}")
        for error in report.errors:
            print(f"ERROR: {error}", file=sys.stderr)
    return 0 if report.ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
