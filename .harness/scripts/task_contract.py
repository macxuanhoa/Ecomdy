import json
import re
import sys
from pathlib import Path

import validate_execution
import validate_routing
import validate_techniques
from context_compiler import normalize_rule

ROOT = Path(__file__).resolve().parents[1]
SHELL_EXECUTABLES = {"sh", "bash", "zsh", "cmd", "cmd.exe", "powershell", "powershell.exe", "pwsh", "pwsh.exe"}
EXECUTABLE_ALLOWLIST = {"python", "python.exe", "python3", "python3.exe", "pytest", "pytest.exe", "gitleaks", "gitleaks.exe"}
PYTHON_MODULE_ALLOWLIST = {"unittest", "pytest", "compileall"}
GITLEAKS_REPORT_OPTIONS = {"--report-path", "--report", "--output", "-o"}
COMMAND_KINDS = {"test", "validation", "secret_scan"}
DEFAULT_DENY_PATHS = [
    ".git/**",
    ".harness/state/**",
    ".harness/cache/**",
    ".harness/logs/**",
    "docs/00-original/**",
    ".harness/docs/00-original/**",
    ".env",
    ".env.*",
    "*.pem",
    "*.key",
]
TASK_REQUIRED_FIELDS = {
    "schema_version", "task_id", "trace_id", "objective", "acceptance_criteria",
    "route_id", "profile_id", "recipe_id", "verification_technique_id",
    "scope", "commands", "budgets", "approvals",
}
TASK_FIELDS = TASK_REQUIRED_FIELDS | {"evidence_dir", "secret_scan_required"}
SCOPE_FIELDS = {"allow_paths", "deny_paths", "base_commit", "max_changed_files", "max_changed_bytes"}
COMMAND_FIELDS = {"id", "kind", "argv", "criteria", "timeout_seconds", "max_output_bytes"}
BUDGET_FIELDS = {"max_iterations", "max_runtime_minutes", "max_cost_usd", "max_retries"}


def load_json(path):
    if path == "-":
        return json.load(sys.stdin)
    return json.loads(Path(path).read_text(encoding="utf-8"))


def stable_hash(value):
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    import hashlib
    return hashlib.sha256(payload).hexdigest()


def file_hash(path):
    import hashlib
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def check_fields(value, allowed, label, errors, required=None):
    if not isinstance(value, dict):
        errors.append(f"{label} must be an object")
        return False
    required = allowed if required is None else required
    missing = sorted(required - set(value))
    extra = sorted(set(value) - allowed)
    if missing:
        errors.append(f"{label} missing fields: {', '.join(missing)}")
    if extra:
        errors.append(f"{label} has unknown fields: {', '.join(extra)}")
    return True


def check_string_array(value, label, errors, allow_empty=False):
    if not isinstance(value, list) or (not allow_empty and not value):
        errors.append(f"{label} must be an array of non-empty strings")
        return False
    if any(not isinstance(item, str) or not item.strip() for item in value):
        errors.append(f"{label} must contain only non-empty strings")
        return False
    return True


def check_positive_int(value, label, errors, maximum=None):
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        errors.append(f"{label} must be a positive integer")
        return False
    if maximum is not None and value > maximum:
        errors.append(f"{label} must not exceed {maximum}")
        return False
    return True


def validate_argv(argv, label, errors):
    if not check_string_array(argv, f"{label}.argv", errors):
        return
    if any("\x00" in item for item in argv):
        errors.append(f"{label}.argv must not contain NUL bytes")
        return
    for arg in argv[1:]:
        if Path(arg).is_absolute() or re.search(r"(^|[\\/=])\.\.([\\/]|$)", arg) or "://" in arg:
            errors.append(f"{label}.argv must not reference absolute, parent-traversal or URL paths")
    executable = Path(argv[0]).name.lower()
    if executable in SHELL_EXECUTABLES:
        errors.append(f"{label}.argv must not invoke a shell")
        return
    if executable not in EXECUTABLE_ALLOWLIST:
        errors.append(f"{label}.argv executable is not allowlisted: {executable}")
        return
    if executable.startswith("python"):
        if any(arg in {"-c", "--command"} for arg in argv[1:]):
            errors.append(f"{label}.argv must not execute inline Python code")
        if "-m" in argv[1:]:
            index = argv.index("-m", 1)
            module = argv[index + 1] if index + 1 < len(argv) else None
            if module not in PYTHON_MODULE_ALLOWLIST:
                errors.append(f"{label}.argv Python module is not allowlisted: {module}")
    elif executable in {"gitleaks", "gitleaks.exe"}:
        if any(arg in GITLEAKS_REPORT_OPTIONS or any(arg.startswith(option + "=") for option in GITLEAKS_REPORT_OPTIONS) for arg in argv[1:]):
            errors.append(f"{label}.argv Gitleaks report-file options are not allowed; capture redacted stdout evidence instead")


def validate_task_contract(contract):
    errors = []
    if not check_fields(contract, TASK_FIELDS, "task", errors, required=TASK_REQUIRED_FIELDS):
        return errors
    if contract.get("schema_version") != "1.0":
        errors.append("task.schema_version must be 1.0")
    for field in ("task_id", "objective", "route_id", "profile_id", "verification_technique_id"):
        if not isinstance(contract.get(field), str) or not contract[field].strip():
            errors.append(f"task.{field} must be a non-empty string")
    if not re.fullmatch(r"TRACE-[0-9]{3}", str(contract.get("trace_id"))):
        errors.append("task.trace_id must match TRACE-NNN")
    recipe_id = contract.get("recipe_id")
    if recipe_id is not None and (not isinstance(recipe_id, str) or not re.fullmatch(r"RECIPE-[0-9]{3}", recipe_id)):
        errors.append("task.recipe_id must be null or match RECIPE-NNN")
    check_string_array(contract.get("acceptance_criteria"), "task.acceptance_criteria", errors)
    check_string_array(contract.get("approvals"), "task.approvals", errors, allow_empty=True)
    if "secret_scan_required" in contract and not isinstance(contract["secret_scan_required"], bool):
        errors.append("task.secret_scan_required must be a boolean")

    evidence_dir = contract.get("evidence_dir", ".harness/state/evidence")
    normalized_evidence = normalize_rule(evidence_dir, "task.evidence_dir", errors)
    if normalized_evidence is not None and not normalized_evidence.startswith(".harness/state/"):
        errors.append("task.evidence_dir must be a repository-relative directory under .harness/state/")

    scope = contract.get("scope")
    if check_fields(scope, SCOPE_FIELDS, "task.scope", errors, required={"allow_paths", "max_changed_files", "max_changed_bytes"}):
        allow_paths = scope.get("allow_paths")
        if check_string_array(allow_paths, "task.scope.allow_paths", errors):
            for index, rule in enumerate(allow_paths):
                normalize_rule(rule, f"task.scope.allow_paths[{index}]", errors)
        deny_paths = scope.get("deny_paths", DEFAULT_DENY_PATHS)
        if check_string_array(deny_paths, "task.scope.deny_paths", errors, allow_empty=True):
            for index, rule in enumerate(deny_paths):
                normalize_rule(rule, f"task.scope.deny_paths[{index}]", errors)
        base_commit = scope.get("base_commit")
        if base_commit is not None and (not isinstance(base_commit, str) or not re.fullmatch(r"[0-9a-fA-F]{7,64}", base_commit)):
            errors.append("task.scope.base_commit must be null or a hexadecimal commit ID")
        check_positive_int(scope.get("max_changed_files"), "task.scope.max_changed_files", errors)
        check_positive_int(scope.get("max_changed_bytes"), "task.scope.max_changed_bytes", errors)

    budgets = contract.get("budgets")
    if check_fields(budgets, BUDGET_FIELDS, "task.budgets", errors):
        check_positive_int(budgets.get("max_iterations"), "task.budgets.max_iterations", errors)
        check_positive_int(budgets.get("max_runtime_minutes"), "task.budgets.max_runtime_minutes", errors)
        for field in ("max_cost_usd", "max_retries"):
            value = budgets.get(field)
            if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
                errors.append(f"task.budgets.{field} must be a non-negative number")
        if budgets.get("max_iterations") != 1:
            errors.append("task.budgets.max_iterations must remain 1 for controlled verification")
        if budgets.get("max_retries") != 0:
            errors.append("task.budgets.max_retries must remain 0 for controlled verification")
        if budgets.get("max_cost_usd") != 0:
            errors.append("task.budgets.max_cost_usd must remain 0; paid calls are not authorized")

    commands = contract.get("commands")
    command_ids = []
    covered_criteria = set()
    secret_scan_present = False
    total_timeout = 0
    if not isinstance(commands, list) or not commands:
        errors.append("task.commands must be a non-empty array")
        commands = []
    for index, command in enumerate(commands):
        label = f"task.commands[{index}]"
        if not check_fields(command, COMMAND_FIELDS, label, errors):
            continue
        command_id = command.get("id")
        if not isinstance(command_id, str) or not re.fullmatch(r"CHECK-[0-9]{3}", command_id):
            errors.append(f"{label}.id must match CHECK-NNN")
        else:
            command_ids.append(command_id)
        if command.get("kind") not in COMMAND_KINDS:
            errors.append(f"{label}.kind is invalid")
        validate_argv(command.get("argv"), label, errors)
        criteria = command.get("criteria")
        if check_string_array(criteria, f"{label}.criteria", errors):
            accepted = set(contract.get("acceptance_criteria", [])) if isinstance(contract.get("acceptance_criteria"), list) else set()
            for criterion in criteria:
                if criterion not in accepted:
                    errors.append(f"{label}.criteria contains an unknown acceptance criterion")
                covered_criteria.add(criterion)
        timeout = command.get("timeout_seconds")
        if check_positive_int(timeout, f"{label}.timeout_seconds", errors, maximum=300):
            total_timeout += timeout
        check_positive_int(command.get("max_output_bytes"), f"{label}.max_output_bytes", errors, maximum=262144)
        argv = command.get("argv")
        if command.get("kind") == "secret_scan":
            secret_scan_present = True
            executable = Path(argv[0]).name.lower() if isinstance(argv, list) and argv and isinstance(argv[0], str) else ""
            if executable not in {"gitleaks", "gitleaks.exe"}:
                errors.append(f"{label} secret_scan must use the reviewed Gitleaks executable")
            if not isinstance(argv, list) or "--redact" not in argv:
                errors.append(f"{label} secret_scan must include --redact")
    if len(command_ids) != len(set(command_ids)):
        errors.append("task.commands IDs must be unique")
    accepted_criteria = set(contract.get("acceptance_criteria", [])) if isinstance(contract.get("acceptance_criteria"), list) else set()
    if accepted_criteria - covered_criteria:
        errors.append("Every acceptance criterion must be covered by a verification command: " + ", ".join(sorted(accepted_criteria - covered_criteria)))
    if contract.get("secret_scan_required") and not secret_scan_present:
        errors.append("task.secret_scan_required needs a secret_scan command")
    if isinstance(budgets, dict) and isinstance(budgets.get("max_runtime_minutes"), int) and total_timeout > budgets["max_runtime_minutes"] * 60:
        errors.append("task command timeouts exceed task.budgets.max_runtime_minutes")

    techniques = validate_techniques.load_json(validate_techniques.REGISTRY_PATH)
    technique_ids = {item["id"] for item in techniques["techniques"]}
    manifests = validate_routing.load(validate_routing.ROUTING_DIR / "manifests.json")["manifests"]
    profiles = validate_routing.load(validate_routing.ROUTING_DIR / "profiles.json")["profiles"]
    recipes = validate_routing.load(validate_routing.ROUTING_DIR / "recipes.json")["recipes"]
    route_profiles = {item["id"]: item["profile"] for item in manifests}
    profile_ids = {item["id"] for item in profiles}
    recipe_profiles = {item["id"]: item["profile_id"] for item in recipes}
    validate_execution.check_route(contract, technique_ids, route_profiles, profile_ids, recipe_profiles, "task", errors)
    if contract.get("verification_technique_id") not in technique_ids:
        errors.append("task.verification_technique_id is unknown")
    return errors
