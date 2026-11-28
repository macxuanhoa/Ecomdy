import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import validate_techniques


class EcomdyMappingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.techniques = validate_techniques.load_json(validate_techniques.REGISTRY_PATH)
        cls.technique_ids = {item["id"] for item in cls.techniques["techniques"]}
        cls.mapping = validate_techniques.load_json(ROOT / "registry" / "ecomdy-mapping.json")

    def test_mapping_covers_existing_modules_without_claiming_implementation(self):
        self.assertEqual(self.mapping["status"], "PROPOSED_MAPPING")
        self.assertEqual([item["module_id"] for item in self.mapping["modules"]], [f"M{number:02d}" for number in range(1, 21)])

    def test_all_recommended_techniques_exist(self):
        records = self.mapping["modules"] + self.mapping["cross_cutting"]
        for record in records:
            for technique_id in record["recommended_techniques"]:
                self.assertIn(technique_id, self.technique_ids)

    def test_product_workflows_are_existing_specifications(self):
        allowed = {f"WF-P{number:02d}" for number in range(1, 14)}
        for module in self.mapping["modules"]:
            self.assertTrue(set(module["workflow_ids"]).issubset(allowed))

    def test_each_module_has_verification_and_evidence(self):
        for module in self.mapping["modules"]:
            self.assertTrue(module["required_tests"])
            self.assertTrue(module["evidence_to_retain"])
            self.assertTrue(module["responsible_roles"])
            self.assertIn("boundary_note", module)


if __name__ == "__main__":
    unittest.main()
