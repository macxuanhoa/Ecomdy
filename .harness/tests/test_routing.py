import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import validate_routing
import validate_techniques


class RoutingRegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.techniques = validate_techniques.load_json(validate_techniques.REGISTRY_PATH)
        cls.technique_ids = {item["id"] for item in cls.techniques["techniques"]}
        cls.profiles = validate_routing.load(validate_routing.ROUTING_DIR / "profiles.json")
        cls.manifests = validate_routing.load(validate_routing.ROUTING_DIR / "manifests.json")
        cls.recipes = validate_routing.load(validate_routing.ROUTING_DIR / "recipes.json")
        cls.schema = validate_routing.load(validate_routing.SCHEMA_PATH)
        cls.profile_ids = {item["id"] for item in cls.profiles["profiles"]}
        cls.route_profiles = {item["id"]: item["profile"] for item in cls.manifests["manifests"]}

    def test_all_routing_registries_are_valid(self):
        errors, profiles, routes, recipes = validate_routing.validate_all()
        self.assertEqual(errors, [])
        self.assertEqual(profiles, 9)
        self.assertGreaterEqual(routes, 10)
        self.assertEqual(recipes, 24)

    def test_autonomous_is_blocked_and_parallel_is_not_default(self):
        for profile in self.profiles["profiles"]:
            if profile["name"] == "AUTONOMOUS":
                self.assertEqual(profile["execution_status"], "BLOCKED")
                self.assertEqual(profile["implementation_status"], "blocked_design")
            if profile["name"] != "PARALLEL":
                self.assertEqual(profile["max_parallel_agents"], 1)

    def test_manifests_have_contiguous_sequences_and_exclude_originals(self):
        for manifest in self.manifests["manifests"]:
            self.assertEqual([step["step"] for step in manifest["sequence"]], list(range(1, len(manifest["sequence"]) + 1)))
            self.assertFalse(manifest["context_scope"]["include_originals"])
            self.assertFalse(set(manifest["required_techniques"]) & set(manifest["incompatible_techniques"]))

    def test_manifest_runtime_limits_remain_advisory(self):
        for manifest in self.manifests["manifests"]:
            self.assertEqual(manifest["runtime_limits"]["enforcement"], "advisory")
        changed = copy.deepcopy(self.manifests)
        del changed["manifests"][0]["runtime_limits"]["enforcement"]
        errors = validate_routing.validate_manifests(changed, self.technique_ids, self.profile_ids, self.schema)
        self.assertTrue(any("runtime_limits.enforcement must remain advisory" in error for error in errors))

    def test_recipes_match_route_profiles(self):
        self.assertEqual(len(self.recipes["recipes"]), 24)
        for recipe in self.recipes["recipes"]:
            self.assertEqual(recipe["profile_id"], self.route_profiles[recipe["route_id"]])
            self.assertTrue(set(recipe["techniques"]).issubset(self.technique_ids))

    def test_duplicate_profile_id_is_rejected(self):
        changed = copy.deepcopy(self.profiles)
        changed["profiles"][1]["id"] = changed["profiles"][0]["id"]
        errors = validate_routing.validate_profiles(changed, self.technique_ids, self.schema)
        self.assertTrue(any("Duplicate profile IDs" in error for error in errors))

    def test_unknown_technique_reference_is_rejected(self):
        changed = copy.deepcopy(self.profiles)
        changed["profiles"][0]["required_techniques"].append("TECH-999")
        errors = validate_routing.validate_profiles(changed, self.technique_ids, self.schema)
        self.assertTrue(any("unknown technique: TECH-999" in error for error in errors))

    def test_selected_incompatible_technique_is_rejected(self):
        changed = copy.deepcopy(self.manifests)
        changed["manifests"][0]["required_techniques"].append("TECH-014")
        errors = validate_routing.validate_manifests(changed, self.technique_ids, self.profile_ids, self.schema)
        self.assertTrue(any("selects an incompatible technique" in error for error in errors))

    def test_recipe_techniques_must_fit_route_and_profile_allow_lists(self):
        route_techniques = {
            item["id"]: (set(item["required_techniques"]) | set(item["optional_techniques"]), set(item["incompatible_techniques"]))
            for item in self.manifests["manifests"]
        }
        profile_techniques = {
            item["id"]: set(item["required_techniques"]) | set(item["optional_techniques"])
            for item in self.profiles["profiles"]
        }
        changed = copy.deepcopy(self.recipes)
        changed["recipes"][0]["techniques"].append("TECH-014")
        errors = validate_routing.validate_recipes(changed, self.technique_ids, self.profile_ids, self.route_profiles, self.schema, route_techniques, profile_techniques)
        self.assertTrue(any("not allowed by its route" in error for error in errors))
        self.assertTrue(any("incompatible with its route" in error for error in errors))

    def test_unknown_recipe_route_is_rejected(self):
        changed = copy.deepcopy(self.recipes)
        changed["recipes"][0]["route_id"] = "ROUTE-UNKNOWN"
        errors = validate_routing.validate_recipes(changed, self.technique_ids, self.profile_ids, self.route_profiles, self.schema)
        self.assertTrue(any("route_id is unknown" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
