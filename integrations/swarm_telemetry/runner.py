"""Independent source collection and notification delivery over existing roads."""
from __future__ import annotations
import json
import os
import shutil
import subprocess
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from queue import Queue,Empty,Full
from threading import Event,Thread,RLock

from .store import now,redact,stable_id

def unwrap(value):
    for _ in range(6):
        if isinstance(value,dict) and isinstance(value.get("result"),dict): value=value["result"]
        elif isinstance(value,dict) and isinstance(value.get("structuredContent"),dict): value=value["structuredContent"]
        elif isinstance(value,dict) and isinstance(value.get("content"),list):
            texts=[v.get("text","") for v in value["content"] if v.get("type")=="text"]
            if not texts: break
            try: value=json.loads(texts[0])
            except (ValueError,TypeError): break
        else: break
    return value

class Gateway:
    def __init__(self,url="http://127.0.0.1:8878",timeout=25):
        self.url=url.rstrip("/")
        self.timeout=timeout
    def call(self,name,arguments=None,operation_id=None):
        op=operation_id or "telemetry-read:"+stable_id(name,arguments or {},now())
        body={"request_id":op,"call_id":op,"name":name,"arguments":arguments or {}}
        request=urllib.request.Request(self.url+"/v1/tools/call",data=json.dumps(body).encode(),headers={"Content-Type":"application/json"})
        with urllib.request.urlopen(request,timeout=self.timeout) as response: value=json.load(response)
        if value.get("isError") or value.get("error"):
            return value
        return unwrap(value)

class Runner:
    def __init__(self,store,config=None):
        self.store=store
        self.config=config or {}
        self.stop_event=Event()
        self.queue=Queue(maxsize=4096)
        self.gateway=Gateway(self.config.get("gateway","http://127.0.0.1:8878"))
        self.thread=None
        self.last_provider={}
        self.errors={}
        self.dropped=0
        self.provider_threads=[]
        self.discovered_sources=[]
        self.reader_wakes={name:Event() for name in ("local","inventory","census","discovery","machine","slack","github","services")}
        self.storage_status={}
        self._storage_lock=RLock()
        self._storage_checked=0
        self._storage_reported={}
    def storage_ready(self,label="collection"):
        with self._storage_lock:
            stamp=time.monotonic()
            if not self.storage_status or stamp-self._storage_checked>=5:
                floor=max(1024**3,int(self.config.get("collection_min_free_bytes",1024**3)))
                try:
                    free=shutil.disk_usage(Path(self.store.path).parent).free
                    status={"status":"ready" if free>=floor else "pending_storage","free_bytes":free,"required_free_bytes":floor,"observed_at":now(),"scope":"telemetry source collection only","checkpoints_preserved":True,"swarm_execution_independent":True}
                except OSError as error:
                    status={"status":"pending_storage","error":type(error).__name__,"required_free_bytes":floor,"observed_at":now(),"scope":"telemetry source collection only","checkpoints_preserved":True,"swarm_execution_independent":True}
                self.storage_status=status
                self._storage_checked=stamp
            status=dict(self.storage_status)
            last=self._storage_reported.get(label,{})
            if last.get("status")!=status["status"] or stamp-last.get("at",0)>=60:
                self._storage_reported[label]={"status":status["status"],"at":stamp}
                try:
                    self.store.state("storage_guard",status)
                    if status["status"]!="ready":
                        health=self.store.state("source_reader_health:"+label) or {}
                        self.store.state("source_reader_health:"+label,{**health,"status":"pending_storage","storage_observed_at":status["observed_at"],"required_free_bytes":status["required_free_bytes"],"checkpoints_preserved":True})
                except Exception as error: self.errors["storage-status"]=type(error).__name__
            return status["status"]=="ready"
    def storage_wait(self,label):
        return {"kind":label,"status":"pending_storage","checkpoints_preserved":True,"new_source_reads":0}
    def request_collection(self,kind):
        wake=self.reader_wakes.get(kind)
        if wake: wake.set()
        return bool(wake)
    def ingest_batch(self,events,**parts):
        batch_size=max(1,min(1000,int(self.config.get("source_ingest_batch_events",128))))
        results=[]
        for offset in range(0,len(events),batch_size):
            results.append(self.store.ingest(events[offset:offset+batch_size]))
        results.append(self.store.ingest([],**parts))
        return {"inserted":sum(result.get("inserted",0) for result in results),"events":len(events),"batches":len(results)}
    def offer(self,events,**parts):
        try: self.queue.put_nowait((events,parts)); return len(events)
        except Full: self.dropped+=len(events); return 0
    def collect_local(self):
        if not self.storage_ready("local"): return self.storage_wait("local")
        from .collectors import collect_transcripts
        roots=self.config.get("transcript_roots",[])
        if not roots: return {"inserted":0}
        result=collect_transcripts(roots,self.store.checkpoints(),self.config.get("transcript_batch_files",64))
        coverage=result.get("coverage",[])
        if isinstance(coverage,dict): coverage=[coverage]
        for row in coverage:
            row.setdefault("source_id","transcripts")
            row.setdefault("source","machine-transcripts")
            row.setdefault("status","live" if row.get("complete") else "backfilling")
            row.setdefault("observed_at",now())
            row.setdefault("records",len(result.get("events",[])))
        return self.ingest_batch(result.get("events",[]),coverage=coverage,checkpoints=result.get("checkpoints",{}))
    def collect_census(self):
        from .census import collect_census
        config={**self.config,"gateway_url":self.config.get("gateway","http://127.0.0.1:8878")}
        path=self.config.get("native_runtime_path")
        if path:
            try: config.update(json.loads(Path(path).read_text(encoding="utf-8-sig")))
            except (OSError,ValueError): pass
        value=collect_census(config)
        self.store.state("census",value)
        self.store.ingest([],coverage=value.get("coverage",[]))
        return value.get("counts",{})
    def collect_discovery(self):
        from .discovery import discover_sources
        config={**self.config,"service_catalog_path":self.config.get("service_catalog_path",str(Path(self.store.path).parent/"service-catalog.json"))}
        previous=self.store.state("source_discovery") or {}
        result=discover_sources(config,state=previous.get("state",{}))
        self.discovered_sources=result.get("sources",[])
        for key in ("slack_channels","github_repositories"):
            self.config[key]=sorted(set(self.config.get(key,[])+result.get(key,[])))
        self.store.state("source_discovery",result)
        coverage=result.get("coverage",[])
        if isinstance(coverage,dict): coverage=[coverage]
        self.store.ingest([],coverage=coverage+self.discovered_sources,accounts=result.get("accounts",[]))
        return {"sources":len(self.discovered_sources),"channels":len(self.config.get("slack_channels",[])),"repositories":len(self.config.get("github_repositories",[]))}
    def collect_machine(self):
        if not self.storage_ready("machine"): return self.storage_wait("machine")
        from .machine_activity import collect_machine_activity
        result=collect_machine_activity(self.config,checkpoints=self.store.checkpoints())
        coverage=result.get("coverage",[])
        if isinstance(coverage,dict): coverage=[coverage]
        return self.ingest_batch(result.get("events",[]),coverage=coverage,checkpoints=result.get("checkpoints",{}))
    def collect_extended(self,kind):
        if not self.storage_ready(kind): return self.storage_wait(kind)
        from .source_engine import SourceEngine
        return SourceEngine(self.store,self.config).run(kind)
    def _source_error(self,source,exc):
        self.errors[source]=type(exc).__name__
        try:
            self.store.ingest([],coverage=[{"source_id":source,"source":source.split(":")[0],"status":"pending_recovery","observed_at":now(),"complete":False,"error":type(exc).__name__,"collection_only":True}])
            self.store.state("source_reader_health:"+source,{"observed_at":now(),"error":type(exc).__name__,"complete":False,"retrying":True})
        except Exception as storage_error:
            # A failed diagnostic write cannot terminate a source worker.
            self.errors["diagnostic:"+source]=type(storage_error).__name__
    def collect_slack(self):
        if not self.storage_ready("slack"): return self.storage_wait("slack")
        from .collectors import normalize_slack
        checkpoints=self.store.checkpoints()
        result=[]
        channels=self.config.get("slack_channels",[])
        for channel in channels:
            sid="slack:"+channel
            checkpoint=checkpoints.get(sid,{})
            args={"channel_id":channel,"limit":100}
            if checkpoint.get("cursor"): args["cursor"]=checkpoint["cursor"]
            elif checkpoint.get("high_water"):
                args["oldest"]=str(max(0,float(checkpoint["high_water"])-300))
            try:
                payload=self.gateway.call("slack_read_channel",args)
                if payload.get("isError") or payload.get("error"):
                    self._source_error(sid,RuntimeError("connector_unavailable")); continue
                payload={**payload,"channel_id":channel}
                page_ref=self.store.custody.seal(payload,sid+":page:"+str(args.get("cursor",args.get("oldest","origin"))))
                events=normalize_slack(payload)
                for event in events: event.setdefault("metadata",{})["page_source_ref"]=page_ref
                native=payload.get("messages",[])
                cursor=(payload.get("response_metadata") or {}).get("next_cursor") or payload.get("next_cursor")
                timestamps=[str(v.get("ts")) for v in native if isinstance(v,dict) and v.get("ts")]
                high_water=max(timestamps,key=float) if timestamps else checkpoint.get("high_water")
                self.store.ingest(events,coverage=[{"source_id":sid,"source":"slack","scope":channel,"status":"live","observed_at":now(),"records":len(events),"complete":not bool(cursor),"cursor":cursor,"historical_complete":checkpoint.get("historical_complete",False) or not bool(cursor)}],checkpoints={sid:{"cursor":cursor,"high_water":high_water,"historical_complete":checkpoint.get("historical_complete",False) or not bool(cursor)}})
                # Thread pages are independent source partitions, including old roots with new replies.
                for message in native if isinstance(native,list) else []:
                    if not isinstance(message,dict) or not message.get("reply_count"): continue
                    ts=str(message.get("thread_ts") or message.get("ts"))
                    thread_id=sid+":"+ts
                    tc=checkpoints.get(thread_id,{})
                    thread_args={"channel_id":channel,"thread_ts":ts,"limit":100}
                    if tc.get("cursor"): thread_args["cursor"]=tc["cursor"]
                    try:
                        thread=self.gateway.call("slack_read_thread",thread_args)
                        thread={**thread,"channel_id":channel}
                        thread_ref=self.store.custody.seal(thread,thread_id+":page:"+str(thread_args.get("cursor","origin")))
                        te=normalize_slack(thread)
                        for event in te: event.setdefault("metadata",{})["page_source_ref"]=thread_ref
                        next_cursor=(thread.get("response_metadata") or {}).get("next_cursor") or thread.get("next_cursor")
                        self.store.ingest(te,coverage=[{"source_id":thread_id,"source":"slack","scope":channel+"/"+ts,"status":"live","observed_at":now(),"records":len(te),"complete":not bool(next_cursor),"cursor":next_cursor}],checkpoints={thread_id:{"cursor":next_cursor}})
                    except Exception as exc: self._source_error(thread_id,exc)
                result.append({"source":sid,"records":len(events)})
            except Exception as exc: self._source_error(sid,exc)
        return result
    def collect_github(self):
        if not self.storage_ready("github"): return self.storage_wait("github")
        from .collectors import normalize_github
        results=[]
        for repo in self.config.get("github_repositories",[]):
            sid="github:"+repo
            checkpoint=self.store.checkpoints().get(sid,{})
            page=int(checkpoint.get("page",1))
            command=[self.config.get("gh","gh"),"api",f"repos/{repo}/issues?state=all&sort=updated&direction=desc&per_page=100&page={page}"]
            try:
                completed=subprocess.run(command,capture_output=True,text=True,timeout=30,creationflags=getattr(subprocess,"CREATE_NO_WINDOW",0))
                if completed.returncode:
                    raise RuntimeError("github_connector_read_failed")
                data=json.loads(completed.stdout)
                page_ref=self.store.custody.seal(completed.stdout,sid+":issues:"+str(page))
                events=normalize_github({"items":data,"repository":repo},repo=repo)
                for event in events: event.setdefault("metadata",{})["page_source_ref"]=page_ref
                more=len(data)==100
                self.store.ingest(events,coverage=[{"source_id":sid,"source":"github","scope":repo,"status":"live","observed_at":now(),"records":len(events),"complete":not more,"historical_complete":checkpoint.get("historical_complete",False) or not more,"page":page}],checkpoints={sid:{"page":page+1 if more else 1,"historical_complete":checkpoint.get("historical_complete",False) or not more}})
                results.append({"source":sid,"records":len(events)})
            except Exception as exc: self._source_error(sid,exc)
        return results
    def collect_inventory(self):
        from .account_inventory import collect_account_inventory
        paths=self.config.get("inventory_paths",[])
        payloads=[]
        for path in paths:
            try:
                value=json.loads(Path(path).read_text(encoding="utf-8-sig"))
                payloads.append({"source":str(path),"data":value})
            except Exception as exc: self._source_error("inventory:"+Path(path).name,exc)
        try:
            refs=self.gateway.call("credential_references",{})
            if not refs.get("isError") and not refs.get("error"):
                payloads.append({"source":"shared-secure-reference-metadata","data":refs})
                self.errors.pop("inventory:credential_references",None)
                observed=now()
                self.store.ingest([],coverage=[{"source_id":"inventory:credential_references","source":"inventory","status":"observed","observed_at":observed,"complete":True,"records":len(refs.get("references",[])),"scope":"all returned shared secure credential reference metadata","same_references_for_every_peer":bool(refs.get("same_references_for_every_peer"))}])
                self.store.state("source_reader_health:inventory:credential_references",{"status":"observed","observed_at":observed,"records":len(refs.get("references",[])),"complete":True})
        except Exception as exc: self._source_error("inventory:credential_references",exc)
        result=collect_account_inventory(payloads)
        if isinstance(result,list): accounts=result; coverage=[]
        else: accounts=result.get("accounts",result.get("records",[])); coverage=result.get("coverage",[])
        if isinstance(coverage,dict): coverage=[coverage]
        return self.store.ingest([],accounts=accounts,coverage=coverage)
    def collect_once(self,providers=True):
        local=self.collect_local()
        provider_results={}
        if providers:
            try: provider_results["discovery"]=self.collect_discovery()
            except Exception as exc: self._source_error("discovery",exc)
            with ThreadPoolExecutor(max_workers=3,thread_name_prefix="measurement-source") as pool:
                futures={name:pool.submit(fn) for name,fn in (("slack",lambda:self.collect_extended("slack")),("github",lambda:self.collect_extended("github")),("services",lambda:self.collect_extended("services")),("inventory",self.collect_inventory),("census",self.collect_census),("machine",self.collect_machine))}
                for name,future in futures.items():
                    try: provider_results[name]=future.result()
                    except Exception as exc: self._source_error(name,exc)
        state={"mode":"passive","observed_at":now(),"local":local,"providers":provider_results,"errors":self.errors,"dropped_observations":self.dropped,"jev_required":False}
        self.store.state("collector",state)
        return state
    def dispatch_notifications(self):
        channel=self.config.get("notification_channel")
        if not channel: return {"sent":0,"enabled":False}
        sent=0
        for note in self.store.records("notifications",limit=1000)["notifications"]:
            if note.get("delivery_state")!="available": continue
            # Backfill remains available in the feed, without replaying old notices to Slack.
            occurred=note.get("occurred_at")
            if not isinstance(occurred,str) or not occurred: continue
            try:
                from datetime import datetime,timezone
                age=(datetime.now(timezone.utc)-datetime.fromisoformat(occurred.replace("Z","+00:00"))).total_seconds()
                if age>float(self.config.get("notification_max_age_seconds",3600)): continue
            except (ValueError,TypeError,KeyError): continue
            if note.get("owner_attention"): continue
            text=note.get("title","Swarm update")+"\n"+note.get("body","")
            refs=note.get("source_refs",[])
            urls=[v.get("url") if isinstance(v,dict) else v for v in refs]
            text+="".join("\n"+v for v in urls if isinstance(v,str) and v.startswith("https://"))
            operation_id="telemetry-notice:"+note["notification_id"]
            self.store.delivery_receipt(note["notification_id"],"pending",{"operation_id":operation_id})
            try:
                receipt=self.gateway.call("slack_post_message",{"channel_id":channel,"text":text},operation_id)
                uncertain=bool(receipt.get("uncertain"))
                failed=bool(receipt.get("isError") or receipt.get("error"))
                state="uncertain" if uncertain else "failed" if failed else "sent"
                self.store.delivery_receipt(note["notification_id"],state,receipt)
                sent+=state=="sent"
            except Exception as exc:
                self.store.delivery_receipt(note["notification_id"],"uncertain",{"operation_id":operation_id,"error":type(exc).__name__})
        return {"sent":sent,"enabled":True}
    def start(self):
        self.thread=Thread(target=self.run,daemon=True,name="passive-swarm-measurement")
        self.thread.start()
        for name,fn in (("local",lambda:self.collect_once(providers=False)),("inventory",self.collect_inventory),("census",self.collect_census),("discovery",self.collect_discovery),("machine",self.collect_machine),("slack",lambda:self.collect_extended("slack")),("github",lambda:self.collect_extended("github")),("services",lambda:self.collect_extended("services"))):
            def loop(reader=fn,label=name):
                while not self.stop_event.is_set():
                    self.reader_wakes[label].clear()
                    try:
                        result=reader()
                        self.errors.pop(label,None)
                        self.last_provider[label]={"observed_at":now(),"result":result}
                        if label=="slack": self.dispatch_notifications()
                    except Exception as exc: self._source_error(label,exc)
                    interval=15 if label=="census" else float(self.config.get("local_refresh_seconds",5)) if label=="local" else float(self.config.get("provider_refresh_seconds",120))
                    self.reader_wakes[label].wait(interval)
            worker=Thread(target=loop,daemon=True,name="passive-"+name+"-collector")
            worker.start()
            self.provider_threads.append(worker)
    def run(self):
        pending=None
        while not self.stop_event.is_set() or pending is not None or not self.queue.empty():
            if pending is None:
                try: pending=self.queue.get(timeout=0.25)
                except Empty: continue
            events,parts=pending
            try:
                self.ingest_batch(events,**parts)
            except Exception as exc:
                # Keep the already accepted observation in-flight until its
                # bounded transaction succeeds; a full queue cannot discard it.
                self._source_error("observation-queue",exc)
                time.sleep(0.25)
            else:
                self.queue.task_done()
                pending=None
                self.errors.pop("observation-queue",None)
    def stop(self):
        self.stop_event.set()
        for wake in self.reader_wakes.values(): wake.set()
