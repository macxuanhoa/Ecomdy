import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import validate_catalogue


class CatalogueReconciliationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalogue = validate_catalogue.load(validate_catalogue.CATALOGUE / "source-145.json")
        cls.crosswalk = validate_catalogue.load(validate_catalogue.CATALOGUE / "crosswalk.json")
        cls.registry = validate_catalogue.load(validate_catalogue.ROOT / "registry" / "techniques.json")
        cls.summary = validate_catalogue.load(validate_catalogue.CATALOGUE / "reconciliation-summary.json")

    def test_complete_reconciliation_is_valid(self):
        self.assertEqual(validate_catalogue.validate(), [])

    def test_source_counts_and_namespace_are_preserved(self):
        self.assertEqual(len(self.catalogue["techniques"]), 145)
        source_ids = {entry["source_id"] for entry in self.catalogue["techniques"]}
        self.assertIn("A01", source_ids)
        self.assertIn("H20", source_ids)
        self.assertEqual(self.summary["unresolved_mappings"], [])

    def test_existing_ids_are_preserved_and_registry_is_expanded(self):
        ids = [card["id"] for card in self.registry["techniques"]]
        self.assertEqual(ids[:40], [f"TECH-{number:03d}" for number in range(1, 41)])
        self.assertEqual(ids[40:], [f"TECH-{number:03d}" for number in range(41, 107)])
        self.assertEqual(self.summary["existing_entries_reused"], 35)
        self.assertEqual(self.summary["source_rows_mapped_to_existing"], 76)
        self.assertEqual(self.summary["new_entries_added"], 66)

    def test_every_source_alias_has_one_canonical_card(self):
        aliases = [alias for card in self.registry["techniques"] for alias in card["catalogue_aliases"]]
        self.assertEqual(len(aliases), 145)
        self.assertEqual(len(set(aliases)), 145)

    def test_classification_totals_are_reported(self):
        self.assertEqual(self.summary["exact_matches"], 26)
        self.assertEqual(self.summary["partial_matches"], 50)
        self.assertEqual(self.summary["related_methods"], 41)
        self.assertEqual(self.summary["distinct_techniques"], 28)
        self.assertEqual(self.summary["overlapping_source_entries"], 117)

    def test_new_cards_do_not_claim_execution(self):
        for card in self.registry["techniques"][40:]:
            self.assertIsNone(card["invocation"])
            self.assertEqual(card["status"], "AVAILABLE IN REGISTRY")
            self.assertEqual(card["resource_implications"]["measurement_status"], "not_measured")

    def test_duplicate_mapping_is_rejected(self):
        changed = copy.deepcopy(self.crosswalk)
        changed["mappings"][1]["source_id"] = changed["mappings"][0]["source_id"]
        original = validate_catalogue.load
        try:
            validate_catalogue.load = lambda path: changed if path.name == "crosswalk.json" else original(path)
            errors = validate_catalogue.validate()
        finally:
            validate_catalogue.load = original
        self.assertTrue(any("exactly once" in error for error in errors))

    def test_unknown_canonical_mapping_is_rejected(self):
        changed = copy.deepcopy(self.crosswalk)
        changed["mappings"][0]["canonical_id"] = "TECH-999"
        original = validate_catalogue.load
        try:
            validate_catalogue.load = lambda path: changed if path.name == "crosswalk.json" else original(path)
            errors = validate_catalogue.validate()
        finally:
            validate_catalogue.load = original
        self.assertTrue(any("unknown canonical ID TECH-999" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
