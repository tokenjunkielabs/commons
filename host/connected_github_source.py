#!/usr/bin/env python3
"""Materialize exact GitHub connector file responses in a cloud working copy."""
from __future__ import annotations

import argparse
import base64
import binascii
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import tempfile


class SourceImportError(ValueError):
    def __init__(self, code: str, detail: str, path: str | None = None):
        self.code, self.detail, self.path = code, detail, path
        super().__init__(detail)


def blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def _file_payload(response: object, *, fallback_sha=None, fallback_encoding=None) -> dict:
    """Read native fetch_file/fetch_blob and GET-contents tool envelopes."""
    pending = [response]
    for _ in range(32):
        if not pending:
            break
        value = pending.pop(0)
        if not isinstance(value, dict):
            continue
        if value.get("isError") is True:
            raise SourceImportError("SOURCE_TOOL_ERROR", "The source tool reported an error.")
        if isinstance(value.get("sha"), str) and isinstance(value.get("encoding"), str):
            return value
        # Native fetch_blob returns only the decoded content. Its request SHA
        # and explicit text encoding must accompany that otherwise bare result.
        if (isinstance(value.get("content"), str)
                and not any(isinstance(value.get(key), dict) for key in ("structuredContent", "result", "data"))
                and isinstance(fallback_sha, str) and isinstance(fallback_encoding, str)):
            return {**value, "sha": fallback_sha, "encoding": fallback_encoding}
        for key in ("structuredContent", "result", "data"):
            if isinstance(value.get(key), dict):
                pending.append(value[key])
        content = value.get("content")
        texts = [content] if isinstance(content, str) else []
        if isinstance(content, list):
            texts.extend(block["text"] for block in content
                         if isinstance(block, dict) and block.get("type") == "text"
                         and isinstance(block.get("text"), str))
        for text in texts:
            try:
                decoded = json.loads(text)
            except (ValueError, RecursionError):
                continue
            if isinstance(decoded, dict):
                pending.append(decoded)
    raise SourceImportError("SOURCE_RESPONSE_SHAPE", "No encoded GitHub file/blob was found in the response.")


def _source(entry: object) -> dict:
    if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
        raise SourceImportError("SOURCE_ENTRY_SHAPE", "Each file needs a path and its original response.")
    name = entry["path"]
    pieces = name.split("/")
    if (not name or name.startswith("/") or "\\" in name or "\0" in name
            or any(part in ("", ".", "..") for part in pieces)
            or ":" in pieces[0]):
        raise SourceImportError("SOURCE_PATH", "Use a relative repository path without traversal.", name)
    mode = entry.get("mode")
    if mode is not None and mode not in ("100644", "100755"):
        raise SourceImportError("SOURCE_MODE", "File mode must be 100644 or 100755 when supplied.", name)
    payload = _file_payload(entry.get("response"), fallback_sha=entry.get("blob_sha"),
                            fallback_encoding=entry.get("encoding"))
    expected = payload["sha"]
    if not re.fullmatch(r"[0-9a-fA-F]{40}", expected):
        raise SourceImportError("SOURCE_SHA", "The response needs a complete Git blob SHA.", name)
    if "blob_sha" in entry and (not isinstance(entry["blob_sha"], str)
            or entry["blob_sha"].lower() != expected.lower()):
        raise SourceImportError("SOURCE_SHA_MISMATCH", "The response differs from the supplied request blob SHA.", name)
    content = payload.get("content")
    if not isinstance(content, str):
        raise SourceImportError("SOURCE_CONTENT", "The response has no file content string.", name)
    if payload.get("path") is not None and payload["path"] != name:
        raise SourceImportError("SOURCE_PATH_MISMATCH", "The returned path differs from the requested file.", name)
    encoding = payload["encoding"].lower()
    try:
        if encoding in ("utf-8", "utf8"):
            data = content.encode("utf-8")
        elif encoding == "base64":
            data = base64.b64decode("".join(content.split()), validate=True)
        else:
            raise SourceImportError("SOURCE_ENCODING", "Request full UTF-8 or base64 content.", name)
    except (UnicodeError, binascii.Error, ValueError) as exc:
        if isinstance(exc, SourceImportError):
            raise
        raise SourceImportError("SOURCE_ENCODING", "The encoded file content is invalid.", name) from None
    actual = blob_sha(data)
    if actual != expected.lower():
        raise SourceImportError("SOURCE_BLOB_MISMATCH", "Content does not match its Git blob; fetch the complete file/blob again.", name)
    if "size" in payload and (type(payload["size"]) is not int or payload["size"] != len(data)):
        raise SourceImportError("SOURCE_SIZE_MISMATCH", "Content does not match the returned byte count.", name)
    return {"path": name, "data": data, "blob_sha": actual, "mode": mode,
            "source_url": payload.get("display_url") or payload.get("html_url") or payload.get("url")}


def _destination(root: Path, item: dict) -> Path:
    destination = root.joinpath(*PurePosixPath(item["path"]).parts)
    current = root
    for part in PurePosixPath(item["path"]).parts[:-1]:
        current = current / part
        if current.is_symlink() or (current.exists() and not current.is_dir()):
            raise SourceImportError("DESTINATION_CONFLICT", "A parent path is not an ordinary directory.", item["path"])
    if destination.is_symlink():
        raise SourceImportError("DESTINATION_CONFLICT", "An existing symlink is preserved.", item["path"])
    if destination.exists():
        if (not destination.is_file() or destination.stat().st_size != len(item["data"])
                or destination.read_bytes() != item["data"]):
            raise SourceImportError("DESTINATION_CONFLICT", "An existing destination differs and is preserved.", item["path"])
        if item["mode"] is not None and stat.S_IMODE(destination.stat().st_mode) != int(item["mode"][-3:], 8):
            raise SourceImportError("DESTINATION_CONFLICT", "Existing file permissions differ and are preserved.", item["path"])
    return destination


def materialize(manifest: object, output_directory: str | Path) -> dict:
    """Validate all source bytes before writing; never replace existing files."""
    if not isinstance(manifest, dict) or not isinstance(manifest.get("files"), list) or not manifest["files"]:
        raise SourceImportError("SOURCE_MANIFEST", "Input must contain a nonempty files array.")
    files = {}
    for entry in manifest["files"]:
        item = _source(entry)
        previous = files.get(item["path"])
        if previous is not None:
            if previous["data"] != item["data"] or previous["mode"] != item["mode"]:
                raise SourceImportError("SOURCE_DUPLICATE_CONFLICT", "Two source entries disagree for the same path.", item["path"])
            continue
        files[item["path"]] = item
    for name in files:
        if any(str(parent) in files for parent in PurePosixPath(name).parents if str(parent) != "."):
            raise SourceImportError("SOURCE_PATH_CONFLICT", "A source file is also another file's parent directory.", name)
    root = Path(output_directory).expanduser().resolve()
    if root.exists() and not root.is_dir():
        raise SourceImportError("DESTINATION_CONFLICT", "Output must be a directory.")
    for item in files.values():
        _destination(root, item)
    results = []
    for item in files.values():
        destination = _destination(root, item)
        outcome = "unchanged"
        if not destination.exists():
            destination.parent.mkdir(parents=True, exist_ok=True)
            _destination(root, item)
            descriptor, staging = tempfile.mkstemp(prefix=".github-source-", dir=destination.parent)
            try:
                with os.fdopen(descriptor, "wb") as stream:
                    stream.write(item["data"])
                    stream.flush()
                    os.fsync(stream.fileno())
                    os.fchmod(stream.fileno(), int((item["mode"] or "100644")[-3:], 8))
                try:
                    # Atomic create-only publication preserves a concurrent edit.
                    os.link(staging, destination)
                    outcome = "written"
                except FileExistsError:
                    _destination(root, item)
            finally:
                Path(staging).unlink(missing_ok=True)
        result = {"path": item["path"], "blob_sha": item["blob_sha"],
                  "bytes": len(item["data"]), "state": outcome}
        if item["mode"] is not None:
            result["mode"] = item["mode"]
        if isinstance(item["source_url"], str):
            result["source_url"] = item["source_url"]
        results.append(result)
    return {"ok": True, "output_directory": str(root), "files": results,
            "written": sum(row["state"] == "written" for row in results),
            "unchanged": sum(row["state"] == "unchanged" for row in results)}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", help="JSON export containing files: [{path, response, mode?}]")
    parser.add_argument("output_directory", help="Cloud working directory for exact source files")
    args = parser.parse_args(argv)
    try:
        with Path(args.manifest).open(encoding="utf-8") as stream:
            manifest = json.load(stream)
        result = materialize(manifest, args.output_directory)
    except SourceImportError as exc:
        result = {"ok": False, "error": exc.code, "detail": exc.detail}
        if exc.path is not None:
            result["path"] = exc.path
    except (OSError, UnicodeError, ValueError, RecursionError) as exc:
        result = {"ok": False, "error": "SOURCE_IMPORT_IO" if isinstance(exc, OSError) else "SOURCE_IMPORT_JSON",
                  "detail": type(exc).__name__ + ": import did not complete; existing files were preserved."}
    print(json.dumps(result, ensure_ascii=True, sort_keys=True))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
