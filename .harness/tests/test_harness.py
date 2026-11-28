import tempfile, unittest, sys, json
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import harness
class StarterTests(unittest.TestCase):
    def test_init_preserves_existing_files(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d); (p/'AGENTS.md').write_text('custom')
            harness.initialize(p); harness.initialize(p)
            self.assertEqual((p/'AGENTS.md').read_text(),'custom')
            self.assertEqual((p/'.gitignore').read_text().splitlines().count('.env'),1)
    def test_ingest_inventory(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d); harness.initialize(p); (p/'docs/00-original/brief.txt').write_text('hello'); harness.ingest(p)
            rows=json.loads((p/'docs/01-project-context/SOURCE_REGISTRY.json').read_text())
            self.assertEqual(len(rows),1); self.assertEqual(rows[0]['status'],'inventoried_not_extracted'); self.assertEqual(len(rows[0]['sha256']),64)
    def test_ingest_refuses_to_overwrite_without_opt_in(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d); harness.initialize(p); (p/'docs/00-original/brief.txt').write_text('hello'); harness.ingest(p)
            registry=p/'docs/01-project-context/SOURCE_REGISTRY.json'; prompt=p/'docs/01-project-context/CONTEXT_UPDATE_PROMPT.md'
            registry.write_text('owner-edited registry'); prompt.write_text('owner-edited prompt')
            with self.assertRaises(SystemExit): harness.ingest(p)
            self.assertEqual(registry.read_text(),'owner-edited registry'); self.assertEqual(prompt.read_text(),'owner-edited prompt')
            harness.ingest(p,overwrite=True)
            self.assertEqual(json.loads(registry.read_text())[0]['status'],'inventoried_not_extracted')
    def test_route_command_returns_recommended_json(self):
        with tempfile.TemporaryDirectory() as d:
            task=Path(d)/'task.json'; output=Path(d)/'route.json'
            task.write_text(json.dumps({'task_id':'TASK-CLI-001','task_type':'documentation','risk':'low','complexity':'low','changed_file_count':2}))
            stdout=StringIO()
            with patch('sys.argv',['harness.py','route','--task',str(task),'--output',str(output)]), redirect_stdout(stdout):
                self.assertEqual(harness.main(),0)
            self.assertEqual(json.loads(output.read_text())['route_id'],'ROUTE-QUICK-DOCS')
    def test_route_command_distinguishes_no_match_and_blocked(self):
        cases=[({'task_id':'TASK-NO-MATCH','task_type':'unknown'},2),({'task_id':'TASK-BLOCKED','task_type':'documentation','execution_mode':'AUTONOMOUS'},3)]
        with tempfile.TemporaryDirectory() as d:
            for index,(task,expected) in enumerate(cases):
                path=Path(d)/f'task-{index}.json'; path.write_text(json.dumps(task))
                with patch('sys.argv',['harness.py','route','--task',str(path)]), redirect_stdout(StringIO()):
                    self.assertEqual(harness.main(),expected)
    def test_capabilities_command_reports_blocked_tool(self):
        stdout=StringIO()
        with patch('sys.argv',['harness.py','capabilities','--strict']), redirect_stdout(stdout):
            self.assertEqual(harness.main(),2)
        self.assertEqual(json.loads(stdout.getvalue())['registries']['tools']['blocked'],['TOOL-001'])
    def test_compile_command_selects_recipe(self):
        with tempfile.TemporaryDirectory() as d:
            task=Path(d)/'task.json'; route=Path(d)/'route.json'; output=Path(d)/'compiled.json'
            task.write_text(json.dumps({'task_id':'TASK-COMPILE-CLI','task_type':'feature','acceptance_criteria_present':True}))
            with patch('sys.argv',['harness.py','route','--task',str(task),'--output',str(route)]), redirect_stdout(StringIO()):
                self.assertEqual(harness.main(),0)
            with patch('sys.argv',['harness.py','compile','--task',str(route),'--task-type','feature','--output',str(output)]), redirect_stdout(StringIO()):
                self.assertEqual(harness.main(),0)
            self.assertEqual(json.loads(output.read_text())['recipe_id'],'RECIPE-001')
    def test_context_command_compiles_local_manifest(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); (root/'docs').mkdir(); (root/'docs'/'a.md').write_text('local')
            request=root/'context.json'; request.write_text(json.dumps({'include_paths':['docs'],'max_files':2,'max_bytes':100}))
            stdout=StringIO()
            with patch('sys.argv',['harness.py','context','--task',str(request),'--project',str(root)]), redirect_stdout(stdout):
                self.assertEqual(harness.main(),0)
            self.assertEqual(json.loads(stdout.getvalue())['summary']['file_count'],1)
if __name__=='__main__': unittest.main()
