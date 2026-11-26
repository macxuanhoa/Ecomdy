# Source Registry and Document Inventory

## Supplied source materials

| ID | File | Type / scope | Use | Publication state |
|---|---|---|---|---|
| SRC-01 | `docs/00-original/challenge-brief.xlsx` | Challenge Briefs + Tasks by Discipline | Official Challenge 2 requirements and tasks | Local-only; excluded by Git |
| SRC-02 | `docs/00-original/master-blueprint.pdf` | 34-page bilingual target blueprint | Proposed architecture, capabilities, workflows, roadmap | Local-only; excluded by Git |
| SRC-03 | `docs/00-original/business-workstream-plan.pdf` | 7-page business workstream plan | Proposed business research, work packages, and validation | Local-only; excluded by Git |
| SRC-04 | `docs/00-original/challenge-notes.jpg` | User-provided Vietnamese notes | Proposed trend, market, data, model-routing, and assistant directions | Local-only; excluded by Git |

Checksums and local-only flags are maintained in [`source-manifest.json`](source-manifest.json). Original files are preserved in `docs/00-original/`; the tracked README in that folder states that originals must not be force-added without permission.

## Reading / extraction record

- SRC-01: both workbook sheets read in full; source register in `docs/01-requirements.md` uses the source cell locations.
- SRC-02 and SRC-03: all 34 + 7 pages text-extracted and reviewed.
- SRC-04: image dimensions checked and content visually reviewed.
- The attachment folder contained no ZIP. No additional chat attachment was available in this workspace.

## Source quality and authority

The workbook is the primary source for official challenge requirements. The business plan, blueprint, and JPG are supporting material; their extensions, estimates, technical choices, and priorities are not official challenge requirements unless independently confirmed. No external market, legal, or vendor research has been used to state a product fact.
