# Tool Installation, Activation and Verification

**As of:** 2026-11-28 (Asia/Saigon)
**Authority:** [Tool manifest](../registry/installation/tool-manifest.json) and [manifest schema](../schemas/tool-manifest.schema.json)
**Status:** Wave 1 controlled activation is recorded separately from the advisory manifest. Proposed commands in the manifest remain `NOT_RUN`; only commands in [activation evidence](../registry/installation/activation-evidence.json) have observed execution status.

## 1. Current boundary

The repository works with Python 3.10+ for its starter CLI and validators. External candidates are optional development capabilities, not Ecomdy product dependencies. No candidate in this guide changes product requirements, architecture, Jira authority or branch protection.

The manifest is versioned research data. It does not install packages, grant credentials, create MCP sessions or enforce network access. Any activation requires explicit scope approval, compatibility/security review and a reversible project-scoped test.

### Lifecycle states

| State | Required evidence | Current candidate example |
|---|---|---|
| `AVAILABLE IN REGISTRY` | Stable ID and research/card record | All `TOOL-*` records exist in the manifest |
| `RESEARCHED` | Canonical source, version basis and reviewed limitations | Remaining candidates retain research records |
| `APPROVED` | Named owner decision with scope, permissions and rollback | Wave 1 controlled evaluation/installation authorized; no integration approval |
| `INSTALLED` | Exact command, exit code and installed artifact/version | Four internal Qoder skills; Mermaid CLI, Gitleaks and Graphviz user scope |
| `CONFIGURED` | Project configuration and permission review | Four internal skills copied into project scope; external runtime configuration remains limited |
| `AVAILABLE IN SESSION` | Host exposes the skill/tool to the active session | Diagram Design was exposed in the earlier session; newly installed skills require catalog reload |
| `SMOKE TESTED` | Bounded output and observed evidence | Diagram Design, Mermaid CLI, Gitleaks and Graphviz |
| `INTEGRATED` | Adopted workflow passes acceptance and is reproducible | None |
| `DEFERRED` | Reason and reconsideration condition | Competing or higher-risk candidates |
| `REJECTED` | Recorded decision and rationale | Structurizr Lite |
| `BLOCKED` | Explicit blocker and next owner/action | Runtime enforcement and autonomy remain blocked |

Do not skip from `RESEARCHED` to `INTEGRATED`. An installed package is not a configured project capability; a session-visible skill is not automatically inherited by clones or CI.

## 2. Observed environment

These observations apply to the audited shell on 2026-11-28, not necessarily to the Qoder host process:

| Component | Observed state | Consequence |
|---|---|---|
| Python | 3.11.9 | Meets the current harness baseline and Serena's Python floor |
| Node.js | 22.18.0 | Meets Mermaid CLI's recorded floor; below OpenSpec 2.2.0 and Promptfoo 0.126.0 floors |
| npm | 10.9.3 | Available; pinned Mermaid CLI installed with lifecycle scripts disabled |
| Python Playwright | 1.60.0 | Existing Chromium used by Mermaid smoke test; does not prove Playwright MCP or coding-agent CLI installation |
| Pillow | 12.1.1 | Local image utility; not an agent capability by itself |
| Installed user scope | Mermaid CLI 12.2.0, Gitleaks 8.30.1, Graphviz 16.1.2 | Exact paths and smoke evidence are recorded in activation evidence |
| Missing on PATH | `structurizr`, `drawio`, `gh`; OpenSpec not installed | Remaining candidates are not activated; OpenSpec is blocked by Node compatibility |

Git is present in the current repository. Graphviz is installed user scope and can regenerate approved DOT assets locally, but it is not inherited by clones or CI. Mermaid uses the existing Playwright Chromium and did not download a browser.

## 3. Candidate registry

| ID | Candidate | Pinned/researched version | License | Disposition | Decision |
|---|---|---:|---|---|---|
| TOOL-001 | OpenSpec | 2.2.0 | MIT | Blocked / deferred | Node 22.18.0 is below required >=22.20.0; not installed |
| TOOL-002 | Superpowers | 7.0.2 | MIT | Deferred | Host hooks/autonomy conflict with advisory controls |
| TOOL-003 | GitHub Spec Kit | 1.4.5 | MIT | Deferred | Governance alternative; avoid competing defaults |
| TOOL-004 | BMAD Method | 6.12.4 | MIT with trademark terms | Deferred | Broad ceremony and executable helper risk |
| TOOL-005 | Beads | 1.3.4 | MIT | Deferred | Task-memory alternative must not replace Jira authority |
| TOOL-006 | Promptfoo | 0.126.0 | MIT | Deferred | Node floor not met in the observed shell |
| TOOL-007 | Serena | 2.1.0 | Apache-2.0 | Deferred | Review indexing, backend and telemetry before use |
| TOOL-008 | Context7 | 4.9.1 | MIT | Deferred | Remote documentation/MCP use requires privacy review |
| TOOL-009 | Playwright MCP | 0.0.86 | Apache-2.0 | Deferred | Alpha line; browser permissions and isolation required |
| TOOL-010 | Playwright coding-agent CLI | 0.1.25 | Apache-2.0 | Deferred | Alpha line; separate from Python Playwright |
| TOOL-011 | Playwright test runner | 1.65.1 | Apache-2.0 | Deferred | Use only for an approved browser-test workflow |
| TOOL-012 | GitHub MCP Server | 2.3.0 | MIT | Deferred | Token/remote-tool mode and least privilege need review |
| TOOL-013 | Diagram Design | 2.6.131 | See manifest | Installed user scope | Session-visible and earlier smoke-tested; not clone/CI inherited |
| TOOL-014 | Draw.io core/Desktop | 32.7.7 | Apache-2.0 | Deferred | Local editor option; no installation performed |
| TOOL-015 | Draw.io MCP | 1.13.1 / 1.11.0 | Apache-2.0 | Deferred | Hosted private-diagram use is rejected in manifest notes |
| TOOL-016 | Mermaid CLI | 12.2.0 | MIT | Installed user scope | Smoke-tested on one isolated fixture; no workflow integration |
| TOOL-017 | Gitleaks | 8.30.1 | MIT | Installed user scope | Smoke-tested with one deterministic fake-secret fixture and redaction |
| TOOL-018 | Graphviz | 16.1.2 | EPL-1.0 | Installed user scope | Smoke-tested on one isolated DOT fixture; existing diagrams preserved |
| TOOL-019 | Structurizr | 2026.10.26 / 6.2.4 | Apache-2.0 | Deferred | Architecture option; no paid server authorized |
| TOOL-020 | Structurizr Lite | 2025.11.08 | Apache-2.0 | Rejected | Duplicate local architecture tooling without a demonstrated need |

Four internal skills were installed into project scope with `skills@1.5.22`: `task-contract`, `security-review`, `test-first` and `handoff`. Their installed copies match the canonical `.harness/skills/` sources by SHA-256. The running session catalog has not been reloaded, so they remain `INSTALLED`, not `AVAILABLE IN SESSION`.

The manifest holds the detailed capabilities, platforms, agent compatibility, dependencies, permissions, telemetry/privacy notes, conflicts, resource implications, reproducibility controls, commands and canonical sources for every row.

## 4. Selection policy

Use the smallest capability that closes an evidenced gap:

1. Prefer an existing repository script or instruction when it already satisfies the need.
2. Use deterministic local validation before adding an agentic framework.
3. Select one default specification workflow. OpenSpec is only the proposed candidate; do not activate OpenSpec, Spec Kit, BMAD and Superpowers as competing defaults.
4. Keep Jira as intended task authority. Do not replace it with Beads or another local tracker without a governance decision.
5. Treat browser, MCP, hosted documentation and remote repository tools as permissioned external boundaries.
6. No paid model, hosted evaluation, Structurizr server, production service or live crawling is authorized.
7. Do not install a tool merely to claim feature completeness.

## 5. Installation gate

Before running any proposed command:

- obtain an explicit owner decision for the candidate, version, environment and purpose;
- verify canonical repository, pinned version, license and release provenance;
- inspect dependencies, install scripts, permissions, telemetry and network behavior;
- confirm the observed runtime meets the candidate's version floor;
- create a clean task branch or disposable copy and record HEAD/status;
- define allowed paths, commands, credentials, network destinations and stop conditions;
- prepare rollback/uninstall/recovery steps;
- reject commands that wrap unreviewed remote scripts or require secrets in tracked files.

The exact proposed argv is stored in the manifest. `NOT_RUN` remains intentional for those proposals. Wave 1 commands that were actually executed are recorded separately in [activation evidence](../registry/installation/activation-evidence.json) with argv, exit code and observations. Do not edit `NOT_RUN` to `PASS` without running and observing the command.

## 6. Activation gate

Activation is separate from installation:

- prefer project-scoped skills/configuration over global defaults;
- preserve `AGENTS.md` authority and reject generated overwrites;
- expose only reviewed commands, tools and MCP functions;
- use least-privilege credentials and store secrets outside the repository;
- disable telemetry and update checks where the tool supports it and the approved policy requires it;
- document which agents/hosts are compatible; compatibility with one host is not universal compatibility;
- verify that a clean clone can reproduce the approved setup without user-scope packages.

## 7. MCP and credentials

| Candidate | Credential boundary | Current rule |
|---|---|---|
| Context7 | Remote documentation retrieval | Deferred; inspect request privacy and endpoint trust |
| Playwright MCP/CLI | Browser profile, downloads and navigation permissions | Deferred; use isolated profile and bounded origins |
| GitHub MCP Server | Fine-grained token, toolsets and read/write scopes | Deferred; prefer read-only local/remote mode after review |
| Draw.io MCP | Hosted or local service access | Deferred; do not send private diagrams to an unreviewed hosted service |
| Serena | Optional model backend and language-server processes | Deferred; review backend credentials, indexing paths and telemetry |
| OpenSpec / Spec Kit / BMAD | Normally no model key for local CLI work | Still require project-scoped workflow approval |

Never place tokens in the manifest, prompts, diagrams, test fixtures, logs or committed MCP configuration. A credential's existence does not authorize its use.

## 8. Verification and integration

A tool becomes `SMOKE TESTED` only after a bounded task demonstrates its intended capability with observed evidence. It becomes `INTEGRATED` only after the approved workflow acceptance criteria pass in a reproducible environment.

Record:

- exact version and source;
- host/OS, runtime versions and configuration;
- command and exit code;
- selected/attempted/executed/verified timestamps;
- generated or changed paths;
- security/permission observations;
- output excerpt and truncation status;
- runtime/token/cost only when actually measured;
- cleanup, rollback and known limitations.

The existing validator checks this manifest's structure and research semantics. It does not execute proposed commands or prove candidate effectiveness.

### Wave 1 observed evidence

The [activation evidence record](../registry/installation/activation-evidence.json) captures the controlled Wave 1 run on 2026-11-28:

- OpenSpec 2.2.0 was not installed because observed Node 22.18.0 is below its `>=22.20.0` requirement.
- Superpowers 7.0.2 remains deferred because host hook compatibility and autonomous defaults are not established.
- Four internal skills were installed at project scope and verified against canonical source hashes.
- Mermaid CLI 12.2.0 rendered an isolated router fixture to SVG and PNG using existing Playwright Chromium.
- Gitleaks 8.30.1 detected one deterministic fake `github-pat` fixture, returned expected exit code 1 and redacted the secret.
- Graphviz 16.1.2 rendered an isolated DOT fixture to SVG and PNG.
- Temporary smoke artifacts may disappear; exact commands and retained hashes are the durable evidence.

No candidate is claimed `INTEGRATED`, no full repository/history scan was run, and no existing repository diagram was regenerated.

## 9. Update, uninstall and recovery

- **Update:** review release notes and permission changes, test a pinned update in a disposable copy, then update the manifest deliberately.
- **Uninstall:** remove only the approved package/configuration and review generated project files; preserve approved specifications and evidence.
- **Recover:** restore generated integration files from Git, disable the skill/MCP, revoke exposed credentials if necessary and rerun repository validators.
- **Do not:** force-push, discard unrelated work, remove unfamiliar user-scope packages or delete product artifacts to complete an uninstall.

## 10. Implemented checks

```bash
python .harness/scripts/validate_tool_manifest.py
python -m unittest discover -s .harness/tests -p "test_tool_manifest.py" -v
```

These checks are implemented and tested. All install/activate/verify commands inside the manifest remain proposals; separate activation evidence records only the bounded Wave 1 commands actually observed.
