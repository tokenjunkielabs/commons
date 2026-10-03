"""Passive, resumable encrypted-source copying through an existing Drive binding.

The private SQLite journal contains an immutable, complete source_records
snapshot. Ciphertext is streamed with sqlite3.blobopen; this module never loads
a key, imports the encryption implementation, or decrypts source material.
Native connector calls are handed to their existing host as explicit jobs.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import sqlite3
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path


VERSION = 1
IO_BYTES = 1024 * 1024
MANIFEST_FORMAT = "swarm-remote-custody-v1"
COLUMNS = ("ref", "source_id", "sha256", "byte_length", "character_length",
           "iv", "ciphertext", "mac", "format", "key_reference")
META_COLUMNS = tuple(name for name in COLUMNS if name != "ciphertext")
SOURCE_DDL = ("CREATE TABLE source_records (ref TEXT PRIMARY KEY,source_id TEXT,"
              "sha256 TEXT,byte_length INTEGER,character_length INTEGER,iv BLOB,"
              "ciphertext BLOB,mac BLOB,format TEXT,key_reference TEXT)")
TOOL_PREFIX = "mcp__codex_apps__google_drive_"
ID_RE = re.compile(r"[A-Za-z0-9_-]{1,256}\Z")
HASH_RE = re.compile(r"[0-9a-f]{64}\Z")


class CustodyError(Exception):
    """Only the fixed code is suitable for operational output."""

    def __init__(self, code):
        self.code = code
        super().__init__(code)


def _require(condition, code):
    if not condition:
        raise CustodyError(code)


def _json(value):
    return json.dumps(value, ensure_ascii=True, sort_keys=True,
                      separators=(",", ":"), allow_nan=False)


def _digest(value):
    return hashlib.sha256(_json(value).encode("utf-8")).hexdigest()


def _typed(value):
    if value is None:
        return {"type": "null", "value": None}
    if isinstance(value, bytes):
        return {"type": "blob", "value": base64.b64encode(value).decode("ascii")}
    if isinstance(value, str):
        return {"type": "text", "value": value}
    if isinstance(value, int):
        return {"type": "integer", "value": value}
    if isinstance(value, float):
        return {"type": "real", "value": value}
    raise CustodyError("UNSUPPORTED_SOURCE_VALUE")


def _untyped(item):
    _require(isinstance(item, dict) and set(item) == {"type", "value"},
             "INVALID_MANIFEST_VALUE")
    kind, value = item["type"], item["value"]
    if kind == "null" and value is None:
        return None
    if kind == "blob" and isinstance(value, str):
        return base64.b64decode(value, validate=True)
    if kind == "text" and isinstance(value, str):
        return value
    if kind == "integer" and type(value) is int:
        return value
    if kind == "real" and type(value) in (int, float):
        return float(value)
    raise CustodyError("INVALID_MANIFEST_VALUE")


def _metadata_values(metadata):
    _require(isinstance(metadata, dict) and set(metadata) == set(META_COLUMNS),
             "INVALID_SOURCE_METADATA")
    values = {name: _untyped(metadata[name]) for name in META_COLUMNS}
    _require(isinstance(values["ref"], str), "INVALID_SOURCE_REFERENCE")
    _require(isinstance(values["iv"], bytes) and isinstance(values["mac"], bytes),
             "INVALID_SOURCE_BLOBS")
    return values


def _record_id(metadata, ciphertext_sha256, ciphertext_bytes):
    return _digest({"metadata": metadata, "ciphertext_sha256": ciphertext_sha256,
                    "ciphertext_bytes": ciphertext_bytes})


def _provider_id(value):
    _require(isinstance(value, str) and ID_RE.fullmatch(value), "INVALID_PROVIDER_ID")
    return value


def _hash_file(path):
    digest, size = hashlib.sha256(), 0
    with Path(path).open("rb") as handle:
        while block := handle.read(IO_BYTES):
            digest.update(block)
            size += len(block)
    return digest.hexdigest(), size


def _private_file(path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY |
                 getattr(os, "O_NOFOLLOW", 0), 0o600)
    os.close(fd)


@contextmanager
def _db(path):
    path = Path(path).resolve()
    _require(path.is_file(), "JOURNAL_NOT_FOUND")
    db = sqlite3.connect(path.as_uri() + "?mode=rw", uri=True, timeout=30)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA busy_timeout=30000")
    db.execute("PRAGMA foreign_keys=ON")
    db.execute("PRAGMA synchronous=FULL")
    db.execute("PRAGMA temp_store=MEMORY")
    try:
        yield db
    finally:
        db.close()


def _meta(db, key):
    row = db.execute("SELECT value FROM metadata WHERE key=?", (key,)).fetchone()
    _require(row is not None, "INCOMPLETE_JOURNAL")
    return json.loads(row[0])


def _set_meta(db, key, value):
    db.execute("INSERT INTO metadata(key,value) VALUES (?,?) "
               "ON CONFLICT(key) DO UPDATE SET value=excluded.value", (key, _json(value)))


def _check_journal(db):
    _require(_meta(db, "version") == VERSION, "UNSUPPORTED_JOURNAL_VERSION")


def _object(db, object_id):
    row = db.execute("SELECT * FROM objects WHERE object_id=?", (object_id,)).fetchone()
    _require(row is not None, "OBJECT_NOT_FOUND")
    return row


def _insert_source(db, rowid, values, size):
    slots = ["zeroblob(?)" if name == "ciphertext" else "?" for name in COLUMNS]
    bindings = [rowid] + [size if name == "ciphertext" else values[name] for name in COLUMNS]
    db.execute("INSERT INTO source_records(rowid," + ",".join(COLUMNS) + ") VALUES (?," +
               ",".join(slots) + ")", bindings)


def _initialize_journal(journal, binding):
    """Publish a complete empty journal without replacing an existing file."""
    journal.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    with tempfile.TemporaryDirectory(prefix=".custody-bootstrap-", dir=journal.parent) as directory:
        temporary = Path(directory) / "journal.sqlite3"
        _private_file(temporary)
        with _db(temporary) as db:
            db.executescript("""
                CREATE TABLE metadata(key TEXT PRIMARY KEY,value TEXT NOT NULL);
                CREATE TABLE records(seq INTEGER PRIMARY KEY,source_rowid INTEGER UNIQUE,
                    record_id TEXT UNIQUE,metadata_json TEXT NOT NULL,
                    ciphertext_bytes INTEGER NOT NULL,ciphertext_sha256 TEXT,
                    chunk_count INTEGER NOT NULL DEFAULT 0);
                CREATE TABLE objects(seq INTEGER PRIMARY KEY,object_id TEXT UNIQUE,
                    kind TEXT NOT NULL,record_seq INTEGER REFERENCES records(seq),
                    part INTEGER,offset_bytes INTEGER NOT NULL,size_bytes INTEGER NOT NULL,
                    sha256 TEXT NOT NULL,file_name TEXT UNIQUE,state TEXT NOT NULL,
                    remote_file_id TEXT,search_complete INTEGER NOT NULL DEFAULT 0,
                    upload_attempts INTEGER NOT NULL DEFAULT 0,readback_sha256 TEXT,
                    readback_bytes INTEGER,last_error_code TEXT,
                    UNIQUE(record_seq,part));
                CREATE TABLE candidates(object_id TEXT NOT NULL,file_id TEXT NOT NULL,
                    state TEXT NOT NULL,PRIMARY KEY(object_id,file_id));
                CREATE INDEX objects_pending ON objects(state,seq);
            """)
            db.execute(SOURCE_DDL)
            with db:
                _set_meta(db, "version", VERSION)
                _set_meta(db, "prepared", False)
                for key, value in binding.items():
                    _set_meta(db, key, value)
        # A concurrent initializer may have published first. Reuse that file
        # through prepare's existing binding checks; never overwrite it.
        try:
            os.link(temporary, journal)
        except FileExistsError:
            pass


def prepare(source_db, journal, operation_id, account_ref, folder_id,
            chunk_bytes=4 * 1024 * 1024):
    """Capture all rows at one SQLite read snapshot; repeating reuses that snapshot."""
    _require(hasattr(sqlite3.Connection, "blobopen"), "SQLITE_BLOBOPEN_REQUIRED")
    _require(isinstance(operation_id, str) and operation_id.strip(), "OPERATION_ID_REQUIRED")
    _require(isinstance(account_ref, str) and account_ref.strip(), "ACCOUNT_REFERENCE_REQUIRED")
    _require(type(chunk_bytes) is int and 0 < chunk_bytes <= 64 * 1024 * 1024,
             "INVALID_CHUNK_BYTES")
    folder_id = _provider_id(folder_id)
    source_path, journal = Path(source_db).resolve(), Path(journal).resolve()
    _require(source_path != journal, "SOURCE_JOURNAL_COLLISION")
    _require(source_path.is_file(), "SOURCE_DATABASE_NOT_FOUND")
    source_stat = source_path.stat()
    source_identity = {"path": str(source_path), "device": source_stat.st_dev,
                       "inode": source_stat.st_ino}
    destination = {"provider": "google_drive", "account_ref": account_ref,
                   "folder_id": folder_id}
    destination_key = _digest(destination)
    operation_key = _digest({"operation_id": operation_id, "source": source_identity,
                             "destination_key": destination_key})
    binding = {"operation_id": operation_id, "source_identity": source_identity,
               "destination": destination, "destination_key": destination_key,
               "operation_key": operation_key, "chunk_bytes": chunk_bytes}
    if not journal.exists():
        _initialize_journal(journal, binding)
    with _db(journal) as db:
        _check_journal(db)
        for key, value in binding.items():
            _require(_meta(db, key) == value, "OPERATION_INPUT_OR_DESTINATION_CHANGED")
        if _meta(db, "prepared"):
            return _status(db)
        _require(db.execute("SELECT COUNT(*) FROM records").fetchone()[0] == 0,
                 "INCOMPLETE_SNAPSHOT_CONFLICT")
        source = sqlite3.connect(source_path.as_uri() + "?mode=ro", uri=True, timeout=30)
        source.row_factory = sqlite3.Row
        try:
            source.execute("PRAGMA busy_timeout=30000")
            source.execute("BEGIN")
            schema = [row[1] for row in source.execute("PRAGMA table_info(source_records)")]
            _require(schema == list(COLUMNS), "SOURCE_SCHEMA_MISMATCH")
            db.execute("BEGIN IMMEDIATE")
            snapshot_digest, count = hashlib.sha256(), 0
            query = ("SELECT rowid AS source_rowid," + ",".join(META_COLUMNS) +
                     ",length(ciphertext) AS ciphertext_bytes,typeof(ciphertext) AS blob_type "
                     "FROM source_records ORDER BY rowid")
            for row in source.execute(query):
                _require(row["blob_type"] == "blob", "INVALID_CIPHERTEXT_TYPE")
                size, rowid = row["ciphertext_bytes"], row["source_rowid"]
                values = {name: row[name] for name in META_COLUMNS}
                metadata = {name: _typed(values[name]) for name in META_COLUMNS}
                _metadata_values(metadata)
                _insert_source(db, rowid, values, size)
                record_seq = db.execute(
                    "INSERT INTO records(source_rowid,metadata_json,ciphertext_bytes) VALUES (?,?,?)",
                    (rowid, _json(metadata), size)).lastrowid
                cipher_digest, offset, part = hashlib.sha256(), 0, 0
                with source.blobopen("source_records", "ciphertext", rowid, readonly=True) as incoming:
                    with db.blobopen("source_records", "ciphertext", rowid, readonly=False) as outgoing:
                        while offset < size or part == 0:
                            length = min(chunk_bytes, size - offset)
                            remaining, chunk_digest = length, hashlib.sha256()
                            while remaining:
                                block = incoming.read(min(IO_BYTES, remaining))
                                _require(bool(block), "SOURCE_CIPHERTEXT_TRUNCATED")
                                outgoing.write(block)
                                cipher_digest.update(block)
                                chunk_digest.update(block)
                                remaining -= len(block)
                            db.execute("INSERT INTO objects(kind,record_seq,part,offset_bytes,"
                                       "size_bytes,sha256,state) VALUES ('chunk',?,?,?,?,?,'pending_search')",
                                       (record_seq, part, offset, length, chunk_digest.hexdigest()))
                            offset += length
                            part += 1
                cipher_hash = cipher_digest.hexdigest()
                record_id = _record_id(metadata, cipher_hash, size)
                db.execute("UPDATE records SET record_id=?,ciphertext_sha256=?,chunk_count=? WHERE seq=?",
                           (record_id, cipher_hash, part, record_seq))
                for chunk in db.execute("SELECT seq,part,sha256 FROM objects WHERE record_seq=?", (record_seq,)):
                    object_id = _digest({"operation_key": operation_key, "record_id": record_id,
                                         "part": chunk["part"], "sha256": chunk["sha256"]})
                    name = "src-{}-{}-{:08x}.bin".format(operation_key, record_id, chunk["part"])
                    db.execute("UPDATE objects SET object_id=?,file_name=? WHERE seq=?",
                               (object_id, name, chunk["seq"]))
                snapshot_digest.update((record_id + "\n").encode("ascii"))
                count += 1
            _set_meta(db, "snapshot_sha256", snapshot_digest.hexdigest())
            _set_meta(db, "records_total", count)
            _set_meta(db, "prepared", True)
            db.commit()
        except BaseException:
            db.rollback()
            raise
        finally:
            source.close()
        return _status(db)


def _stage_path(journal, name):
    folder = Path(str(Path(journal).resolve()) + ".objects")
    folder.mkdir(exist_ok=True, mode=0o700)
    _require(not folder.is_symlink(), "INVALID_STAGING_DIRECTORY")
    os.chmod(folder, 0o700)
    _require(Path(name).name == name and "/" not in name and "\\" not in name,
             "INVALID_OBJECT_NAME")
    return folder / name


def _write_resumable(path, blocks):
    """Resume an identical prefix, append only, and retain partial bytes on failure."""
    fd = os.open(path, os.O_CREAT | os.O_RDWR | getattr(os, "O_NOFOLLOW", 0), 0o600)
    digest, written = hashlib.sha256(), 0
    with os.fdopen(fd, "r+b") as handle:
        os.chmod(path, 0o600)
        existing = os.fstat(handle.fileno()).st_size
        for block in blocks:
            prefix = min(len(block), max(0, existing - written))
            if prefix:
                _require(handle.read(prefix) == block[:prefix], "STAGING_PREFIX_CONFLICT")
            if prefix < len(block):
                handle.write(block[prefix:])
            written += len(block)
            digest.update(block)
        _require(existing <= written, "STAGING_LENGTH_CONFLICT")
        handle.flush()
        os.fsync(handle.fileno())
    return digest.hexdigest(), written


def _chunk_blocks(db, row):
    source_rowid = db.execute("SELECT source_rowid FROM records WHERE seq=?",
                             (row["record_seq"],)).fetchone()[0]
    with db.blobopen("source_records", "ciphertext", source_rowid, readonly=True) as blob:
        blob.seek(row["offset_bytes"])
        remaining = row["size_bytes"]
        while remaining:
            block = blob.read(min(IO_BYTES, remaining))
            _require(bool(block), "SNAPSHOT_CIPHERTEXT_TRUNCATED")
            remaining -= len(block)
            yield block


def _stage_object(db, row, journal):
    path = _stage_path(journal, row["file_name"])
    if row["kind"] == "chunk":
        digest, size = _write_resumable(path, _chunk_blocks(db, row))
    else:
        _require(path.is_file(), "MANIFEST_STAGE_MISSING")
        digest, size = _hash_file(path)
    _require(digest == row["sha256"] and size == row["size_bytes"], "STAGED_OBJECT_MISMATCH")
    return path


def _manifest_blocks(db):
    digest = hashlib.sha256()
    header = {"type": "header", "format": MANIFEST_FORMAT,
              "operation_key": _meta(db, "operation_key"),
              "destination_key": _meta(db, "destination_key"),
              "snapshot_sha256": _meta(db, "snapshot_sha256"),
              "records_total": _meta(db, "records_total"),
              "chunks_total": db.execute("SELECT COUNT(*) FROM objects WHERE kind='chunk'").fetchone()[0]}
    block = (_json(header) + "\n").encode("utf-8")
    digest.update(block)
    yield block
    for record in db.execute("SELECT * FROM records ORDER BY seq"):
        item = {"type": "record", "record_id": record["record_id"],
                "metadata": json.loads(record["metadata_json"]),
                "ciphertext_bytes": record["ciphertext_bytes"],
                "ciphertext_sha256": record["ciphertext_sha256"],
                "chunk_count": record["chunk_count"]}
        block = (_json(item) + "\n").encode("utf-8")
        digest.update(block)
        yield block
        for chunk in db.execute("SELECT * FROM objects WHERE record_seq=? ORDER BY part", (record["seq"],)):
            _require(chunk["state"] == "confirmed" and chunk["remote_file_id"], "CHUNK_NOT_CONFIRMED")
            item = {"type": "chunk", "record_id": record["record_id"], "part": chunk["part"],
                    "offset_bytes": chunk["offset_bytes"], "size_bytes": chunk["size_bytes"],
                    "sha256": chunk["sha256"], "file_name": chunk["file_name"],
                    "provider": "google_drive", "file_id": chunk["remote_file_id"]}
            block = (_json(item) + "\n").encode("utf-8")
            digest.update(block)
            yield block
    yield (_json({"type": "complete", "records_total": header["records_total"],
                  "chunks_total": header["chunks_total"],
                  "content_sha256": digest.hexdigest()}) + "\n").encode("utf-8")


def _ensure_manifest(db, journal):
    if not _meta(db, "prepared") or db.execute("SELECT 1 FROM objects WHERE kind='manifest'").fetchone():
        return
    if db.execute("SELECT 1 FROM objects WHERE kind='chunk' AND state!='confirmed'").fetchone():
        return
    operation_key, snapshot_hash = _meta(db, "operation_key"), _meta(db, "snapshot_sha256")
    name = "src-{}-manifest-{}.jsonl".format(operation_key, snapshot_hash)
    digest, size = _write_resumable(_stage_path(journal, name), _manifest_blocks(db))
    object_id = _digest({"operation_key": operation_key, "manifest_sha256": digest})
    db.execute("INSERT INTO objects(object_id,kind,offset_bytes,size_bytes,sha256,file_name,state) "
               "VALUES (?,'manifest',0,?,?,?,'pending_search')", (object_id, size, digest, name))


def _status(db):
    prepared = _meta(db, "prepared")
    total = _meta(db, "records_total") if prepared else 0
    manifest = db.execute("SELECT * FROM objects WHERE kind='manifest'").fetchone()
    confirmed = bool(manifest and manifest["state"] == "confirmed")
    states = dict(db.execute("SELECT state,COUNT(*) FROM objects GROUP BY state"))
    byte_row = db.execute("SELECT COALESCE(SUM(size_bytes),0),"
                          "COALESCE(SUM(CASE WHEN state='confirmed' THEN size_bytes ELSE 0 END),0) "
                          "FROM objects").fetchone()
    ciphertext = db.execute("SELECT COALESCE(SUM(size_bytes),0),"
                            "COALESCE(SUM(CASE WHEN state='confirmed' THEN size_bytes ELSE 0 END),0) "
                            "FROM objects WHERE kind='chunk'").fetchone()
    complete_ciphertexts = db.execute(
        "SELECT COUNT(*) FROM records r WHERE NOT EXISTS "
        "(SELECT 1 FROM objects o WHERE o.record_seq=r.seq AND o.state!='confirmed')").fetchone()[0]
    return {"ok": True, "operation_key": _meta(db, "operation_key"),
            "destination_key": _meta(db, "destination_key"), "snapshot_complete": prepared,
            "copy_state": "confirmed" if confirmed else "pending",
            "records_total": total, "records_confirmed": total if confirmed else 0,
            "records_ciphertext_confirmed": complete_ciphertexts,
            "objects_total": sum(states.values()), "objects_confirmed": states.get("confirmed", 0),
            "object_states": states, "bytes_total": byte_row[0], "bytes_confirmed": byte_row[1],
            "ciphertext_bytes_total": ciphertext[0], "ciphertext_bytes_confirmed": ciphertext[1],
            "manifest": None if not manifest else {
                "object_id": manifest["object_id"], "state": manifest["state"],
                "sha256": manifest["sha256"], "file_id": manifest["remote_file_id"]}}


def status(journal):
    with _db(journal) as db:
        _check_journal(db)
        return _status(db)


def _fetch_args(file_id):
    return {"url": "https://drive.google.com/file/d/" + _provider_id(file_id) + "/view",
            "download_raw_file": True, "include_base64": False}


def jobs(journal, limit=100, cursor=0):
    """A finite native handoff pass. Issuing an upload durably records uncertainty."""
    _require(type(limit) is int and 0 < limit <= 1000 and type(cursor) is int and cursor >= 0,
             "INVALID_PAGE")
    with _db(journal) as db, db:
        _check_journal(db)
        _require(_meta(db, "prepared"), "SNAPSHOT_NOT_PREPARED")
        db.execute("BEGIN IMMEDIATE")
        _ensure_manifest(db, journal)
        destination = _meta(db, "destination")
        rows = db.execute("SELECT * FROM objects WHERE seq>? AND state!='confirmed' "
                          "ORDER BY seq LIMIT ?", (cursor, limit + 1)).fetchall()
        result = []
        for row in rows[:limit]:
            state = row["state"]
            job = {"object_id": row["object_id"], "cursor": row["seq"]}
            if state == "pending_upload":
                path = _stage_object(db, row, journal)
                db.execute("UPDATE objects SET state='upload_uncertain',search_complete=0,"
                           "upload_attempts=upload_attempts+1 WHERE object_id=?", (row["object_id"],))
                job.update(action="upload", tool_name=TOOL_PREFIX + "upload_file", args={
                    "file_uri": str(path), "file_name": row["file_name"],
                    "mime_type": "application/octet-stream", "parent_folder_id": destination["folder_id"]})
            elif state == "pending_readback":
                job.update(action="readback", file_id=row["remote_file_id"],
                           tool_name=TOOL_PREFIX + "fetch", args=_fetch_args(row["remote_file_id"]))
            else:
                _require(state in ("pending_search", "upload_uncertain"), "INVALID_OBJECT_STATE")
                query = "name = '{}' and '{}' in parents and trashed = false".format(
                    row["file_name"], destination["folder_id"])
                job.update(action="search", tool_name=TOOL_PREFIX + "search", args={
                    "special_filter_query_str": query, "topn": 100})
            result.append(job)
        return {"ok": True, "operation_key": _meta(db, "operation_key"), "jobs": result,
                "next_cursor": rows[limit - 1]["seq"] if len(rows) > limit else None,
                "pass_complete": len(rows) <= limit, "copy_state": _status(db)["copy_state"]}


def _receipt(row):
    return {"ok": True, "object_id": row["object_id"], "state": row["state"],
            "file_id": row["remote_file_id"], "sha256": row["sha256"], "bytes": row["size_bytes"]}


def _choose_candidate(db, object_id, complete=False):
    row = _object(db, object_id)
    if row["state"] == "confirmed":
        return
    if row["state"] == "pending_readback" and db.execute(
            "SELECT 1 FROM candidates WHERE object_id=? AND file_id=? AND state='pending'",
            (object_id, row["remote_file_id"])).fetchone():
        return
    candidate = db.execute("SELECT file_id FROM candidates WHERE object_id=? AND state='pending' "
                           "ORDER BY file_id LIMIT 1", (object_id,)).fetchone()
    if candidate:
        db.execute("UPDATE objects SET state='pending_readback',remote_file_id=? WHERE object_id=?",
                   (candidate[0], object_id))
    else:
        db.execute("UPDATE objects SET state=?,remote_file_id=NULL WHERE object_id=?",
                   ("pending_upload" if complete else "pending_search", object_id))


def record_search(journal, object_id, file_ids=(), complete=False):
    """Record only IDs from the exact-name query; complete excludes omitted pages."""
    file_ids = sorted({_provider_id(value) for value in file_ids})
    with _db(journal) as db, db:
        _check_journal(db)
        db.execute("BEGIN IMMEDIATE")
        row = _object(db, object_id)
        if row["state"] == "confirmed":
            return _receipt(row)
        for file_id in file_ids:
            db.execute("INSERT OR IGNORE INTO candidates VALUES (?,?,'pending')", (object_id, file_id))
        db.execute("UPDATE objects SET search_complete=? WHERE object_id=?", (int(bool(complete)), object_id))
        _choose_candidate(db, object_id, bool(complete))
        return _receipt(_object(db, object_id))


def record_upload(journal, object_id, file_id):
    file_id = _provider_id(file_id)
    with _db(journal) as db, db:
        _check_journal(db)
        db.execute("BEGIN IMMEDIATE")
        row = _object(db, object_id)
        if row["state"] == "confirmed":
            return _receipt(row)
        db.execute("INSERT OR IGNORE INTO candidates VALUES (?,?,'pending')", (object_id, file_id))
        _choose_candidate(db, object_id)
        return _receipt(_object(db, object_id))


def record_failure(journal, object_id, code="NATIVE_CALL_FAILED"):
    _require(isinstance(code, str) and re.fullmatch(r"[A-Z][A-Z0-9_]{0,79}", code),
             "INVALID_ERROR_CODE")
    with _db(journal) as db, db:
        _check_journal(db)
        db.execute("BEGIN IMMEDIATE")
        row = _object(db, object_id)
        if row["state"] != "confirmed":
            db.execute("UPDATE objects SET last_error_code=? WHERE object_id=?", (code, object_id))
        return _receipt(_object(db, object_id))


def record_readback(journal, object_id, file_id, download):
    file_id = _provider_id(file_id)
    with _db(journal) as db, db:
        _check_journal(db)
        db.execute("BEGIN IMMEDIATE")
        row = _object(db, object_id)
        if row["state"] == "confirmed":
            return _receipt(row)
        _require(db.execute("SELECT 1 FROM candidates WHERE object_id=? AND file_id=?",
                            (object_id, file_id)).fetchone(), "READBACK_RECEIPT_NOT_RECORDED")
        expected = _stage_object(db, row, journal)
        downloaded = Path(download).resolve()
        _require(downloaded != expected.resolve(), "REMOTE_DOWNLOAD_REQUIRED")
        equal, digest, size = True, hashlib.sha256(), 0
        with expected.open("rb") as left, downloaded.open("rb") as right:
            while True:
                a, b = left.read(IO_BYTES), right.read(IO_BYTES)
                if a != b:
                    equal = False
                    break
                if not b:
                    break
                digest.update(b)
                size += len(b)
        if equal and digest.hexdigest() == row["sha256"] and size == row["size_bytes"]:
            db.execute("UPDATE candidates SET state='confirmed' WHERE object_id=? AND file_id=?",
                       (object_id, file_id))
            db.execute("UPDATE objects SET state='confirmed',remote_file_id=?,readback_sha256=?,"
                       "readback_bytes=?,last_error_code=NULL WHERE object_id=?",
                       (file_id, digest.hexdigest(), size, object_id))
            return _receipt(_object(db, object_id))
        db.execute("UPDATE candidates SET state='mismatch' WHERE object_id=? AND file_id=?",
                   (object_id, file_id))
        db.execute("UPDATE objects SET last_error_code='READBACK_BYTE_MISMATCH' WHERE object_id=?", (object_id,))
        _choose_candidate(db, object_id)
        result = _receipt(_object(db, object_id))
        result.update(ok=False, code="READBACK_BYTE_MISMATCH")
        return result


def _manifest_events(manifest, expected_manifest_sha256=None):
    """Validate the entire streaming manifest, including completeness and ordering."""
    if expected_manifest_sha256 is not None:
        _require(HASH_RE.fullmatch(expected_manifest_sha256), "INVALID_MANIFEST_DIGEST")
        _require(_hash_file(manifest)[0] == expected_manifest_sha256, "MANIFEST_DIGEST_MISMATCH")
    digest, snapshot = hashlib.sha256(), hashlib.sha256()
    header, current, records, chunks = None, None, 0, 0

    def record_complete():
        if current is not None:
            _require(current["part"] == current["chunk_count"] and
                     current["offset"] == current["ciphertext_bytes"], "INCOMPLETE_RECORD_MANIFEST")

    with Path(manifest).open("rb") as handle:
        while True:
            line = handle.readline(16 * 1024 * 1024 + 1)
            _require(bool(line), "MANIFEST_COMPLETION_MISSING")
            _require(len(line) <= 16 * 1024 * 1024 and line.endswith(b"\n"), "INVALID_MANIFEST_LINE")
            item = json.loads(line)
            _require(isinstance(item, dict), "INVALID_MANIFEST_ITEM")
            kind = item.get("type")
            if header is None:
                _require(kind == "header" and item.get("format") == MANIFEST_FORMAT,
                         "UNSUPPORTED_MANIFEST")
                for name in ("operation_key", "destination_key", "snapshot_sha256"):
                    _require(isinstance(item.get(name), str) and HASH_RE.fullmatch(item[name]),
                             "INVALID_MANIFEST_IDENTITY")
                for name in ("records_total", "chunks_total"):
                    _require(type(item.get(name)) is int and item[name] >= 0, "INVALID_MANIFEST_TOTAL")
                header = item
            elif kind == "complete":
                record_complete()
                _require(records == header["records_total"] == item.get("records_total") and
                         chunks == header["chunks_total"] == item.get("chunks_total"),
                         "MANIFEST_TOTAL_MISMATCH")
                _require(snapshot.hexdigest() == header["snapshot_sha256"], "MANIFEST_SNAPSHOT_MISMATCH")
                _require(digest.hexdigest() == item.get("content_sha256"), "MANIFEST_CONTENT_MISMATCH")
                _require(not handle.read(1), "MANIFEST_TRAILING_CONTENT")
                yield item
                return
            elif kind == "record":
                record_complete()
                metadata = item.get("metadata")
                _metadata_values(metadata)
                _require(type(item.get("ciphertext_bytes")) is int and item["ciphertext_bytes"] >= 0,
                         "INVALID_RECORD_LENGTH")
                _require(type(item.get("chunk_count")) is int and item["chunk_count"] > 0,
                         "INVALID_CHUNK_COUNT")
                _require(isinstance(item.get("ciphertext_sha256"), str) and
                         HASH_RE.fullmatch(item["ciphertext_sha256"]), "INVALID_RECORD_DIGEST")
                _require(item.get("record_id") == _record_id(metadata, item["ciphertext_sha256"],
                                                             item["ciphertext_bytes"]),
                         "MANIFEST_RECORD_MISMATCH")
                current = {"record_id": item["record_id"], "part": 0, "offset": 0,
                           "chunk_count": item["chunk_count"], "ciphertext_bytes": item["ciphertext_bytes"]}
                snapshot.update((item["record_id"] + "\n").encode("ascii"))
                records += 1
                _require(records <= header["records_total"], "MANIFEST_RECORD_OVERFLOW")
            elif kind == "chunk":
                _require(current is not None and current["part"] < current["chunk_count"],
                         "UNEXPECTED_MANIFEST_CHUNK")
                _require(item.get("record_id") == current["record_id"] and
                         type(item.get("part")) is int and item["part"] == current["part"] and
                         type(item.get("offset_bytes")) is int and item["offset_bytes"] == current["offset"],
                         "CHUNK_POSITION_MISMATCH")
                _require(type(item.get("size_bytes")) is int and item["size_bytes"] >= 0 and
                         current["offset"] + item["size_bytes"] <= current["ciphertext_bytes"],
                         "INVALID_CHUNK_LENGTH")
                _require(item["size_bytes"] > 0 or
                         (current["ciphertext_bytes"] == 0 and current["chunk_count"] == 1),
                         "INVALID_EMPTY_CHUNK")
                _require(isinstance(item.get("sha256"), str) and HASH_RE.fullmatch(item["sha256"]),
                         "INVALID_CHUNK_DIGEST")
                _require(item.get("provider") == "google_drive", "UNSUPPORTED_MANIFEST_PROVIDER")
                _provider_id(item.get("file_id"))
                expected_name = "src-{}-{}-{:08x}.bin".format(header["operation_key"],
                                                           current["record_id"], current["part"])
                _require(item.get("file_name") == expected_name, "INVALID_MANIFEST_OBJECT_NAME")
                current["part"] += 1
                current["offset"] += item["size_bytes"]
                chunks += 1
                _require(chunks <= header["chunks_total"], "MANIFEST_CHUNK_OVERFLOW")
            else:
                raise CustodyError("UNEXPECTED_MANIFEST_ITEM")
            digest.update(line)
            yield item


def restore_jobs(manifest, limit=100, cursor=0, expected_manifest_sha256=None):
    """Emit native downloads using only the remote manifest, without the journal."""
    _require(type(limit) is int and 0 < limit <= 1000 and type(cursor) is int and cursor >= 0,
             "INVALID_PAGE")
    result, position, more, header = [], 0, False, None
    for item in _manifest_events(manifest, expected_manifest_sha256):
        if item["type"] == "header":
            header = item
        elif item["type"] == "chunk":
            position += 1
            if position <= cursor:
                continue
            if len(result) == limit:
                more = True
                continue
            result.append({"cursor": position, "action": "download", "file_id": item["file_id"],
                           "file_name": item["file_name"], "sha256": item["sha256"],
                           "tool_name": TOOL_PREFIX + "fetch", "args": _fetch_args(item["file_id"])})
    return {"ok": True, "operation_key": header["operation_key"], "jobs": result,
            "next_cursor": result[-1]["cursor"] if more else None, "pass_complete": not more,
            "records_total": header["records_total"], "chunks_total": header["chunks_total"],
            "manifest_sha256": _hash_file(manifest)[0]}


def restore(manifest, downloads, output_db, expected_manifest_sha256=None):
    """Create a NEW source_records database from downloaded manifest and chunks.

    ``downloads`` is a JSON file (or mapping in the Python API) from provider file
    IDs or opaque manifest filenames to actual native-download local paths.
    Existing files, the input database and its original rows are never replaced.
    A failed restoration retains its incomplete output file for inspection.
    """
    _require(hasattr(sqlite3.Connection, "blobopen"), "SQLITE_BLOBOPEN_REQUIRED")
    manifest = Path(manifest).resolve()
    if not isinstance(downloads, dict):
        with Path(downloads).open("r", encoding="utf-8") as handle:
            downloads = json.load(handle)
    _require(isinstance(downloads, dict), "INVALID_DOWNLOAD_MAPPING")
    header = None
    # Validate the complete manifest and the actual download mapping before
    # reserving a new output filename. Ciphertext remains streamed below.
    for item in _manifest_events(manifest, expected_manifest_sha256):
        if item["type"] == "header":
            header = item
        elif item["type"] == "chunk":
            path = downloads.get(item["file_id"], downloads.get(item["file_name"]))
            _require(isinstance(path, str) and Path(path).is_file(), "REMOTE_CHUNK_DOWNLOAD_MISSING")
    manifest_hash = _hash_file(manifest)[0]
    output_db = Path(output_db).resolve()
    _require(not output_db.exists(), "RESTORE_DESTINATION_ALREADY_EXISTS")
    _private_file(output_db)
    db = sqlite3.connect(str(output_db), timeout=30)
    db.execute("PRAGMA synchronous=FULL")
    db.execute("PRAGMA temp_store=MEMORY")
    incoming_record, outgoing, cipher_digest, cipher_size = None, None, None, 0
    count, total_bytes = 0, 0

    def finish_record():
        nonlocal outgoing
        if outgoing is not None:
            outgoing.close()
            outgoing = None
            _require(cipher_size == incoming_record["ciphertext_bytes"] and
                     cipher_digest.hexdigest() == incoming_record["ciphertext_sha256"],
                     "RESTORED_CIPHERTEXT_MISMATCH")

    try:
        db.execute("BEGIN IMMEDIATE")
        db.execute(SOURCE_DDL)
        for item in _manifest_events(manifest, manifest_hash):
            kind = item["type"]
            if kind == "record":
                finish_record()
                count += 1
                incoming_record, cipher_digest, cipher_size = item, hashlib.sha256(), 0
                _insert_source(db, count, _metadata_values(item["metadata"]), item["ciphertext_bytes"])
                outgoing = db.blobopen("source_records", "ciphertext", count, readonly=False)
            elif kind == "chunk":
                path = downloads.get(item["file_id"], downloads.get(item["file_name"]))
                chunk_digest, chunk_size = hashlib.sha256(), 0
                with Path(path).open("rb") as source:
                    while block := source.read(min(IO_BYTES, item["size_bytes"] - chunk_size + 1)):
                        chunk_size += len(block)
                        _require(chunk_size <= item["size_bytes"], "REMOTE_CHUNK_LENGTH_MISMATCH")
                        outgoing.write(block)
                        chunk_digest.update(block)
                        cipher_digest.update(block)
                        cipher_size += len(block)
                        total_bytes += len(block)
                _require(chunk_size == item["size_bytes"] and chunk_digest.hexdigest() == item["sha256"],
                         "REMOTE_CHUNK_DIGEST_MISMATCH")
            elif kind == "complete":
                finish_record()
        db.execute("CREATE TABLE remote_custody_restore(operation_key TEXT,manifest_sha256 TEXT,"
                   "snapshot_sha256 TEXT,records_restored INTEGER,ciphertext_bytes_restored INTEGER)")
        db.execute("INSERT INTO remote_custody_restore VALUES (?,?,?,?,?)",
                   (header["operation_key"], manifest_hash, header["snapshot_sha256"], count, total_bytes))
        db.commit()
    except BaseException:
        if outgoing is not None:
            outgoing.close()
        db.rollback()
        raise
    finally:
        db.close()
    return {"ok": True, "operation_key": header["operation_key"], "restore_state": "confirmed",
            "records_restored": count, "ciphertext_bytes_restored": total_bytes,
            "manifest_sha256": manifest_hash, "snapshot_sha256": header["snapshot_sha256"]}


class _Parser(argparse.ArgumentParser):
    def error(self, message):
        raise CustodyError("INVALID_ARGUMENTS")


def _parser():
    parser = _Parser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True, parser_class=_Parser)
    p = sub.add_parser("prepare")
    for name in ("source-db", "journal", "operation-id", "account-ref", "folder-id"):
        p.add_argument("--" + name, required=True)
    p.add_argument("--chunk-bytes", type=int, default=4 * 1024 * 1024)
    for name in ("jobs", "status", "record-search", "record-upload", "record-readback", "record-failure"):
        p = sub.add_parser(name)
        p.add_argument("--journal", required=True)
        if name == "jobs":
            p.add_argument("--limit", type=int, default=100)
            p.add_argument("--cursor", type=int, default=0)
        if name.startswith("record-"):
            p.add_argument("--object-id", required=True)
        if name == "record-search":
            p.add_argument("--file-id", action="append", default=[], dest="file_ids")
            p.add_argument("--complete", action="store_true")
        if name in ("record-upload", "record-readback"):
            p.add_argument("--file-id", required=True)
        if name == "record-readback":
            p.add_argument("--download", required=True)
        if name == "record-failure":
            p.add_argument("--code", default="NATIVE_CALL_FAILED")
    for name in ("restore", "restore-jobs"):
        p = sub.add_parser(name)
        p.add_argument("--manifest", required=True)
        p.add_argument("--expected-manifest-sha256")
        if name == "restore-jobs":
            p.add_argument("--limit", type=int, default=100)
            p.add_argument("--cursor", type=int, default=0)
        else:
            p.add_argument("--downloads", required=True)
            p.add_argument("--output-db", required=True)
    return parser


def main(argv=None):
    try:
        args = vars(_parser().parse_args(argv))
        command = args.pop("command").replace("-", "_")
        result = globals()[command](**args)
        print(_json(result))
        return 0 if result.get("ok") else 1
    except KeyboardInterrupt:
        print(_json({"ok": False, "error": "KeyboardInterrupt", "code": "INTERRUPTED"}), file=sys.stderr)
        return 130
    except Exception as exc:
        code = exc.code if isinstance(exc, CustodyError) else (
            "SQLITE_ERROR" if isinstance(exc, sqlite3.Error) else
            "FILESYSTEM_ERROR" if isinstance(exc, OSError) else "INVALID_DATA")
        print(_json({"ok": False, "error": type(exc).__name__, "code": code}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
