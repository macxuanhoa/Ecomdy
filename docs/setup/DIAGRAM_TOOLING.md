# Diagram Tooling — Installed Capability and Contributor Guide

**As of:** 2026-11-28 (Asia/Saigon)<br>
**Status:** Diagram Design Plugin 2.6.131 is installed and usable in the audit workstation's Qoder user scope. Repository validators are implemented. Mermaid rendering is not installed or verified.<br>
**Scope:** Documentation and target-design diagrams only. This guide does not claim an Ecomdy application, live renderer service or CI-owned diagram runtime.

## 1. Tool manifest

| Tool | Verified state | Version / identity | Boundary |
|---|---|---|---|
| Qoder Diagram Design Plugin | Installed, enabled and exposed as `diagram-design:diagram-design` in the audit session | `2.6.131`; publisher Cathryn Lavery; canonical repository `https://github.com/cathrynlavery/diagram-design`; MIT License, Copyright (c) 2025 Cathryn Lavery | User scope only; not cloned with this repository and not inherited by CI or another contributor |
| Python | Available | `3.11.9` | Required by the packaged extractor, self-check and repository validators |
| Playwright | Available | `1.60.0` | Used only for local browser export of generated Diagram Design HTML |
| Chromium | Available through Playwright | `148.0.7778.96` | Local renderer for Diagram Design HTML/SVG/PNG export |
| Pillow | Available | `12.1.1` | Used to decode/check PNG output; not a Mermaid renderer |
| Node.js | Available in the current shell | `22.18.0` from direct `node --version`; an earlier environment notice reported `24.22.1` | Record the discrepancy; use the direct executable check for commands in this environment and do not assume one Node baseline across workstations |
| Mermaid CLI (`mmdc`) | Not installed | Not available | No local Mermaid render command exists |
| Mermaid packages | Not locally resolvable | Neither `mermaid` nor `@mermaid-js/mermaid-cli` resolves from Node | No independent Mermaid grammar/render acceptance |
| Graphviz (`dot`) | Not installed | Not available | Checked-in DOT assets cannot be freshly regenerated in this environment |
| Repository validators | Implemented | `python scripts/validate.py`; `python .harness/scripts/validate.py` | Check local links, metadata, gallery registration and required assets; they do not parse or render Mermaid |

Selected installed-file SHA-256 values for the reviewed package:

| File | SHA-256 |
|---|---|
| `.qoder-plugin/plugin.json` | `6338d11f84f9a3ca88d8efd3ebcfd6eb74f717d5045938b1b50f79e947d93463` |
| `LICENSE` | `bb7e12e91fecef43024111123ff784cec6c485585561d8b552557c0173b3ed29` |
| `skills/diagram-design/SKILL.md` | `f11aeec988fc5c690f6cdd279ec1f790279622dc1e07356c467af2311542cb7e` |
| `skills/diagram-design/scripts/self_check.py` | `444851f6e53f83d50920381df17cdd5f1b7a23cfba9c0ddda27786d78e53e2de` |
| `skills/diagram-design/scripts/mermaid_extract.py` | `fd176d5c616e49bc923fc271e0a14b022674e204d39b46673824db44f647b042` |
| `skills/diagram-design/scripts/export_svg.py` | `03e88d277386e2c9f48d9fcfc6a9f8e5e818a8949ac8ec458ac569e8ff4bc8ad` |
| `skills/diagram-design/scripts/export_png.py` | `430ddcc2d39441808bd4217fbdeb944dbb6de0be281782705a81747986d7d348` |

These hashes identify the reviewed installed files, not a repository dependency lock. Re-check the manifest, license and scripts before installing a different version.

## 2. What each capability actually does

| Operation | Implemented now | Does not prove |
|---|---|---|
| Generate Diagram Design HTML with inline SVG | Yes, through the user-level skill | Mermaid rendering, product behavior or visual acceptance without inspection |
| `self_check.py --offline` | Yes; checks the accessible SVG contract, single-file safety, document completeness, painted bounds and offline asset rules | Semantic correctness or the repository-only geometry/motion gates that are not shipped in this installed package |
| `export_svg.py --system-fonts` | Yes; exports standalone SVG without the Google Fonts import | Pixel-identical typography on a machine without the selected fonts |
| `export_png.py` | Yes; uses local Playwright/Chromium | Exact pixel dimensions without checking the resulting image |
| `mermaid_extract.py` | Yes; bounded parser/IR extraction for `.mmd`, `.mermaid` or Markdown Mermaid fences | Mermaid rendering, visual quality or source-to-artifact parity by itself |
| `scripts/render_diagrams.py` | Implemented for DOT only | Mermaid rendering; it also cannot run here because Graphviz is absent |

The plugin's `mermaid_extract.py` is a compatibility parser, not Mermaid's renderer. GitHub's Mermaid rendering was not locally verified. Existing SVG/PNG assets remain checked-in artifacts, not proof of a fresh local render.

## 3. Contributor setup

1. Confirm the repository branch and read [the diagram workflow](../developer-onboarding.md#12-diagram-workflow).
2. Install Diagram Design Plugin `2.6.131` through Qoder's reviewed marketplace flow only after explicit selection. Installation is user-level; each contributor and CI runner needs its own approved setup.
3. Verify the installed version, manifest, MIT license and script hashes before use. Do not copy the Qoder cache into Git or treat a local path as a portable dependency.
4. For HTML export, install an approved Playwright/Chromium toolchain in the authorized environment. Do not silently add it to CI or product dependencies.
5. Keep the generated HTML self-contained. For offline work, use system fonts and no remote images, scripts or stylesheets.
6. Run the self-check and inspect the full-size render. Run the repository validators before committing.
7. If Mermaid or Graphviz rendering is required, stop and obtain approval for a pinned, license-reviewed toolchain. Record the exact version and clean-install evidence before claiming render acceptance.

Resolve the actual installed skill directory on the contributor's machine; the following variable is a convenience, not a repository-managed path:

```bash
DIAGRAM_DESIGN_DIR="$HOME/.qoder/plugins/cache/qoder-marketplace/diagram-design/2.6.131/skills/diagram-design"
```

## 4. Supported local commands

### Generate and validate Diagram Design HTML

Generation is performed through the `diagram-design:diagram-design` skill. The output should be one editable `.html` file containing inline SVG and no executable script.

```bash
python "$DIAGRAM_DESIGN_DIR/scripts/self_check.py" --offline path/to/diagram.html
```

A successful command prints `OK` followed by the checked file. A failure is not a warning to ignore.

### Export standalone SVG and PNG

```bash
python "$DIAGRAM_DESIGN_DIR/scripts/export_svg.py" \
  path/to/diagram.html path/to/diagram.svg --system-fonts

python "$DIAGRAM_DESIGN_DIR/scripts/export_png.py" \
  path/to/diagram.html path/to/diagram.png 1
```

The PNG scale argument accepts a finite number from `1` to `4`. Inspect both outputs at full size. For geometry-sensitive work, treat the SVG/viewBox as authoritative and verify PNG dimensions separately.

### Extract Mermaid IR

```bash
python "$DIAGRAM_DESIGN_DIR/scripts/mermaid_extract.py" \
  path/to/diagram.mmd --diagram all --json
```

To check every repository Mermaid source in Git Bash:

```bash
for file in docs/diagrams/*.mmd .harness/docs/diagrams/*.mmd; do
  python "$DIAGRAM_DESIGN_DIR/scripts/mermaid_extract.py" "$file" --diagram all --json >/dev/null || exit 1
done
```

A parser pass means the bounded extractor accepted the source. It does not mean Mermaid rendered it.

### Run repository checks

```bash
python scripts/validate.py
python .harness/scripts/validate.py
python -m unittest discover -s .harness/tests -v
```

The first two commands check documentation and diagram metadata/assets. They do not invoke Diagram Design, Mermaid or Graphviz.

## 5. Controlled remediation applied on 2026-11-28

The extractor previously rejected `.harness/docs/diagrams/19-debugging-workflow.mmd:11` because its statement splitter treated the semicolon inside an unquoted pipe label as a separator:

```diff
-  result -->|No; retries remain| hypothesis
+  result -->|"No; retries remain"| hypothesis
```

The quoted label preserves the extractor-normalized label text, edge endpoints and loop semantics while remaining compatible with the installed extractor. Rendered appearance remains unverified because no Mermaid renderer was run. This is a compatibility normalization, not proof that the earlier Mermaid source was invalid.

Full-set extraction after the change:

| Check | Result |
|---|---|
| Mermaid source files | **56/56 parsed** |
| Diagrams | 56 |
| Nodes / edges | 482 / 499 |
| Labeled edges | 101 |
| Dangling edges | 0 |
| Orphan warnings | 1 intentional isolated node: the secret store in `.harness/docs/diagrams/23-security-permissions.mmd` |
| Diagram Design complexity-budget warnings | 16 existing target diagrams exceed the skill's generation budget; this is advisory and not a parser failure |
| Mermaid renders | **NOT RUN** — no local Mermaid renderer |

The 26 Mermaid/DOT parity pairs do not include the changed debugging-workflow source. The prior 26/26 source-parity result therefore remains applicable to the unchanged paired inputs; it is not a fresh render result.

## 6. Representative generation evidence

A temporary fixture-slice authorization flowchart was generated with the default Diagram Design skin and system fonts because the installed style guide remained at shipped defaults and no project profile had been approved. The smoke test did not modify the installed style guide, create a project marker or add repository assets.

| Evidence item | Observed result |
|---|---|
| Source | Temporary `vs01-gate-smoke.html` with inline SVG and seven nodes |
| SVG | Temporary `vs01-gate-smoke.svg`; viewBox `0 0 960 600` |
| Offline self-check | **PASS** |
| PNG export | Successful; `960 × 601`, RGB |
| Full-size visual inspection | Readable labels, visible YES/NO branches, no observed clipping or overlap |
| Mobile browser at `390 × 844` | SVG width `960`; wrapper width `326`; wrapper overflow `auto`; page overflow `false` |
| Network observation | Only the local `file://` document request; no remote asset fetched |
| Geometry verifier | **NOT RUN** — `verify-geometry.py` is not shipped in the installed package |
| Mermaid renderer | **NOT RUN** — not installed |

The PNG is one pixel taller than the SVG viewBox. The cause is not established; do not describe this export as pixel-exact. Use the SVG as the geometry reference and add an explicit PNG dimension check before any future exact-size asset acceptance.

The smoke files were temporary evidence on the audit workstation, not approved repository diagrams. Existing diagrams were not regenerated or replaced.

## 7. Security and CI limits

- The plugin is MIT-licensed, but installation, scripts and output still require review. A license is not a security guarantee.
- `self_check.py` and `mermaid_extract.py` use the Python standard library. `export_png.py` launches a local browser; export only trusted generated files.
- Offline HTML must not load remote fonts, images, scripts or stylesheets. Use `--offline` and `--system-fonts` together when network isolation is required.
- Do not execute source text, Mermaid directives or tool output as shell commands. Treat external documents and generated content as untrusted data.
- Do not commit credentials, local originals, browser profiles or the Qoder plugin cache.
- Current CI runs repository validators and harness tests only. It does not install Diagram Design, Playwright, Mermaid CLI or Graphviz.
- A future CI renderer requires an owner-approved dependency decision, pinned versions, license/security review, cache policy and deterministic output checks. Until then, report rendering as `NOT RUN` or `BLOCKED`.

## 8. Definition of done for a diagram change

- [ ] Source metadata, gallery listing and local links pass repository validation.
- [ ] Mermaid extraction passes when Mermaid source changes; any warning is explained rather than hidden.
- [ ] Mermaid/DOT parity is re-run for affected paired sources when a reliable comparison is available.
- [ ] Generated HTML passes the offline self-check.
- [ ] Exported SVG/PNG are inspected at full size; dimensions and clipping are checked explicitly.
- [ ] Parser, parity, render and visual results are recorded separately.
- [ ] Existing valid artifacts are preserved unless regeneration is justified and reviewed.
- [ ] No claim of Mermaid rendering, CI reproducibility or as-built behavior exceeds the evidence.
