import json
import re
import sys
from datetime import datetime
from pathlib import Path

import validate_routing
import validate_techniques

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "execution.schema.json"
TRACE_EXAMPLE = ROOT / "templates" / "execution-trace.example.json"
CHECKPOINT_EXAMPLE = ROOT / "templates" / "checkpoint.example.json"

TRACE_FIELDS = {
    "schema_version", "trace_id", "task_id", "status", "created_at", "updated_at",
    "route_id", "profile_id", "recipe_id", "repository", "context", "steps",
    "verification", "resources", "budgets", "approvals", "blockers", "artifacts",
    "limitations", "next_action",
}
CHECKPOINT_FIELDS = {
    "schema_version", "checkpoint_id", "created_at", "task_id", "trace_id", "status",
    "route_id", "profile_id", "recipe_id", "repository", "completed_step_ids",
    "pending_step_ids", "blockers", "evidence_paths", "next_action", "resume_conditions",
}
STEP_FIELDS = {
    "step_id", "sequence", "technique_id", "agent_id", "status", "timestamps",
    "inputs", "outputs", "commands", "notes",
}
COMMAND_FIELDS = {
    "argv", "cwd", "status", "exit_code", "started_at", "finished_at", "output_excerpt",
    "output_truncated", "output_bytes", "evidence_path",
}
STEP_STATUSES = {"SELECTED", "ATTEMPTED", "EXECUTED", "VERIFIED", "SKIPPED", "BLOCKED", "FAILED"}
COMMAND_STATUSES = {"NOT_RUN", "PASS", "FAIL", "TIMEOUT", "BLOCKED"}
SHELL_EXECUTABLES = {"sh", "bash", "zsh", "cmd", "cmd.exe", "powershell", "powershell.exe", "pwsh", "pwsh.exe"}
TRACE_STATUSES = {"IN_PROGRESS", "COMPLETED", "BLOCKED", "FAILED", "ABORTED"}
CHECKPOINT_STATUSES = {"READY_TO_RESUME", "BLOCKED", "COMPLETE"}


def load(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError(f"Missing file: {path}")
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path}: {exc}")


def check_fields(item, required, label, errors):
    if not isinstance(item, dict):
        errors.append(f"{label} must be an object")
        return False
    missing = sorted(required - set(item))
    extra = sorted(set(item) - required)
    if missing:
        errors.append(f"{label} missing fields: {', '.join(missing)}")
    if extra:
        errors.append(f"{label} has unknown fields: {', '.join(extra)}")
    return True


def check_string_array(value, label, errors, allow_empty=True):
    if not isinstance(value, list) or (not allow_empty and not value):
        errors.append(f"{label} must be {'a non-empty' if not allow_empty else 'an'} array of non-empty strings")
        return
    if any(not isinstance(entry, str) or not entry.strip() for entry in value):
        errors.append(f"{label} must contain only non-empty strings")


def check_timestamp(value, label, errors, allow_null=False):
    if value is None and allow_null:
        return
    if not isinstance(value, str):
        errors.append(f"{label} must be an ISO-8601 timestamp")
        return
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        errors.append(f"{label} must be an ISO-8601 timestamp")


def check_repository(repository, label, errors):
    fields = {"branch", "head_commit", "base_commit", "changed_paths", "untracked_paths"}
    if not check_fields(repository, fields, label, errors):
        return
    for field in ("branch", "head_commit", "base_commit"):
        value = repository[field]
        if value is not None and (not isinstance(value, str) or not value.strip()):
            errors.append(f"{label}.{field} must be a non-empty string or null")
    for field in ("changed_paths", "untracked_paths"):
        check_string_array(repository[field], f"{label}.{field}", errors)


def check_context(context, label, errors):
    fields = {"manifest_path", "input_hashes", "excluded_paths", "limits", "enforcement"}
    if not check_fields(context, fields, label, errors):
        return
    manifest_path = context["manifest_path"]
    if manifest_path is not None and (not isinstance(manifest_path, str) or not manifest_path.strip()):
        errors.append(f"{label}.manifest_path must be a non-empty string or null")
    for field in ("input_hashes", "excluded_paths"):
        check_string_array(context[field], f"{label}.{field}", errors)
    if context["enforcement"] != "advisory":
        errors.append(f"{label}.enforcement must remain advisory")
    limits = context["limits"]
    if not check_fields(limits, {"max_files", "max_bytes"}, f"{label}.limits", errors):
        return
    for field in ("max_files", "max_bytes"):
        if not isinstance(limits[field], int) or isinstance(limits[field], bool) or limits[field] < 1:
            errors.append(f"{label}.limits.{field} must be a positive integer")


def check_command(command, label, errors):
    if not check_fields(command, COMMAND_FIELDS, label, errors):
        return
    check_string_array(command["argv"], f"{label}.argv", errors, allow_empty=False)
    argv = command["argv"]
    if isinstance(argv, list) and argv and all(isinstance(arg, str) for arg in argv):
        executable = Path(argv[0]).name.lower()
        if executable in SHELL_EXECUTABLES and any(arg.lower() in {"-c", "/c", "-command"} for arg in argv[1:]):
            errors.append(f"{label} must not wrap commands in a shell")
    if not isinstance(command["cwd"], str) or not command["cwd"].strip():
        errors.append(f"{label}.cwd must be a non-empty string")
    status = command["status"]
    if status not in COMMAND_STATUSES:
        errors.append(f"{label}.status is invalid")
        return
    exit_code = command["exit_code"]
    if status == "NOT_RUN":
        if exit_code is not None or command["started_at"] is not None or command["finished_at"] is not None:
            errors.append(f"{label} NOT_RUN cannot contain an exit code or execution timestamps")
    elif status == "TIMEOUT":
        if exit_code is not None:
            errors.append(f"{label} TIMEOUT must have null exit_code")
        check_timestamp(command["started_at"], f"{label}.started_at", errors)
        check_timestamp(command["finished_at"], f"{label}.finished_at", errors)
    elif status == "BLOCKED":
        if exit_code is not None or command["started_at"] is not None or command["finished_at"] is not None:
            errors.append(f"{label} BLOCKED cannot contain an exit code or execution timestamps")
    else:
        if not isinstance(exit_code, int) or isinstance(exit_code, bool):
            errors.append(f"{label} {status} must have an integer exit_code")
        elif status == "PASS" and exit_code != 0:
            errors.append(f"{label} PASS requires exit_code 0")
        elif status == "FAIL" and exit_code == 0:
            errors.append(f"{label} FAIL requires a non-zero exit_code")
        check_timestamp(command["started_at"], f"{label}.started_at", errors)
        check_timestamp(command["finished_at"], f"{label}.finished_at", errors)
    evidence_path = command["evidence_path"]
    if evidence_path is not None and (not isinstance(evidence_path, str) or not evidence_path.strip()):
        errors.append(f"{label}.evidence_path must be a non-empty string or null")
    if not isinstance(command["output_excerpt"], str):
        errors.append(f"{label}.output_excerpt must be a string")
    if not isinstance(command["output_truncated"], bool):
        errors.append(f"{label}.output_truncated must be a boolean")
    output_bytes = command["output_bytes"]
    if output_bytes is not None and (not isinstance(output_bytes, int) or isinstance(output_bytes, bool) or output_bytes < 0):
        errors.append(f"{label}.output_bytes must be a non-negative integer or null")


def check_step(step, label, errors):
    if not check_fields(step, STEP_FIELDS, label, errors):
        return
    if not re.fullmatch(r"STEP-[0-9]{3}", str(step["step_id"])):
        errors.append(f"{label}.step_id is invalid")
    if not isinstance(step["sequence"], int) or isinstance(step["sequence"], bool) or step["sequence"] < 1:
        errors.append(f"{label}.sequence must be a positive integer")
    if not re.fullmatch(r"TECH-[0-9]{3}", str(step["technique_id"])):
        errors.append(f"{label}.technique_id is invalid")
    agent_id = step["agent_id"]
    if agent_id is not None and not re.fullmatch(r"A[0-9]{2}", str(agent_id)):
        errors.append(f"{label}.agent_id is invalid")
    status = step["status"]
    if status not in STEP_STATUSES:
        errors.append(f"{label}.status is invalid")
        return
    timestamps = step["timestamps"]
    if not check_fields(timestamps, {"selected_at", "attempted_at", "executed_at", "verified_at"}, f"{label}.timestamps", errors):
        return
    for field, value in timestamps.items():
        check_timestamp(value, f"{label}.timestamps.{field}", errors, allow_null=True)
    for field in ("inputs", "outputs"):
        check_string_array(step[field], f"{label}.{field}", errors)
    if not isinstance(step["commands"], list):
        errors.append(f"{label}.commands must be an array")
    else:
        for index, command in enumerate(step["commands"]):
            check_command(command, f"{label}.commands[{index}]", errors)
    if not isinstance(step["notes"], str):
        errors.append(f"{label}.notes must be a string")

    required_times = {
        "SELECTED": ("selected_at",),
        "ATTEMPTED": ("selected_at", "attempted_at"),
        "EXECUTED": ("selected_at", "attempted_at", "executed_at"),
        "VERIFIED": ("selected_at", "attempted_at", "executed_at", "verified_at"),
        "SKIPPED": ("selected_at",),
        "BLOCKED": ("selected_at",),
        "FAILED": ("selected_at", "attempted_at"),
    }
    forbidden_times = {
        "SELECTED": ("attempted_at", "executed_at", "verified_at"),
        "ATTEMPTED": ("executed_at", "verified_at"),
        "EXECUTED": ("verified_at",),
        "VERIFIED": (),
        "SKIPPED": ("attempted_at", "executed_at", "verified_at"),
        "BLOCKED": ("executed_at", "verified_at"),
        "FAILED": ("verified_at",),
    }
    for field in required_times[status]:
        if timestamps[field] is None:
            errors.append(f"{label} {status} requires {field}")
    for field in forbidden_times[status]:
        if timestamps[field] is not None:
            errors.append(f"{label} {status} cannot have {field}")
    if status == "VERIFIED" and not step["outputs"] and not any(command.get("status") == "PASS" for command in step["commands"]):
        errors.append(f"{label} VERIFIED requires output or PASS command evidence")


def check_route(data, technique_ids, route_profiles, profile_ids, recipe_profiles, label, errors):
    route_id = data.get("route_id")
    profile_id = data.get("profile_id")
    recipe_id = data.get("recipe_id")
    if route_id not in route_profiles:
        errors.append(f"{label}.route_id is unknown")
    elif profile_id != route_profiles[route_id]:
        errors.append(f"{label}.profile_id does not match its route")
    if profile_id not in profile_ids:
        errors.append(f"{label}.profile_id is unknown")
    if recipe_id is not None:
        if recipe_id not in recipe_profiles:
            errors.append(f"{label}.recipe_id is unknown")
        elif recipe_profiles[recipe_id] != profile_id:
            errors.append(f"{label}.recipe_id does not match its profile")


def check_resources(resources, label, errors):
    fields = {"iterations", "runtime_seconds", "retries", "token_usage", "cost_usd", "measurement_status"}
    if not check_fields(resources, fields, label, errors):
        return
    for field in ("iterations", "retries"):
        if not isinstance(resources[field], int) or isinstance(resources[field], bool) or resources[field] < 0:
            errors.append(f"{label}.{field} must be a non-negative integer")
    for field in ("runtime_seconds", "cost_usd"):
        value = resources[field]
        if value is not None and (not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0):
            errors.append(f"{label}.{field} must be a non-negative number or null")
    token_usage = resources["token_usage"]
    if token_usage is not None:
        if not check_fields(token_usage, {"input", "output", "total"}, f"{label}.token_usage", errors):
            return
        for field, value in token_usage.items():
            if value is not None and (not isinstance(value, int) or isinstance(value, bool) or value < 0):
                errors.append(f"{label}.token_usage.{field} must be a non-negative integer or null")
    if resources["measurement_status"] not in {"unknown", "partial", "measured"}:
        errors.append(f"{label}.measurement_status is invalid")
    elif resources["measurement_status"] == "unknown" and any(resources[field] is not None for field in ("runtime_seconds", "token_usage", "cost_usd")):
        errors.append(f"{label} unknown measurement cannot contain runtime, token or cost values")


def check_budgets(budgets, label, errors):
    fields = {"max_iterations", "max_runtime_minutes", "max_cost_usd", "max_retries", "enforcement"}
    if not check_fields(budgets, fields, label, errors):
        return
    for field in ("max_iterations", "max_runtime_minutes"):
        if not isinstance(budgets[field], int) or isinstance(budgets[field], bool) or budgets[field] < 1:
            errors.append(f"{label}.{field} must be a positive integer")
    if not isinstance(budgets["max_retries"], int) or isinstance(budgets["max_retries"], bool) or budgets["max_retries"] < 0:
        errors.append(f"{label}.max_retries must be a non-negative integer")
    if not isinstance(budgets["max_cost_usd"], (int, float)) or isinstance(budgets["max_cost_usd"], bool) or budgets["max_cost_usd"] < 0:
        errors.append(f"{label}.max_cost_usd must be a non-negative number")
    if budgets["enforcement"] != "advisory":
        errors.append(f"{label}.enforcement must remain advisory until runtime controls are verified")


def validate_trace(data, technique_ids, route_profiles, profile_ids, recipe_profiles):
    errors = []
    label = "trace"
    if not check_fields(data, TRACE_FIELDS, label, errors):
        return errors
    if data["schema_version"] != "1.0":
        errors.append("trace.schema_version must be 1.0")
    if not re.fullmatch(r"TRACE-[0-9]{3}", str(data["trace_id"])):
        errors.append("trace.trace_id is invalid")
    if not isinstance(data["task_id"], str) or not data["task_id"].strip():
        errors.append("trace.task_id must be a non-empty string")
    if data["status"] not in TRACE_STATUSES:
        errors.append("trace.status is invalid")
    check_timestamp(data["created_at"], "trace.created_at", errors)
    check_timestamp(data["updated_at"], "trace.updated_at", errors)
    check_route(data, technique_ids, route_profiles, profile_ids, recipe_profiles, label, errors)
    check_repository(data["repository"], "trace.repository", errors)
    check_context(data["context"], "trace.context", errors)
    steps = data["steps"]
    if not isinstance(steps, list):
        errors.append("trace.steps must be an array")
        steps = []
    sequences = []
    step_ids = []
    for index, step in enumerate(steps):
        check_step(step, f"trace.steps[{index}]", errors)
        if isinstance(step, dict):
            sequences.append(step.get("sequence"))
            step_ids.append(step.get("step_id"))
            if step.get("technique_id") not in technique_ids:
                errors.append(f"trace.steps[{index}].technique_id is unknown")
    if sequences != sorted(sequences) or len(sequences) != len(set(sequences)):
        errors.append("trace.steps sequences must be unique and ascending")
    if sequences and sequences != list(range(1, len(sequences) + 1)):
        errors.append("trace.steps sequences must be contiguous from 1")
    if len(step_ids) != len(set(step_ids)):
        errors.append("trace.steps step IDs must be unique")

    verification = data["verification"]
    if not check_fields(verification, {"acceptance_criteria", "results"}, "trace.verification", errors):
        return errors
    check_string_array(verification["acceptance_criteria"], "trace.verification.acceptance_criteria", errors, allow_empty=False)
    results = verification["results"]
    if not isinstance(results, list):
        errors.append("trace.verification.results must be an array")
        results = []
    for index, result in enumerate(results):
        result_label = f"trace.verification.results[{index}]"
        if not check_fields(result, {"criterion", "status", "evidence"}, result_label, errors):
            continue
        if not isinstance(result["criterion"], str) or not result["criterion"].strip():
            errors.append(f"{result_label}.criterion must be a non-empty string")
        if result["status"] not in {"PASS", "FAIL", "NOT_RUN", "BLOCKED"}:
            errors.append(f"{result_label}.status is invalid")
        check_string_array(result["evidence"], f"{result_label}.evidence", errors)

    check_resources(data["resources"], "trace.resources", errors)
    check_budgets(data["budgets"], "trace.budgets", errors)
    for field in ("approvals", "blockers", "limitations"):
        check_string_array(data[field], f"trace.{field}", errors)
    if not isinstance(data["artifacts"], list):
        errors.append("trace.artifacts must be an array")
    else:
        for index, artifact in enumerate(data["artifacts"]):
            artifact_label = f"trace.artifacts[{index}]"
            if not check_fields(artifact, {"path", "sha256", "bytes", "kind"}, artifact_label, errors):
                continue
            if not isinstance(artifact["path"], str) or not artifact["path"].strip():
                errors.append(f"{artifact_label}.path must be a non-empty string")
            if not re.fullmatch(r"[0-9a-f]{64}", str(artifact["sha256"])):
                errors.append(f"{artifact_label}.sha256 is invalid")
            if not isinstance(artifact["bytes"], int) or isinstance(artifact["bytes"], bool) or artifact["bytes"] < 0:
                errors.append(f"{artifact_label}.bytes must be a non-negative integer")
            if artifact["kind"] not in {"source", "test_result", "log", "report", "diagram", "other"}:
                errors.append(f"{artifact_label}.kind is invalid")
    if not isinstance(data["next_action"], str) or not data["next_action"].strip():
        errors.append("trace.next_action must be a non-empty string")

    if data["status"] == "COMPLETED":
        if not steps or any(step.get("status") not in {"VERIFIED", "SKIPPED"} for step in steps):
            errors.append("trace COMPLETED requires every step VERIFIED or SKIPPED")
        if not results or any(result.get("status") != "PASS" for result in results):
            errors.append("trace COMPLETED requires PASS evidence for every acceptance result")
        if data["blockers"]:
            errors.append("trace COMPLETED cannot contain blockers")
    elif data["status"] == "BLOCKED" and not data["blockers"]:
        errors.append("trace BLOCKED requires at least one blocker")
    return errors


def validate_checkpoint(data, route_profiles, profile_ids, recipe_profiles):
    errors = []
    label = "checkpoint"
    if not check_fields(data, CHECKPOINT_FIELDS, label, errors):
        return errors
    if data["schema_version"] != "1.0":
        errors.append("checkpoint.schema_version must be 1.0")
    if not re.fullmatch(r"CHECKPOINT-[0-9]{3}", str(data["checkpoint_id"])):
        errors.append("checkpoint.checkpoint_id is invalid")
    if not re.fullmatch(r"TRACE-[0-9]{3}", str(data["trace_id"])):
        errors.append("checkpoint.trace_id is invalid")
    if not isinstance(data["task_id"], str) or not data["task_id"].strip():
        errors.append("checkpoint.task_id must be a non-empty string")
    if data["status"] not in CHECKPOINT_STATUSES:
        errors.append("checkpoint.status is invalid")
    check_timestamp(data["created_at"], "checkpoint.created_at", errors)
    check_route(data, set(), route_profiles, profile_ids, recipe_profiles, label, errors)
    check_repository(data["repository"], "checkpoint.repository", errors)
    for field in ("completed_step_ids", "pending_step_ids", "blockers", "evidence_paths", "resume_conditions"):
        check_string_array(data[field], f"checkpoint.{field}", errors)
    for field in ("completed_step_ids", "pending_step_ids"):
        for index, step_id in enumerate(data[field]):
            if not re.fullmatch(r"STEP-[0-9]{3}", step_id):
                errors.append(f"checkpoint.{field}[{index}] is invalid")
    if set(data["completed_step_ids"]) & set(data["pending_step_ids"]):
        errors.append("checkpoint completed and pending step IDs must be disjoint")
    if not isinstance(data["next_action"], str) or not data["next_action"].strip():
        errors.append("checkpoint.next_action must be a non-empty string")
    if data["status"] == "COMPLETE":
        if data["pending_step_ids"] or data["blockers"]:
            errors.append("checkpoint COMPLETE cannot contain pending steps or blockers")
        if not data["completed_step_ids"]:
            errors.append("checkpoint COMPLETE requires completed steps")
    elif data["status"] == "BLOCKED":
        if not data["blockers"]:
            errors.append("checkpoint BLOCKED requires at least one blocker")
    elif data["status"] == "READY_TO_RESUME":
        if data["blockers"] or not data["pending_step_ids"] or not data["resume_conditions"]:
            errors.append("checkpoint READY_TO_RESUME requires pending steps, resume conditions and no blockers")
    return errors


def validate_document(data):
    techniques = validate_techniques.load_json(validate_techniques.REGISTRY_PATH)
    technique_ids = {item["id"] for item in techniques["techniques"]}
    manifests = validate_routing.load(validate_routing.ROUTING_DIR / "manifests.json")
    profiles = validate_routing.load(validate_routing.ROUTING_DIR / "profiles.json")
    recipes = validate_routing.load(validate_routing.ROUTING_DIR / "recipes.json")
    route_profiles = {item["id"]: item["profile"] for item in manifests["manifests"]}
    profile_ids = {item["id"] for item in profiles["profiles"]}
    recipe_profiles = {item["id"]: item["profile_id"] for item in recipes["recipes"]}
    if not isinstance(data, dict):
        return ["execution document must be an object"]
    if "checkpoint_id" in data:
        return validate_checkpoint(data, route_profiles, profile_ids, recipe_profiles)
    return validate_trace(data, technique_ids, route_profiles, profile_ids, recipe_profiles)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    paths = [Path(value) for value in argv] if argv else [TRACE_EXAMPLE, CHECKPOINT_EXAMPLE]
    errors = []
    for path in paths:
        try:
            data = load(path)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        errors.extend(f"{path.name}: {error}" for error in validate_document(data))
    if errors:
        print("Execution contracts: FAIL")
        for error in errors:
            print("-", error)
        return 1
    print(f"Execution contracts: PASS ({len(paths)} documents; templates are not run evidence)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
