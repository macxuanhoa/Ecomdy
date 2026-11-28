import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOGUE = ROOT / "registry" / "catalogue"
REGISTRY = ROOT / "registry" / "techniques.json"
TASK_TYPES = {
    "A": ["requirements", "specification", "planning", "change_control"],
    "B": ["context_engineering", "repository_analysis", "prompt_preparation"],
    "C": ["agent_orchestration", "task_routing", "execution_control"],
    "D": ["implementation", "refactoring", "api_design", "migration"],
    "E": ["testing", "debugging", "evaluation", "verification"],
    "F": ["ai_product_engineering", "retrieval", "provider_integration"],
    "G": ["architecture", "diagrams", "frontend", "accessibility"],
    "H": ["collaboration", "security", "automation", "delivery"],
}


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    source = load(CATALOGUE / "source-145.json")
    registry = load(REGISTRY)
    drafts = load(CATALOGUE / "new-technique-drafts.json")
    with (CATALOGUE / "crosswalk.tsv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    source_by_id = {entry["source_id"]: entry for entry in source["techniques"]}
    aliases = {}
    for row in rows:
        aliases.setdefault(row["canonical_id"], []).append(row["source_id"])
        row["source_group"] = source_by_id[row["source_id"]]["group"]
        row["source_name"] = source_by_id[row["source_id"]]["name"]
        row["source_usage_context_vi"] = source_by_id[row["source_id"]]["usage_context_vi"]
    cards = [card for card in registry["techniques"] if int(card["id"].split("-")[1]) <= 40]
    for card in cards:
        card["applicable_task_types"] = TASK_TYPES[card["category"]["id"]]
        card["catalogue_aliases"] = aliases.get(card["id"], [])
        if card["catalogue_aliases"]:
            for reference in (".harness/registry/catalogue/source-145.json", ".harness/registry/catalogue/crosswalk.json"):
                if reference not in card["source_references"]:
                    card["source_references"].append(reference)
    cards.extend(drafts)
    cards.sort(key=lambda card: card["id"])
    registry["techniques"] = cards
    registry["registry_version"] = "0.2.0"
    registry["baseline_note"] = (
        "Reconciled from the owner-supplied 145-source catalogue. TECH-001–TECH-040 are preserved; "
        "76 source rows reuse 35 existing cards and 66 new canonical cards were added, producing 106 cards. "
        "Source IDs are aliases in a separate namespace from agent role IDs. Catalogue presence does not prove execution or integration."
    )
    write(REGISTRY, registry)
    write(CATALOGUE / "crosswalk.json", {
        "schema_version": "1.0",
        "source_catalogue": ".harness/registry/catalogue/source-145.json",
        "source_sha256": hashlib.sha256((CATALOGUE / "source-145.json").read_bytes()).hexdigest(),
        "mappings": rows,
    })
    classifications = Counter(row["classification"] for row in rows)
    reused_rows = sum(row["canonical_id"] in {f"TECH-{number:03d}" for number in range(1, 41)} for row in rows)
    summary = {
        "schema_version": "1.0",
        "source_entries_imported": len(rows),
        "existing_canonical_entries_preserved": 40,
        "existing_entries_reused": len({row["canonical_id"] for row in rows if row["canonical_id"] in {f"TECH-{number:03d}" for number in range(1, 41)}}),
        "source_rows_mapped_to_existing": reused_rows,
        "new_entries_added": len(drafts),
        "overlapping_source_entries": classifications["exact_match"] + classifications["partial_match"] + classifications["related_method"],
        "exact_matches": classifications["exact_match"],
        "partial_matches": classifications["partial_match"],
        "related_methods": classifications["related_method"],
        "distinct_techniques": classifications["distinct_technique"],
        "aliases": len(rows),
        "final_canonical_technique_count": len(cards),
        "existing_entries_without_source_alias": sorted({f"TECH-{number:03d}" for number in range(1, 41)} - set(aliases)),
        "unresolved_mappings": [],
    }
    write(CATALOGUE / "reconciliation-summary.json", summary)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
