import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import validate_tool_manifest


class ToolManifestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = validate_tool_manifest.load(validate_tool_manifest.MANIFEST_PATH)

    def tool(self, tool_id):
        return next(tool for tool in self.manifest["tools"] if tool["id"] == tool_id)

    def test_twenty_unique_advisory_candidates(self):
        self.assertEqual(len(self.manifest["tools"]), 20)
        ids = [tool["id"] for tool in self.manifest["tools"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(validate_tool_manifest.validate_manifest(self.manifest), [])
        self.assertEqual(self.manifest["status"], "ADVISORY_RESEARCH")
        self.assertTrue(all(tool["required"] is False for tool in self.manifest["tools"]))

    def test_no_candidate_claims_approval_or_integration(self):
        disallowed = {"APPROVED", "CONFIGURED", "INTEGRATED"}
        self.assertTrue(all(tool["status"] not in disallowed for tool in self.manifest["tools"]))

    def test_only_diagram_design_is_installed_and_smoke_tested(self):
        installed = [tool["id"] for tool in self.manifest["tools"] if tool["disposition"] == "INSTALLED_USER_SCOPE"]
        smoke_tested = [tool["id"] for tool in self.manifest["tools"] if tool["status"] == "SMOKE TESTED"]
        self.assertEqual(installed, ["TOOL-013"])
        self.assertEqual(smoke_tested, ["TOOL-013"])
        self.assertTrue(self.tool("TOOL-013")["verification"]["evidence"])
        self.assertFalse(self.tool("TOOL-013")["compatible_skills"] == [])

    def test_structurizr_lite_remains_rejected(self):
        tool = self.tool("TOOL-020")
        self.assertEqual(tool["status"], "REJECTED")
        self.assertEqual(tool["disposition"], "REJECTED")

    def test_resource_measurements_remain_not_measured(self):
        for tool in self.manifest["tools"]:
            self.assertEqual(tool["resource_implications"]["measurement_status"], "not_measured")

    def test_all_procedures_are_complete(self):
        required = {"install", "activate", "verify", "update", "uninstall", "recovery"}
        self.assertEqual(set(self.manifest["shared_procedures"]), required)
        for tool in self.manifest["tools"]:
            self.assertEqual(set(tool["procedures"]), required)
            for procedure in required:
                self.assertTrue(tool["procedures"][procedure])

    def test_proposed_commands_are_not_execution_evidence(self):
        for tool in self.manifest["tools"]:
            commands = tool["installation"]["proposed_commands"] + tool["verification"]["proposed_commands"]
            for command in commands:
                self.assertEqual(command["execution_status"], "NOT_RUN")
        changed = copy.deepcopy(self.manifest)
        changed["tools"][0]["installation"]["proposed_commands"][0]["execution_status"] = "VERIFIED"
        errors = validate_tool_manifest.validate_manifest(changed)
        self.assertTrue(any("must remain NOT_RUN" in error for error in errors))

    def test_duplicate_tool_ids_fail(self):
        changed = copy.deepcopy(self.manifest)
        changed["tools"][1]["id"] = changed["tools"][0]["id"]
        errors = validate_tool_manifest.validate_manifest(changed)
        self.assertIn("Duplicate tool IDs", errors)

    def test_installed_status_requires_evidence(self):
        changed = copy.deepcopy(self.manifest)
        self.tool_from(changed, "TOOL-013")["verification"]["evidence"] = []
        errors = validate_tool_manifest.validate_manifest(changed)
        self.assertTrue(any("SMOKE TESTED requires evidence" in error for error in errors))

    def tool_from(self, manifest, tool_id):
        return next(tool for tool in manifest["tools"] if tool["id"] == tool_id)

    def test_malformed_command_argv_fails_without_exception(self):
        changed = copy.deepcopy(self.manifest)
        changed["tools"][0]["installation"]["proposed_commands"][0]["argv"] = {"bad": "shape"}
        errors = validate_tool_manifest.validate_manifest(changed)
        self.assertTrue(any("must be a non-empty array of non-empty strings" in error for error in errors))

    def test_non_object_manifest_fails_cleanly(self):
        errors = validate_tool_manifest.validate_manifest([])
        self.assertEqual(errors, ["manifest must be an object"])


if __name__ == "__main__":
    unittest.main()
