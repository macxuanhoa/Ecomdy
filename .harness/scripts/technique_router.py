import argparse
import hashlib
import json
import sys
from pathlib import Path

import validate_routing
import validate_techniques

ROOT = Path(__file__).resolve().parents[1]
BOOLEAN_FIELDS = {
    "acceptance_criteria_present",
    "failure_observed",
    "behavior_change_intended",
    "mutation_required",
    "authoritative_sources_present",
    "contract_change",
    "data_source_approved",
    "authorized_scope",
    "existing_gallery_identified",
    "independent_scopes",
}


def load_task(path):
    if path == "-":
        return json.load(sys.stdin)
    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate_task(task):
    errors = []
    if not isinstance(task, dict):
        return ["task input must be a JSON object"]
    for field in ("task_id", "task_type"):
        if not isinstance(task.get(field), str) or not task[field].strip():
            errors.append(f"{field} must be a non-empty string")
    for field in BOOLEAN_FIELDS:
        if field in task and not isinstance(task[field], bool):
            errors.append(f"{field} must be a boolean")
    if "changed_file_count" in task:
        value = task["changed_file_count"]
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            errors.append("changed_file_count must be a non-negative integer")
    if "execution_mode" in task and task["execution_mode"] not in {"ADVISORY", "PARALLEL", "AUTONOMOUS"}:
        errors.append("execution_mode must be ADVISORY, PARALLEL or AUTONOMOUS")
    if "route_id" in task and (not isinstance(task["route_id"], str) or not task["route_id"].strip()):
        errors.append("route_id must be a non-empty string when supplied")
    optional = task.get("optional_techniques", [])
    if not isinstance(optional, list) or any(not isinstance(item, str) or not item.strip() for item in optional):
        errors.append("optional_techniques must be an array of non-empty strings")
    elif len(optional) != len(set(optional)):
        errors.append("optional_techniques must not contain duplicates")
    reasons = task.get("optional_reasons", {})
    if not isinstance(reasons, dict) or any(not isinstance(key, str) or not isinstance(value, str) or not value.strip() for key, value in reasons.items()):
        errors.append("optional_reasons must map technique IDs to non-empty strings")
    return errors


def evaluate_rule(rule, task):
    field = rule["field"]
    if field not in task:
        return False, {"field": field, "operator": rule["operator"], "expected": rule["value"], "actual": None, "matched": False, "reason": "missing field"}
    actual = task[field]
    expected = rule["value"]
    operator = rule["operator"]
    matched = False
    if operator == "equals":
        matched = type(actual) is type(expected) and actual == expected
    elif operator == "in":
        matched = isinstance(expected, list) and any(type(actual) is type(item) and actual == item for item in expected)
    elif operator == "lte":
        matched = not isinstance(actual, bool) and isinstance(actual, (int, float)) and not isinstance(expected, bool) and isinstance(expected, (int, float)) and actual <= expected
    elif operator == "gte":
        matched = not isinstance(actual, bool) and isinstance(actual, (int, float)) and not isinstance(expected, bool) and isinstance(expected, (int, float)) and actual >= expected
    return matched, {"field": field, "operator": operator, "expected": expected, "actual": actual, "matched": matched}


def input_hash(task):
    payload = json.dumps(task, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def techniques_conflict(cards, left, right):
    return right in cards[left]["conflicting_techniques"] or left in cards[right]["conflicting_techniques"]


def empty_result(task, state):
    return {
        "schema_version": "1.0",
        "task_id": task.get("task_id"),
        "input_sha256": input_hash(task),
        "state": state,
        "runtime_state": "BLOCKED" if state == "BLOCKED" else "NOT_SELECTED",
        "execution_state": "NOT_EXECUTED",
        "decisions": [],
        "selected": {},
    }


def route_task(task):
    errors = validate_task(task)
    if errors:
        result = empty_result(task if isinstance(task, dict) else {}, "BLOCKED")
        result["errors"] = errors
        return result
    if task.get("execution_mode") == "AUTONOMOUS":
        result = empty_result(task, "BLOCKED")
        result["errors"] = ["AUTONOMOUS execution is blocked until runtime controls are approved and verified"]
        return result

    routing_errors, _, _, _ = validate_routing.validate_all()
    technique_errors = validate_techniques.validate_registry(validate_techniques.load_json(validate_techniques.REGISTRY_PATH))
    if routing_errors or technique_errors:
        result = empty_result(task, "BLOCKED")
        result["errors"] = routing_errors + technique_errors
        return result

    registry = validate_techniques.load_json(validate_techniques.REGISTRY_PATH)
    cards = {card["id"]: card for card in registry["techniques"]}
    profiles = validate_routing.load(validate_routing.ROUTING_DIR / "profiles.json")["profiles"]
    manifests = validate_routing.load(validate_routing.ROUTING_DIR / "manifests.json")["manifests"]
    recipes = validate_routing.load(validate_routing.ROUTING_DIR / "recipes.json")["recipes"]
    profile_by_id = {profile["id"]: profile for profile in profiles}

    candidates = []
    decisions = []
    for manifest in manifests:
        rule_results = [evaluate_rule(rule, task) for rule in manifest["activation_rules"]]
        matched = all(result[0] for result in rule_results)
        decision = {
            "route_id": manifest["id"],
            "matched": matched,
            "specificity": len(rule_results),
            "rules": [result[1] for result in rule_results],
        }
        decisions.append(decision)
        if matched:
            candidates.append(manifest)

    requested_route = task.get("route_id")
    if requested_route:
        candidates = [manifest for manifest in candidates if manifest["id"] == requested_route]
        if not candidates:
            result = empty_result(task, "BLOCKED")
            result["decisions"] = decisions
            result["errors"] = [f"Requested route {requested_route} does not match the task activation rules"]
            return result
    if not candidates:
        result = empty_result(task, "NO_MATCH")
        result["decisions"] = decisions
        result["guidance"] = "Provide the missing activation facts or choose an approved task type; do not infer a route from vague keywords."
        return result

    highest = max(len(manifest["activation_rules"]) for manifest in candidates)
    finalists = [manifest for manifest in candidates if len(manifest["activation_rules"]) == highest]
    if len(finalists) != 1:
        result = empty_result(task, "BLOCKED")
        result["decisions"] = decisions
        result["errors"] = ["Multiple equally specific routes match; supply route_id explicitly"]
        result["candidate_route_ids"] = sorted(manifest["id"] for manifest in finalists)
        return result

    manifest = finalists[0]
    profile = profile_by_id[manifest["profile"]]
    if profile["execution_status"] == "BLOCKED":
        result = empty_result(task, "BLOCKED")
        result["decisions"] = decisions
        result["errors"] = [f"Profile {profile['id']} is BLOCKED"]
        return result

    required = list(manifest["required_techniques"])
    incompatible = set(manifest["incompatible_techniques"])
    if incompatible & set(required):
        result = empty_result(task, "BLOCKED")
        result["decisions"] = decisions
        result["errors"] = ["A required technique is marked incompatible by the route"]
        return result
    required_conflicts = []
    for technique_id in required:
        for other_id in required:
            if technique_id < other_id and techniques_conflict(cards, technique_id, other_id):
                required_conflicts.append([technique_id, other_id])
    if required_conflicts:
        result = empty_result(task, "BLOCKED")
        result["decisions"] = decisions
        result["errors"] = ["Required techniques conflict: " + "; ".join("/".join(pair) for pair in required_conflicts)]
        return result

    selected_optional = []
    excluded_optional = []
    allowed_optional = set(manifest["optional_techniques"]) - incompatible
    for technique_id in task.get("optional_techniques", []):
        reason = task.get("optional_reasons", {}).get(technique_id)
        if technique_id in required:
            excluded_optional.append({"technique_id": technique_id, "reason": "Already required by the route"})
        elif technique_id not in allowed_optional:
            excluded_optional.append({"technique_id": technique_id, "reason": "Not an allowed optional technique for this route"})
        elif not reason:
            excluded_optional.append({"technique_id": technique_id, "reason": "A non-empty optional_reasons entry is required"})
        else:
            conflict = next((other for other in required + selected_optional if techniques_conflict(cards, technique_id, other)), None)
            if conflict:
                excluded_optional.append({"technique_id": technique_id, "reason": f"Conflicts with selected technique {conflict}"})
            else:
                selected_optional.append(technique_id)

    selected = required + selected_optional
    result = {
        "schema_version": "1.0",
        "task_id": task["task_id"],
        "task_type": task["task_type"],
        "input_sha256": input_hash(task),
        "state": "RECOMMENDED",
        "runtime_state": "RECOMMENDED",
        "execution_state": "NOT_EXECUTED",
        "route_id": manifest["id"],
        "profile_id": profile["id"],
        "profile_name": profile["name"],
        "profile_execution_status": profile["execution_status"],
        "max_parallel_agents": profile["max_parallel_agents"],
        "rationale": manifest["rationale"],
        "selected": {
            "required_techniques": required,
            "optional_techniques": selected_optional,
            "optional_reasons": {item: task.get("optional_reasons", {}).get(item) for item in selected_optional},
            "techniques": selected,
            "excluded_optional": excluded_optional,
            "incompatible_techniques": sorted(incompatible),
        },
        "sequence": manifest["sequence"],
        "context_scope": manifest["context_scope"],
        "runtime_limits": manifest["runtime_limits"],
        "retry_limits": manifest["retry_limits"],
        "verification_gates": manifest["verification_gates"],
        "approval_conditions": manifest["approval_conditions"],
        "stop_conditions": manifest["stop_conditions"],
        "fallback": manifest["fallback"],
        "compatible_recipe_ids": sorted(recipe["id"] for recipe in recipes if recipe["route_id"] == manifest["id"]),
        "decisions": decisions,
        "limitations": [
            "Selection is advisory and is not an attempt, execution or verification.",
            "Technique registration does not establish installation, configuration or session availability.",
            "Context and runtime limits remain advisory until an approved enforcement layer exists.",
        ],
    }
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description="Deterministic advisory DevHarness technique router")
    parser.add_argument("input", nargs="?", default="-", help="Task JSON file or - for stdin")
    parser.add_argument("--output", help="Write the routing record to this path")
    args = parser.parse_args(argv)
    try:
        task = load_task(args.input)
        result = route_task(task)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Route input error: {exc}", file=sys.stderr)
        return 1
    text = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        try:
            Path(args.output).write_text(text, encoding="utf-8")
        except OSError as exc:
            print(f"Route output error: {exc}", file=sys.stderr)
            return 1
    print(text, end="")
    return {"RECOMMENDED": 0, "NO_MATCH": 2, "BLOCKED": 3}.get(result["state"], 1)


if __name__ == "__main__":
    sys.exit(main())
