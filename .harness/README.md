# DevHarness OS

Reusable agentic engineering harness • v0.1 starter • advisory mode.

![Control plane](docs/diagrams/02-control-plane.svg)

## Quick start
Python 3.10+; Git optional for local init; Graphviz only for regenerating images.

```powershell
python harness.py doctor
python harness.py init --project ../../my-project
# place authorized files in my-project/docs/00-original
python harness.py ingest --project ../../my-project
python -m unittest discover -s tests -v
python scripts/validate.py
```

The example destination is outside the Ecomdy checkout when this harness is run from `Ecomdy/.harness/`. Choose a different destination as needed; never initialize a workspace inside a public repository by accident. If this is a standalone harness clone rather than the embedded `.harness/` directory, set `--project` to a path outside that checkout.

Open the generated `docs/01-project-context/CONTEXT_UPDATE_PROMPT.md` in your coding agent with access to the workspace. The CLI inventories and hashes files; it does not parse or extract content, call models, implement tasks or schedule jobs yet. No secrets required. Existing files are preserved on init, except new ignore entries may be appended. `ingest` refuses to overwrite an existing generated registry or prompt unless `--overwrite` is explicitly supplied.

## Documentation
- [Master vision](docs/01-vision.md)
- [Capabilities, agents, skills and tools](docs/02-registries.md)
- [Workflows and loops](docs/03-workflows.md)
- [Development roadmap](docs/04-roadmap.md)
- [Diagram catalogue](docs/diagrams/README.md)
- [Contribution protocol](CONTRIBUTING.md)

Future capabilities are proposals, not features already implemented. Project-specific data must stay outside this reusable repository.
