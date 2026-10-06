#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, math, statistics, sys
from collections import defaultdict
from pathlib import Path

def pct(xs, q):
    if not xs: return None
    xs=sorted(xs); p=(len(xs)-1)*q; a=math.floor(p); b=math.ceil(p)
    return xs[a] if a==b else xs[a]*(b-p)+xs[b]*(p-a)

def load(path):
    rows=[]
    for n,line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(),1):
        if not line.strip(): continue
        try: row=json.loads(line)
        except json.JSONDecodeError as e: raise ValueError(f"line {n}: {e}") from e
        if not isinstance(row,dict): raise ValueError(f"line {n}: object required")
        rows.append(row)
    return rows

def score(rows, k):
    by=defaultdict(dict); walls=[]; fracs=[]; reqs=[]; fail=defaultdict(int); inv=budget=0
    for n,r in enumerate(rows,1):
        cid=r.get("task_id"); a=r.get("attempt"); passed=r.get("passed")
        wall=r.get("wall_ms"); timeout=r.get("timeout_sec"); requests=r.get("house_requests")
        invariants=r.get("finance_invariant_failures"); code=r.get("failure_code")
        if not isinstance(cid,str) or not cid: raise ValueError(f"row {n}: task_id")
        if not isinstance(a,int) or isinstance(a,bool) or not 1<=a<=k: raise ValueError(f"row {n}: attempt")
        if a in by[cid]: raise ValueError(f"duplicate {cid}/{a}")
        if not isinstance(passed,bool): raise ValueError(f"row {n}: passed")
        if not isinstance(wall,(int,float)) or isinstance(wall,bool) or wall<0: raise ValueError(f"row {n}: wall_ms")
        if not isinstance(timeout,(int,float)) or isinstance(timeout,bool) or timeout<=0: raise ValueError(f"row {n}: timeout_sec")
        if not isinstance(requests,int) or isinstance(requests,bool) or requests<0: raise ValueError(f"row {n}: house_requests")
        if not isinstance(invariants,int) or isinstance(invariants,bool) or invariants<0: raise ValueError(f"row {n}: finance_invariant_failures")
        if code is not None and not isinstance(code,str): raise ValueError(f"row {n}: failure_code")
        if passed and (code or invariants): raise ValueError(f"row {n}: inconsistent pass receipt")
        by[cid][a]=r; walls.append(float(wall)); fracs.append(float(wall)/(float(timeout)*1000)); reqs.append(requests)
        budget += requests>25; inv += invariants>0
        if not passed: fail[code or "unspecified"]+=1
    complete=[t for t,v in by.items() if set(v)==set(range(1,k+1))]
    missing=sorted(set(by)-set(complete))
    pass1=sum(by[t][1]["passed"] for t in complete)/len(complete) if complete else None
    passk=sum(any(by[t][a]["passed"] for a in range(1,k+1)) for t in complete)/len(complete) if complete else None
    flaky=[t for t in complete if len({by[t][a]["passed"] for a in range(1,k+1)})>1]
    return {
      "tasks_seen":len(by),"complete_tasks":len(complete),"incomplete_tasks":missing,
      "practice_pass_at_1":pass1,f"practice_pass_at_{k}":passk,"flaky_tasks":sorted(flaky),
      "flaky_task_rate":len(flaky)/len(complete) if complete else None,
      "participant_failure_counts":dict(sorted(fail.items())),"finance_invariant_failure_runs":inv,
      "house_request_budget_violations":budget,
      "house_requests":{"median":statistics.median(reqs) if reqs else None,"p95":pct(reqs,.95),"max":max(reqs) if reqs else None},
      "wall_ms":{"median":statistics.median(walls) if walls else None,"p95":pct(walls,.95),"max":max(walls) if walls else None},
      "timeout_fraction":{"median":statistics.median(fracs) if fracs else None,"p95":pct(fracs,.95),"max":max(fracs) if fracs else None}
    }

def main():
    p=argparse.ArgumentParser(); p.add_argument("receipts"); p.add_argument("--attempts",type=int,default=3)
    p.add_argument("--min-pass1",type=float,default=0.0); p.add_argument("--max-flaky-rate",type=float,default=1.0)
    p.add_argument("--max-timeout-p95",type=float,default=.8); a=p.parse_args()
    try: m=score(load(a.receipts),a.attempts)
    except (OSError,ValueError) as e: print(f"ERROR: {e}",file=sys.stderr); return 2
    bad=[]
    if m["incomplete_tasks"]: bad.append("incomplete receipts")
    if m["practice_pass_at_1"] is None or m["practice_pass_at_1"]<a.min_pass1: bad.append("pass@1 gate")
    if m["flaky_task_rate"] is None or m["flaky_task_rate"]>a.max_flaky_rate: bad.append("flaky gate")
    if m["finance_invariant_failure_runs"]: bad.append("finance invariant failures")
    if m["house_request_budget_violations"]: bad.append(">25 House requests")
    if m["timeout_fraction"]["p95"] is None or m["timeout_fraction"]["p95"]>a.max_timeout_p95: bad.append("timeout-margin gate")
    print(json.dumps(m,indent=2,sort_keys=True)); print("GATE: "+("FAIL" if bad else "PASS"),file=sys.stderr)
    for x in bad: print("- "+x,file=sys.stderr)
    return 1 if bad else 0

if __name__=="__main__": raise SystemExit(main())
