import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

import validate_techniques
import validate_tool_manifest

ROOT = Path(__file__).resolve().parents[1]
COMMANDS = {
    "TOOL-001": "openspec",
    "TOOL-014": "drawio",
    "TOOL-016": "mmdc",
    "TOOL-017": "gitleaks",
    "TOOL-018": "dot",
    "TOOL-019": "structurizr",
}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def project_skills(root):
    records = []
    repository = root.parent
    canonical = root / "skills"
    installed = repository / ".qoder" / "skills"
    lock_path = repository / "skills-lock.json"
    lock = json.loads(lock_path.read_text(encoding="utf-8")) if lock_path.exists() else {"skills": {}}
    for source in sorted(canonical.glob("*/SKILL.md")):
        name = source.parent.name
        copy = installed / name / "SKILL.md"
        registered = True
        present = copy.exists()
        matches = present and source.read_bytes() == copy.read_bytes()
        lock_record = lock.get("skills", {}).get(name)
        lock_source = lock_record.get("source") if isinstance(lock_record, dict) else None
        locked = (
            isinstance(lock_record, dict)
            and lock_record.get("sourceType") == "local"
            and isinstance(lock_record.get("computedHash"), str)
            and bool(lock_record["computedHash"].strip())
            and isinstance(lock_source, str)
            and (repository / lock_source).resolve() == source.parent.resolve()
        )
        session_keys = {name.lower(), f"internal-skill-{name}".lower()}
        records.append({
            "capability_id": f"INTERNAL-SKILL-{name.upper()}",
            "name": name,
            "kind": "skill",
            "source": source.relative_to(repository).as_posix(),
            "sha256": sha256(source),
            "lifecycle": {
                "registered": registered,
                "installed": present,
                "configured": present and matches and locked,
                "available_in_session": None,
                "smoke_tested": False,
                "integrated": False,
                "verified": False,
            },
            "installed_copy": copy.relative_to(repository).as_posix() if present else None,
            "installed_copy_matches_source": matches if present else None,
            "lock_record_matches_source": locked,
            "session_keys": sorted(session_keys),
            "notes": ["Project installation does not prove current-session availability or workflow integration"],
        })
    return records


def detect_tool_install(tool, evidence_by_id, root):
    record = evidence_by_id.get(tool["id"], {})
    installed_path = record.get("installed_path")
    if installed_path:
        path = Path(installed_path)
        if path.exists():
            return True, installed_path
        command = COMMANDS.get(tool["id"])
        fallback = shutil.which(command) if command else None
        return bool(fallback), fallback or installed_path
    if tool["id"] == "TOOL-013":
        plugin_root = Path.home() / ".qoder" / "plugins" / "cache" / "qoder-marketplace" / "diagram-design"
        pinned = plugin_root / tool["version"] / "skills" / "diagram-design" / "SKILL.md"
        return (True, str(pinned)) if pinned.exists() else (None, None)
    command = COMMANDS.get(tool["id"])
    if command:
        detected = shutil.which(command)
        if detected:
            return True, detected
        if tool["id"] == "TOOL-001" and record.get("status") == "BLOCKED":
            return False, None
        return None, None
    return None, None


def inspect_capabilities(root=ROOT, session_skills=()):
    errors = []
    manifest = validate_tool_manifest.load(root / "registry" / "installation" / "tool-manifest.json")
    evidence_path = root / "registry" / "installation" / "activation-evidence.json"
    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    evidence_by_id = {record["capability_id"]: record for record in evidence["records"]}
    techniques = validate_techniques.load_json(root / "registry" / "techniques.json")
    errors.extend(validate_tool_manifest.validate_manifest(manifest))
    errors.extend(validate_techniques.validate_registry(techniques))

    session = {item.lower() for item in session_skills}
    skills = project_skills(root)
    for skill in skills:
        keys = set(skill.pop("session_keys"))
        skill["lifecycle"]["available_in_session"] = True if keys & session else None

    tools = []
    for tool in manifest["tools"]:
        installed, detected_path = detect_tool_install(tool, evidence_by_id, root)
        keys = {tool["id"].lower(), tool["name"].lower()}
        if tool["id"] == "TOOL-013":
            keys.add("diagram-design")
        smoke_tested = tool["status"] == "SMOKE TESTED" or evidence_by_id.get(tool["id"], {}).get("status") == "SMOKE TESTED"
        verified = tool["verification"]["status"] == "VERIFIED" and installed is not False
        configured = None
        notes = []
        if tool["kind"] == "skill":
            configured = bool(detected_path and Path(detected_path).is_relative_to(root))
        elif tool["id"] == "TOOL-001":
            configured = False
        else:
            notes.append("No machine-readable project activation contract was inspected")
        if tool["disposition"] == "INSTALLED_USER_SCOPE" and installed is False:
            notes.append("Manifest claims user-scope installation but the recorded artifact was not found")
        if tool["status"] == "BLOCKED":
            notes.append(tool.get("notes", "Capability is blocked"))
        tools.append({
            "capability_id": tool["id"],
            "name": tool["name"],
            "kind": tool["kind"],
            "version": tool["version"],
            "manifest_status": tool["status"],
            "disposition": tool["disposition"],
            "detected_path": detected_path,
            "lifecycle": {
                "registered": True,
                "installed": installed,
                "configured": configured,
                "available_in_session": True if keys & session else None,
                "smoke_tested": smoke_tested,
                "integrated": tool["status"] == "INTEGRATED",
                "verified": verified,
            },
            "notes": notes,
        })

    status_counts = {}
    kind_counts = {}
    for card in techniques["techniques"]:
        status_counts[card["status"]] = status_counts.get(card["status"], 0) + 1
        kind_counts[card["kind"]] = kind_counts.get(card["kind"], 0) + 1
    lifecycle_counts = {key: 0 for key in ("registered", "installed", "configured", "available_in_session", "smoke_tested", "integrated", "verified")}
    unknown_counts = dict(lifecycle_counts)
    for capability in skills + tools:
        for key, value in capability["lifecycle"].items():
            if value is True:
                lifecycle_counts[key] += 1
            elif value is None:
                unknown_counts[key] += 1
    blocked = [tool["capability_id"] for tool in tools if tool["manifest_status"] == "BLOCKED"]
    return {
        "schema_version": "1.0",
        "status": "FAIL" if errors else "PASS",
        "scope": "Local registry, project skill copies and detectable installed artifacts; not an OS sandbox or host catalog",
        "registries": {
            "techniques": {"count": len(techniques["techniques"]), "status_counts": status_counts, "kind_counts": kind_counts},
            "tools": {"count": len(tools), "blocked": blocked},
            "skills": {"count": len(skills)},
        },
        "lifecycle_true_counts": lifecycle_counts,
        "lifecycle_unknown_counts": unknown_counts,
        "skills": skills,
        "tools": tools,
        "session_observation": {
            "provided": bool(session),
            "capabilities": sorted(session),
            "limitation": "Absence from this optional observation is unknown, not proof of unavailability",
        },
        "errors": errors,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="Inspect registered, installed, configured, session, smoke, integration and verification states")
    parser.add_argument("--root", default=str(ROOT), help="Repository root")
    parser.add_argument("--session-skill", action="append", default=[], help="Capability ID or skill name observed in the active host catalog; repeatable")
    parser.add_argument("--strict", action="store_true", help="Return non-zero when any optional capability is BLOCKED")
    args = parser.parse_args(argv)
    try:
        result = inspect_capabilities(Path(args.root).resolve(), args.session_skill)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Capability inspection error: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if result["status"] == "FAIL":
        return 1
    if args.strict and result["registries"]["tools"]["blocked"]:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
