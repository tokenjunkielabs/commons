from __future__ import annotations
import json, tempfile, unittest
from pathlib import Path
import agent

def make(root:Path,tid="t1-test"):
    task=root/"task"; (task/"environment/data").mkdir(parents=True)
    (task/"instruction.md").write_text("# Task\nRead environment/data/value.txt and write result.json.\n")
    (task/"card.toml").write_text(f'[task]\nid="{tid}"\n[agent]\ntimeout_sec=120\n')
    (task/"environment/data/value.txt").write_text("41")
    return task

class Tests(unittest.TestCase):
    def test_two_call_success_and_checker_exclusion(self):
        with tempfile.TemporaryDirectory() as raw:
            root=Path(raw); task=make(root); out=root/"out"; (task/"checks").mkdir(); (task/"checks/secret.txt").write_text("DO_NOT_LEAK")
            calls=[]
            def house(**kw):
                calls.append(kw)
                if len(calls)==1:return "Read local value."
                return json.dumps({"program":"import json,os\nfrom pathlib import Path\nr=Path(os.environ['QFBENCH_TASK_DIR']);o=Path(os.environ['QFBENCH_OUTPUT_DIR']);o.mkdir(parents=True,exist_ok=True)\nv=int((r/'environment/data/value.txt').read_text());(o/'result.json').write_text(json.dumps({'value':v+1}))"})
            agent.solve(task,out,house)
            self.assertEqual(json.loads((out/"result.json").read_text()),{"value":42}); self.assertEqual(len(calls),2)
            self.assertFalse(any("DO_NOT_LEAK" in x["user"] for x in calls))
    def test_one_repair(self):
        with tempfile.TemporaryDirectory() as raw:
            root=Path(raw); task=make(root,"t1-repair"); out=root/"out"; calls=[]
            def house(**kw):
                calls.append(kw)
                if len(calls)==1:return "plan"
                if len(calls)==2:return json.dumps({"program":"def broken(:\n pass"})
                return json.dumps({"program":"import os\nfrom pathlib import Path\no=Path(os.environ['QFBENCH_OUTPUT_DIR']);o.mkdir(parents=True,exist_ok=True);(o/'result.json').write_text('{}')"})
            agent.solve(task,out,house); self.assertEqual(len(calls),3); self.assertIn("PY_COMPILE_ERROR",calls[2]["user"])
    def test_forbidden(self):
        with self.assertRaises(agent.AgentError):agent.validate("print(open('/input/checks/x').read())")
        with self.assertRaises(agent.AgentError):agent.validate("open('/app/output/reward.json','w').write('{}')")
if __name__=="__main__":unittest.main()
