"""Optional reads and nonblocking observation; never required for execution."""
from __future__ import annotations
import json
import urllib.request
from queue import Queue,Full
from threading import Thread

class Client:
    def __init__(self,base_url="http://127.0.0.1:8893",timeout=10):
        self.base_url=base_url.rstrip("/")
        self.timeout=timeout
    def call(self,name,arguments=None):
        req=urllib.request.Request(self.base_url+"/api/telemetry/tools/call",data=json.dumps({"name":name,"arguments":arguments or {}}).encode(),headers={"Content-Type":"application/json"})
        with urllib.request.urlopen(req,timeout=self.timeout) as response: return json.load(response)

class Observer:
    """Best-effort optional observer; emit() never waits for network or disk."""
    def __init__(self,base_url="http://127.0.0.1:8893",queue_size=2048):
        self.base_url=base_url.rstrip("/")
        self.queue=Queue(maxsize=queue_size)
        self.dropped=0
        self.failed=0
        Thread(target=self._deliver,daemon=True,name="optional-telemetry-observer").start()
    def emit(self,event):
        try: self.queue.put_nowait(event); return True
        except Full: self.dropped+=1; return False
    def _deliver(self):
        while True:
            event=self.queue.get()
            try:
                req=urllib.request.Request(self.base_url+"/api/telemetry/observe",data=json.dumps({"events":[event]}).encode(),headers={"Content-Type":"application/json"})
                with urllib.request.urlopen(req,timeout=2) as response: response.read(1024)
            except Exception: self.failed+=1
            finally: self.queue.task_done()
