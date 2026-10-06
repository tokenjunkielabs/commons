#!/usr/bin/env python3
from __future__ import annotations
import argparse, ast, json, os, py_compile, re, subprocess, sys, tempfile, time, tomllib
import urllib.error, urllib.request
from pathlib import Path

BLOCKED={"checks","check","reference","references","reference_data","solution","solutions","oracle","oracles","expected","answer","answers","private-test","private_test","dev"}
TEXT={".py",".json",".toml",".yaml",".yml",".txt",".md",".csv",".tsv",".ini",".cfg",".sql"}
NET={"aiohttp","boto3","botocore","httpx","openai","requests","socket","urllib","yfinance"}
RESERVED={"reward.json","reward.txt","pytest_report.json"}
MAX_FILES=18; MAX_CONTEXT=120_000; REQUEST_LIMIT=3

class AgentError(RuntimeError): pass

def read(path:Path,n:int)->str:
    return path.read_bytes()[:n*4].decode("utf-8","replace")[:n]

def blocked(rel:Path)->bool:
    return any(x.lower() in BLOCKED for x in rel.parts)

def timeout_for(task:Path)->float:
    try:
        return float(tomllib.loads((task/"card.toml").read_text())["agent"]["timeout_sec"])
    except Exception:
        return 1800.0

def task_id(task:Path)->str:
    try:
        return str(tomllib.loads((task/"card.toml").read_text())["task"]["id"])
    except Exception:
        return task.name

def context(task:Path)->str:
    parts=[]
    if (task/"instruction.md").is_file(): parts.append("## instruction.md\n"+read(task/"instruction.md",48_000))
    if (task/"card.toml").is_file(): parts.append("## card.toml\n"+read(task/"card.toml",12_000))
    inventory=[]; previews=[]; used=0; seen=set()
    for root in (task/"environment/data",task/"data"):
        if not root.is_dir(): continue
        for p in sorted(root.rglob("*")):
            if not p.is_file() or p in seen: continue
            seen.add(p); rel=p.relative_to(task)
            if blocked(rel): continue
            if len(inventory)>=MAX_FILES:
                inventory.append("- ... more task-data files omitted from prompt ..."); break
            inventory.append(f"- {rel.as_posix()} ({p.stat().st_size} bytes)")
            if p.suffix.lower() in TEXT and used<MAX_CONTEXT:
                s=read(p,min(6000,MAX_CONTEXT-used)); used+=len(s)
                previews.append(f"### {rel.as_posix()} (bounded preview)\n{s}")
    if inventory: parts.append("## Safe task-data inventory\n"+"\n".join(inventory))
    if previews: parts.append("## Safe task-data previews\n"+"\n\n".join(previews))
    return "\n\n".join(parts)[:MAX_CONTEXT]

def content(resp:dict)->str:
    try: c=resp["choices"][0]["message"]["content"]
    except Exception as e: raise AgentError("House response missing message content") from e
    if isinstance(c,str): return c
    if isinstance(c,list): return "".join(x.get("text","") for x in c if isinstance(x,dict))
    raise AgentError("House response content is not text")

class House:
    def __init__(self):
        miss=[k for k in ("MODEL_ENDPOINT","MODEL_NAME","MODEL_TOKEN") if not os.getenv(k)]
        if miss: raise AgentError("missing House environment: "+", ".join(miss))
        self.url=os.environ["MODEL_ENDPOINT"].rstrip("/")+"/v1/chat/completions"
        self.model=os.environ["MODEL_NAME"]; self.token=os.environ["MODEL_TOKEN"]; self.calls=0
    def __call__(self,*,system,user,max_tokens,timeout,thinking):
        if self.calls>=REQUEST_LIMIT: raise AgentError("baseline House request limit exceeded")
        self.calls+=1
        body={"model":self.model,"messages":[{"role":"system","content":system},{"role":"user","content":user}],
              "max_tokens":min(int(max_tokens),4000),"temperature":0,
              "chat_template_kwargs":{"enable_thinking":bool(thinking)}}
        req=urllib.request.Request(self.url,data=json.dumps(body).encode(),method="POST",
            headers={"Authorization":"Bearer "+self.token,"Content-Type":"application/json"})
        try:
            with urllib.request.urlopen(req,timeout=max(10.0,timeout)) as r: raw=r.read()
        except urllib.error.HTTPError as e:
            raise AgentError(f"House HTTP {e.code}: "+e.read(4096).decode("utf-8","replace")) from e
        except OSError as e: raise AgentError(f"House request failed: {e}") from e
        try: return content(json.loads(raw))
        except json.JSONDecodeError as e: raise AgentError("House returned non-JSON") from e

def program_from(text:str)->str:
    s=text.strip()
    if s.startswith("```"):
        s=re.sub(r"^```(?:json)?\s*","",s,flags=re.I); s=re.sub(r"\s*```$","",s)
    try: obj=json.loads(s)
    except json.JSONDecodeError:
        a,b=s.find("{"),s.rfind("}")
        if a<0 or b<=a: raise AgentError("implementation contained no JSON object")
        try: obj=json.loads(s[a:b+1])
        except json.JSONDecodeError as e: raise AgentError("implementation JSON invalid") from e
    if not isinstance(obj,dict) or not isinstance(obj.get("program"),str): raise AgentError("implementation requires string `program`")
    validate(obj["program"]); return obj["program"]

def validate(src:str)->None:
    low=src.lower()
    for token in ("/checks","\\\\checks","checks/","checks\\\\","reference_data","/reference","\\\\reference","oracle_","reward.json","reward.txt","pytest_report.json"):
        if token in low: raise AgentError("generated program references forbidden evaluation material: "+token)
    try: tree=ast.parse(src)
    except SyntaxError: return
    for n in ast.walk(tree):
        if isinstance(n,ast.Import):
            bad={a.name.split(".",1)[0] for a in n.names}&NET
            if bad: raise AgentError("generated program imports network package(s): "+str(sorted(bad)))
        elif isinstance(n,ast.ImportFrom) and n.module and n.module.split(".",1)[0] in NET:
            raise AgentError("generated program imports network package: "+n.module.split(".",1)[0])
        elif isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and isinstance(n.func.value,ast.Name) and n.func.value.id=="os" and n.func.attr in {"system","popen"}:
            raise AgentError("generated program may not spawn shell commands")

def run_generated(path:Path,task:Path,out:Path,seconds:float)->tuple[int,str]:
    try: py_compile.compile(str(path),doraise=True)
    except py_compile.PyCompileError as e: return 2,"PY_COMPILE_ERROR\n"+str(e)
    env=os.environ.copy(); env["QFBENCH_TASK_DIR"]=str(task); env["QFBENCH_OUTPUT_DIR"]=str(out)
    try:
        p=subprocess.run([sys.executable,str(path)],cwd=task,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=max(10.0,seconds))
        return p.returncode,p.stdout[-12000:]
    except subprocess.TimeoutExpired as e:
        x=e.stdout or ""; x=x.decode("utf-8","replace") if isinstance(x,bytes) else x
        return 124,x[-8000:]+f"\nprogram timed out after {seconds:.1f}s"

def solve(task:Path,out:Path,house)->None:
    task=task.resolve(); out.mkdir(parents=True,exist_ok=True)
    limit=timeout_for(task); started=time.monotonic(); ctx=context(task)
    if not ctx.strip(): raise AgentError("task has no readable instruction/card/data context")
    remain=lambda reserve:max(10.0,limit-(time.monotonic()-started)-reserve)
    system=("You are the approved House coding model for Agenthon Track 1. Use only supplied context and local task files. "
            "Never inspect checks, reference answers, oracle/expected files, reward files, hidden evaluation material, network tools, or external data. "
            "Follow the requested output schema exactly.")
    plan=house(system=system,user=f"Task id: {task_id(task)}\nAgent timeout: {limit:.1f}s\n\n{ctx}\n\n"
        "Give a concise plan for one Python program that computes the exact deliverables from local task data. Identify outputs, conventions, and likely failure modes. No code.",
        max_tokens=2400,timeout=min(300,remain(90)),thinking=True)
    reply=house(system=system,user=f"Task id: {task_id(task)}\nAgent timeout: {limit:.1f}s\n\n{ctx}\n\n## Plan\n{plan[-20000:]}\n\n"
        "Return ONLY JSON {\"program\":\"...\"}. The program must be complete Python 3.13, read task root from QFBENCH_TASK_DIR, write every requested deliverable under QFBENCH_OUTPUT_DIR, "
        "use only local data/scientific packages, and never read checks/reference/oracle/expected/reward material or use network access. Keep deterministic and dependency-light.",
        max_tokens=4000,timeout=min(300,remain(60)),thinking=False)
    src=program_from(reply)
    with tempfile.TemporaryDirectory(prefix="agenthon-t1-") as td:
        path=Path(td)/"solution.py"
        def attempt(code):
            path.write_text(code)
            return run_generated(path,task,out,min(remain(10),max(30,limit*.55)))
        code,evidence=attempt(src)
        if code:
            repaired=house(system=system,user=f"Task id: {task_id(task)}\n\n{ctx}\n\nThe local program failed. Repair only this demonstrated failure; do not broaden scope or inspect checks.\n"
                f"## Failure\n{evidence[-10000:]}\n\n## Previous program\n{src[-28000:]}\n\nReturn ONLY JSON {{\"program\":\"...\"}} with the complete repaired program.",
                max_tokens=4000,timeout=min(300,remain(30)),thinking=False)
            src=program_from(repaired); code,evidence=attempt(src)
            if code: raise AgentError(f"generated solver failed after one repair (exit {code}):\n{evidence}")
    bad=[p for p in out.rglob("*") if p.is_file() and p.name.lower() in RESERVED]
    if bad:
        for p in bad:
            try:p.unlink()
            except OSError:pass
        raise AgentError("generated solver attempted reserved verifier output(s): "+", ".join(p.name for p in bad))
    if not any(p.is_file() for p in out.rglob("*")): raise AgentError("solver produced no deliverables")

def main(argv=None)->int:
    p=argparse.ArgumentParser(); p.add_argument("verb"); p.add_argument("--task-dir",required=True); p.add_argument("--out",required=True)
    a=p.parse_args(argv)
    if a.verb!="solve": p.error("verb must be solve")
    try: solve(Path(a.task_dir),Path(a.out),House())
    except AgentError as e: print("AGENT_ERROR:",e,file=sys.stderr); return 2
    return 0

if __name__=="__main__": raise SystemExit(main())
