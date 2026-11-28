import io
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import capability_doctor


class CapabilityDoctorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = capability_doctor.inspect_capabilities(ROOT)

    def test_registry_counts_and_validation_status(self):
        self.assertEqual(self.result["status"], "PASS")
        self.assertEqual(self.result["registries"]["techniques"]["count"], 106)
        self.assertEqual(self.result["registries"]["tools"]["count"], 20)
        self.assertEqual(self.result["registries"]["tools"]["blocked"], ["TOOL-001"])

    def test_internal_skills_are_discovered_with_installation_states(self):
        skills = {item["name"]: item for item in self.result["skills"]}
        self.assertEqual(set(skills), {"debug", "diagram", "handoff", "scoped-task", "security-review", "task-contract", "test-first"})
        self.assertEqual(self.result["registries"]["skills"]["count"], 7)
        for name in ("handoff", "security-review", "task-contract", "test-first"):
            skill = skills[name]
            self.assertTrue(skill["lifecycle"]["registered"])
            self.assertTrue(skill["lifecycle"]["installed"])
            self.assertTrue(skill["lifecycle"]["configured"])
            self.assertTrue(skill["installed_copy_matches_source"])
            self.assertTrue(skill["lock_record_matches_source"])
            self.assertFalse(skill["lifecycle"]["integrated"])
            self.assertFalse(skill["lifecycle"]["verified"])
        for name in ("debug", "diagram", "scoped-task"):
            self.assertTrue(skills[name]["lifecycle"]["registered"])
            self.assertFalse(skills[name]["lifecycle"]["installed"])
            self.assertFalse(skills[name]["lifecycle"]["configured"])

    def test_session_observation_is_explicit_and_sparse(self):
        result = capability_doctor.inspect_capabilities(ROOT, ["TOOL-013", "task-contract"])
        skills = {item["name"]: item for item in result["skills"]}
        tools = {item["capability_id"]: item for item in result["tools"]}
        self.assertTrue(skills["task-contract"]["lifecycle"]["available_in_session"])
        self.assertIsNone(skills["handoff"]["lifecycle"]["available_in_session"])
        self.assertTrue(tools["TOOL-013"]["lifecycle"]["available_in_session"])
        self.assertIsNone(tools["TOOL-016"]["lifecycle"]["available_in_session"])
        self.assertTrue(result["session_observation"]["provided"])

    def test_unobserved_capabilities_remain_unknown(self):
        for capability in self.result["skills"] + self.result["tools"]:
            self.assertIsNone(capability["lifecycle"]["available_in_session"])
            self.assertFalse(capability["lifecycle"]["integrated"])
            lifecycle = capability["lifecycle"]
            self.assertEqual(set(lifecycle), {
                "registered", "installed", "configured", "available_in_session",
                "smoke_tested", "integrated", "verified",
            })
            self.assertTrue(all(value is None or isinstance(value, bool) for value in lifecycle.values()))

    def test_openspec_is_blocked_and_not_installed(self):
        tool = next(item for item in self.result["tools"] if item["capability_id"] == "TOOL-001")
        self.assertEqual(tool["manifest_status"], "BLOCKED")
        self.assertFalse(tool["lifecycle"]["installed"])
        self.assertFalse(tool["lifecycle"]["configured"])
        self.assertTrue(any("Node" in note for note in tool["notes"]))

    def test_smoke_tested_tools_have_evidence_without_integration_claim(self):
        tools = {item["capability_id"]: item for item in self.result["tools"]}
        for tool_id in ("TOOL-013", "TOOL-016", "TOOL-017", "TOOL-018"):
            self.assertTrue(tools[tool_id]["lifecycle"]["smoke_tested"])
            self.assertTrue(tools[tool_id]["lifecycle"]["verified"])
            self.assertFalse(tools[tool_id]["lifecycle"]["integrated"])

    def test_missing_artifact_is_distinct_from_unknown_install_state(self):
        with patch.object(capability_doctor.shutil, "which", return_value=None):
            installed, detected_path = capability_doctor.detect_tool_install(
                {"id": "TOOL-016"},
                {"TOOL-016": {"installed_path": str(ROOT / "missing-mmdc")}},
                ROOT,
            )
        self.assertFalse(installed)
        self.assertIsNotNone(detected_path)
        unknown, unknown_path = capability_doctor.detect_tool_install({"id": "TOOL-002"}, {}, ROOT)
        self.assertIsNone(unknown)
        self.assertIsNone(unknown_path)
        with patch.object(capability_doctor.shutil, "which", return_value=None):
            absent_on_path, absent_path = capability_doctor.detect_tool_install({"id": "TOOL-014"}, {}, ROOT)
            blocked, blocked_path = capability_doctor.detect_tool_install(
                {"id": "TOOL-001"}, {"TOOL-001": {"status": "BLOCKED"}}, ROOT
            )
        self.assertIsNone(absent_on_path)
        self.assertIsNone(absent_path)
        self.assertFalse(blocked)
        self.assertIsNone(blocked_path)

    def test_strict_mode_detects_blocked_optional_capability(self):
        from unittest.mock import patch
        with patch.object(capability_doctor, "inspect_capabilities", return_value=self.result), patch("sys.argv", ["capability_doctor.py", "--strict"]), redirect_stdout(io.StringIO()):
            self.assertEqual(capability_doctor.main(), 2)


if __name__ == "__main__":
    unittest.main()
