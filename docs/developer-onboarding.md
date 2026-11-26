# Developer Onboarding

## Current repository

This repository is a documentation/design baseline, not a running Ecomdy product. A new contributor can inspect requirements, diagrams, setup decisions, and validation without installing application dependencies.

## Prerequisites

- Git.
- Python 3.10 or newer for the documentation validator.
- Graphviz only if regenerating the DOT diagram renderings.
- GitHub access appropriate to the work; do not place credentials in chat or repository files.

## Start working

```bash
git clone https://github.com/macxuanhoa/Ecomdy.git
cd Ecomdy
python scripts/validate.py
```

1. Read `AGENTS.md`, `README.md`, `docs/project-context.md`, and `docs/01-requirements.md`.
2. Check `docs/setup/EXECUTION_STATUS.md`, `TASK_REGISTRY.md`, and `BLOCKERS.md` before taking a task.
3. Create a topic branch from the current default branch and record the requirement IDs, allowed paths, acceptance checks, and dependencies.
4. Preserve local-only originals under `docs/00-original/`; do not force-add them.
5. Run the relevant checks, record exact results, and update traceability and documentation.
6. Open a pull request; `main` requires a pull request, the `validate` check, and resolved conversations. There is currently no minimum approval count.

## Existing-project and session handoff

For a new session, start with the latest [handoff](setup/HANDOFF.md), then inspect Git status and the current commit before changing files. Use scoped search; do not reread every source or diagram unless the task requires it. Mark assumptions and conflicts explicitly.

## Product and DevHarness commands

No Ecomdy app install, migration, product test, deployment, or user workflow command exists yet. The reusable DevHarness OS is included at `.harness/` as an advisory development tool, not as a product dependency:

```bash
python .harness/harness.py doctor
python -m unittest discover -s .harness/tests -v
python .harness/scripts/validate.py
```

Use the [Harness Installation Guide](harness-installation-guide.md) for initializing another workspace and generating a source inventory. The CLI does not extract documents, call models, execute implementation tasks, or schedule jobs.
