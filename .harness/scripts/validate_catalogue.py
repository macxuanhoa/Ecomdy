import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOGUE = ROOT / "registry" / "catalogue"
CLASSIFICATIONS = {"exact_match", "partial_match", "related_method", "distinct_technique"}
EXPECTED_GROUPS = {"A": 14, "B": 18, "C": 20, "D": 18, "E": 20, "F": 20, "G": 15, "H": 20}


def load(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError(f"Missing file: {path.relative_to(ROOT)}")
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path.relative_to(ROOT)}: {exc}")


def validate():
    errors = []
    manifest = load(CATALOGUE / "source-manifest.json")
    source = load(CATALOGUE / "source-145.json")
    entries = source.get("techniques") if isinstance(source, dict) else None
    if not isinstance(entries, list):
        return ["Source catalogue must contain a techniques array"]
    crosswalk = load(CATALOGUE / "crosswalk.json")
    summary = load(CATALOGUE / "reconciliation-summary.json")
    registry = load(ROOT / "registry" / "techniques.json")
    source_hash = hashlib.sha256((CATALOGUE / "source-145.json").read_bytes()).hexdigest()
    recorded_hash = next((item["sha256"] for item in manifest["artifacts"] if item["path"].endswith("source-145.json")), None)
    if source_hash != recorded_hash or crosswalk["source_sha256"] != source_hash:
        errors.append("Source catalogue hash does not match its manifest or crosswalk")
    source_ids = [entry.get("source_id") for entry in entries if isinstance(entry, dict)]
    if len(entries) != 145 or len(set(source_ids)) != 145:
        errors.append("Source catalogue must contain 145 unique entries")
    expected_ids = {f"{group}{number:02d}" for group, count in EXPECTED_GROUPS.items() for number in range(1, count + 1)}
    if set(source_ids) != expected_ids:
        errors.append("Source catalogue IDs do not match A01-H20 group ranges")
    groups = Counter(entry.get("group") for entry in entries if isinstance(entry, dict))
    if dict(groups) != EXPECTED_GROUPS:
        errors.append(f"Source group counts differ: {dict(groups)}")
    mappings = crosswalk.get("mappings")
    if not isinstance(mappings, list) or len(mappings) != 145:
        errors.append("Crosswalk must contain exactly 145 mappings")
        return errors
    mapped_ids = [row.get("source_id") for row in mappings if isinstance(row, dict)]
    if len(set(mapped_ids)) != 145 or set(mapped_ids) != expected_ids:
        errors.append("Crosswalk must map every source ID exactly once")
    cards = registry.get("techniques", [])
    card_by_id = {card.get("id"): card for card in cards if isinstance(card, dict)}
    alias_to_card = {}
    for card in cards:
        if not isinstance(card, dict):
            continue
        for alias in card.get("catalogue_aliases", []):
            if alias in alias_to_card:
                errors.append(f"Catalogue alias {alias} appears on multiple cards")
            alias_to_card[alias] = card.get("id")
    classifications = Counter()
    reused = set()
    for row in mappings:
        if not isinstance(row, dict):
            errors.append("Crosswalk mapping must be an object")
            continue
        source_id = row.get("source_id")
        canonical_id = row.get("canonical_id")
        if row.get("classification") not in CLASSIFICATIONS:
            errors.append(f"{source_id} has invalid classification")
        classifications[row.get("classification")] += 1
        if canonical_id not in card_by_id:
            errors.append(f"{source_id} references unknown canonical ID {canonical_id}")
            continue
        if alias_to_card.get(source_id) != canonical_id:
            errors.append(f"{source_id} crosswalk/card alias mismatch")
        if int(canonical_id.split("-")[1]) <= 40:
            reused.add(canonical_id)
    if len(cards) != 106:
        errors.append(f"Canonical registry must contain 106 cards, found {len(cards)}")
    if len(alias_to_card) != 145:
        errors.append(f"Canonical cards must expose 145 unique aliases, found {len(alias_to_card)}")
    expected_summary = {
        "source_entries_imported": 145,
        "existing_canonical_entries_preserved": 40,
        "existing_entries_reused": len(reused),
        "new_entries_added": 66,
        "overlapping_source_entries": classifications["exact_match"] + classifications["partial_match"] + classifications["related_method"],
        "exact_matches": classifications["exact_match"],
        "partial_matches": classifications["partial_match"],
        "related_methods": classifications["related_method"],
        "distinct_techniques": classifications["distinct_technique"],
        "aliases": 145,
        "final_canonical_technique_count": len(cards),
        "unresolved_mappings": [],
    }
    for key, value in expected_summary.items():
        if summary.get(key) != value:
            errors.append(f"Reconciliation summary {key} must be {value!r}")
    return errors


def main():
    try:
        errors = validate()
    except ValueError as exc:
        errors = [str(exc)]
    if errors:
        print("Catalogue reconciliation: FAIL")
        for error in errors:
            print("-", error)
        return 1
    print("Catalogue reconciliation: PASS (145 sources; 106 canonical techniques; 0 unresolved)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
