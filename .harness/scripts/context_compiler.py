import argparse
import hashlib
import json
import os
import re
import stat
import sys
from pathlib import Path

DEFAULT_EXCLUDED_DIRS = (".git", ".harness/state", ".harness/cache", ".harness/logs")
ORIGINAL_DIRS = ("docs/00-original", ".harness/docs/00-original")


def stable_hash(value):
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def file_hash(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize_rule(value, label, errors):
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{label} must be a non-empty string")
        return None
    rule = value.strip().replace("\\", "/")
    if rule.startswith("/") or re.match(r"^[A-Za-z]:", rule) or "://" in rule:
        errors.append(f"{label} must be a repository-relative local path")
        return None
    parts = rule.split("/")
    if any(part == ".." for part in parts) or "\x00" in rule:
        errors.append(f"{label} must not escape the project root")
        return None
    return rule.rstrip("/") or "."


def glob_regex(pattern):
    output = []
    index = 0
    while index < len(pattern):
        char = pattern[index]
        if char == "*":
            if index + 1 < len(pattern) and pattern[index + 1] == "*":
                index += 2
                if index < len(pattern) and pattern[index] == "/":
                    output.append("(?:.*/)?")
                    index += 1
                else:
                    output.append(".*")
                continue
            output.append("[^/]*")
        elif char == "?":
            output.append("[^/]")
        else:
            output.append(re.escape(char))
        index += 1
    return re.compile("^" + "".join(output) + "$")


def matches_rule(path, rule):
    if any(char in rule for char in "*?["):
        return bool(glob_regex(rule).fullmatch(path))
    return path == rule or path.startswith(rule.rstrip("/") + "/")


def protected_reason(path, include_originals):
    parts = path.split("/")
    if ".git" in parts:
        return "Git metadata is excluded"
    for directory in DEFAULT_EXCLUDED_DIRS[1:]:
        if path == directory or path.startswith(directory + "/"):
            return "Local harness runtime state is excluded"
    if not include_originals:
        for directory in ORIGINAL_DIRS:
            if path == directory or path.startswith(directory + "/"):
                return "Original source material is excluded by default"
    return None


def excluded_reason(path, rules, include_originals):
    reason = protected_reason(path, include_originals)
    if reason:
        return reason
    for rule in rules:
        if matches_rule(path, rule):
            return f"Matched exclude rule: {rule}"
    return None


def blocked_result(request, errors, **extra):
    result = {
        "schema_version": "1.0",
        "state": "BLOCKED",
        "runtime_state": "BLOCKED",
        "execution_state": "NOT_EXECUTED",
        "input_sha256": stable_hash(request),
        "errors": errors,
        "files": [],
        "limitations": ["Context compilation inventories local files only; it does not load content into a model or execute a task."],
    }
    result.update(extra)
    return result


def validate_request(request):
    if not isinstance(request, dict):
        return ["context request must be a JSON object"]
    errors = []
    includes = request.get("include_paths")
    if not isinstance(includes, list) or not includes:
        errors.append("include_paths must be a non-empty array")
    excludes = request.get("exclude_paths", [])
    if not isinstance(excludes, list):
        errors.append("exclude_paths must be an array")
    for field in ("max_files", "max_bytes"):
        value = request.get(field)
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            errors.append(f"{field} must be a positive integer")
    if "include_originals" in request and not isinstance(request["include_originals"], bool):
        errors.append("include_originals must be a boolean")
    if "baseline_manifest" in request and (not isinstance(request["baseline_manifest"], str) or not request["baseline_manifest"].strip()):
        errors.append("baseline_manifest must be a non-empty repository-relative path")
    return errors


def discover_files(root, include_rules, exclude_rules, include_originals, excluded, warnings, errors):
    candidates = {}

    def add_file(path, source_rule):
        relative = path.relative_to(root).as_posix()
        reason = excluded_reason(relative, exclude_rules, include_originals)
        if reason:
            excluded.append({"path": relative, "reason": reason})
            return
        if path.is_symlink():
            errors.append(f"Explicitly included path is a symlink: {relative}")
            return
        try:
            resolved = path.resolve(strict=True)
        except OSError as exc:
            errors.append(f"Cannot resolve included path {relative}: {exc}")
            return
        if not resolved.is_relative_to(root.resolve()):
            errors.append(f"Included path escapes the project root: {relative}")
            return
        mode = path.stat().st_mode
        if not stat.S_ISREG(mode):
            errors.append(f"Included path is not a regular file: {relative}")
            return
        candidates.setdefault(relative, {"path": path, "source_rule": source_rule})

    def walk_directory(directory, source_rule):
        for current, dirnames, filenames in os.walk(directory, topdown=True, followlinks=False):
            current_path = Path(current)
            kept_dirs = []
            for name in sorted(dirnames):
                child = current_path / name
                relative = child.relative_to(root).as_posix()
                if child.is_symlink():
                    excluded.append({"path": relative, "reason": "Symlink directory skipped"})
                    continue
                reason = excluded_reason(relative + "/", exclude_rules, include_originals)
                if reason:
                    excluded.append({"path": relative, "reason": reason})
                    continue
                kept_dirs.append(name)
            dirnames[:] = kept_dirs
            for name in sorted(filenames):
                child = current_path / name
                relative = child.relative_to(root).as_posix()
                if child.is_symlink():
                    excluded.append({"path": relative, "reason": "Symlink file skipped"})
                    continue
                reason = excluded_reason(relative, exclude_rules, include_originals)
                if reason:
                    excluded.append({"path": relative, "reason": reason})
                    continue
                add_file(child, source_rule)

    for rule in include_rules:
        matched = False
        if any(char in rule for char in "*?["):
            for path in sorted(root.glob(rule), key=lambda item: item.as_posix()):
                matched = True
                if path.is_symlink():
                    excluded.append({"path": path.relative_to(root).as_posix(), "reason": "Symlink match skipped"})
                elif path.is_dir():
                    walk_directory(path, rule)
                elif path.is_file():
                    add_file(path, rule)
                else:
                    errors.append(f"Include pattern matched a non-regular path: {path.relative_to(root).as_posix()}")
        else:
            path = root / rule
            if not path.exists() and not path.is_symlink():
                errors.append(f"Include path does not exist: {rule}")
                continue
            matched = True
            if path.is_symlink():
                errors.append(f"Explicitly included path is a symlink: {rule}")
            elif path.is_dir():
                walk_directory(path, rule)
            elif path.is_file():
                add_file(path, rule)
            else:
                errors.append(f"Include path is not a regular file or directory: {rule}")
        if not matched:
            errors.append(f"Include pattern matched no local paths: {rule}")
    return candidates


def load_baseline(root, rule, errors):
    if rule is None:
        return None, None
    normalized = normalize_rule(rule, "baseline_manifest", errors)
    if normalized is None:
        return None, None
    path = root / normalized
    if path.is_symlink():
        errors.append("baseline_manifest must not be a symlink")
        return None, None
    try:
        resolved = path.resolve(strict=True)
    except OSError as exc:
        errors.append(f"Cannot resolve baseline_manifest: {exc}")
        return None, None
    if not resolved.is_relative_to(root.resolve()):
        errors.append("baseline_manifest must be an eligible file inside the project root")
        return None, None
    baseline_parts = normalized.split("/")
    if ".git" in baseline_parts or any(normalized == directory or normalized.startswith(directory + "/") for directory in ORIGINAL_DIRS):
        errors.append("baseline_manifest must not read Git metadata or original source material")
        return None, None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"Cannot read baseline_manifest: {exc}")
        return None, None
    if not isinstance(data, dict) or not isinstance(data.get("files"), list):
        errors.append("baseline_manifest must contain a files array")
        return None, None
    baseline = {}
    for item in data["files"]:
        if not isinstance(item, dict) or not isinstance(item.get("path"), str) or not isinstance(item.get("sha256"), str):
            errors.append("baseline_manifest contains an invalid file record")
            return None, None
        baseline[item["path"]] = item["sha256"]
    return baseline, file_hash(path)


def compile_context(request, root=None):
    root_path = Path(root).resolve() if root is not None else Path.cwd().resolve()
    errors = validate_request(request)
    if errors:
        return blocked_result(request, errors)
    if not root_path.is_dir():
        return blocked_result(request, ["project root is not a directory"])

    include_rules = []
    for index, value in enumerate(request["include_paths"]):
        normalized = normalize_rule(value, f"include_paths[{index}]", errors)
        if normalized is not None:
            include_rules.append(normalized)
    exclude_rules = []
    for index, value in enumerate(request.get("exclude_paths", [])):
        normalized = normalize_rule(value, f"exclude_paths[{index}]", errors)
        if normalized is not None:
            exclude_rules.append(normalized)
    include_originals = request.get("include_originals", False)
    baseline, baseline_hash = load_baseline(root_path, request.get("baseline_manifest"), errors)
    if errors:
        return blocked_result(request, errors)

    excluded = []
    warnings = []
    candidates = discover_files(root_path, include_rules, exclude_rules, include_originals, excluded, warnings, errors)
    if errors:
        return blocked_result(request, errors, excluded=sorted(excluded, key=lambda item: item["path"]))
    ordered = sorted(candidates.items())
    if not ordered:
        return blocked_result(request, ["No eligible local files remain after path and exclusion checks"], excluded=sorted(excluded, key=lambda item: item["path"]))
    if len(ordered) > request["max_files"]:
        return blocked_result(request, [f"Context exceeds max_files: {len(ordered)} > {request['max_files']}"], excluded=sorted(excluded, key=lambda item: item["path"]), limit_violation={"kind": "max_files", "observed": len(ordered), "limit": request["max_files"], "first_omitted_path": ordered[request["max_files"]][0]})

    total_bytes = 0
    expected_sizes = {}
    for relative, item in ordered:
        try:
            size = item["path"].stat().st_size
        except OSError as exc:
            return blocked_result(request, [f"Cannot stat {relative}: {exc}"])
        if not stat.S_ISREG(item["path"].stat().st_mode):
            return blocked_result(request, [f"Changed path is no longer a regular file: {relative}"])
        expected_sizes[relative] = size
        total_bytes += size
        if total_bytes > request["max_bytes"]:
            return blocked_result(request, [f"Context exceeds max_bytes: {total_bytes} > {request['max_bytes']}"], excluded=sorted(excluded, key=lambda item: item["path"]), limit_violation={"kind": "max_bytes", "observed_at_least": total_bytes, "limit": request["max_bytes"], "first_omitted_path": relative})

    files = []
    content_pool = {}
    for relative, item in ordered:
        try:
            digest = file_hash(item["path"])
            size = item["path"].stat().st_size
        except OSError as exc:
            return blocked_result(request, [f"Cannot hash {relative}: {exc}"])
        if size != expected_sizes[relative]:
            return blocked_result(request, [f"File size changed during context compilation: {relative}"])
        content_id = "sha256:" + digest
        record = {
            "path": relative,
            "sha256": digest,
            "bytes": size,
            "estimated_tokens": (size + 3) // 4,
            "content_id": content_id,
            "content_included": False,
            "extraction_status": "metadata_only",
            "provenance": {
                "kind": "local_file",
                "root_relative": True,
                "requested_rule": item["source_rule"],
                "authority": "owner-supplied local include path",
            },
            "lazy_load_guidance": "Load only when the current compiled step needs this exact path; content is not embedded in this manifest.",
        }
        files.append(record)
        if digest not in content_pool:
            content_pool[digest] = {"content_id": content_id, "sha256": digest, "bytes": size, "paths": [relative]}
        else:
            content_pool[digest]["paths"].append(relative)

    logical_bytes = sum(item["bytes"] for item in files)
    unique_bytes = sum(item["bytes"] for item in content_pool.values())
    estimated_tokens = sum(item["estimated_tokens"] for item in files)
    delta = None
    if baseline is not None:
        current = {item["path"]: item["sha256"] for item in files}
        delta = {
            "baseline_sha256": baseline_hash,
            "added_paths": sorted(set(current) - set(baseline)),
            "removed_paths": sorted(set(baseline) - set(current)),
            "changed_paths": sorted(path for path in set(current) & set(baseline) if current[path] != baseline[path]),
            "unchanged_paths": sorted(path for path in set(current) & set(baseline) if current[path] == baseline[path]),
        }
    warnings.extend([
        "Token counts are bytes/4 heuristic estimates, not provider measurements.",
        "File hashes prove observed bytes only; they do not establish source authority or content approval.",
    ])
    return {
        "schema_version": "1.0",
        "manifest_id": "CONTEXT-" + stable_hash({"request": request, "files": files})[:12].upper(),
        "state": "COMPILED",
        "runtime_state": "COMPILED",
        "execution_state": "NOT_EXECUTED",
        "input_sha256": stable_hash(request),
        "policy": {
            "project_root": ".",
            "local_only": True,
            "network_enabled": False,
            "content_embedded": False,
            "include_originals": include_originals,
            "enforcement": "advisory",
        },
        "limits": {"max_files": request["max_files"], "max_bytes": request["max_bytes"], "include_originals": include_originals, "enforcement": "advisory"},
        "files": files,
        "content_pool": [content_pool[key] for key in sorted(content_pool)],
        "summary": {
            "file_count": len(files),
            "unique_content_count": len(content_pool),
            "logical_bytes": logical_bytes,
            "unique_bytes": unique_bytes,
            "deduplicated_bytes": logical_bytes - unique_bytes,
            "estimated_tokens": estimated_tokens,
            "token_measurement_status": "not_measured",
            "estimate_method": "bytes_div_4_heuristic",
        },
        "excluded": sorted(excluded, key=lambda item: (item["path"], item["reason"])),
        "delta": delta,
        "warnings": warnings,
        "limitations": [
            "The manifest contains paths, hashes and metadata, not file contents.",
            "Limits are enforced for this compilation only; they do not constrain an independent agent terminal.",
            "No model provider, network service or task executor was invoked.",
            "Hashing and metadata inventory do not approve a source for collection or model use.",
        ],
    }


def load_json(path):
    if path == "-":
        return json.load(sys.stdin)
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main(argv=None):
    parser = argparse.ArgumentParser(description="Compile a bounded local-first DevHarness context manifest")
    parser.add_argument("input", nargs="?", default="-", help="Context request JSON file or - for stdin")
    parser.add_argument("--project", default=".", help="Project root")
    parser.add_argument("--output", help="Write the context manifest to this path")
    args = parser.parse_args(argv)
    try:
        request = load_json(args.input)
        result = compile_context(request, args.project)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Context compile input error: {exc}", file=sys.stderr)
        return 1
    text = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        try:
            Path(args.output).write_text(text, encoding="utf-8")
        except OSError as exc:
            print(f"Context compile output error: {exc}", file=sys.stderr)
            return 1
    print(text, end="")
    return {"COMPILED": 0, "BLOCKED": 3}.get(result["state"], 1)


if __name__ == "__main__":
    sys.exit(main())
