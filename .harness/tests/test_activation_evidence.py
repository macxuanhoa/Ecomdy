import hashlib
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import validate_tool_manifest


class ActivationEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.evidence = json.loads((ROOT / "registry" / "installation" / "activation-evidence.json").read_text(encoding="utf-8"))
        cls.records = {record["capability_id"]: record for record in cls.evidence["records"]}

    def test_openspec_is_blocked_without_installation(self):
        record = self.records["TOOL-001"]
        self.assertEqual(record["status"], "BLOCKED")
        self.assertIn(">=22.20.0", record["reason"])
        self.assertNotIn("commands", record)

    def test_internal_skill_copies_match_canonical_hashes(self):
        for capability_id in (
            "INTERNAL-SKILL-TASK-CONTRACT",
            "INTERNAL-SKILL-SECURITY-REVIEW",
            "INTERNAL-SKILL-TEST-FIRST",
            "INTERNAL-SKILL-HANDOFF",
        ):
            record = self.records[capability_id]
            source = ROOT.parent / record["source"]
            installed = ROOT.parent / record["installed_copy"]
            self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), record["sha256"])
            self.assertEqual(source.read_bytes(), installed.read_bytes())
            self.assertEqual(record["status"], "INSTALLED")

    def test_wave1_tools_have_bounded_smoke_evidence(self):
        for tool_id in ("TOOL-016", "TOOL-017", "TOOL-018"):
            record = self.records[tool_id]
            self.assertEqual(record["status"], "SMOKE TESTED")
            self.assertEqual(record["disposition"], "INSTALLED_USER_SCOPE")
            self.assertTrue(record["commands"])
            self.assertTrue(record["evidence"])
            self.assertTrue(record["limitations"])

    def test_no_record_claims_integration(self):
        self.assertTrue(all(record["status"] != "INTEGRATED" for record in self.evidence["records"]))

    def test_manifest_proposals_remain_not_run(self):
        manifest = validate_tool_manifest.load(validate_tool_manifest.MANIFEST_PATH)
        for tool in manifest["tools"]:
            commands = tool["installation"]["proposed_commands"] + tool["verification"]["proposed_commands"]
            self.assertTrue(all(command["execution_status"] == "NOT_RUN" for command in commands))

    def test_evidence_commands_use_argv_without_shell_wrappers(self):
        for record in self.evidence["records"]:
            for command in record.get("commands", []):
                self.assertIsInstance(command["argv"], list)
                self.assertTrue(command["argv"])
                self.assertNotIn(command["argv"][0], {"bash", "sh", "cmd", "powershell"})


if __name__ == "__main__":
    unittest.main()
