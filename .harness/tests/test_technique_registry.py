import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import validate_techniques


class TechniqueRegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = validate_techniques.load_json(validate_techniques.REGISTRY_PATH)

    def test_registry_is_valid_and_covers_all_categories(self):
        self.assertEqual(validate_techniques.validate_registry(self.registry), [])
        categories = {card["category"]["id"] for card in self.registry["techniques"]}
        self.assertEqual(categories, set("ABCDEFGH"))

    def test_ids_are_unique_and_stable(self):
        ids = [card["id"] for card in self.registry["techniques"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(all(validate_techniques.re.fullmatch(r"TECH-[0-9]{3}", item) for item in ids))

    def test_missing_required_card_field_is_rejected(self):
        changed = copy.deepcopy(self.registry)
        del changed["techniques"][0]["acceptance_criteria"]
        errors = validate_techniques.validate_registry(changed)
        self.assertTrue(any("acceptance_criteria" in error for error in errors))

    def test_duplicate_id_is_rejected(self):
        changed = copy.deepcopy(self.registry)
        changed["techniques"][1]["id"] = changed["techniques"][0]["id"]
        errors = validate_techniques.validate_registry(changed)
        self.assertTrue(any("Duplicate technique IDs" in error for error in errors))

    def test_unknown_technique_reference_is_rejected(self):
        changed = copy.deepcopy(self.registry)
        changed["techniques"][0]["alternative_techniques"] = ["TECH-999"]
        errors = validate_techniques.validate_registry(changed)
        self.assertTrue(any("unknown ID: TECH-999" in error for error in errors))

    def test_unverified_invocation_is_rejected(self):
        changed = copy.deepcopy(self.registry)
        changed["techniques"][0]["kind"] = "script"
        changed["techniques"][0]["invocation"] = {"argv": ["python", "x.py"], "cwd": ".", "verification_status": "ATTEMPTED"}
        errors = validate_techniques.validate_registry(changed)
        self.assertTrue(any("verification_status is invalid" in error for error in errors))

    def test_no_registry_entry_claims_execution(self):
        for card in self.registry["techniques"]:
            self.assertIsNone(card["invocation"])
            self.assertNotIn(card["kind"], validate_techniques.EXECUTABLE_KINDS)
            self.assertEqual(card["status"], "AVAILABLE IN REGISTRY")
            self.assertEqual(card["resource_implications"]["measurement_status"], "not_measured")


if __name__ == "__main__":
    unittest.main()
