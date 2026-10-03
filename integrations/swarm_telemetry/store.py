"""Append-only measurements and cached views; never calls an upstream provider."""
from __future__ import annotations

import hashlib
import copy
import json
import re
import sqlite3
import time
from threading import Lock, RLock
from datetime import datetime, timezone, timedelta
from pathlib import Path

SCHEMA_VERSION = 1
_DB_WRITE_LOCK = RLock()
_PRIVATE_KEYS = {"password", "passwd", "secret", "access_token", "refresh_token", "api_key", "apikey", "authorization", "cookie", "cookies", "private_key", "encrypted_content", "reasoning", "chain_of_thought", "recovery_code", "otp", "base_instructions"}
_SECRETS = re.compile(r"(?i)(?:\b(?:sk|ghp|gho|github_pat|xox[baprs])[-_][A-Za-z0-9_-]{12,}|\bBearer\s+[A-Za-z0-9._~+/-]{8,}|-----BEGIN [^-]*PRIVATE KEY-----[\s\S]*?-----END [^-]*PRIVATE KEY-----|\b(?:password|api[_-]?key|access[_-]?token|refresh[_-]?token)\s*[:=]\s*[\"']?[^\s\"',;]{6,})")

def now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def redact(value):
    if isinstance(value, dict):
        return {str(k): redact(v) for k, v in value.items() if str(k).lower() not in _PRIVATE_KEYS}
    if isinstance(value, (list, tuple)):
        return [redact(v) for v in value]
    if isinstance(value, str):
        return _SECRETS.sub("[redacted]", value)
    if value is None or isinstance(value, (bool, int, float)):
        return value
    return str(value)

def stable_id(*parts):
    return hashlib.sha256("\x1f".join(str(p) for p in parts).encode()).hexdigest()[:32]

def iso(value):
    if not value:
        return None
    try:
        if isinstance(value, (int, float)) or (isinstance(value, str) and re.fullmatch(r"\d+(?:\.\d+)?", value)):
            number = float(value)
            if number > 100000000000:
                number /= 1000
            return datetime.fromtimestamp(number, timezone.utc).isoformat().replace("+00:00", "Z")
        return datetime.fromisoformat(str(value).replace("Z", "+00:00")).astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    except (ValueError, OverflowError, OSError):
        return None

class Store:
    def __init__(self, path, key_loader=None):
        self.path = str(Path(path))
        self._snapshot_cache={}
        self._snapshot_lock=Lock()
        self._write_lock=_DB_WRITE_LOCK
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        with self._write_lock, self.connect() as db:
            db.executescript("""
                PRAGMA journal_mode=WAL;
                CREATE TABLE IF NOT EXISTS events (
                    seq INTEGER PRIMARY KEY AUTOINCREMENT, event_id TEXT UNIQUE NOT NULL,
                    source TEXT NOT NULL, source_id TEXT, occurred_at TEXT, observed_at TEXT NOT NULL,
                    event_type TEXT, peer_id TEXT, session_id TEXT, agent_id TEXT, parent_agent_id TEXT,
                    provider TEXT, model TEXT, harness TEXT, work_id TEXT, operation_id TEXT,
                    status TEXT, summary TEXT, url TEXT, payload TEXT NOT NULL);
                CREATE INDEX IF NOT EXISTS event_time ON events(occurred_at);
                CREATE INDEX IF NOT EXISTS event_session ON events(session_id,seq);
                CREATE INDEX IF NOT EXISTS event_work ON events(work_id,seq);
                CREATE INDEX IF NOT EXISTS event_operation ON events(operation_id,seq);
                CREATE INDEX IF NOT EXISTS event_source_cursor ON events(source,seq);
                CREATE INDEX IF NOT EXISTS event_peer_census ON events(peer_id);
                CREATE INDEX IF NOT EXISTS event_provider_census ON events(provider,session_id);
                CREATE INDEX IF NOT EXISTS event_harness_census ON events(harness,session_id);
                CREATE TABLE IF NOT EXISTS sessions (session_id TEXT PRIMARY KEY, agent_id TEXT,
                    peer_id TEXT, parent_agent_id TEXT, provider TEXT, model TEXT, harness TEXT,
                    status TEXT, summary TEXT, work_id TEXT, last_activity_at TEXT, payload TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS coverage (source_id TEXT PRIMARY KEY, payload TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS coverage_projection (source_id TEXT PRIMARY KEY,
                    source TEXT, account_ref TEXT, harness TEXT, status TEXT, complete INTEGER, observed_at TEXT);
                CREATE TRIGGER IF NOT EXISTS coverage_projection_insert AFTER INSERT ON coverage BEGIN
                    INSERT OR REPLACE INTO coverage_projection VALUES (new.source_id,
                        COALESCE(json_extract(new.payload,'$.service'),json_extract(new.payload,'$.source'),'unknown'),
                        COALESCE(json_extract(new.payload,'$.account_ref'),json_extract(new.payload,'$.account_id'),''),
                        COALESCE(json_extract(new.payload,'$.harness'),''),
                        COALESCE(json_extract(new.payload,'$.status'),'unknown'),
                        json_extract(new.payload,'$.complete'),json_extract(new.payload,'$.observed_at'));
                END;
                CREATE TRIGGER IF NOT EXISTS coverage_projection_delete AFTER DELETE ON coverage BEGIN
                    DELETE FROM coverage_projection WHERE source_id=old.source_id;
                END;
                INSERT OR IGNORE INTO coverage_projection SELECT source_id,
                    COALESCE(json_extract(payload,'$.service'),json_extract(payload,'$.source'),'unknown'),
                    COALESCE(json_extract(payload,'$.account_ref'),json_extract(payload,'$.account_id'),''),
                    COALESCE(json_extract(payload,'$.harness'),''),COALESCE(json_extract(payload,'$.status'),'unknown'),
                    json_extract(payload,'$.complete'),json_extract(payload,'$.observed_at') FROM coverage;
                CREATE INDEX IF NOT EXISTS coverage_group ON coverage_projection(source,account_ref,harness,status,complete,observed_at);
                CREATE TABLE IF NOT EXISTS checkpoints (source_id TEXT PRIMARY KEY, payload TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS accounts (account_id TEXT PRIMARY KEY, payload TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS notifications (notification_id TEXT PRIMARY KEY,
                    occurred_at TEXT, payload TEXT NOT NULL, delivery_state TEXT DEFAULT 'available', receipt TEXT);
                CREATE TABLE IF NOT EXISTS runtime_state (key TEXT PRIMARY KEY, payload TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS source_records (ref TEXT PRIMARY KEY,source_id TEXT,sha256 TEXT,byte_length INTEGER,character_length INTEGER,iv BLOB,ciphertext BLOB,mac BLOB,format TEXT,key_reference TEXT);
                CREATE INDEX IF NOT EXISTS source_record_sizes ON source_records(byte_length,character_length);
            """)
        from .custody import Custody
        self.custody = Custody(self.path, key_loader=key_loader, write_lock=self._write_lock)

    def connect(self):
        db = sqlite3.connect(self.path, timeout=30)
        db.execute("PRAGMA busy_timeout=30000")
        db.row_factory = sqlite3.Row
        return db

    def envelope(self, **items):
        return {"ok": True, "schema_version": SCHEMA_VERSION, "observed_at": now(), **items}

    def ingest(self, events, *, coverage=None, accounts=None, checkpoints=None):
        inserted = []
        if isinstance(coverage,dict):
            if coverage and all(isinstance(v,dict) for v in coverage.values()):
                coverage=[{"source_id":str(k),**v} for k,v in coverage.items()]
            else:
                coverage=[{"source_id":str(coverage.get("source_id") or coverage.get("source") or "collection-progress"),**coverage}]
        if isinstance(accounts,dict): accounts=list(accounts.values())
        incoming_rows=list(events or ())
        prepared=[]
        custody_records=[]
        source_bodies={}
        for incoming in incoming_rows:
            if not isinstance(incoming,dict): continue
            source_body=incoming.get("full_source")
            source_ref=None
            if source_body is not None:
                source_ref,custody_record=self.custody.prepare(source_body,incoming.get("source_id") or incoming.get("event_id"))
                custody_records.append(custody_record)
            event=redact({key:value for key,value in incoming.items() if key!="full_source"})
            if source_ref: event["source_record_ref"]=source_ref
            prepared.append(event)
            if source_body is not None: source_bodies[id(event)]=source_body
        columns = "event_id source source_id occurred_at observed_at event_type peer_id session_id agent_id parent_agent_id provider model harness work_id operation_id status summary url".split()
        for event in prepared:
            event["source"] = str(event.get("source") or "observation")
            event["source_id"] = str(event.get("source_id") or event.get("event_id") or stable_id(event))
            event["event_id"] = str(event.get("event_id") or stable_id(event["source"], event["source_id"], event.get("event_type"), event.get("occurred_at")))
            event["occurred_at"] = iso(event.get("occurred_at"))
            event["observed_at"] = iso(event.get("observed_at")) or now()
            complete_summary=str(event.get("summary") or "")
            event["summary"] = complete_summary[:1200]
            event["summary_is_projection"] = len(complete_summary)>1200

        candidate_ids=list(dict.fromkeys(event["event_id"] for event in prepared))
        with self._write_lock, self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            # One bounded lookup discovers existing revisions in this serialized
            # writer transaction. SQLite's 999-parameter ceiling is respected.
            prior_by_id={}
            for start in range(0,len(candidate_ids),500):
                ids=candidate_ids[start:start+500]
                if not ids: continue
                marks=",".join("?" for _ in ids)
                prior_by_id.update({row["event_id"]:row["payload"] for row in db.execute(
                    "SELECT event_id,payload FROM events WHERE event_id IN ("+marks+")",ids)})
            batch_source_hashes={}
            for event in prepared:
                source_ref=event.get("source_record_ref")
                base_id=event["event_id"]
                prior_payload=prior_by_id.get(base_id)
                old_hash=((json.loads(prior_payload).get("source_record_ref") or {}).get("sha256") if prior_payload else None)
                previous_hash=batch_source_hashes.get(base_id,old_hash)
                if source_ref:
                    current_hash=source_ref.get("sha256")
                    if previous_hash is not None and previous_hash != current_hash:
                        event["supersedes_event_id"]=base_id
                        event["event_id"] = base_id+":revision:"+str(current_hash or stable_id(source_ref))[:16]
                    else:
                        batch_source_hashes.setdefault(base_id,current_hash)
            # Ciphertext and its operational reference commit atomically with the
            # event row and cursor. Custody never opens a second writer connection.
            self.custody.insert_prepared(db,custody_records)
            session_updates={}
            for event in prepared:
                source_ref=event.get("source_record_ref")
                if not isinstance(event, dict):
                    continue
                values = [event.get(key) for key in columns] + [json.dumps(event, ensure_ascii=False)]
                cursor = db.execute("INSERT OR IGNORE INTO events (" + ",".join(columns) + ",payload) VALUES (" + ",".join("?" for _ in values) + ")", values)
                if not cursor.rowcount:
                    continue
                inserted.append(event)
                sid = event.get("session_id")
                if sid:
                    peer=session_updates.get(sid)
                    if peer is None:
                        previous=db.execute("SELECT payload FROM sessions WHERE session_id=?",(sid,)).fetchone()
                        peer=json.loads(previous[0]) if previous else {"session_id":sid,"agent_id":event.get("agent_id") or sid,"usage":{}}
                        session_updates[sid]=peer
                    for key in ("agent_id", "peer_id", "parent_agent_id", "provider", "model", "harness", "work_id"):
                        if event.get(key):
                            peer[key] = event[key]
                    at = event.get("occurred_at") or event["observed_at"]
                    if not peer.get("last_activity_at") or at >= peer["last_activity_at"]:
                        peer["last_activity_at"] = at
                        if event.get("status"):
                            peer["status"] = event["status"]
                        if event.get("summary"):
                            peer["summary"] = event["summary"]
                        peer["last_event_id"] = event["event_id"]
                    metrics = event.get("metrics") or {}
                    for key,value in metrics.items():
                        usage_metric=(key in {"input_tokens","output_tokens","cached_tokens","cached_input_tokens","reasoning_tokens","reasoning_output_tokens","total_tokens","cache_write_input_tokens","cost_usd","duration_ms"}
                                      or (key.startswith(("turn_delta_","thread_delta_","total_delta_")) and key.endswith("_tokens")))
                        if usage_metric and isinstance(value,(int,float)) and not isinstance(value,bool) and value>=0:
                            peer.setdefault("usage",{})[key]=peer.get("usage",{}).get(key,0)+value
            session_keys="session_id agent_id peer_id parent_agent_id provider model harness status summary work_id last_activity_at".split()
            for peer in session_updates.values():
                db.execute("INSERT OR REPLACE INTO sessions ("+",".join(session_keys)+",payload) VALUES ("+",".join("?" for _ in range(len(session_keys)+1))+ ")",
                           [peer.get(key) for key in session_keys]+[json.dumps(peer,ensure_ascii=False)])
            for item in coverage or []:
                if not isinstance(item,dict): continue
                item = redact(item)
                sid = str(item.get("source_id") or item.get("source") or "unknown")
                db.execute("INSERT OR REPLACE INTO coverage VALUES (?,?)", (sid, json.dumps(item, ensure_ascii=False)))
            for item in accounts or []:
                if not isinstance(item,dict): continue
                item = redact(item)
                aid = str(item.get("account_id") or item.get("id") or stable_id(item.get("service"), item.get("name"), item.get("reference")))
                item["account_id"] = aid
                db.execute("INSERT OR REPLACE INTO accounts VALUES (?,?)", (aid, json.dumps(item, ensure_ascii=False)))
            for key, value in (checkpoints or {}).items():
                db.execute("INSERT OR REPLACE INTO checkpoints VALUES (?,?)", (str(key), json.dumps(redact(value), ensure_ascii=False)))
            from .notifications import notifications_for_events,notification_events_for_source,merge_notification_metadata
            derived_notices=[]
            for event in inserted:
                if id(event) in source_bodies:
                    derived_notices.extend(notification_events_for_source(event,source_bodies[id(event)]))
            for item in notifications_for_events(inserted+derived_notices):
                item = redact(item)
                previous=db.execute("SELECT payload FROM notifications WHERE notification_id=?",(item["notification_id"],)).fetchone()
                if previous:
                    old=json.loads(previous[0])
                    item=merge_notification_metadata(old,item)
                    db.execute("UPDATE notifications SET payload=? WHERE notification_id=?",(json.dumps(item,ensure_ascii=False),item["notification_id"]))
                else:
                    db.execute("INSERT INTO notifications (notification_id,occurred_at,payload) VALUES (?,?,?)", (item["notification_id"], item.get("occurred_at") or now(), json.dumps(item, ensure_ascii=False)))
                for target in item.get("supersedes",[]):
                    prior_note=db.execute("SELECT payload FROM notifications WHERE notification_id=?",(target,)).fetchone()
                    if prior_note:
                        resolved=json.loads(prior_note[0]); resolved["status"]="resolved"; resolved["resolved_by"]=item["notification_id"]
                        db.execute("UPDATE notifications SET payload=? WHERE notification_id=?",(json.dumps(resolved,ensure_ascii=False),target))
        return self.envelope(inserted=len(inserted), duplicates=max(0,len(prepared)-len(inserted)))

    def checkpoints(self):
        with self.connect() as db:
            return {row[0]: json.loads(row[1]) for row in db.execute("SELECT * FROM checkpoints")}

    def state(self, key, value=None):
        if value is not None:
            with self._write_lock, self.connect() as db:
                db.execute("INSERT OR REPLACE INTO runtime_state VALUES (?,?)", (key, json.dumps(redact(value))))
                row = db.execute("SELECT payload FROM runtime_state WHERE key=?", (key,)).fetchone()
        else:
            with self.connect() as db:
                row = db.execute("SELECT payload FROM runtime_state WHERE key=?", (key,)).fetchone()
        return json.loads(row[0]) if row else None

    def events(self, *, cursor=0, limit=100, source=None, provider=None, harness=None, q=None, session_id=None, work_id=None, operation_id=None, event_id=None, order="asc"):
        descending = order == "desc"
        where = ["seq<?"] if descending and int(cursor)>0 else ["seq>?"]
        args = [int(cursor)] if descending and int(cursor)>0 else [0]
        if event_id:
            where.append("event_id=?")
            args.append(str(event_id))
        for key, value in (("source", source), ("provider", provider), ("harness", harness), ("session_id", session_id), ("work_id", work_id), ("operation_id", operation_id)):
            if value:
                where.append(key+"=?")
                args.append(value)
        if q:
            where.append("summary LIKE ?")
            args.append("%"+str(q)+"%")
        size = max(1, min(int(limit), 1000))
        with self.connect() as db:
            rows = list(db.execute("SELECT seq,payload FROM events WHERE " + " AND ".join(where) + " ORDER BY seq "+("DESC" if descending else "ASC")+" LIMIT ?", args+[size+1]))
        has_more = len(rows)>size
        selected = rows[:size]
        return self.envelope(events=[{**json.loads(row[1]), "cursor": row[0]} for row in selected], next_cursor=selected[-1][0] if selected else int(cursor), has_more=has_more)

    def peers(self, *, provider=None, harness=None, q=None, limit=1000):
        where, args = [], []
        for key, value in (("provider", provider), ("harness", harness)):
            if value:
                where.append(key+"=?")
                args.append(value)
        if q:
            where.append("(summary LIKE ? OR session_id LIKE ? OR peer_id LIKE ?)")
            args += ["%"+str(q)+"%"]*3
        with self.connect() as db:
            rows = list(db.execute("SELECT payload FROM sessions"+(" WHERE "+" AND ".join(where) if where else "")+" ORDER BY last_activity_at DESC LIMIT ?", args+[max(1,min(int(limit),10000))]))
        current = datetime.now(timezone.utc)
        peers = []
        for row in rows:
            item = json.loads(row[0])
            item["reported_status"] = item.get("status")
            try:
                age = (current-datetime.fromisoformat(item["last_activity_at"].replace("Z","+00:00"))).total_seconds()
            except (KeyError,ValueError):
                age = None
            item["activity_age_seconds"] = age
            if item.get("status") in {"executing", "running", "started", "waiting", "tool_wait"} and (age is None or age>300):
                item["status"] = "unknown"
            item["recently_observed"] = age is not None and 0<=age<=900
            peers.append(item)
        census=self.state("census") or {}
        by_id={item.get("session_id") or item.get("agent_id"):item for item in peers}
        for observation in census.get("peers",[]):
            sid=observation.get("session_id") or observation.get("agent_id")
            if sid:
                previous=by_id.get(sid,{})
                by_id[sid]={**previous,**{k:v for k,v in observation.items() if v is not None},"usage":previous.get("usage",observation.get("usage",{}))}
        peers=list(by_id.values())
        if provider: peers=[p for p in peers if p.get("provider")==provider]
        if harness: peers=[p for p in peers if p.get("harness")==harness]
        return self.envelope(peers=peers, returned=len(peers),complete=False,census_coverage=census.get("coverage",[]))

    def records(self, table, *, limit=1000, cursor="", q=None, source=None, provider=None, harness=None):
        if table not in {"coverage","accounts","notifications"}:
            raise ValueError("Unknown measurement collection")
        with self.connect() as db:
            identity={"coverage":"source_id","accounts":"account_id","notifications":"notification_id"}[table]
            where=[identity+">?"]
            args=[str(cursor or "")]
            if q:
                where.append("payload LIKE ?"); args.append("%"+str(q)+"%")
            for key,value in (("source",source),("provider",provider),("harness",harness)):
                if value:
                    where.append("json_extract(payload,'$."+key+"')=?"); args.append(value)
            size=max(1,min(int(limit),10000))
            clause=" WHERE "+" AND ".join(where)+" ORDER BY "+identity+" LIMIT ?"
            if table == "notifications":
                rows = list(db.execute("SELECT payload,delivery_state,receipt,notification_id FROM notifications"+clause,args+[size+1]))
                has_more=len(rows)>size; rows=rows[:size]
                items = [{**json.loads(row[0]), "delivery_state":row[1], "receipt":json.loads(row[2]) if row[2] else None} for row in rows]
            else:
                rows=list(db.execute("SELECT payload,"+identity+" FROM "+table+clause,args+[size+1]))
                has_more=len(rows)>size; rows=rows[:size]
                items=[json.loads(row[0]) for row in rows]
            next_cursor=rows[-1][-1] if rows else cursor
        return self.envelope(**{table:items},returned=len(items),next_cursor=next_cursor,has_more=has_more,result_complete=not has_more,corpus_complete=False)

    def work(self):
        with self.connect() as db:
            rows = list(db.execute("SELECT work_id,COUNT(*) AS events,COUNT(DISTINCT session_id) AS sessions,MIN(occurred_at) AS started_at,MAX(occurred_at) AS updated_at FROM events WHERE work_id IS NOT NULL AND work_id!='' GROUP BY work_id ORDER BY updated_at DESC LIMIT 1000"))
            items=[]
            for row in rows:
                item=dict(row)
                latest=db.execute("SELECT payload FROM events WHERE work_id=? ORDER BY COALESCE(occurred_at,observed_at) DESC,seq DESC LIMIT 1",(row["work_id"],)).fetchone()
                event=json.loads(latest[0])
                item.update(status=event.get("status"),summary=event.get("summary"),url=event.get("url"),source=event.get("source"))
                items.append(item)
        return self.envelope(work=items)

    def snapshot(self, *, detailed=False):
        cache=self._snapshot_cache.get(bool(detailed))
        if cache and time.monotonic()-cache[0]<5:
            return cache[1]
        # Readers reuse the last completed view while one refresh runs. Writes
        # never wait on a dashboard refresh and frequent ingest cannot evict it.
        if not self._snapshot_lock.acquire(blocking=cache is None):
            return {**cache[1],"snapshot_cache_age_seconds":round(time.monotonic()-cache[0],3),"snapshot_refreshing":True}
        try:
            cache=self._snapshot_cache.get(bool(detailed))
            if cache and time.monotonic()-cache[0]<5:
                return cache[1]
            value=self._snapshot(detailed=detailed)
            self._snapshot_cache[bool(detailed)]=(time.monotonic(),value)
            return value
        finally:
            self._snapshot_lock.release()

    def _snapshot(self, *, detailed=False):
        with self.connect() as db:
            event_count=db.execute("SELECT COUNT(*) FROM events").fetchone()[0]
            session_count=db.execute("SELECT COUNT(*) FROM sessions").fetchone()[0]
            peer_count=db.execute("SELECT COUNT(DISTINCT peer_id) FROM events WHERE peer_id IS NOT NULL AND peer_id!=''").fetchone()[0]
            providers=[dict(row) for row in db.execute("SELECT COALESCE(provider,'unknown') AS provider,COUNT(*) AS events,COUNT(DISTINCT session_id) AS sessions FROM events GROUP BY provider ORDER BY events DESC")]
            harnesses=[dict(row) for row in db.execute("SELECT COALESCE(harness,'unknown') AS harness,COUNT(*) AS events,COUNT(DISTINCT session_id) AS sessions FROM events GROUP BY harness ORDER BY events DESC")]
            activity=[dict(row) for row in db.execute("SELECT SUBSTR(occurred_at,1,10) AS date,COUNT(*) AS events FROM events WHERE occurred_at IS NOT NULL GROUP BY date ORDER BY date DESC LIMIT 90")][::-1]
            usage={"input_tokens":0,"output_tokens":0,"cached_tokens":0,"reasoning_tokens":0,"cost_usd":None,"sessions_with_usage":0}
            for row in db.execute("SELECT payload FROM sessions"):
                item=json.loads(row[0]).get("usage",{})
                if item:
                    usage["sessions_with_usage"]+=1
                for key in ("input_tokens","output_tokens","cached_tokens","reasoning_tokens"):
                    usage[key]+=item.get(key,0)
                if item.get("cost_usd") is not None:
                    usage["cost_usd"]=(usage["cost_usd"] or 0)+item["cost_usd"]
            usage["accounting_coverage"] = usage["sessions_with_usage"]/session_count if session_count else None
            captured=db.execute("SELECT COUNT(*),COALESCE(SUM(byte_length),0),SUM(character_length) FROM source_records").fetchone()
        peers=self.peers(limit=10000)["peers"]
        counts={"events":event_count,"sessions":session_count,"peers":peer_count,"executing":sum(p.get("status") in {"executing","running","started"} for p in peers),"waiting":sum(p.get("status") in {"waiting","tool_wait","blocked"} for p in peers),"recently_observed":sum(bool(p.get("recently_observed")) for p in peers),"unknown":sum(p.get("status") in {None,"unknown"} for p in peers)}
        coverage_page=self.records("coverage")
        coverage=coverage_page["coverage"]
        value=self.envelope(counts=counts,usage=usage,providers=providers,harnesses=harnesses,activity=activity,coverage=coverage,sources=coverage,notifications=self.records("notifications",limit=100)["notifications"],work=self.work()["work"],accounts=self.records("accounts")["accounts"],runtime=self.state("collector"),definitions={"executing":"Fresh explicit runtime execution observations; stale execution state becomes unknown.","recently_observed":"Session activity within the preceding 15 minutes, independent of execution state.","peers":"Distinct recorded peer labels; shared accounts and sessions are separate entities.","usage":"Incremental reported usage; absent monetary charges are unknown."})
        value["census"]=self.state("census")
        value["storage"]=self.state("storage_guard")
        value["reader_health"]={kind:self.state("source_reader_health:"+kind) for kind in ("slack","github","services")}
        value["capture"]={"records":captured[0],"bytes":captured[1],"characters":captured[2],"exact_source_custody":True,"key_reference":"telemetry/source-custody-key"}
        value["coverage_page"]={key:coverage_page[key] for key in ("returned","next_cursor","has_more","result_complete","corpus_complete")}
        value["source_groups"]=self.coverage_summary()
        value["corpus_scope"]="All accounts and all services: Slack, GitHub, machine and cloud activity"
        value["corpus_complete"]=False
        if detailed:
            value["peers"]=peers
            with self.connect() as db:
                value["events"]=[{**json.loads(row[1]),"cursor":row[0]} for row in db.execute("SELECT seq,payload FROM events ORDER BY seq DESC LIMIT 300")]
        return value

    def coverage_summary(self):
        """All recorded partitions, independent of source-list pagination."""
        groups={}
        with self.connect() as db:
            rows=db.execute("SELECT source,account_ref,harness,status,complete,COUNT(*) AS partitions,MAX(observed_at) AS observed_at FROM coverage_projection GROUP BY source,account_ref,harness,status,complete")
            for row in rows:
                key=(row["source"],row["account_ref"],row["harness"])
                group=groups.setdefault(key,{"name":key[0],"account":key[1],"harness":key[2],"partitions":0,"complete":0,"pending":0,"unknown":0,"statuses":{},"metrics":{},"observed_at":None,"scope":"all recorded source partitions"})
                count=row["partitions"]
                group["partitions"]+=count
                group["complete" if row["complete"]==1 else "pending" if row["complete"]==0 else "unknown"]+=count
                group["statuses"][row["status"]]=group["statuses"].get(row["status"],0)+count
                if row["observed_at"] and (not group["observed_at"] or row["observed_at"]>group["observed_at"]): group["observed_at"]=row["observed_at"]
        return sorted(groups.values(),key=lambda item:(-item["partitions"],item["name"],item["account"]))

    def metrics(self):
        snapshot=self.snapshot()
        return self.envelope(metrics=[{"metric":key,"value":value,"definition":snapshot["definitions"].get(key),"scope":"collected observations"} for key,value in snapshot["counts"].items()],usage=snapshot["usage"],providers=snapshot["providers"],harnesses=snapshot["harnesses"],activity=snapshot["activity"],coverage=snapshot["coverage"])

    def delivery_receipt(self, notification_id, state, receipt):
        with self._write_lock, self.connect() as db:
            db.execute("UPDATE notifications SET delivery_state=?,receipt=? WHERE notification_id=?",(state,json.dumps(redact(receipt)),notification_id))

    def export(self, path, *, public=False):
        value=copy.deepcopy(self.snapshot(detailed=True))
        if public:
            # Public bake has operational metadata; private excerpts remain in the source runtime.
            for event in value.get("events",[]):
                if event.get("source") in {"codex","claude","gemini","transcript","gmail"}:
                    event["summary"]="Session execution observation"
                    event.pop("metadata",None)
                    event.pop("url",None)
            for peer in value.get("peers",[]):
                peer["summary"]="Session execution observation"
            for item in value.get("coverage",[]):
                item.pop("path",None)
                item.pop("roots",None)
            value["sources"]=value["coverage"]
        dest=Path(path)
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_text(json.dumps(redact(value),ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        return self.envelope(path=str(dest),bytes=dest.stat().st_size,public=public)
