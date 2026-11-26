# DevHarness OS Installation Guide

**State:** The repository includes the DevHarness OS v0.1 advisory starter in `.harness/`. The commands below are implemented locally; this is not an autonomous agent runtime.

## Requirements

- Python 3.10 or newer.
- Git is optional for local project initialization.
- Graphviz is optional and only needed to regenerate DOT diagram images.

The CLI uses Python's standard library and requires no API key or provider credentials.

## Check the bundled harness

Run these commands from the Ecomdy repository root:

```powershell
python .harness/harness.py doctor
python -m unittest discover -s .harness/tests -p "test_*.py" -v
python .harness/scripts/validate.py
```

`doctor` reports Python and optional local tools. The tests cover the current starter behavior. The validator checks relative Markdown links and the presence of expected diagram assets under `.harness/`.

## Initialize another project workspace

Choose a destination outside the Ecomdy checkout so project-specific files do not enter this public repository. From the Ecomdy repository root, run:

```powershell
Set-Location .harness
python harness.py init --project ../../my-project
python harness.py ingest --project ../../my-project
```

Replace `../../my-project` with the intended destination. `init` creates starter instructions, harness configuration, task template, documentation folders, and ignore rules. It preserves existing files and appends missing ignore rules; inspect the resulting diff before using the workspace.

Place only authorized source materials in the new project's `docs/00-original/` folder before running `ingest`. The command inventories file paths, sizes, and SHA-256 hashes and writes `docs/01-project-context/SOURCE_REGISTRY.json` plus a context prompt. It reads file bytes to compute hashes but does not parse or extract document contents. It refuses to replace either output if it already exists; review or back them up before intentionally rerunning with `--overwrite`. It does not approve requirements, call AI models, implement tasks, or schedule jobs. Review generated inventories and prompts before giving them to an agent.

## Reuse and current limits

The `.harness/` directory can be copied into another workspace as a starting component. It is coupled only to its own templates, scripts, docs, and config; no Ecomdy runtime package or service is imported. Review `.harness/AGENTS.md` and its documentation before adapting it.

Current limitations: advisory execution only; no model/provider adapters, document extraction, repository-wide AST map, permission enforcement, durable task runner, scheduler, automation service, or product integration. A separate harness remote or release artifact has not been created.
