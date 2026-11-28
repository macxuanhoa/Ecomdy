import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "registry" / "installation" / "tool-manifest.json"
SCHEMA_PATH = ROOT / "schemas" / "tool-manifest.schema.json"

STATUSES = {"AVAILABLE IN REGISTRY", "RESEARCHED", "APPROVED", "INSTALLED", "CONFIGURED", "AVAILABLE IN SESSION", "SMOKE TESTED", "INTEGRATED", "DEFERRED", "REJECTED", "BLOCKED"}
DISPOSITIONS = {"PROPOSED", "DEFERRED", "REJECTED", "INSTALLED_USER_SCOPE"}
COMMAND_STATUSES = {"NOT_RUN", "ATTEMPTED", "EXECUTED", "VERIFIED", "BLOCKED"}
SHELL_EXECUTABLES = {"sh", "bash", "zsh", "cmd", "cmd.exe", "powershell", "powershell.exe", "pwsh", "pwsh.exe"}
PROCEDURE_FIELDS = {"install", "activate", "verify", "update", "uninstall", "recovery"}
TOOL_FIELDS = {
    "id", "name", "kind", "canonical_repository", "version", "version_basis", "license",
    "maintenance", "status", "disposition", "required", "recommendation", "capabilities",
    "platforms", "agent_compatibility", "dependencies", "compatible_skills", "mcp_credentials",
    "network", "permissions", "telemetry_privacy", "security", "conflicts", "resource_implications",
    "reproducibility", "installation", "procedures", "verification", "sources", "notes",
}


def load(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError(f"Missing file: {path.relative_to(ROOT)}")
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path.relative_to(ROOT)}: {exc}")


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


def check_string(value, label, errors):
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{label} must be a non-empty string")


def check_array(value, label, errors, allow_empty=True):
    if not isinstance(value, list) or (not allow_empty and not value):
        errors.append(f"{label} must be {'a non-empty' if not allow_empty else 'an'} array of non-empty strings")
        return
    if any(not isinstance(entry, str) or not entry.strip() for entry in value):
        errors.append(f"{label} must contain only non-empty strings")


def check_url(value, label, errors):
    check_string(value, label, errors)
    if isinstance(value, str):
        parsed = urlparse(value)
        if parsed.scheme != "https" or not parsed.netloc:
            errors.append(f"{label} must be an HTTPS URL")


def check_command(command, label, errors):
    fields = {"argv", "cwd", "execution_status"}
    if not check_fields(command, fields, label, errors):
        return
    check_array(command["argv"], f"{label}.argv", errors, allow_empty=False)
    argv = command["argv"]
    if isinstance(argv, list) and argv and all(isinstance(arg, str) for arg in argv):
        executable = Path(argv[0]).name.lower()
        if executable in SHELL_EXECUTABLES and any(arg.lower() in {"-c", "/c", "-command"} for arg in argv[1:]):
            errors.append(f"{label} must not wrap commands in a shell")
    check_string(command["cwd"], f"{label}.cwd", errors)
    if command["execution_status"] not in COMMAND_STATUSES:
        errors.append(f"{label}.execution_status is invalid")
    elif command["execution_status"] != "NOT_RUN":
        errors.append(f"{label} research manifest commands must remain NOT_RUN")


def check_procedures(procedures, label, errors):
    if not check_fields(procedures, PROCEDURE_FIELDS, label, errors):
        return
    for field in PROCEDURE_FIELDS:
        check_array(procedures[field], f"{label}.{field}", errors, allow_empty=False)


def validate_tool(tool, index):
    errors = []
    label = f"tools[{index}]"
    if not check_fields(tool, TOOL_FIELDS, label, errors):
        return errors
    if not re.fullmatch(r"TOOL-[0-9]{3}", str(tool["id"])):
        errors.append(f"{label}.id is invalid")
    for field in ("name", "kind", "version", "version_basis", "maintenance", "recommendation", "notes"):
        check_string(tool[field], f"{label}.{field}", errors)
    if tool["kind"] not in {"tool", "framework", "mcp_server", "skill", "script"}:
        errors.append(f"{label}.kind is invalid")
    check_url(tool["canonical_repository"], f"{label}.canonical_repository", errors)
    if tool["status"] not in STATUSES:
        errors.append(f"{label}.status is invalid")
    if tool["disposition"] not in DISPOSITIONS:
        errors.append(f"{label}.disposition is invalid")
    if not isinstance(tool["required"], bool):
        errors.append(f"{label}.required must be a boolean")
    for field in ("capabilities", "platforms", "dependencies", "compatible_skills", "permissions", "telemetry_privacy", "security", "conflicts", "reproducibility"):
        check_array(tool[field], f"{label}.{field}", errors)

    license_data = tool["license"]
    if not check_fields(license_data, {"name", "spdx", "url", "notes"}, f"{label}.license", errors):
        return errors
    for field in ("name", "spdx"):
        check_string(license_data[field], f"{label}.license.{field}", errors)
    check_url(license_data["url"], f"{label}.license.url", errors)
    if not isinstance(license_data["notes"], str):
        errors.append(f"{label}.license.notes must be a string")

    compatibility = tool["agent_compatibility"]
    if not check_fields(compatibility, {"qoder", "claude_code", "codex", "generic_cli"}, f"{label}.agent_compatibility", errors):
        return errors
    for field, value in compatibility.items():
        check_string(value, f"{label}.agent_compatibility.{field}", errors)

    credentials = tool["mcp_credentials"]
    if credentials is not None:
        if not check_fields(credentials, {"required", "storage", "scopes", "notes"}, f"{label}.mcp_credentials", errors):
            return errors
        if not isinstance(credentials["required"], bool):
            errors.append(f"{label}.mcp_credentials.required must be a boolean")
        check_string(credentials["storage"], f"{label}.mcp_credentials.storage", errors)
        check_array(credentials["scopes"], f"{label}.mcp_credentials.scopes", errors)
        check_string(credentials["notes"], f"{label}.mcp_credentials.notes", errors)

    network = tool["network"]
    if not check_fields(network, {"installation", "runtime", "notes"}, f"{label}.network", errors):
        return errors
    for field in ("installation", "runtime"):
        if not isinstance(network[field], bool):
            errors.append(f"{label}.network.{field} must be a boolean")
    check_string(network["notes"], f"{label}.network.notes", errors)

    resources = tool["resource_implications"]
    if not check_fields(resources, {"token", "runtime", "measurement_status"}, f"{label}.resource_implications", errors):
        return errors
    check_string(resources["token"], f"{label}.resource_implications.token", errors)
    check_string(resources["runtime"], f"{label}.resource_implications.runtime", errors)
    if resources["measurement_status"] != "not_measured":
        errors.append(f"{label}.resource_implications.measurement_status must be not_measured")

    installation = tool["installation"]
    if not check_fields(installation, {"method", "proposed_commands"}, f"{label}.installation", errors):
        return errors
    check_string(installation["method"], f"{label}.installation.method", errors)
    if not isinstance(installation["proposed_commands"], list):
        errors.append(f"{label}.installation.proposed_commands must be an array")
    else:
        for command_index, command in enumerate(installation["proposed_commands"]):
            check_command(command, f"{label}.installation.proposed_commands[{command_index}]", errors)

    check_procedures(tool["procedures"], f"{label}.procedures", errors)
    verification = tool["verification"]
    if not check_fields(verification, {"status", "proposed_commands", "evidence"}, f"{label}.verification", errors):
        return errors
    if verification["status"] not in COMMAND_STATUSES:
        errors.append(f"{label}.verification.status is invalid")
    if not isinstance(verification["proposed_commands"], list):
        errors.append(f"{label}.verification.proposed_commands must be an array")
    else:
        for command_index, command in enumerate(verification["proposed_commands"]):
            check_command(command, f"{label}.verification.proposed_commands[{command_index}]", errors)
    check_array(verification["evidence"], f"{label}.verification.evidence", errors)

    if not isinstance(tool["sources"], list) or not tool["sources"]:
        errors.append(f"{label}.sources must be a non-empty array")
    else:
        for source_index, source in enumerate(tool["sources"]):
            check_url(source, f"{label}.sources[{source_index}]", errors)

    if tool["status"] in {"APPROVED", "CONFIGURED", "INTEGRATED"} and not verification["evidence"]:
        errors.append(f"{label} {tool['status']} requires verification evidence")
    if tool["status"] == "SMOKE TESTED" and not verification["evidence"]:
        errors.append(f"{label} SMOKE TESTED requires evidence")
    if tool["status"] == "REJECTED" and tool["disposition"] != "REJECTED":
        errors.append(f"{label} REJECTED status requires REJECTED disposition")
    if tool["disposition"] == "INSTALLED_USER_SCOPE" and tool["status"] not in {"INSTALLED", "AVAILABLE IN SESSION", "SMOKE TESTED", "INTEGRATED"}:
        errors.append(f"{label} installed user-scope disposition requires an installed-or-later status")
    return errors


def validate_manifest(data):
    errors = []
    top_fields = {"schema_version", "manifest_version", "status", "as_of", "baseline_requirements", "environment_observation", "selection_policy", "tools", "shared_procedures"}
    if not check_fields(data, top_fields, "manifest", errors):
        return errors
    if data["schema_version"] != "1.0":
        errors.append("manifest.schema_version must be 1.0")
    check_string(data["manifest_version"], "manifest.manifest_version", errors)
    if data["status"] != "ADVISORY_RESEARCH":
        errors.append("manifest.status must be ADVISORY_RESEARCH")
    check_string(data["as_of"], "manifest.as_of", errors)

    requirements = data["baseline_requirements"]
    if not isinstance(requirements, list) or not requirements:
        errors.append("manifest.baseline_requirements must be a non-empty array")
    else:
        for index, requirement in enumerate(requirements):
            label = f"manifest.baseline_requirements[{index}]"
            if not check_fields(requirement, {"name", "constraint", "required", "rationale"}, label, errors):
                continue
            for field in ("name", "constraint", "rationale"):
                check_string(requirement[field], f"{label}.{field}", errors)
            if not isinstance(requirement["required"], bool):
                errors.append(f"{label}.required must be a boolean")

    environment = data["environment_observation"]
    env_fields = {"observed_at", "python", "node", "npm", "missing_commands", "python_packages", "limitations"}
    if check_fields(environment, env_fields, "manifest.environment_observation", errors):
        for field in ("observed_at", "python", "node", "npm"):
            check_string(environment[field], f"manifest.environment_observation.{field}", errors)
        check_array(environment["missing_commands"], "manifest.environment_observation.missing_commands", errors)
        check_array(environment["limitations"], "manifest.environment_observation.limitations", errors, allow_empty=False)
        if not isinstance(environment["python_packages"], dict):
            errors.append("manifest.environment_observation.python_packages must be an object")
        else:
            for package, version in environment["python_packages"].items():
                check_string(package, "manifest.environment_observation.python_packages key", errors)
                check_string(version, f"manifest.environment_observation.python_packages.{package}", errors)

    policy = data["selection_policy"]
    policy_fields = {"default_spec_workflow", "multi_framework_rule", "network_default", "paid_services", "installation_authorization"}
    if check_fields(policy, policy_fields, "manifest.selection_policy", errors):
        for field in policy_fields:
            check_string(policy[field], f"manifest.selection_policy.{field}", errors)

    check_procedures(data["shared_procedures"], "manifest.shared_procedures", errors)
    tools = data["tools"]
    if not isinstance(tools, list) or not tools:
        errors.append("manifest.tools must be a non-empty array")
        return errors
    ids = [tool.get("id") for tool in tools if isinstance(tool, dict)]
    if len(ids) != len(set(ids)):
        errors.append("Duplicate tool IDs")
    for index, tool in enumerate(tools):
        errors.extend(validate_tool(tool, index))
    return errors


def main():
    try:
        data = load(MANIFEST_PATH)
        load(SCHEMA_PATH)
    except ValueError as exc:
        print("Tool manifest: FAIL")
        print("-", exc)
        return 1
    errors = validate_manifest(data)
    if errors:
        print("Tool manifest: FAIL")
        for error in errors:
            print("-", error)
        return 1
    print(f"Tool manifest: PASS ({len(data['tools'])} candidates; advisory research, proposed commands NOT_RUN)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
