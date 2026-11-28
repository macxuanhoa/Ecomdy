import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "registry" / "techniques.json"
SCHEMA_PATH = ROOT / "schemas" / "technique.schema.json"

KINDS = {
    "methodology",
    "design_pattern",
    "agent_pattern",
    "skill",
    "tool",
    "mcp_server",
    "framework",
    "script",
    "workflow",
    "policy",
}
STATUSES = {
    "AVAILABLE IN REGISTRY",
    "RESEARCHED",
    "APPROVED",
    "INSTALLED",
    "CONFIGURED",
    "AVAILABLE IN SESSION",
    "SMOKE TESTED",
    "INTEGRATED",
    "DEFERRED",
    "REJECTED",
    "BLOCKED",
}
CATEGORIES = set("ABCDEFGH")
EXECUTABLE_KINDS = {"tool", "mcp_server", "framework", "script"}
ARRAY_FIELDS = {
    "when_to_use",
    "when_not_to_use",
    "trigger_conditions",
    "prerequisites",
    "inputs",
    "outputs",
    "applicable_task_types",
    "catalogue_aliases",
    "supporting_skills",
    "supporting_tools",
    "compatible_agents",
    "workflow_steps",
    "acceptance_criteria",
    "verification_procedure",
    "security_considerations",
    "conflicting_techniques",
    "alternative_techniques",
    "source_references",
}
STRING_FIELDS = {
    "id",
    "name",
    "description",
    "purpose",
    "problem_solved",
    "example_prompt",
    "ecomdy_example",
    "fallback_procedure",
    "implementation_status",
}
IMPLEMENTATION_STATUSES = {
    "documented_advisory",
    "manual_instruction_exists",
    "candidate_uninstalled",
    "implemented_verified",
}


def load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError(f"Missing file: {path.relative_to(ROOT)}")
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path.relative_to(ROOT)}: {exc}")


def validate_registry(data):
    errors = []
    if not isinstance(data, dict):
        return ["Registry root must be an object"]

    required_top = {"schema_version", "registry_version", "status", "baseline_note", "techniques"}
    missing_top = sorted(required_top - set(data))
    if missing_top:
        errors.append("Registry missing fields: " + ", ".join(missing_top))
    extra_top = sorted(set(data) - required_top)
    if extra_top:
        errors.append("Registry has unknown fields: " + ", ".join(extra_top))

    if data.get("schema_version") != "1.0":
        errors.append("schema_version must be 1.0")
    if not isinstance(data.get("registry_version"), str) or not data.get("registry_version", "").strip():
        errors.append("registry_version must be a non-empty string")
    if data.get("status") != "AVAILABLE IN REGISTRY":
        errors.append("Registry status must be AVAILABLE IN REGISTRY")
    if not isinstance(data.get("baseline_note"), str) or not data.get("baseline_note", "").strip():
        errors.append("baseline_note must explain registry provenance and gaps")

    techniques = data.get("techniques")
    if not isinstance(techniques, list) or not techniques:
        return errors + ["techniques must be a non-empty array"]

    schema = load_json(SCHEMA_PATH)
    required_card = set(schema["$defs"]["technique"]["required"])
    allowed_card = set(schema["$defs"]["technique"]["properties"])

    ids = []
    for index, card in enumerate(techniques):
        label = f"techniques[{index}]"
        if not isinstance(card, dict):
            errors.append(f"{label} must be an object")
            continue
        missing = sorted(required_card - set(card))
        extra = sorted(set(card) - allowed_card)
        if missing:
            errors.append(f"{label} missing fields: {', '.join(missing)}")
        if extra:
            errors.append(f"{label} has unknown fields: {', '.join(extra)}")

        technique_id = card.get("id")
        if isinstance(technique_id, str):
            ids.append(technique_id)
            if not re.fullmatch(r"TECH-[0-9]{3}", technique_id):
                errors.append(f"{label} has invalid ID: {technique_id}")
        else:
            errors.append(f"{label}.id must be a string")

        for field in STRING_FIELDS:
            value = card.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{label}.{field} must be a non-empty string")

        category = card.get("category")
        if not isinstance(category, dict):
            errors.append(f"{label}.category must be an object")
        else:
            if category.get("id") not in CATEGORIES:
                errors.append(f"{label}.category.id must be A-H")
            if not isinstance(category.get("name"), str) or not category.get("name", "").strip():
                errors.append(f"{label}.category.name must be a non-empty string")
            if set(category) - {"id", "name"}:
                errors.append(f"{label}.category has unknown fields")

        if card.get("kind") not in KINDS:
            errors.append(f"{label}.kind is invalid")
        if card.get("status") not in STATUSES:
            errors.append(f"{label}.status is invalid")
        if card.get("implementation_status") not in IMPLEMENTATION_STATUSES:
            errors.append(f"{label}.implementation_status is invalid")

        for field in ARRAY_FIELDS:
            value = card.get(field)
            if not isinstance(value, list) or any(not isinstance(item, str) or not item.strip() for item in value):
                errors.append(f"{label}.{field} must be an array of non-empty strings")

        agents = card.get("compatible_agents", [])
        if isinstance(agents, list):
            for agent in agents:
                if not isinstance(agent, str) or not re.fullmatch(r"A[0-9]{2}", agent):
                    errors.append(f"{label}.compatible_agents has invalid agent ID: {agent!r}")

        aliases = card.get("catalogue_aliases", [])
        if isinstance(aliases, list):
            for alias in aliases:
                if not isinstance(alias, str) or not re.fullmatch(r"[A-H][0-9]{2}", alias):
                    errors.append(f"{label}.catalogue_aliases has invalid source ID: {alias!r}")

        invocation = card.get("invocation")
        if invocation is not None:
            if card.get("kind") not in EXECUTABLE_KINDS:
                errors.append(f"{label} has invocation but kind is not executable")
            if not isinstance(invocation, dict):
                errors.append(f"{label}.invocation must be null or an object")
            else:
                if set(invocation) != {"argv", "cwd", "verification_status"}:
                    errors.append(f"{label}.invocation fields are invalid")
                argv = invocation.get("argv")
                if not isinstance(argv, list) or not argv or any(not isinstance(item, str) or not item for item in argv):
                    errors.append(f"{label}.invocation.argv must be a non-empty string array")
                if not isinstance(invocation.get("cwd"), str) or not invocation.get("cwd", "").strip():
                    errors.append(f"{label}.invocation.cwd must be a non-empty string")
                if invocation.get("verification_status") not in {"SMOKE TESTED", "VERIFIED"}:
                    errors.append(f"{label}.invocation.verification_status is invalid")

        resources = card.get("resource_implications")
        if not isinstance(resources, dict):
            errors.append(f"{label}.resource_implications must be an object")
        else:
            expected = {"relative_token_cost", "relative_runtime", "network_required", "paid_service_required", "measurement_status"}
            if set(resources) != expected:
                errors.append(f"{label}.resource_implications fields are invalid")
            if resources.get("relative_token_cost") not in {"low", "medium", "high", "unknown"}:
                errors.append(f"{label}.relative_token_cost is invalid")
            if resources.get("relative_runtime") not in {"low", "medium", "high", "unknown"}:
                errors.append(f"{label}.relative_runtime is invalid")
            if not isinstance(resources.get("network_required"), bool):
                errors.append(f"{label}.network_required must be boolean")
            if not isinstance(resources.get("paid_service_required"), bool):
                errors.append(f"{label}.paid_service_required must be boolean")
            if resources.get("measurement_status") != "not_measured":
                errors.append(f"{label}.measurement_status must be not_measured")

    duplicates = sorted({item for item in ids if ids.count(item) > 1})
    if duplicates:
        errors.append("Duplicate technique IDs: " + ", ".join(duplicates))
    expected_ids = [f"TECH-{number:03d}" for number in range(1, len(ids) + 1)]
    if sorted(ids) != expected_ids:
        errors.append("Technique IDs must be contiguous from TECH-001 without gaps")

    aliases = [alias for card in techniques if isinstance(card, dict) and isinstance(card.get("catalogue_aliases"), list) for alias in card["catalogue_aliases"]]
    duplicate_aliases = sorted({item for item in aliases if aliases.count(item) > 1})
    if duplicate_aliases:
        errors.append("Duplicate catalogue aliases: " + ", ".join(duplicate_aliases))

    id_set = set(ids)
    for card in techniques:
        if not isinstance(card, dict):
            continue
        technique_id = card.get("id", "<unknown>")
        for field in ("conflicting_techniques", "alternative_techniques"):
            refs = card.get(field, [])
            if isinstance(refs, list):
                for ref in refs:
                    if ref not in id_set:
                        errors.append(f"{technique_id}.{field} references unknown ID: {ref}")

    covered = {card.get("category", {}).get("id") for card in techniques if isinstance(card, dict) and isinstance(card.get("category"), dict)}
    if covered != CATEGORIES:
        errors.append("Registry must cover categories A-H; missing: " + ", ".join(sorted(CATEGORIES - covered)))

    return errors


def main():
    try:
        data = load_json(REGISTRY_PATH)
        errors = validate_registry(data)
    except ValueError as exc:
        errors = [str(exc)]
    if errors:
        print("Technique registry: FAIL")
        for error in errors:
            print("-", error)
        return 1
    print(f"Technique registry: PASS ({len(data['techniques'])} techniques, categories A-H)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
