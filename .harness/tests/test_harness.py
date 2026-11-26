import tempfile, unittest, sys, json
from pathlib import Path
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
if __name__=='__main__': unittest.main()
