import copy
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import technique_router


class TechniqueRouterTests(unittest.TestCase):
    def task(self, **updates):
        task = {
            "task_id": "TASK-ROUTER-001",
            "task_type": "documentation",
            "risk": "low",
            "complexity": "low",
            "changed_file_count": 2,
            "mutation_required": True,
        }
        task.update(updates)
        return task

    def test_most_specific_matching_route_is_selected(self):
        result = technique_router.route_task(self.task())
        self.assertEqual(result["state"], "RECOMMENDED")
        self.assertEqual(result["route_id"], "ROUTE-QUICK-DOCS")
        self.assertEqual(result["profile_id"], "PROFILE-QUICK")
        self.assertEqual(result["runtime_state"], "RECOMMENDED")
        self.assertEqual(result["execution_state"], "NOT_EXECUTED")
        self.assertTrue(any(item["route_id"] == "ROUTE-DOCS" and item["matched"] for item in result["decisions"]))

    def test_standard_docs_route_matches_medium_risk(self):
        result = technique_router.route_task(self.task(risk="medium", complexity="medium", changed_file_count=8))
        self.assertEqual(result["route_id"], "ROUTE-DOCS")
        self.assertEqual(result["profile_id"], "PROFILE-STANDARD")

    def test_missing_activation_fact_returns_no_match(self):
        result = technique_router.route_task(self.task(task_type="feature", acceptance_criteria_present=False))
        self.assertEqual(result["state"], "NO_MATCH")
        self.assertEqual(result["runtime_state"], "NOT_SELECTED")
        self.assertIn("guidance", result)

    def test_autonomous_mode_is_blocked(self):
        result = technique_router.route_task(self.task(execution_mode="AUTONOMOUS"))
        self.assertEqual(result["state"], "BLOCKED")
        self.assertTrue(any("AUTONOMOUS" in error for error in result["errors"]))

    def test_requested_route_must_match_activation_rules(self):
        result = technique_router.route_task(self.task(route_id="ROUTE-FEATURE"))
        self.assertEqual(result["state"], "BLOCKED")
        self.assertTrue(any("does not match" in error for error in result["errors"]))

    def test_optional_technique_requires_reason_and_route_allowance(self):
        task = self.task(optional_techniques=["TECH-009", "TECH-014"], optional_reasons={"TECH-009": "Needed for bounded context compression"})
        result = technique_router.route_task(task)
        self.assertIn("TECH-009", result["selected"]["optional_techniques"])
        excluded = {item["technique_id"]: item["reason"] for item in result["selected"]["excluded_optional"]}
        self.assertIn("not an allowed optional", excluded["TECH-014"].lower())
        missing_reason = technique_router.route_task(self.task(optional_techniques=["TECH-009"]))
        self.assertIn("non-empty optional_reasons", missing_reason["selected"]["excluded_optional"][0]["reason"])

    def test_optional_conflict_is_excluded(self):
        registry = technique_router.validate_techniques.load_json(technique_router.validate_techniques.REGISTRY_PATH)
        cards = {card["id"]: card for card in registry["techniques"]}
        cards["TECH-004"]["conflicting_techniques"] = ["TECH-040"]
        task = self.task(optional_techniques=["TECH-040"], optional_reasons={"TECH-040": "Attempt conflict with required technique"})
        original_load = technique_router.validate_techniques.load_json
        with patch.object(technique_router.validate_techniques, "load_json", side_effect=lambda path: registry if Path(path).name == "techniques.json" else original_load(path)):
            result = technique_router.route_task(task)
        self.assertNotIn("TECH-040", result["selected"]["optional_techniques"])
        self.assertTrue(any("Conflicts" in item["reason"] for item in result["selected"]["excluded_optional"]))

    def test_input_hash_is_deterministic_and_order_independent(self):
        first = self.task()
        second = dict(reversed(list(first.items())))
        self.assertEqual(technique_router.input_hash(first), technique_router.input_hash(second))

    def test_malformed_task_is_blocked_without_exception(self):
        result = technique_router.route_task({"task_id": "TASK-BAD"})
        self.assertEqual(result["state"], "BLOCKED")
        self.assertTrue(any("task_type" in error for error in result["errors"]))

    def test_required_conflict_blocks_selection(self):
        registry = technique_router.validate_techniques.load_json(technique_router.validate_techniques.REGISTRY_PATH)
        cards = {card["id"]: card for card in registry["techniques"]}
        cards["TECH-004"]["conflicting_techniques"] = ["TECH-006"]
        original_load = technique_router.validate_techniques.load_json
        with patch.object(technique_router.validate_techniques, "load_json", side_effect=lambda path: registry if Path(path).name == "techniques.json" else original_load(path)):
            result = technique_router.route_task(self.task())
        self.assertEqual(result["state"], "BLOCKED")
        self.assertTrue(any("Required techniques conflict" in error for error in result["errors"]))

    def test_equal_specificity_requires_explicit_route(self):
        manifests = technique_router.validate_routing.load(technique_router.validate_routing.ROUTING_DIR / "manifests.json")
        alternate = copy.deepcopy(next(item for item in manifests["manifests"] if item["id"] == "ROUTE-QUICK-DOCS"))
        alternate["id"] = "ROUTE-QUICK-ALT"
        manifests["manifests"].append(alternate)
        original_load = technique_router.validate_routing.load

        def load_with_alternate(path):
            if Path(path).name == "manifests.json":
                return manifests
            return original_load(path)

        with patch.object(technique_router.validate_routing, "load", side_effect=load_with_alternate):
            ambiguous = technique_router.route_task(self.task())
            explicit = technique_router.route_task(self.task(route_id="ROUTE-QUICK-ALT"))
        self.assertEqual(ambiguous["state"], "BLOCKED")
        self.assertEqual(ambiguous["candidate_route_ids"], ["ROUTE-QUICK-ALT", "ROUTE-QUICK-DOCS"])
        self.assertEqual(explicit["state"], "RECOMMENDED")
        self.assertEqual(explicit["route_id"], "ROUTE-QUICK-ALT")

    def test_cli_writes_deterministic_json_and_exit_code(self):
        task = self.task()
        with tempfile.TemporaryDirectory() as directory:
            task_path = Path(directory) / "task.json"
            output_path = Path(directory) / "route.json"
            task_path.write_text(json.dumps(task), encoding="utf-8")
            stdout = StringIO()
            with redirect_stdout(stdout):
                exit_code = technique_router.main([str(task_path), "--output", str(output_path)])
            self.assertEqual(exit_code, 0)
            record = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(record["route_id"], "ROUTE-QUICK-DOCS")
            self.assertEqual(record, technique_router.route_task(task))
            self.assertEqual(json.loads(stdout.getvalue()), record)

    def test_duplicate_optional_techniques_are_rejected(self):
        result = technique_router.route_task(self.task(optional_techniques=["TECH-009", "TECH-009"]))
        self.assertEqual(result["state"], "BLOCKED")
        self.assertTrue(any("must not contain duplicates" in error for error in result["errors"]))

    def test_rule_evaluation_is_type_safe(self):
        self.assertFalse(technique_router.evaluate_rule({"field": "value", "operator": "equals", "value": 1}, {"value": True})[0])
        self.assertFalse(technique_router.evaluate_rule({"field": "value", "operator": "in", "value": 1}, {"value": 1})[0])
        self.assertFalse(technique_router.evaluate_rule({"field": "value", "operator": "lte", "value": True}, {"value": 1})[0])

    def test_selection_does_not_claim_capability_availability(self):
        result = technique_router.route_task(self.task())
        self.assertTrue(any("does not establish installation" in item for item in result["limitations"]))
        self.assertTrue(all(step["step"] > 0 for step in result["sequence"]))


if __name__ == "__main__":
    unittest.main()
