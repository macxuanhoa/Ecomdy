import json
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

import scope_checker
import task_contract
import validate_execution


def utc_now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def redact_output(text):
    text = re.sub(r"-----BEGIN [^-]+PRIVATE KEY-----.*?-----END [^-]+PRIVATE KEY-----", "[REDACTED PRIVATE KEY]", text, flags=re.DOTALL)
    text = re.sub(r"(?i)\b(authorization|api[_-]?key|password|passwd|secret|token)\b\s*[:=]\s*[\"']?[^\s\"',;]+", r"\1=[REDACTED]", text)
    text = re.sub(r"\bBearer\s+[A-Za-z0-9._~+/=-]+", "Bearer [REDACTED]", text, flags=re.IGNORECASE)
    text = re.sub(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16}|eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,})", "[REDACTED]", text)
    return text


def blocked_command(command, reason):
    return {
        "argv": list(command["argv"]),
        "cwd": ".",
        "status": "BLOCKED",
        "exit_code": None,
        "started_at": None,
        "finished_at": None,
        "output_excerpt": "",
        "output_truncated": False,
        "output_bytes": None,
        "evidence_path": None,
    }, {"id": command["id"], "status": "BLOCKED", "reason": reason}


def resolve_executable(argv):
    requested = argv[0]
    name = Path(requested).name.lower()
    if name.startswith("python"):
        expected = Path(sys.executable).resolve()
        candidate = Path(requested).resolve() if Path(requested).is_absolute() else expected
        if candidate != expected:
            raise ValueError(f"Python executable is not the current reviewed interpreter: {requested}")
        return str(expected)
    found = shutil.which(requested)
    if not found:
        raise ValueError(f"Allowlisted executable is not available: {requested}")
    expected = Path(found).resolve()
    candidate = Path(requested).resolve() if Path(requested).is_absolute() else expected
    if candidate != expected:
        raise ValueError(f"Executable path does not match the reviewed PATH artifact: {requested}")
    return str(expected)


def terminate_process(process):
    if process.poll() is not None:
        return
    try:
        if os.name == "nt":
            process.terminate()
        else:
            os.killpg(process.pid, signal.SIGTERM)
    except OSError:
        process.terminate()
    try:
        process.wait(timeout=2)
    except subprocess.TimeoutExpired:
        try:
            if os.name == "nt":
                process.kill()
            else:
                os.killpg(process.pid, signal.SIGKILL)
        except OSError:
            process.kill()
        process.wait(timeout=2)


def scoped_path(root, value):
    candidate = Path(value)
    raw = candidate if candidate.is_absolute() else root / candidate
    if raw.is_symlink():
        raise ValueError(f"Command path must not be a symlink: {value}")
    path = raw.resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError(f"Command path escapes the project root: {value}")
    if not path.exists():
        raise ValueError(f"Command path does not exist: {value}")
    return path


def validate_command_paths(command, root):
    argv = command["argv"]
    executable = Path(argv[0]).name.lower()
    candidates = []
    if executable.startswith("python"):
        path_options = {"-s", "--start-directory", "-t", "--top-level-directory"}
        for index, arg in enumerate(argv[1:], start=1):
            if arg in path_options and index + 1 < len(argv):
                candidates.append(argv[index + 1])
            elif any(arg.startswith(option + "=") for option in {"--start-directory", "--top-level-directory"}):
                candidates.append(arg.split("=", 1)[1])
            elif arg.endswith(".py") and not arg.startswith("-"):
                candidates.append(arg)
    elif executable in {"gitleaks", "gitleaks.exe"}:
        path_options = {"--source", "-s", "--config", "--baseline-path", "--gitleaks-ignore-path"}
        for index, arg in enumerate(argv[1:], start=1):
            if arg in path_options and index + 1 < len(argv):
                candidates.append(argv[index + 1])
            elif any(arg.startswith(option + "=") for option in path_options if option.startswith("--")):
                candidates.append(arg.split("=", 1)[1])
    for value in candidates:
        scoped_path(root, value)


def execute_command(command, root, evidence_dir):
    try:
        validate_command_paths(command, root)
        executable = resolve_executable(command["argv"])
    except ValueError as exc:
        return blocked_command(command, str(exc))
    argv = [executable, *command["argv"][1:]]
    started_at = utc_now()
    started = time.monotonic()
    kwargs = {"start_new_session": True} if os.name != "nt" else {"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP}
    try:
        process = subprocess.Popen(
            argv,
            cwd=root,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=False,
            **kwargs,
        )
    except OSError as exc:
        record, event = blocked_command(command, f"Process could not start: {exc}")
        event["reason"] = f"Process could not start: {exc}"
        return record, event

    captured = bytearray()
    output_bytes = 0
    overflow = threading.Event()
    output_limit = command["max_output_bytes"]

    def read_output():
        nonlocal output_bytes
        while True:
            chunk = process.stdout.read(4096)
            if not chunk:
                break
            output_bytes += len(chunk)
            remaining = output_limit - len(captured)
            if remaining > 0:
                captured.extend(chunk[:remaining])
            if output_bytes > output_limit:
                overflow.set()

    reader = threading.Thread(target=read_output, daemon=True)
    reader.start()
    timed_out = False
    deadline = started + command["timeout_seconds"]
    while True:
        if overflow.is_set():
            terminate_process(process)
            break
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            timed_out = True
            terminate_process(process)
            break
        try:
            process.wait(timeout=min(0.1, remaining))
            break
        except subprocess.TimeoutExpired:
            continue
    reader.join(timeout=2)
    if reader.is_alive():
        try:
            process.stdout.close()
        except OSError:
            pass
        reader.join(timeout=1)
    else:
        process.stdout.close()
    finished_at = utc_now()
    runtime_seconds = round(time.monotonic() - started, 6)
    raw = bytes(captured).decode("utf-8", errors="replace")
    redacted = redact_output(raw)
    encoded = redacted.encode("utf-8")[:output_limit]
    excerpt = encoded.decode("utf-8", errors="ignore")
    truncated = overflow.is_set() or output_bytes > output_limit
    log_path = evidence_dir / f"{command['id']}.log"
    log_text = excerpt
    if truncated:
        log_text += f"\n[OUTPUT TRUNCATED AT {output_limit} BYTES; OBSERVED {output_bytes} BYTES]\n"
    log_path.write_text(log_text, encoding="utf-8")
    if timed_out:
        status = "TIMEOUT"
        exit_code = None
        termination_reason = "timeout"
    elif overflow.is_set():
        status = "FAIL"
        exit_code = process.returncode if isinstance(process.returncode, int) and process.returncode != 0 else 1
        termination_reason = "output_cap"
    else:
        status = "PASS" if process.returncode == 0 else "FAIL"
        exit_code = process.returncode
        termination_reason = None
    record = {
        "argv": argv,
        "cwd": ".",
        "status": status,
        "exit_code": exit_code,
        "started_at": started_at,
        "finished_at": finished_at,
        "output_excerpt": excerpt,
        "output_truncated": truncated,
        "output_bytes": output_bytes,
        "evidence_path": log_path.relative_to(root).as_posix(),
    }
    event = {
        "id": command["id"],
        "kind": command["kind"],
        "status": status,
        "runtime_seconds": runtime_seconds,
        "termination_reason": termination_reason,
        "reader_joined": not reader.is_alive(),
    }
    return record, event


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def artifact(root, path, kind):
    return {"path": path.relative_to(root).as_posix(), "sha256": task_contract.file_hash(path), "bytes": path.stat().st_size, "kind": kind}


def prepare_evidence_dir(root, contract):
    base = root / contract.get("evidence_dir", ".harness/state/evidence")
    if base.is_symlink():
        raise ValueError("Evidence directory must not be a symlink")
    resolved = base.resolve()
    state_root = (root / ".harness" / "state").resolve()
    if not resolved.is_relative_to(root.resolve()) or not resolved.is_relative_to(state_root):
        raise ValueError("Evidence directory must remain inside .harness/state")
    base.mkdir(parents=True, exist_ok=True)
    return Path(tempfile.mkdtemp(prefix=contract["trace_id"] + "-", dir=base))


def acceptance_results(contract, commands):
    results = []
    for criterion in contract["acceptance_criteria"]:
        mapped = [item for spec, item in zip(contract["commands"], commands) if criterion in spec["criteria"]]
        statuses = [item["status"] for item in mapped]
        if statuses and all(status == "PASS" for status in statuses):
            status = "PASS"
        elif any(status in {"FAIL", "TIMEOUT"} for status in statuses):
            status = "FAIL"
        else:
            status = "BLOCKED"
        evidence = [item["evidence_path"] for item in mapped if item["evidence_path"]]
        results.append({"criterion": criterion, "status": status, "evidence": evidence})
    return results


def build_trace(contract, scope, commands, results, artifacts, events, created_at, updated_at, runtime_seconds, state):
    attempted = any(item["status"] in {"PASS", "FAIL", "TIMEOUT"} for item in commands)
    if state == "PASS":
        trace_status = "COMPLETED"
        step_status = "VERIFIED"
    elif state == "FAIL":
        trace_status = "FAILED"
        step_status = "FAILED"
    else:
        trace_status = "BLOCKED"
        step_status = "EXECUTED" if attempted else "BLOCKED"
    timestamps = {
        "selected_at": created_at,
        "attempted_at": created_at if attempted else None,
        "executed_at": updated_at if attempted else None,
        "verified_at": updated_at if state == "PASS" else None,
    }
    blockers = []
    if state == "BLOCKED":
        blockers = list(scope.get("errors", [])) + [item["reason"] for item in scope.get("violations", [])]
        blockers.extend(event["reason"] for event in events if event["status"] == "BLOCKED" and event.get("reason"))
    if not blockers:
        blockers = [f"Acceptance criterion did not pass: {item['criterion']}" for item in results if item["status"] != "PASS"]
    repository = scope["repository"]
    repository_fields = {key: repository.get(key) for key in ("branch", "head_commit", "base_commit", "changed_paths", "untracked_paths")}
    outputs = [item["evidence_path"] for item in commands if item["evidence_path"]]
    return {
        "schema_version": "1.0",
        "trace_id": contract["trace_id"],
        "task_id": contract["task_id"],
        "status": trace_status,
        "created_at": created_at,
        "updated_at": updated_at,
        "route_id": contract["route_id"],
        "profile_id": contract["profile_id"],
        "recipe_id": contract["recipe_id"],
        "repository": repository_fields,
        "context": {
            "manifest_path": None,
            "input_hashes": ["task-contract-sha256:" + task_contract.stable_hash(contract)],
            "excluded_paths": list(dict.fromkeys(task_contract.DEFAULT_DENY_PATHS + contract["scope"].get("deny_paths", []))),
            "limits": {"max_files": contract["scope"]["max_changed_files"], "max_bytes": contract["scope"]["max_changed_bytes"]},
            "enforcement": "advisory",
        },
        "steps": [{
            "step_id": "STEP-001",
            "sequence": 1,
            "technique_id": contract["verification_technique_id"],
            "agent_id": None,
            "status": step_status,
            "timestamps": timestamps,
            "inputs": ["Validated task contract", "Repository scope report"],
            "outputs": outputs,
            "commands": commands,
            "notes": "Observed controlled verification only; no product implementation or independent review is implied.",
        }],
        "verification": {"acceptance_criteria": contract["acceptance_criteria"], "results": results},
        "resources": {"iterations": 1 if attempted else 0, "runtime_seconds": runtime_seconds if attempted else None, "retries": 0, "token_usage": None, "cost_usd": None, "measurement_status": "partial" if attempted else "unknown"},
        "budgets": {**contract["budgets"], "enforcement": "advisory"},
        "approvals": contract["approvals"],
        "blockers": blockers,
        "artifacts": artifacts,
        "limitations": [
            "Scope detection is not an OS/process filesystem restriction.",
            "Only direct child timeout/termination is enforced; process-tree and network isolation are not provided.",
            "Command output is bounded and heuristically redacted; redaction is not a guarantee against all sensitive data.",
            "Runtime is observed locally; token usage and cost remain unknown.",
        ],
        "next_action": "Review the evidence and scope report before any merge, handoff or further execution.",
    }


def verify_task(contract, project):
    errors = task_contract.validate_task_contract(contract)
    if errors:
        return {"schema_version": "1.0", "task_id": contract.get("task_id") if isinstance(contract, dict) else None, "state": "BLOCKED", "verification_state": "BLOCKED", "execution_state": "NOT_EXECUTED", "errors": errors, "input_error": True}
    if not contract["approvals"]:
        return {"schema_version": "1.0", "task_id": contract["task_id"], "state": "BLOCKED", "verification_state": "BLOCKED", "execution_state": "NOT_EXECUTED", "errors": ["Task contract has no approval reference; controlled verification cannot start"], "input_error": False}
    try:
        root = scope_checker.repository_root(project)
    except ValueError as exc:
        return {"schema_version": "1.0", "task_id": contract["task_id"], "state": "BLOCKED", "verification_state": "BLOCKED", "execution_state": "NOT_EXECUTED", "errors": [str(exc)], "input_error": False}
    created_at = utc_now()
    started = time.monotonic()
    scope = scope_checker.check_scope(contract, root)
    try:
        evidence_dir = prepare_evidence_dir(root, contract)
    except (OSError, ValueError) as exc:
        return {"schema_version": "1.0", "task_id": contract["task_id"], "state": "BLOCKED", "verification_state": "BLOCKED", "execution_state": "NOT_EXECUTED", "errors": [f"Cannot prepare evidence directory: {exc}"], "scope": scope, "input_error": False}
    scope_path = evidence_dir / "scope.json"
    write_json(scope_path, scope)
    artifacts = [artifact(root, scope_path, "report")]
    commands = []
    events = []
    stopped = scope["state"] != "PASS"
    for command in contract["commands"]:
        if stopped:
            record, event = blocked_command(command, "A prior scope or verification failure stopped the controlled runner")
            commands.append(record)
            events.append(event)
            continue
        record, event = execute_command(command, root, evidence_dir)
        commands.append(record)
        events.append(event)
        if record["evidence_path"]:
            artifacts.append(artifact(root, root / record["evidence_path"], "log"))
        if record["status"] != "PASS":
            stopped = True
    pre_scope = scope
    post_scope = scope_checker.check_scope(contract, root)
    post_scope_path = evidence_dir / "post-scope.json"
    write_json(post_scope_path, post_scope)
    artifacts.append(artifact(root, post_scope_path, "report"))
    scope = dict(pre_scope)
    if post_scope["state"] != "PASS":
        scope["state"] = "BLOCKED"
        scope["violations"] = list(pre_scope.get("violations", [])) + list(post_scope.get("violations", []))
        scope["errors"] = list(pre_scope.get("errors", [])) + list(post_scope.get("errors", []))
    results = acceptance_results(contract, commands)
    if scope["state"] != "PASS":
        state = "BLOCKED"
    elif any(item["status"] in {"FAIL", "TIMEOUT"} for item in commands):
        state = "FAIL"
    elif all(item["status"] == "PASS" for item in results):
        state = "PASS"
    else:
        state = "BLOCKED"
    updated_at = utc_now()
    runtime_seconds = round(time.monotonic() - started, 6)
    trace = build_trace(contract, scope, commands, results, artifacts, events, created_at, updated_at, runtime_seconds, state)
    trace_errors = validate_execution.validate_document(trace)
    if trace_errors:
        return {"schema_version": "1.0", "task_id": contract["task_id"], "state": "BLOCKED", "verification_state": "BLOCKED", "execution_state": "NOT_EXECUTED", "errors": ["Generated trace failed validation: " + "; ".join(trace_errors)], "scope": scope, "evidence_dir": evidence_dir.relative_to(root).as_posix(), "input_error": False}
    trace_path = evidence_dir / "trace.json"
    write_json(trace_path, trace)
    attempted = any(item["status"] in {"PASS", "FAIL", "TIMEOUT"} for item in commands)
    result = {
        "schema_version": "1.0",
        "task_id": contract["task_id"],
        "trace_id": contract["trace_id"],
        "task_contract_sha256": task_contract.stable_hash(contract),
        "state": state,
        "verification_state": {"PASS": "VERIFIED", "FAIL": "FAILED", "BLOCKED": "BLOCKED"}[state],
        "execution_state": "EXECUTED" if attempted else "NOT_EXECUTED",
        "scope": scope,
        "pre_scope": pre_scope,
        "post_scope": post_scope,
        "commands": commands,
        "command_events": events,
        "acceptance_results": results,
        "artifacts": artifacts,
        "evidence_dir": evidence_dir.relative_to(root).as_posix(),
        "scope_path": scope_path.relative_to(root).as_posix(),
        "post_scope_path": post_scope_path.relative_to(root).as_posix(),
        "trace_path": trace_path.relative_to(root).as_posix(),
        "resources": trace["resources"],
        "errors": [],
        "limitations": trace["limitations"],
    }
    verification_path = evidence_dir / "verification.json"
    write_json(verification_path, result)
    manifest_path = evidence_dir / "evidence-manifest.json"
    manifest_files = [artifact(root, path, "log" if path.suffix == ".log" else "report") for path in sorted(evidence_dir.iterdir()) if path.is_file() and path != manifest_path]
    write_json(manifest_path, {"schema_version": "1.0", "task_id": contract["task_id"], "trace_id": contract["trace_id"], "files": manifest_files})
    result["verification_path"] = verification_path.relative_to(root).as_posix()
    result["evidence_manifest_path"] = manifest_path.relative_to(root).as_posix()
    write_json(verification_path, result)
    manifest_files = [artifact(root, path, "log" if path.suffix == ".log" else "report") for path in sorted(evidence_dir.iterdir()) if path.is_file() and path != manifest_path]
    write_json(manifest_path, {"schema_version": "1.0", "task_id": contract["task_id"], "trace_id": contract["trace_id"], "files": manifest_files})
    return result


def main(argv=None):
    import argparse
    parser = argparse.ArgumentParser(description="Run explicit allowlisted verification commands and capture evidence")
    parser.add_argument("input", nargs="?", default="-", help="Task contract JSON file or - for stdin")
    parser.add_argument("--project", default=".", help="Project root")
    parser.add_argument("--output", help="Write the verification record to this path")
    args = parser.parse_args(argv)
    try:
        contract = task_contract.load_json(args.input)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Verification input error: {exc}", file=sys.stderr)
        return 2
    try:
        result = verify_task(contract, args.project)
    except (OSError, ValueError) as exc:
        result = {"schema_version": "1.0", "state": "BLOCKED", "verification_state": "BLOCKED", "execution_state": "NOT_EXECUTED", "errors": [str(exc)], "input_error": False}
    text = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        try:
            Path(args.output).write_text(text, encoding="utf-8")
        except OSError as exc:
            print(f"Verification output error: {exc}", file=sys.stderr)
            return 2
    print(text, end="")
    if result.get("input_error"):
        return 2
    return {"PASS": 0, "FAIL": 1, "BLOCKED": 3}.get(result["state"], 2)


if __name__ == "__main__":
    sys.exit(main())
