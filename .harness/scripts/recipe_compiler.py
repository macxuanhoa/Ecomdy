import argparse
import hashlib
import json
import sys
from pathlib import Path

import context_compiler
import technique_router
import validate_routing
import validate_techniques

ROOT = Path(__file__).resolve().parents[1]


def stable_hash(value):
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def file_hash(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def unique(values):
    return list(dict.fromkeys(values))


def blocked_result(route, errors, **extra):
    result = {
        "schema_version": "1.0",
        "task_id": route.get("task_id") if isinstance(route, dict) else None,
        "route_input_sha256": stable_hash(route) if isinstance(route, dict) else None,
        "state": "BLOCKED",
        "runtime_state": "BLOCKED",
        "execution_state": "NOT_EXECUTED",
        "errors": errors,
        "limitations": ["Compilation is advisory and does not execute or verify a task."],
    }
    result.update(extra)
    return result


def validate_route_record(route):
    if not isinstance(route, dict):
        return ["route input must be a JSON object"]
    errors = []
    if route.get("state") != "RECOMMENDED":
        errors.append("route state must be RECOMMENDED")
    if route.get("execution_state") != "NOT_EXECUTED":
        errors.append("route execution_state must be NOT_EXECUTED")
    for field in ("task_id", "route_id", "profile_id"):
        if not isinstance(route.get(field), str) or not route[field].strip():
            errors.append(f"{field} must be a non-empty string")
    selected = route.get("selected")
    if not isinstance(selected, dict):
        errors.append("selected must be an object")
    else:
        for field in ("required_techniques", "optional_techniques", "techniques"):
            value = selected.get(field)
            if not isinstance(value, list) or any(not isinstance(item, str) or not item.strip() for item in value):
                errors.append(f"selected.{field} must be an array of non-empty strings")
            elif len(value) != len(set(value)):
                errors.append(f"selected.{field} must not contain duplicates")
        optional_reasons = selected.get("optional_reasons", {})
        if not isinstance(optional_reasons, dict):
            errors.append("selected.optional_reasons must be an object")
    return errors


def expand_technique(card):
    fields = (
        "id", "name", "kind", "category", "status", "implementation_status",
        "purpose", "problem_solved", "applicable_task_types", "trigger_conditions",
        "prerequisites", "when_to_use", "when_not_to_use", "supporting_skills",
        "supporting_tools", "compatible_agents", "inputs", "outputs", "workflow_steps",
        "example_prompt", "invocation", "verification_procedure", "acceptance_criteria",
        "security_considerations", "conflicting_techniques", "fallback_procedure",
        "resource_implications", "source_references",
    )
    return {field: card[field] for field in fields if field in card}


def compile_recipe(route, recipe_id=None, task_type=None, context_request=None, project_root=None):
    errors = validate_route_record(route)
    if errors:
        return blocked_result(route, errors)

    routing_errors, _, _, _ = validate_routing.validate_all()
    technique_errors = validate_techniques.validate_registry(validate_techniques.load_json(validate_techniques.REGISTRY_PATH))
    if routing_errors or technique_errors:
        return blocked_result(route, routing_errors + technique_errors)

    technique_registry = validate_techniques.load_json(validate_techniques.REGISTRY_PATH)
    cards = {card["id"]: card for card in technique_registry["techniques"]}
    profiles = {item["id"]: item for item in validate_routing.load(validate_routing.ROUTING_DIR / "profiles.json")["profiles"]}
    manifests = {item["id"]: item for item in validate_routing.load(validate_routing.ROUTING_DIR / "manifests.json")["manifests"]}
    recipes = validate_routing.load(validate_routing.ROUTING_DIR / "recipes.json")["recipes"]
    manifest = manifests.get(route["route_id"])
    profile = profiles.get(route["profile_id"])
    if manifest is None or profile is None:
        return blocked_result(route, ["route or profile is absent from the validated registry"])
    if manifest["profile"] != profile["id"]:
        return blocked_result(route, ["route and profile identities do not match the registry"])
    if profile["execution_status"] == "BLOCKED":
        return blocked_result(route, [f"Profile {profile['id']} is BLOCKED"])

    selected = route["selected"]
    consistency_errors = []
    if selected["required_techniques"] != manifest["required_techniques"]:
        consistency_errors.append("Route required techniques do not match the current manifest")
    allowed_optional = set(manifest["optional_techniques"])
    if not set(selected["optional_techniques"]).issubset(allowed_optional):
        consistency_errors.append("Route optional techniques are not allowed by the current manifest")
    if len(selected["techniques"]) != len(set(selected["techniques"])):
        consistency_errors.append("Route selected techniques contain duplicates")
    if set(selected["techniques"]) != set(selected["required_techniques"]) | set(selected["optional_techniques"]):
        consistency_errors.append("Route selected technique union is inconsistent")
    for technique_id in selected["optional_techniques"]:
        if not selected.get("optional_reasons", {}).get(technique_id):
            consistency_errors.append(f"Route optional technique {technique_id} has no selection reason")
    for field in ("sequence", "context_scope", "runtime_limits", "retry_limits", "verification_gates", "approval_conditions", "stop_conditions", "fallback"):
        if route.get(field) != manifest[field]:
            consistency_errors.append(f"Route {field} does not match the current manifest")
    if route.get("max_parallel_agents") != profile["max_parallel_agents"]:
        consistency_errors.append("Route agent limit does not match the current profile")
    if consistency_errors:
        return blocked_result(route, consistency_errors)

    candidates = [recipe for recipe in recipes if recipe["route_id"] == manifest["id"]]
    recipe = None
    effective_task_type = task_type if task_type is not None else route.get("task_type")
    if recipe_id is not None:
        recipe = next((item for item in candidates if item["id"] == recipe_id), None)
        if recipe is None:
            return blocked_result(route, [f"Recipe {recipe_id} is not compatible with route {manifest['id']}"], candidate_recipe_ids=[item["id"] for item in candidates])
        if task_type is not None and recipe["task_type"] != task_type:
            return blocked_result(route, [f"Recipe {recipe_id} task_type does not match {task_type}"])
    elif not candidates:
        recipe = None
    elif effective_task_type is not None:
        matching = [item for item in candidates if item["task_type"] == effective_task_type]
        if not matching:
            return blocked_result(route, [f"No recipe for route {manifest['id']} has task_type {effective_task_type}"], candidate_recipe_ids=[item["id"] for item in candidates])
        if len(matching) > 1:
            return blocked_result(route, ["Multiple recipes match the supplied task_type; supply recipe_id explicitly"], candidate_recipe_ids=[item["id"] for item in matching])
        recipe = matching[0]
    elif len(candidates) == 1:
        recipe = candidates[0]
    elif len(candidates) > 1:
        return blocked_result(route, ["Multiple compatible recipes exist; supply recipe_id or task_type explicitly"], candidate_recipe_ids=[item["id"] for item in candidates])

    selected = route["selected"]
    route_required = list(selected["required_techniques"])
    selected_optional = list(selected["optional_techniques"])
    profile_required = list(profile["required_techniques"])
    recipe_techniques = list(recipe["techniques"]) if recipe else []
    route_allowed = set(manifest["required_techniques"]) | set(manifest["optional_techniques"])
    profile_allowed = set(profile["required_techniques"]) | set(profile["optional_techniques"])
    outside_route = sorted(set(recipe_techniques) - route_allowed)
    outside_profile = sorted(set(recipe_techniques) - profile_allowed)
    if outside_route:
        errors.append("Recipe techniques are not allowed by the route: " + ", ".join(outside_route))
    if outside_profile:
        errors.append("Recipe techniques are not allowed by the profile: " + ", ".join(outside_profile))

    required = unique(route_required + profile_required + recipe_techniques)
    optional = [item for item in selected_optional if item not in required]
    incompatible = set(manifest["incompatible_techniques"])
    incompatible_selected = sorted(set(required + optional) & incompatible)
    if incompatible_selected:
        errors.append("Selected techniques are incompatible with the route: " + ", ".join(incompatible_selected))
    unknown = sorted(set(required + optional) - set(cards))
    if unknown:
        errors.append("Selected techniques are absent from the registry: " + ", ".join(unknown))
    conflicts = []
    for left_index, left in enumerate(required):
        for right in required[left_index + 1:]:
            if technique_router.techniques_conflict(cards, left, right):
                conflicts.append([left, right])
    for optional_id in optional:
        conflict = next((item for item in required if technique_router.techniques_conflict(cards, optional_id, item)), None)
        if conflict:
            conflicts.append([optional_id, conflict])
    if conflicts:
        errors.append("Compiled techniques conflict: " + "; ".join("/".join(pair) for pair in conflicts))
    if errors:
        return blocked_result(route, errors)

    context_scope = dict(manifest["context_scope"])
    context_scope["max_files"] = min(manifest["context_scope"]["max_files"], profile["context_limits"]["max_files"])
    context_scope["max_bytes"] = min(manifest["context_scope"]["max_bytes"], profile["context_limits"]["max_bytes"])
    context_scope["include_originals"] = False
    context_scope["enforcement"] = "advisory"
    runtime_limits = {
        "max_iterations": min(manifest["runtime_limits"]["max_iterations"], profile["runtime_limits"]["max_iterations"]),
        "max_runtime_minutes": min(manifest["runtime_limits"]["max_runtime_minutes"], profile["runtime_limits"]["max_runtime_minutes"]),
        "max_cost_usd": min(manifest["runtime_limits"]["max_cost_usd"], profile["runtime_limits"]["max_cost_usd"]),
        "enforcement": "advisory",
    }
    retry_limits = {"max_retries": min(manifest["retry_limits"]["max_retries"], profile["retry_limits"]["max_retries"])}

    sequence = []
    sequenced = set()
    for step in manifest["sequence"]:
        sequence.append({
            "step_id": f"STEP-{len(sequence) + 1:03d}",
            "sequence": len(sequence) + 1,
            "technique_id": step["technique"],
            "agent_id": step["agent"],
            "output": step["output"],
            "source": "route_sequence",
            "execution_state": "NOT_EXECUTED",
        })
        sequenced.add(step["technique"])
    unsequenced = []
    for technique_id in required:
        if technique_id not in sequenced:
            unsequenced.append(technique_id)
            sequence.append({
                "step_id": f"STEP-{len(sequence) + 1:03d}",
                "sequence": len(sequence) + 1,
                "technique_id": technique_id,
                "agent_id": None,
                "output": "Technique contract expanded; no registered route output",
                "source": "profile_or_recipe_requirement",
                "execution_state": "NOT_EXECUTED",
            })

    context_manifest = None
    if context_request is not None:
        context_manifest = context_compiler.compile_context(context_request, root=Path(project_root) if project_root else ROOT.parent)
        if context_manifest["state"] == "BLOCKED":
            return blocked_result(route, context_manifest.get("errors", ["Context compilation was blocked"]), context_manifest=context_manifest)

    warnings = []
    if recipe is None:
        warnings.append("No recipe is registered for this route; compiled a route/profile-only advisory contract.")
    if unsequenced:
        warnings.append("Some required techniques have no registered route sequence step and need human ordering before execution.")

    registry_paths = (
        validate_techniques.REGISTRY_PATH,
        validate_routing.ROUTING_DIR / "profiles.json",
        validate_routing.ROUTING_DIR / "manifests.json",
        validate_routing.ROUTING_DIR / "recipes.json",
    )
    result = {
        "schema_version": "1.0",
        "task_id": route["task_id"],
        "task_type": route.get("task_type"),
        "state": "COMPILED",
        "runtime_state": "COMPILED",
        "execution_state": "NOT_EXECUTED",
        "route_id": manifest["id"],
        "profile_id": profile["id"],
        "profile_name": profile["name"],
        "recipe_id": recipe["id"] if recipe else None,
        "route_input_sha256": route.get("input_sha256"),
        "compilation_input_sha256": stable_hash({"route": route, "recipe_id": recipe_id, "task_type": task_type, "context_request": context_request}),
        "registry_sha256": {path.name: file_hash(path) for path in registry_paths},
        "selected": {
            "required_techniques": required,
            "optional_techniques": optional,
            "optional_reasons": {item: selected.get("optional_reasons", {}).get(item) for item in optional},
            "techniques": required + optional,
            "incompatible_techniques": sorted(incompatible),
            "unsequenced_required_techniques": unsequenced,
        },
        "sequence": sequence,
        "techniques": [expand_technique(cards[item]) for item in required + optional],
        "recipe": recipe,
        "inputs": recipe["inputs"] if recipe else ["Validated RECOMMENDED route record"],
        "outputs": unique((recipe["outputs"] if recipe else []) + [step["output"] for step in sequence]),
        "acceptance_checks": unique((recipe["acceptance_checks"] if recipe else []) + profile["verification_gates"] + manifest["verification_gates"]),
        "failure_handling": recipe["failure_handling"] if recipe else profile["fallback"],
        "owner_roles": recipe["owner_roles"] if recipe else [],
        "context_scope": context_scope,
        "context_manifest": context_manifest,
        "runtime_limits": runtime_limits,
        "retry_limits": retry_limits,
        "verification_gates": unique(manifest["verification_gates"] + profile["verification_gates"]),
        "approval_conditions": unique(manifest["approval_conditions"] + profile["approval_conditions"]),
        "stop_conditions": unique(manifest["stop_conditions"] + profile["stop_conditions"]),
        "fallback": manifest["fallback"],
        "disallowed_actions": unique(profile["disallowed_actions"]),
        "max_parallel_agents": profile["max_parallel_agents"],
        "resources": {"iterations": 0, "runtime_seconds": None, "retries": 0, "token_usage": None, "cost_usd": None, "measurement_status": "unknown"},
        "candidate_recipe_ids": [item["id"] for item in candidates],
        "warnings": warnings,
        "limitations": [
            "Compilation is advisory and is not an attempt, execution or verification.",
            "Technique expansion does not establish tool installation, configuration or session availability.",
            "Context and runtime limits remain advisory until an approved enforcement layer exists.",
            "No token usage, cost, runtime or agent execution is measured by compilation.",
        ],
    }
    return result


def load_json(path):
    if path == "-":
        return json.load(sys.stdin)
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main(argv=None):
    parser = argparse.ArgumentParser(description="Compile a deterministic advisory DevHarness recipe contract")
    parser.add_argument("input", nargs="?", default="-", help="Route JSON file or - for stdin")
    parser.add_argument("--recipe", help="Explicit compatible recipe ID")
    parser.add_argument("--task-type", help="Select a unique recipe by task type")
    parser.add_argument("--context", help="Optional context request JSON file")
    parser.add_argument("--project", default=".", help="Project root used for an optional context request")
    parser.add_argument("--output", help="Write the compiled contract to this path")
    args = parser.parse_args(argv)
    try:
        route = load_json(args.input)
        context_request = load_json(args.context) if args.context else None
        result = compile_recipe(route, args.recipe, args.task_type, context_request, args.project)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Recipe compile input error: {exc}", file=sys.stderr)
        return 1
    text = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        try:
            Path(args.output).write_text(text, encoding="utf-8")
        except OSError as exc:
            print(f"Recipe compile output error: {exc}", file=sys.stderr)
            return 1
    print(text, end="")
    return {"COMPILED": 0, "BLOCKED": 3}.get(result["state"], 1)


if __name__ == "__main__":
    sys.exit(main())
