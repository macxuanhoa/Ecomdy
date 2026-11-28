import json
import re
import sys
from pathlib import Path

import validate_techniques

ROOT = Path(__file__).resolve().parents[1]
ROUTING_DIR = ROOT / "registry" / "routing"
SCHEMA_PATH = ROOT / "schemas" / "routing.schema.json"
PROFILE_NAMES = {"QUICK", "STANDARD", "DEEP", "PARALLEL", "AUTONOMOUS", "DEBUG", "DESIGN", "SECURITY", "AUDIT"}
ARRAY_FIELDS = {
    "applicable_task_types",
    "required_techniques",
    "optional_techniques",
    "disallowed_actions",
    "verification_gates",
    "approval_conditions",
    "stop_conditions",
    "task_types",
    "incompatible_techniques",
    "incompatible_tools",
    "include_paths",
    "exclude_paths",
    "inputs",
    "outputs",
    "acceptance_checks",
    "owner_roles",
    "techniques",
}
STRING_FIELDS = {
    "id",
    "name",
    "implementation_status",
    "execution_status",
    "fallback",
    "profile",
    "rationale",
    "task_type",
    "route_id",
    "profile_id",
    "failure_handling",
}


def load(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError(f"Missing file: {path.relative_to(ROOT)}")
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path.relative_to(ROOT)}: {exc}")


def check_fields(item, required, allowed, label, errors):
    if not isinstance(item, dict):
        errors.append(f"{label} must be an object")
        return False
    missing = sorted(set(required) - set(item))
    extra = sorted(set(item) - set(allowed))
    if missing:
        errors.append(f"{label} missing fields: {', '.join(missing)}")
    if extra:
        errors.append(f"{label} has unknown fields: {', '.join(extra)}")
    return True


def check_common(item, label, errors):
    for field in STRING_FIELDS:
        if field in item:
            value = item[field]
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{label}.{field} must be a non-empty string")
    for field in ARRAY_FIELDS:
        if field in item:
            value = item[field]
            if not isinstance(value, list) or any(not isinstance(entry, str) or not entry.strip() for entry in value):
                errors.append(f"{label}.{field} must be an array of non-empty strings")


def check_technique_refs(values, technique_ids, label, errors):
    for value in values:
        if value not in technique_ids:
            errors.append(f"{label} references unknown technique: {value}")


def validate_profiles(data, technique_ids, schema):
    errors = []
    definition = schema["$defs"]["profile"]
    required = set(definition["required"])
    allowed = set(definition["properties"])
    if not check_fields(data, {"schema_version", "registry_version", "status", "profiles"}, {"schema_version", "registry_version", "status", "profiles"}, "profiles registry", errors):
        return errors
    if data.get("schema_version") != "1.0" or data.get("status") != "ADVISORY_DESIGN":
        errors.append("profiles registry schema_version/status is invalid")
    profiles = data.get("profiles")
    if not isinstance(profiles, list) or len(profiles) != 9:
        errors.append("profiles must contain exactly 9 entries")
        return errors

    ids = []
    names = []
    for index, profile in enumerate(profiles):
        label = f"profiles[{index}]"
        if not check_fields(profile, required, allowed, label, errors):
            continue
        check_common(profile, label, errors)
        activation_rules = profile.get("activation_rules")
        if not isinstance(activation_rules, list) or not activation_rules or any(not isinstance(rule, str) or not rule.strip() for rule in activation_rules):
            errors.append(f"{label}.activation_rules must be an array of non-empty strings")
        profile_id = profile.get("id", "")
        ids.append(profile_id)
        names.append(profile.get("name"))
        if not re.fullmatch(r"PROFILE-[A-Z]+", profile_id):
            errors.append(f"{label}.id is invalid")
        if profile.get("name") not in PROFILE_NAMES:
            errors.append(f"{label}.name is invalid")
        if profile.get("execution_status") not in {"NOT_IMPLEMENTED", "BLOCKED", "AVAILABLE", "VERIFIED"}:
            errors.append(f"{label}.execution_status is invalid")
        if profile.get("implementation_status") not in {"advisory_design", "blocked_design", "implemented_verified"}:
            errors.append(f"{label}.implementation_status is invalid")
        for field in ("required_techniques", "optional_techniques"):
            check_technique_refs(profile.get(field, []), technique_ids, f"{label}.{field}", errors)
        if set(profile.get("required_techniques", [])) & set(profile.get("optional_techniques", [])):
            errors.append(f"{label} required and optional techniques overlap")
        context = profile.get("context_limits", {})
        if context.get("enforcement") != "advisory" or context.get("include_originals") is not False:
            errors.append(f"{label}.context_limits must remain advisory and exclude originals")
        runtime = profile.get("runtime_limits", {})
        if runtime.get("enforcement") != "advisory":
            errors.append(f"{label}.runtime_limits.enforcement must remain advisory")
        for field in ("max_iterations", "max_runtime_minutes"):
            if not isinstance(runtime.get(field), int) or runtime.get(field, 0) < 1:
                errors.append(f"{label}.runtime_limits.{field} must be positive")
        if not isinstance(runtime.get("max_cost_usd"), (int, float)) or runtime.get("max_cost_usd", -1) < 0:
            errors.append(f"{label}.runtime_limits.max_cost_usd must be non-negative")
        retry = profile.get("retry_limits", {})
        if not isinstance(retry.get("max_retries"), int) or retry.get("max_retries", -1) < 0:
            errors.append(f"{label}.retry_limits.max_retries must be non-negative")
        if not isinstance(profile.get("max_parallel_agents"), int) or not 1 <= profile.get("max_parallel_agents", 0) <= 3:
            errors.append(f"{label}.max_parallel_agents must be 1-3")
        if profile.get("name") != "PARALLEL" and profile.get("max_parallel_agents") != 1:
            errors.append(f"{label} must not default to multiple agents")

    if len(ids) != len(set(ids)):
        errors.append("Duplicate profile IDs")
    if set(names) != PROFILE_NAMES or len(names) != len(set(names)):
        errors.append("Profiles must cover QUICK, STANDARD, DEEP, PARALLEL, AUTONOMOUS, DEBUG, DESIGN, SECURITY and AUDIT exactly once")
    autonomous = next((item for item in profiles if item.get("name") == "AUTONOMOUS"), {})
    if autonomous.get("execution_status") != "BLOCKED" or autonomous.get("implementation_status") != "blocked_design":
        errors.append("AUTONOMOUS must remain BLOCKED until runtime controls are approved and verified")
    return errors


def validate_manifests(data, technique_ids, profile_ids, schema):
    errors = []
    definition = schema["$defs"]["manifest"]
    required = set(definition["required"])
    allowed = set(definition["properties"])
    if not check_fields(data, {"schema_version", "registry_version", "status", "manifests"}, {"schema_version", "registry_version", "status", "manifests"}, "manifests registry", errors):
        return errors
    if data.get("schema_version") != "1.0" or data.get("status") != "ADVISORY_DESIGN":
        errors.append("manifests registry schema_version/status is invalid")
    manifests = data.get("manifests")
    if not isinstance(manifests, list) or not manifests:
        errors.append("manifests must be a non-empty array")
        return errors

    ids = []
    for index, manifest in enumerate(manifests):
        label = f"manifests[{index}]"
        if not check_fields(manifest, required, allowed, label, errors):
            continue
        check_common(manifest, label, errors)
        activation_rules = manifest.get("activation_rules")
        if not isinstance(activation_rules, list) or not activation_rules:
            errors.append(f"{label}.activation_rules must be a non-empty array")
        else:
            for rule_index, rule in enumerate(activation_rules):
                rule_label = f"{label}.activation_rules[{rule_index}]"
                if not check_fields(rule, {"field", "operator", "value"}, {"field", "operator", "value"}, rule_label, errors):
                    continue
                if not isinstance(rule.get("field"), str) or not rule.get("field", "").strip():
                    errors.append(f"{rule_label}.field must be a non-empty string")
                if rule.get("operator") not in {"equals", "in", "lte", "gte"}:
                    errors.append(f"{rule_label}.operator is invalid")
                if not isinstance(rule.get("value"), (str, int, float, bool, list)):
                    errors.append(f"{rule_label}.value is invalid")
        route_id = manifest.get("id", "")
        ids.append(route_id)
        if not re.fullmatch(r"ROUTE-[A-Z0-9-]+", route_id):
            errors.append(f"{label}.id is invalid")
        if manifest.get("profile") not in profile_ids:
            errors.append(f"{label}.profile is unknown")
        for field in ("required_techniques", "optional_techniques", "incompatible_techniques"):
            check_technique_refs(manifest.get(field, []), technique_ids, f"{label}.{field}", errors)
        required_techniques = set(manifest.get("required_techniques", []))
        optional_techniques = set(manifest.get("optional_techniques", []))
        incompatible = set(manifest.get("incompatible_techniques", []))
        if required_techniques & optional_techniques:
            errors.append(f"{label} required and optional techniques overlap")
        if (required_techniques | optional_techniques) & incompatible:
            errors.append(f"{label} selects an incompatible technique")
        sequence = manifest.get("sequence", [])
        if not isinstance(sequence, list) or not sequence:
            errors.append(f"{label}.sequence must be non-empty")
            continue
        expected_steps = list(range(1, len(sequence) + 1))
        actual_steps = []
        for step_index, step in enumerate(sequence):
            step_label = f"{label}.sequence[{step_index}]"
            step_required = {"step", "technique", "agent", "output"}
            if not check_fields(step, step_required, step_required, step_label, errors):
                continue
            actual_steps.append(step.get("step"))
            check_technique_refs([step.get("technique")], technique_ids, step_label, errors)
            if step.get("technique") not in required_techniques | optional_techniques:
                errors.append(f"{step_label}.technique is not selected by the manifest")
            if not isinstance(step.get("agent"), str) or not re.fullmatch(r"A[0-9]{2}", step.get("agent", "")):
                errors.append(f"{step_label}.agent is invalid")
        if actual_steps != expected_steps:
            errors.append(f"{label}.sequence steps must be contiguous from 1")
        scope = manifest.get("context_scope", {})
        if scope.get("include_originals") is not False:
            errors.append(f"{label}.context_scope must exclude originals by default")
        runtime = manifest.get("runtime_limits", {})
        if runtime.get("enforcement") != "advisory":
            errors.append(f"{label}.runtime_limits.enforcement must remain advisory")
        for field in ("max_iterations", "max_runtime_minutes"):
            if not isinstance(runtime.get(field), int) or runtime.get(field, 0) < 1:
                errors.append(f"{label}.runtime_limits.{field} must be positive")
        if not isinstance(runtime.get("max_cost_usd"), (int, float)) or runtime.get("max_cost_usd", -1) < 0:
            errors.append(f"{label}.runtime_limits.max_cost_usd must be non-negative")
        retry = manifest.get("retry_limits", {})
        if not isinstance(retry.get("max_retries"), int) or retry.get("max_retries", -1) < 0:
            errors.append(f"{label}.retry_limits.max_retries must be non-negative")

    if len(ids) != len(set(ids)):
        errors.append("Duplicate route IDs")
    return errors


def validate_recipes(data, technique_ids, profile_ids, route_profiles, schema, route_techniques=None, profile_techniques=None):
    errors = []
    definition = schema["$defs"]["recipe"]
    required = set(definition["required"])
    allowed = set(definition["properties"])
    if not check_fields(data, {"schema_version", "registry_version", "status", "recipes"}, {"schema_version", "registry_version", "status", "recipes"}, "recipes registry", errors):
        return errors
    if data.get("schema_version") != "1.0" or data.get("status") != "ADVISORY_DESIGN":
        errors.append("recipes registry schema_version/status is invalid")
    recipes = data.get("recipes")
    if not isinstance(recipes, list) or len(recipes) != 24:
        errors.append("recipes must contain exactly 24 entries")
        return errors

    ids = []
    for index, recipe in enumerate(recipes):
        label = f"recipes[{index}]"
        if not check_fields(recipe, required, allowed, label, errors):
            continue
        check_common(recipe, label, errors)
        recipe_id = recipe.get("id", "")
        ids.append(recipe_id)
        if not re.fullmatch(r"RECIPE-[0-9]{3}", recipe_id):
            errors.append(f"{label}.id is invalid")
        if recipe.get("route_id") not in route_profiles:
            errors.append(f"{label}.route_id is unknown")
        elif recipe.get("profile_id") != route_profiles[recipe.get("route_id")]:
            errors.append(f"{label}.profile_id does not match its route")
        if recipe.get("profile_id") not in profile_ids:
            errors.append(f"{label}.profile_id is unknown")
        check_technique_refs(recipe.get("techniques", []), technique_ids, f"{label}.techniques", errors)
        recipe_techniques = set(recipe.get("techniques", []))
        if route_techniques is not None and recipe.get("route_id") in route_techniques:
            route_allowed, route_incompatible = route_techniques[recipe["route_id"]]
            outside_route = recipe_techniques - route_allowed
            if outside_route:
                errors.append(f"{label}.techniques are not allowed by its route: {', '.join(sorted(outside_route))}")
            if recipe_techniques & route_incompatible:
                errors.append(f"{label}.techniques are incompatible with its route: {', '.join(sorted(recipe_techniques & route_incompatible))}")
        if profile_techniques is not None and recipe.get("profile_id") in profile_techniques:
            outside_profile = recipe_techniques - profile_techniques[recipe["profile_id"]]
            if outside_profile:
                errors.append(f"{label}.techniques are not allowed by its profile: {', '.join(sorted(outside_profile))}")
        if recipe.get("implementation_status") != "advisory_design":
            errors.append(f"{label}.implementation_status must be advisory_design")

    if len(ids) != len(set(ids)):
        errors.append("Duplicate recipe IDs")
    return errors


def validate_all():
    techniques = validate_techniques.load_json(validate_techniques.REGISTRY_PATH)
    technique_ids = {item["id"] for item in techniques["techniques"]}
    profiles = load(ROUTING_DIR / "profiles.json")
    manifests = load(ROUTING_DIR / "manifests.json")
    recipes = load(ROUTING_DIR / "recipes.json")
    schema = load(SCHEMA_PATH)

    errors = validate_profiles(profiles, technique_ids, schema)
    profile_ids = {item.get("id") for item in profiles.get("profiles", []) if isinstance(item, dict)}
    errors += validate_manifests(manifests, technique_ids, profile_ids, schema)
    route_profiles = {item.get("id"): item.get("profile") for item in manifests.get("manifests", []) if isinstance(item, dict)}
    route_techniques = {
        item["id"]: (set(item["required_techniques"]) | set(item["optional_techniques"]), set(item["incompatible_techniques"]))
        for item in manifests.get("manifests", [])
        if isinstance(item, dict) and "id" in item and all(isinstance(item.get(field), list) for field in ("required_techniques", "optional_techniques", "incompatible_techniques"))
    }
    profile_techniques = {
        item["id"]: set(item["required_techniques"]) | set(item["optional_techniques"])
        for item in profiles.get("profiles", [])
        if isinstance(item, dict) and "id" in item and all(isinstance(item.get(field), list) for field in ("required_techniques", "optional_techniques"))
    }
    errors += validate_recipes(recipes, technique_ids, profile_ids, route_profiles, schema, route_techniques, profile_techniques)
    return errors, len(profiles.get("profiles", [])), len(manifests.get("manifests", [])), len(recipes.get("recipes", []))


def main():
    try:
        errors, profile_count, manifest_count, recipe_count = validate_all()
    except ValueError as exc:
        errors = [str(exc)]
        profile_count = manifest_count = recipe_count = 0
    if errors:
        print("Routing registry: FAIL")
        for error in errors:
            print("-", error)
        return 1
    print(f"Routing registry: PASS ({profile_count} profiles, {manifest_count} routes, {recipe_count} recipes; advisory only)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
