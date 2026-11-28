# Repository Map

**As of:** 2026-11-28 (Asia/Saigon)<br>
**Purpose:** Help a contributor locate authority, executable behavior, target design, local-only inputs and current delivery state without reading the whole repository.<br>
**Current state:** Documentation/setup repository plus an advisory harness. No Ecomdy application runtime is implemented.

## 1. Actual inventory

| Path | Files | Purpose | Authority / status |
|---|---:|---|---|
| Root | 11 | Entry points, Git/editor settings, project profile, security/contribution/changelog | Repository policy and navigation |
| `.github/` | 4 | Validation workflow, Dependabot, issue and PR templates | Implemented documentation CI; no product CI |
| `docs/` | 139 | Requirements, architecture, product/workflow specs, diagrams, setup evidence, technique docs and ignored originals | Mixed: official/proposed requirements, verified setup evidence and target design |
| `.harness/` | 114 | Advisory Python CLI, config, technique/tool/routing/mapping registries, schemas, prompts, three skills, tests, validators, docs and diagrams | Small executable starter plus advisory contracts; no task executor |
| `scripts/` | 2 | Product documentation validator and DOT renderer | Implemented |
| `prompts/` | 1 | Bootstrap prompt | Instruction only |
| **Non-ignored working files** | **267** | Excludes `.git` and ignored files | Before the R01 commit: 238 tracked files (9 modified) plus 29 untracked artifacts |

A clean acceptance-branch clone at `f516230…` contains 225 tracked files. Preservation commit `4cfab07b8a163715ad608e5aaff6628b990d59a5` added nine new files and modified 24, producing 234 tracked files. The current `devharness/technique-library` branch is based on `4fb08fe5f269445c9ce191d9806fa6dd394e0638` and has 238 tracked files plus 29 untracked artifacts before they are committed. A broader filesystem count can be higher because it also includes ignored/local files; it must not be treated as the Git inventory. Verify counts with `git ls-files` and `git status` rather than treating this snapshot as a released-package count. Default `main` currently contains only `README.md` because PR #1 is unmerged.

## 2. Directory map

```text
.
├── AGENTS.md                 # Agent working rules and stop boundaries
├── CONTRIBUTING.md           # Branch, review and delivery protocol
├── README.md                 # Project entry point and current-state warning
├── SECURITY.md               # Reporting and source/security policy
├── project-profile.json      # Target profile; runtime automation false
├── .github/
│   ├── workflows/validate.yml
│   ├── dependabot.yml
│   ├── ISSUE_TEMPLATE/task.yml
│   └── pull_request_template.md
├── docs/
│   ├── 00-original/          # Local-only source inputs; ignored except README
│   ├── diagrams/             # 32 Mermaid + 14 DOT/SVG/PNG sets
│   ├── setup/                # Acceptance, audit, blockers, decisions, verification, handoff
│   ├── 01-requirements.md    # Official requirement register
│   ├── 02-product-vision.md  # M01–M20 capability registry
│   ├── 03-architecture.md    # Target architecture and assessment
│   ├── 04-workflows.md       # Product/development/harness workflow catalogue
│   ├── 05-roadmap.md         # Stages, milestones, critical path and workstreams
│   ├── 06-validation.md      # Target verification strategy
│   ├── module-specifications.md
│   ├── database-design.md    # Conceptual only; no migration
│   ├── api-design.md         # Proposed resources only; no OpenAPI/server
│   ├── phase1-requirements-delta.md
│   ├── phase1-architecture-delta.md
│   ├── vertical-slice-01-plan.md
│   ├── vs01-owner-approval-pack.md
│   ├── team-development-readiness.md
│   ├── developer-onboarding.md
│   ├── developer-operations.md
│   ├── minimum-viable-harness-plan.md
│   ├── engineering-technique-library.md
│   ├── engineering-technique-mapping.md
│   ├── project-owner-guide.md
│   └── repository-map.md
├── .harness/
│   ├── harness.py            # init, ingest, doctor, route, compile, context, scope, verify, capabilities
│   ├── config/default.json   # Copied config; not enforced by CLI
│   ├── registry/
│   │   ├── capabilities.json
│   │   ├── techniques.json   # 106 canonical advisory technique cards
│   │   ├── ecomdy-mapping.json
│   │   ├── installation/     # 20-candidate tool manifest
│   │   └── routing/          # 9 profiles, 14 routes, 24 recipes
│   ├── schemas/              # Technique, routing, task-contract, execution and tool-manifest contracts
│   ├── templates/            # Task, verification-contract, trace/checkpoint examples
│   ├── prompts/bootstrap.md
│   ├── skills/               # scoped-task, debug, diagram instruction files
│   ├── tests/                # Starter, registry, routing, mapping, execution-contract and execution-gate tests
│   ├── scripts/              # Validators, router/compilers, scope checker, controlled verification runner; DOT renderer
│   └── docs/                 # Harness specs, technique/tool guides and 24 diagrams
├── prompts/BOOTSTRAP.md
└── scripts/
    ├── validate.py
    └── render_diagrams.py
```

## 3. Authority map

| Question | Primary source | Supporting evidence |
|---|---|---|
| What is officially required? | [01-requirements.md](01-requirements.md) | [project-context.md](project-context.md), [product-requirements.md](product-requirements.md) |
| What is merely proposed? | [02-product-vision.md](02-product-vision.md), [module-specifications.md](module-specifications.md) | [phase1-requirements-delta.md](phase1-requirements-delta.md) |
| What is actually implemented? | [CAPABILITY_COVERAGE.md](setup/CAPABILITY_COVERAGE.md) | [COMPREHENSIVE_AUDIT.md](setup/COMPREHENSIVE_AUDIT.md), [VERIFICATION_REPORT.md](setup/VERIFICATION_REPORT.md) |
| What should be built first? | [vertical-slice-01-plan.md](vertical-slice-01-plan.md) | [05-roadmap.md](05-roadmap.md), [sprint-planning.md](sprint-planning.md) |
| How does the target system fit together? | [03-architecture.md](03-architecture.md) | [phase1-architecture-delta.md](phase1-architecture-delta.md), [database-design.md](database-design.md), [api-design.md](api-design.md) |
| How do product and team workflows operate? | [04-workflows.md](04-workflows.md) | [automation-specification.md](automation-specification.md), [CONTRIBUTING.md](../CONTRIBUTING.md) |
| What can DevHarness execute? | [.harness/harness.py](../.harness/harness.py) | [harness-installation-guide.md](harness-installation-guide.md), [.harness/tests](../.harness/tests/test_harness.py) |
| Which engineering techniques are registered? | [.harness/registry/techniques.json](../.harness/registry/techniques.json) | [Technique library](../.harness/docs/05-technique-library.md), [routing guide](../.harness/docs/06-technique-routing.md) |
| Which external tool candidates are researched? | [.harness/registry/installation/tool-manifest.json](../.harness/registry/installation/tool-manifest.json) | [Installation/activation guide](../.harness/docs/10-tool-installation-and-activation.md) |
| What is blocked or awaiting approval? | [BLOCKERS.md](setup/BLOCKERS.md) | [open-questions.md](open-questions.md), [risk-register.md](risk-register.md) |
| Where should a new session resume? | [HANDOFF.md](setup/HANDOFF.md) | [EXECUTION_STATUS.md](setup/EXECUTION_STATUS.md), [PHASE_1_TRANSITION.md](setup/PHASE_1_TRANSITION.md) |

## 4. Executable behavior map

| Command | Implemented behavior | Does not do |
|---|---|---|
| `python scripts/validate.py` | Checks local Markdown links, diagram metadata, gallery listing and required static assets | Does not parse Mermaid, render diagrams, test products or verify semantics |
| `python .harness/harness.py doctor` | Reports Python/project path and optional Git/Graphviz/GitHub CLI availability | Does not validate Jira, credentials, models, source policy or product readiness |
| `python .harness/harness.py route --task task.json --output route.json` | Evaluates explicit activation rules and returns a deterministic advisory route record | Does not execute tasks, compile recipes, route models or enforce limits |
| `python .harness/harness.py compile --task route.json --output compiled.json` | Compiles a compatible recipe and expanded advisory contracts; optionally embeds a context manifest | Does not execute steps, invoke agents, invent missing sequence assignments or measure resources |
| `python .harness/harness.py context --task context.json --output manifest.json` | Builds bounded local metadata manifests with hashes, provenance, deduplication and baseline deltas | Does not embed content, approve sources, call models or enforce OS/process boundaries |
| `python .harness/harness.py scope --task task-contract.json --output scope.json` | Detects staged, unstaged, untracked and rename paths outside the approved contract scope; checks Git HEAD/base and limits | Does not prevent independent edits or provide filesystem/network isolation |
| `python .harness/harness.py verify --task task-contract.json --output verification.json` | Runs approved, allowlisted Python/pytest/Gitleaks argv with pre/post scope checks, bounded logs and hashed evidence | Rejects arbitrary shells; does not support retries, paid calls, checkpoint/resume or a process/network sandbox |
| `python .harness/harness.py capabilities` | Inspects local registry, skill-copy and detectable tool lifecycle states | Does not prove host-wide/session availability, integration or sandbox enforcement |
| `python .harness/harness.py init --project PATH` | Creates missing starter files and appends missing ignore rules | Does not install the reusable harness into the destination or enforce task scope |
| `python .harness/harness.py ingest --project PATH` | Inventories/hashes regular non-symlink files under `PATH/docs/00-original` | Does not extract contents, call models or approve sources |
| `python -m unittest discover -s .harness/tests -v` | Runs harness starter, technique/routing/tool-manifest, mapping, execution-contract and controlled-execution tests | Does not test Ecomdy product behavior |
| `python .harness/scripts/validate.py` | Checks harness Markdown/diagram metadata/assets | Does not execute harness roles or skills |
| `python .harness/scripts/validate_techniques.py` | Validates 106 technique cards, references and status/invocation invariants | Does not prove technique effectiveness or installation |
| `python .harness/scripts/validate_routing.py` | Validates nine profiles, 14 routes and 24 recipes | Does not route or execute tasks |
| `python .harness/scripts/validate_execution.py` | Validates trace/checkpoint structure and state semantics | The validator itself does not execute commands or resume work; `verify` separately captures observed traces |
| `python .harness/scripts/validate_tool_manifest.py` | Checks 20 candidate records, lifecycle semantics, procedures and `NOT_RUN` research commands | Does not install tools, grant credentials or prove effectiveness |
| `python scripts/render_diagrams.py` | Invokes Graphviz to regenerate DOT assets when Graphviz exists | Does not render Mermaid; the audited shell PATH may not include a user-scope Graphviz installation |

There is no application install, migration, API server, UI, collector, scheduler, worker, model call or deployment command.

## 5. Logical data and control flow

```text
Official/local source inputs
        │
        ▼
Requirements and decision records ─────► Jira import-ready backlog (not yet imported)
        │
        ▼
Target architecture + module/workflow contracts
        │
        ▼
Vertical Slice 01 plan ─────► owner gates ─────► future implementation (not started)
        │
        ▼
Requirements → implementation → tests → evidence → review → demo

Repository documentation/harness
        │
        ├── local validators + harness unit tests
        ├── GitHub Actions validate
        ├── draft PR review
        └── manual handoff/checkpoint
```

## 6. Ownership boundaries

| Area | Proposed owner role | Current enforcement |
|---|---|---|
| Product scope, sources, budget, merge/deploy/publish | Project Owner | Human approval required; no named owner assigned |
| Architecture and shared contracts | Technical Lead / Architect | Review policy proposed |
| M01–M03 source/collection | Source & Collection Owner | Placeholder only |
| M04–M11 processing/evidence | Processing & Evidence Owner | Placeholder only |
| M12 persistence/API/migrations | Knowledge & API Owner | Placeholder only |
| M13–M17 content/editorial | Content & Editorial Owner | Placeholder only |
| CI, security, diagrams, deployment readiness | Platform & Quality Owner | Placeholder only |
| `.harness/` behavior | DevHarness Owner | Placeholder only |
| Independent change review | Independent Reviewer | No reviewer assigned or required count verified |

Do not add fictional handles to `CODEOWNERS` or invent Jira assignees.

## 7. Source and confidentiality boundaries

- `docs/00-original/` is local-only and ignored except its README.
- `.harness/docs/00-original/` is also ignored; it is not the default input directory for the bundled `ingest` command.
- A newly initialized workspace uses `<project>/docs/00-original`.
- Never force-add originals, credentials, private source text or personal data.
- No source is approved for collection merely because it appears in a document or diagram.
- No non-public material may be sent to a model provider before an owner-approved data-handling decision.

## 8. Navigation by task

| Task | Read first | Then inspect |
|---|---|---|
| Understand the project | [README.md](../README.md) | [project-context.md](project-context.md), [COMPREHENSIVE_AUDIT.md](setup/COMPREHENSIVE_AUDIT.md) |
| Change documentation | [AGENTS.md](../AGENTS.md), [CONTRIBUTING.md](../CONTRIBUTING.md) | Relevant specification, validator, PR template |
| Plan a product task | [task-register.md](task-register.md), [vertical-slice-01-plan.md](vertical-slice-01-plan.md) | Module/workflow/architecture contracts and acceptance tests |
| Review a PR | [team-development-readiness.md](team-development-readiness.md) | Diff, traceability, exact checks, security/source/diagram impact |
| Change a diagram | [diagram gallery](diagrams/README.md) | [Diagram tooling](setup/DIAGRAM_TOOLING.md), source metadata, paired artifacts, parser/render evidence |
| Use DevHarness | [harness-installation-guide.md](harness-installation-guide.md) | CLI help, tests, config limits, [technique library](../.harness/docs/05-technique-library.md), [routing](../.harness/docs/06-technique-routing.md) and [tool activation](../.harness/docs/10-tool-installation-and-activation.md) |
| Resume a session | [HANDOFF.md](setup/HANDOFF.md) | Git status/HEAD, blockers, execution status, relevant task only |
| Prepare owner decisions | [project-owner-guide.md](project-owner-guide.md) | [VS01 approval pack](vs01-owner-approval-pack.md), open questions, Jira plan, PR state |

## 9. Known map limitations

- The map describes the audited working tree, not a released package.
- Default `main` is not yet equivalent to the acceptance branch.
- Proposed directories such as application source, migrations, API contracts and deployment manifests do not exist and are therefore not shown as current.
- Update this map when product code is first introduced; do not pre-create speculative folders.
