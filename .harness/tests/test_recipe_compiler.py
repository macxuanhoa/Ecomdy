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
import recipe_compiler
import technique_router


class RecipeCompilerTests(unittest.TestCase):
    def route(self, **updates):
        task = {
            "task_id": "TASK-COMPILE-001",
            "task_type": "feature",
            "acceptance_criteria_present": True,
            "changed_file_count": 4,
            "mutation_required": True,
        }
        task.update(updates)
        result = technique_router.route_task(task)
        self.assertEqual(result["state"], "RECOMMENDED")
        return result

    def test_task_type_selects_recipe_and_expands_required_contract(self):
        route = self.route()
        result = recipe_compiler.compile_recipe(route, task_type="feature")
        self.assertEqual(result["state"], "COMPILED")
        self.assertEqual(result["recipe_id"], "RECIPE-001")
        self.assertEqual(result["execution_state"], "NOT_EXECUTED")
        self.assertIn("TECH-008", result["selected"]["required_techniques"])
        self.assertTrue(all(item["execution_state"] == "NOT_EXECUTED" for item in result["sequence"]))
        self.assertEqual(result["resources"]["measurement_status"], "unknown")

    def test_route_task_type_selects_recipe_without_extra_flag(self):
        result = recipe_compiler.compile_recipe(self.route())
        self.assertEqual(result["state"], "COMPILED")
        self.assertEqual(result["recipe_id"], "RECIPE-001")

    def test_route_without_recipe_compiles_explicit_route_only_contract(self):
        route = self.route(task_id="TASK-QUICK-001", task_type="documentation", risk="low", complexity="low", changed_file_count=2, acceptance_criteria_present=True)
        result = recipe_compiler.compile_recipe(route)
        self.assertEqual(result["state"], "COMPILED")
        self.assertIsNone(result["recipe_id"])
        self.assertTrue(any("No recipe" in warning for warning in result["warnings"]))

    def test_multiple_recipes_require_explicit_selection(self):
        route = self.route()
        route.pop("task_type")
        result = recipe_compiler.compile_recipe(route)
        self.assertEqual(result["state"], "BLOCKED")
        self.assertIn("RECIPE-001", result["candidate_recipe_ids"])
        self.assertIn("RECIPE-014", result["candidate_recipe_ids"])

    def test_explicit_recipe_must_match_route_and_task_type(self):
        route = self.route()
        wrong_route = recipe_compiler.compile_recipe(route, recipe_id="RECIPE-019")
        wrong_type = recipe_compiler.compile_recipe(route, recipe_id="RECIPE-001", task_type="ui")
        self.assertEqual(wrong_route["state"], "BLOCKED")
        self.assertEqual(wrong_type["state"], "BLOCKED")

    def test_unmatched_task_type_does_not_silently_fallback(self):
        result = recipe_compiler.compile_recipe(self.route(), task_type="unknown")
        self.assertEqual(result["state"], "BLOCKED")
        self.assertTrue(any("No recipe" in error for error in result["errors"]))

    def test_tampered_route_selection_is_rejected(self):
        route = self.route()
        route["selected"]["required_techniques"].pop()
        route["selected"]["techniques"].pop()
        result = recipe_compiler.compile_recipe(route)
        self.assertEqual(result["state"], "BLOCKED")
        self.assertTrue(any("required techniques" in error for error in result["errors"]))

    def test_malformed_optional_reasons_and_duplicates_are_rejected(self):
        route = self.route()
        route["selected"]["optional_reasons"] = []
        malformed = recipe_compiler.compile_recipe(route)
        self.assertEqual(malformed["state"], "BLOCKED")
        self.assertTrue(any("optional_reasons must be an object" in error for error in malformed["errors"]))

        route = self.route(optional_techniques=["TECH-003"], optional_reasons={"TECH-003": "Explicit bounded specification comparison"})
        route["selected"]["optional_techniques"].append("TECH-003")
        duplicate = recipe_compiler.compile_recipe(route)
        self.assertEqual(duplicate["state"], "BLOCKED")
        self.assertTrue(any("must not contain duplicates" in error for error in duplicate["errors"]))

    def test_non_recommended_route_is_rejected(self):
        route = self.route()
        route["execution_state"] = "EXECUTED"
        result = recipe_compiler.compile_recipe(route, task_type="feature")
        self.assertEqual(result["state"], "BLOCKED")
        self.assertTrue(any("NOT_EXECUTED" in error for error in result["errors"]))

    def test_required_conflict_blocks_compilation(self):
        route = self.route()
        registry = technique_router.validate_techniques.load_json(technique_router.validate_techniques.REGISTRY_PATH)
        cards = {card["id"]: card for card in registry["techniques"]}
        cards["TECH-004"]["conflicting_techniques"] = ["TECH-006"]
        original_load = recipe_compiler.validate_techniques.load_json
        with patch.object(recipe_compiler.validate_techniques, "load_json", side_effect=lambda path: registry if Path(path).name == "techniques.json" else original_load(path)):
            result = recipe_compiler.compile_recipe(route, task_type="feature")
        self.assertEqual(result["state"], "BLOCKED")
        self.assertTrue(any("conflict" in error.lower() for error in result["errors"]))

    def test_limits_use_stricter_route_and_profile_values(self):
        result = recipe_compiler.compile_recipe(self.route(), task_type="feature")
        self.assertEqual(result["runtime_limits"]["enforcement"], "advisory")
        self.assertFalse(result["context_scope"]["include_originals"])
        self.assertEqual(result["max_parallel_agents"], 1)
        self.assertLessEqual(result["context_scope"]["max_files"], 40)

    def test_optional_context_manifest_is_embedded_without_execution(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "docs").mkdir()
            (root / "docs" / "guide.md").write_text("local guide", encoding="utf-8")
            request = {"include_paths": ["docs"], "max_files": 2, "max_bytes": 100}
            result = recipe_compiler.compile_recipe(self.route(), task_type="feature", context_request=request, project_root=root)
            self.assertEqual(result["state"], "COMPILED")
            self.assertEqual(result["context_manifest"]["summary"]["file_count"], 1)
            self.assertNotIn("local guide", json.dumps(result))

    def test_all_registered_recipes_compile_without_execution(self):
        profiles = {item["id"]: item for item in recipe_compiler.validate_routing.load(recipe_compiler.validate_routing.ROUTING_DIR / "profiles.json")["profiles"]}
        manifests = {item["id"]: item for item in recipe_compiler.validate_routing.load(recipe_compiler.validate_routing.ROUTING_DIR / "manifests.json")["manifests"]}
        recipes = recipe_compiler.validate_routing.load(recipe_compiler.validate_routing.ROUTING_DIR / "recipes.json")["recipes"]
        for recipe in recipes:
            with self.subTest(recipe=recipe["id"]):
                manifest = manifests[recipe["route_id"]]
                profile = profiles[manifest["profile"]]
                route = {
                    "task_id": "TASK-ALL-RECIPES",
                    "task_type": recipe["task_type"],
                    "state": "RECOMMENDED",
                    "execution_state": "NOT_EXECUTED",
                    "route_id": manifest["id"],
                    "profile_id": profile["id"],
                    "selected": {"required_techniques": manifest["required_techniques"], "optional_techniques": [], "optional_reasons": {}, "techniques": manifest["required_techniques"]},
                    "sequence": manifest["sequence"],
                    "context_scope": manifest["context_scope"],
                    "runtime_limits": manifest["runtime_limits"],
                    "retry_limits": manifest["retry_limits"],
                    "verification_gates": manifest["verification_gates"],
                    "approval_conditions": manifest["approval_conditions"],
                    "stop_conditions": manifest["stop_conditions"],
                    "fallback": manifest["fallback"],
                    "max_parallel_agents": profile["max_parallel_agents"],
                }
                result = recipe_compiler.compile_recipe(route, recipe_id=recipe["id"], task_type=recipe["task_type"])
                self.assertEqual(result["state"], "COMPILED")
                self.assertEqual(result["execution_state"], "NOT_EXECUTED")

    def test_compilation_is_deterministic(self):
        route = self.route()
        first = recipe_compiler.compile_recipe(route, task_type="feature")
        second = recipe_compiler.compile_recipe(dict(reversed(list(route.items()))), task_type="feature")
        self.assertEqual(first, second)

    def test_cli_writes_compiled_json(self):
        route = self.route()
        with tempfile.TemporaryDirectory() as directory:
            route_path = Path(directory) / "route.json"
            output_path = Path(directory) / "compiled.json"
            route_path.write_text(json.dumps(route), encoding="utf-8")
            stdout = StringIO()
            with redirect_stdout(stdout):
                code = recipe_compiler.main([str(route_path), "--task-type", "feature", "--output", str(output_path)])
            self.assertEqual(code, 0)
            self.assertEqual(json.loads(output_path.read_text(encoding="utf-8"))["recipe_id"], "RECIPE-001")
            self.assertEqual(json.loads(stdout.getvalue()), json.loads(output_path.read_text(encoding="utf-8")))


if __name__ == "__main__":
    unittest.main()
