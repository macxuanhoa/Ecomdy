# Ecomdy Intelligence Platform

**AI-Powered Cross-Border Commerce Intelligence & Content Platform**
Greenwich Industry Challenge 2026 × Ecomdy · Challenge 2

> **Current state:** public documentation and target-design repository. No Ecomdy application, API, database, AI integration, scheduled collector, or deployment is implemented here.

The challenge is to help Ecomdy's Marketing / Content Team research international marketplace, tax, and shipping developments for Vietnamese cross-border sellers; produce evidence-linked weekly digests and channel-specific content drafts; and identify published content that may need updating. Product decisions and implementation status must remain traceable to evidence.

## Contents

- [Product context and official requirements](docs/project-context.md)
- [Requirements register](docs/01-requirements.md) · [traceability](docs/requirements-traceability.md)
- [Product vision and capability registry](docs/02-product-vision.md)
- [Module specifications](docs/module-specifications.md) · [database design](docs/database-design.md) · [API design](docs/api-design.md)
- [Security and governance](docs/security-governance.md) · [risk register](docs/risk-register.md) · [Definition of Ready / Done](docs/definition-of-ready-done.md)
- [Agent and tool registry](docs/agent-tool-registry.md) · [automation](docs/automation-specification.md) · [context engineering](docs/context-engineering.md)
- [Target architecture and candidate stack](docs/03-architecture.md)
- [Technology and harness evaluation](docs/technology-evaluation.md)
- [Business and technical workflows](docs/04-workflows.md)
- [Implementation roadmap](docs/05-roadmap.md)
- [Testing and evidence strategy](docs/06-validation.md)
- [Constraints and assumptions](docs/constraints-assumptions.md) · [conflict report](docs/conflict-report.md) · [open questions](docs/open-questions.md)
- [Source registry](docs/source-registry.md) · [diagram gallery](docs/diagrams/README.md)
- [Documentation portal](docs/README.md)
- [Developer onboarding](docs/developer-onboarding.md) · [deployment strategy](docs/deployment-strategy.md)
- [Environment and capability audit](docs/setup/00_ENVIRONMENT_AND_CAPABILITY_AUDIT.md)
- [Contribution protocol](CONTRIBUTING.md) · [Agent instructions](AGENTS.md) · [Security policy](SECURITY.md) · [Changelog](CHANGELOG.md)

## Problem and intended users

The official brief describes frequent marketplace, tax, and shipping changes, time-consuming research across sources, and outdated published articles. The direct users are the Ecomdy Marketing / Content Team. Vietnamese sellers who sell internationally are the intended beneficiaries. Seller interviews and current Ecomdy process measurements are still outstanding; no user research findings or productivity gains are claimed.

## Challenge capabilities

1. Monitor permitted public sources for marketplace, tax, and shipping news.
2. Produce a weekly seller-focused digest with a source link for each item.
3. Create cited website, social, and short-form video drafts.
4. Flag outdated or inaccurate claims in published articles.
5. Keep all generated content in draft until a person reviews and approves it.

Social-trend intelligence, Telegram, model routing, frequent updates, and multi-market expansion are proposals for later validation, not confirmed MVP requirements.

## Target system architecture

The proposed design separates source ingestion, processing, evidence storage, AI-assisted analysis, application services, API, and user interfaces. It favors a modular product with background work; it does not require each module to be a microservice. DevHarness OS is packaged under `.harness/` as separate development infrastructure and is not an Ecomdy runtime dependency.

![Proposed logical system architecture](docs/diagrams/01-system-architecture.svg)

All diagrams describe a **target proposal**, not an as-built system. See [Architecture](docs/03-architecture.md), [workflow catalogue](docs/diagrams/README.md), and [DevHarness boundary diagram](docs/diagrams/11-harness-boundary.svg).

## Core workflow proposals

- **Collection:** permitted source → fetch with limits → normalize and deduplicate → classify and retain provenance → verify claims → store evidence.
- **Digest:** select eligible evidence → write summaries with source links → check unsupported claims → human review.
- **Content:** choose an event → generate channel drafts → verify claims and citations → review and edit → approve an exact version.
- **Freshness audit:** authorized published article → extract claims → compare with newer evidence → flag for human review.

These workflows are specifications only; none currently runs as a product service.

## Repository structure

Representative, abbreviated view; see [the documentation portal](docs/README.md) for the full index.

```text
.
├── .github/                 # Pull request / CI configuration
├── .harness/                # Reusable advisory development harness
├── docs/
│   ├── 00-original/          # Local originals; Git-ignored except README
│   ├── diagrams/             # Editable DOT/Mermaid plus SVG/PNG renderings
│   ├── 01-requirements.md
│   ├── 02-product-vision.md
│   ├── 03-architecture.md
│   ├── 04-workflows.md
│   ├── 05-roadmap.md
│   ├── 06-validation.md
│   ├── module-specifications.md, database-design.md, api-design.md, …
│   └── setup/                # Audit, plan, status, decisions, verification, handoff
├── prompts/                  # Bootstrap prompt
├── scripts/                  # Documentation validation and diagram rendering
└── project-profile.json      # Proposed project profile
```

## Technology direction

No stack has been approved. Current documentation evaluates candidates such as React/Next.js, Python/FastAPI, PostgreSQL, background workers, and provider adapters. Select technology only after checking existing code (none was supplied), requirements, source constraints, team skills, operating cost, and deployment needs.

## Current implementation status

| Area | State |
|---|---|
| Product vision, requirements, proposed workflows and architecture | Documentation present; owner validation pending |
| Diagrams | Source and rendered assets present; represent target design |
| Documentation validator | Implemented as `python scripts/validate.py`; run locally or in CI |
| GitHub Actions | Documentation and harness validation workflow present; both remote checks passed for the setup PR commit |
| Ecomdy application and runtime | Not implemented |
| DevHarness OS | Bundled under `.harness/` as an advisory starter; independent from Ecomdy runtime |
| Seller interviews, team feedback, benchmarks | Outstanding; no results claimed |

## Quick start

```bash
git clone https://github.com/macxuanhoa/Ecomdy.git
cd Ecomdy
python scripts/validate.py
python .harness/harness.py doctor
python -m unittest discover -s .harness/tests -v
```

The documentation validator uses only the Python standard library. It checks local Markdown links and required diagram assets. It does **not** test an application, external links, legal compliance, or diagram semantics.

The reusable harness CLI is also Python-only. See the [Harness Installation Guide](docs/harness-installation-guide.md) for workspace initialization and source inventory commands. Its current `ingest` command inventories and hashes files but does not extract document contents or execute agent tasks.

### Contributing and continuing work

1. Read [Agent instructions](AGENTS.md), [requirements](docs/01-requirements.md), [current-state audit](docs/setup/00_ENVIRONMENT_AND_CAPABILITY_AUDIT.md), and the relevant specification.
2. Create a feature branch and record a bounded task, scope, acceptance checks, and evidence.
3. Inspect existing files before adding code. Preserve current behavior and source provenance.
4. Run only checks that exist and report exact results; do not claim a target workflow is implemented because a design exists.
5. Update requirements traceability, docs, and verification evidence with any behavior change.

For new projects, existing projects, context refresh, or interrupted sessions, use [the documentation portal](docs/README.md), [Harness Installation Guide](docs/harness-installation-guide.md), and [setup handoff](docs/setup/HANDOFF.md). Ecomdy-specific runtime commands do not exist yet.

## Diagrams

Each diagram has editable source and rendered SVG/PNG assets. Update the source in `docs/diagrams/` and use `python scripts/render_diagrams.py` where Graphviz is installed; the script invokes Graphviz `dot` directly. PNG/SVG assets already present are the current renders. Review semantic changes and rendered readability together.

## GitHub Actions

The current workflow runs the product documentation validator, DevHarness unit tests, and harness documentation validator on pushes, pull requests, and manual dispatch with read-only repository permissions. It disables persisted checkout credentials, does not deploy or run AI jobs, and uses the current major releases of the official checkout and setup-python actions. Dependabot checks GitHub Actions versions monthly and opens reviewable PRs; no product packages are declared. Repository description, topics, labels, milestones, secret scanning, dependency updates, private vulnerability reporting, and `main` branch protection are configured as recorded in the [setup audit](docs/setup/00_ENVIRONMENT_AND_CAPABILITY_AUDIT.md). The monthly version-update config activates on `main` after PR #1 merges.

## Security and source handling

- Never commit credentials, API keys, private user data, or unapproved internal materials.
- The original challenge documents remain in `docs/00-original/`, ignored by Git. Do not force-add them.
- Reusable harness workspace originals belong in `.harness/docs/00-original/` and are ignored by Git too.
- Use an owner-reviewed source allowlist and comply with source terms before any collection implementation.
- Keep generated content draft-only until an authorized person approves it.
- Review external-source content as untrusted input; preserve citations and defend against prompt injection.

## Documentation map

See [docs/README.md](docs/README.md) for source authority, requirements, product documentation, diagrams, setup records, and current gaps. See [the setup plan](docs/setup/SETUP_PLAN.md) for task sequencing.
