import json
import re
import subprocess
import sys
from pathlib import Path

import task_contract
from context_compiler import matches_rule

GIT_TIMEOUT_SECONDS = 30


def run_git(root, args):
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=GIT_TIMEOUT_SECONDS,
            shell=False,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ValueError(f"Git inspection failed: {exc}") from exc
    if result.returncode != 0:
        message = result.stderr.decode("utf-8", errors="replace").strip()
        raise ValueError(f"Git inspection failed with exit code {result.returncode}: {message}")
    try:
        return result.stdout.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Git returned a non-UTF-8 path; scope inspection fails closed") from exc


def repository_root(project):
    root = Path(project).resolve()
    if not root.is_dir():
        raise ValueError("Project root is not a directory")
    top = run_git(root, ["rev-parse", "--show-toplevel"]).strip()
    if not top:
        raise ValueError("Git did not return a repository root")
    return Path(top).resolve()


def parse_status(payload):
    records = payload.split("\x00")
    entries = []
    index = 0
    while index < len(records):
        record = records[index]
        index += 1
        if not record:
            continue
        if len(record) < 4:
            raise ValueError("Malformed Git status record")
        status = record[:2]
        path = record[3:]
        if not path or path.startswith("/") or re.match(r"^[A-Za-z]:", path):
            raise ValueError("Git returned an unsafe repository-relative path")
        parts = path.split("/")
        if ".." in parts or "\x00" in path:
            raise ValueError("Git returned a path that escapes the repository")
        item = {"path": path, "status": status, "staged": False, "unstaged": False, "untracked": False}
        if status == "??":
            item["untracked"] = True
        else:
            item["staged"] = status[0] not in {" ", "?", "!"}
            item["unstaged"] = status[1] not in {" ", "?", "!"}
        if "R" in status or "C" in status:
            if index >= len(records) or not records[index]:
                raise ValueError("Git rename/copy record is missing its second path")
            second = records[index]
            index += 1
            second_parts = second.split("/")
            if second.startswith("/") or re.match(r"^[A-Za-z]:", second) or ".." in second_parts:
                raise ValueError("Git returned an unsafe rename/copy destination")
            item["path"] = path
            item["previous_path"] = second
        entries.append(item)
    return entries


def observed_bytes(root, path):
    candidate = root / path
    if candidate.is_symlink():
        raise ValueError(f"Changed path is a symlink: {path}")
    if not candidate.exists():
        return 0
    if not candidate.is_file():
        raise ValueError(f"Changed path is not a regular file: {path}")
    try:
        return candidate.stat().st_size
    except OSError as exc:
        raise ValueError(f"Cannot stat changed path {path}: {exc}") from exc


def check_scope(contract, project):
    errors = task_contract.validate_task_contract(contract)
    if errors:
        return {"schema_version": "1.0", "state": "BLOCKED", "execution_state": "NOT_EXECUTED", "errors": errors, "violations": []}
    try:
        root = repository_root(project)
        head = run_git(root, ["rev-parse", "--verify", "HEAD"]).strip()
        branch = run_git(root, ["branch", "--show-current"]).strip() or None
        entries = parse_status(run_git(root, ["status", "--porcelain=v1", "-z", "--untracked-files=all"]))
    except ValueError as exc:
        return {"schema_version": "1.0", "state": "BLOCKED", "execution_state": "NOT_EXECUTED", "errors": [str(exc)], "violations": []}

    scope = contract["scope"]
    base_commit = scope.get("base_commit")
    base_resolved = None
    if base_commit is not None:
        try:
            base_resolved = run_git(root, ["rev-parse", "--verify", base_commit + "^{commit}"]).strip()
            run_git(root, ["merge-base", "--is-ancestor", base_resolved, head])
        except ValueError as exc:
            return {"schema_version": "1.0", "state": "BLOCKED", "execution_state": "NOT_EXECUTED", "errors": [f"base_commit is not an ancestor of HEAD or could not be verified: {exc}"], "violations": []}

    paths = set()
    for entry in entries:
        paths.add(entry["path"])
        if entry.get("previous_path"):
            paths.add(entry["previous_path"])
    ordered_paths = sorted(paths)
    allow_paths = scope["allow_paths"]
    deny_paths = list(dict.fromkeys(task_contract.DEFAULT_DENY_PATHS + scope.get("deny_paths", [])))
    violations = []
    total_bytes = 0
    path_bytes = {}
    for path in ordered_paths:
        if not any(matches_rule(path, rule) for rule in allow_paths):
            violations.append({"path": path, "kind": "outside_allowlist", "reason": "Changed path is not allowed by task.scope.allow_paths"})
        denied = next((rule for rule in deny_paths if matches_rule(path, rule)), None)
        if denied:
            violations.append({"path": path, "kind": "denied_path", "reason": f"Changed path matches deny rule: {denied}"})
        try:
            size = observed_bytes(root, path)
        except ValueError as exc:
            violations.append({"path": path, "kind": "unsafe_path", "reason": str(exc)})
            size = 0
        path_bytes[path] = size
        total_bytes += size
    if len(ordered_paths) > scope["max_changed_files"]:
        violations.append({"path": None, "kind": "max_changed_files", "reason": f"Observed {len(ordered_paths)} changed paths; limit is {scope['max_changed_files']}"})
    if total_bytes > scope["max_changed_bytes"]:
        violations.append({"path": None, "kind": "max_changed_bytes", "reason": f"Observed {total_bytes} working-tree bytes; limit is {scope['max_changed_bytes']}"})

    staged = sorted({entry["path"] for entry in entries if entry["staged"]} | {entry["previous_path"] for entry in entries if entry["staged"] and entry.get("previous_path")})
    unstaged = sorted({entry["path"] for entry in entries if entry["unstaged"]} | {entry["previous_path"] for entry in entries if entry["unstaged"] and entry.get("previous_path")})
    untracked = sorted(entry["path"] for entry in entries if entry["untracked"])
    tracked_changed = sorted(set(staged) | set(unstaged))
    state = "BLOCKED" if violations else "PASS"
    return {
        "schema_version": "1.0",
        "task_id": contract["task_id"],
        "state": state,
        "execution_state": "NOT_EXECUTED",
        "repository": {
            "root": ".",
            "branch": branch,
            "head_commit": head,
            "base_commit": base_resolved,
            "changed_paths": tracked_changed,
            "untracked_paths": untracked,
        },
        "observations": {
            "staged_paths": staged,
            "unstaged_paths": unstaged,
            "untracked_paths": untracked,
            "path_statuses": entries,
            "path_bytes": path_bytes,
            "changed_file_count": len(ordered_paths),
            "changed_bytes_working_tree": total_bytes,
        },
        "limits": {
            "max_changed_files": scope["max_changed_files"],
            "max_changed_bytes": scope["max_changed_bytes"],
            "enforcement": "detection_only",
        },
        "violations": violations,
        "errors": [],
        "limitations": [
            "Scope inspection detects current Git status; it does not prevent an independent agent from editing files.",
            "Gitignored paths are not reported as untracked by this status-based inspection.",
            "Changed bytes describe existing working-tree files, not historical or staged blob contents.",
            "A controlled verification runner can refuse to start after a scope violation, but this is not an OS/process filesystem sandbox.",
        ],
    }


def main(argv=None):
    parser = __import__("argparse").ArgumentParser(description="Check repository changes against an explicit task contract")
    parser.add_argument("input", nargs="?", default="-", help="Task contract JSON file or - for stdin")
    parser.add_argument("--project", default=".", help="Project root")
    parser.add_argument("--output", help="Write the scope report to this path")
    args = parser.parse_args(argv)
    try:
        contract = task_contract.load_json(args.input)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Scope input error: {exc}", file=sys.stderr)
        return 2
    result = check_scope(contract, args.project)
    text = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        try:
            Path(args.output).write_text(text, encoding="utf-8")
        except OSError as exc:
            print(f"Scope output error: {exc}", file=sys.stderr)
            return 2
    print(text, end="")
    if result.get("errors"):
        return 2
    return 0 if result["state"] == "PASS" else 3


if __name__ == "__main__":
    sys.exit(main())
