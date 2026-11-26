# Diagram catalogue

All diagrams are target designs, not as-built evidence. Mermaid and DOT are editable; PNG and SVG are rendered from DOT.

**Metadata:** Numbered source files carry diagram IDs, version `0.1`, and target state in source comments. The 12 initial diagrams have local PNG/SVG assets. Supplemental Mermaid files render directly when opened on GitHub; separate PNG/SVG assets were not generated because Graphviz is unavailable. See [GitHub Mermaid rendering](https://docs.github.com/en/repositories/working-with-files/using-files/working-with-non-code-files#displaying-mermaid-files-on-github).

## Workspace bootstrap

![Workspace bootstrap](01-bootstrap.svg)

[PNG](01-bootstrap.png) · [SVG](01-bootstrap.svg) · [Mermaid](01-bootstrap.mmd) · [DOT](01-bootstrap.dot)

<details><summary>Mermaid source rendered by GitHub</summary>

```mermaid
flowchart TD
  n0["Detect environment"]
  n1["Inventory repository"]
  n2["Configure project profile"]
  n3["Index inputs"]
  n4["Generate context update prompt"]
  n5["Owner approves baseline"]
  n0 --> n1
  n1 --> n2
  n2 --> n3
  n3 --> n4
  n4 --> n5
```

</details>

## DevHarness control plane

![DevHarness control plane](02-control-plane.svg)

[PNG](02-control-plane.png) · [SVG](02-control-plane.svg) · [Mermaid](02-control-plane.mmd) · [DOT](02-control-plane.dot)

<details><summary>Mermaid source rendered by GitHub</summary>

```mermaid
flowchart TD
  owner["Project owner"]
  cli["CLI / dashboard / IDE"]
  orch["Orchestrator / state machine"]
  ctx["Context / memory / repository index"]
  plan["Specification / planning / prompts"]
  exec["Agents / skills / tool adapters"]
  qa["Tests / review / policy gates"]
  auto["Scheduler / observability"]
  repo["Workspace / Git / documents / state"]
  owner --> cli
  cli --> orch
  orch --> ctx
  orch --> plan
  orch --> exec
  exec --> qa
  orch --> auto
  ctx --> repo
  plan --> repo
  qa --> repo
  auto --> repo
```

</details>

## Progressive context loading

![Progressive context loading](03-context.svg)

[PNG](03-context.png) · [SVG](03-context.svg) · [Mermaid](03-context.mmd) · [DOT](03-context.dot)

<details><summary>Mermaid source rendered by GitHub</summary>

```mermaid
flowchart TD
  n0["L0 — Core rules"]
  n1["L1 — Project summary"]
  n2["L2 — Task contract"]
  n3["L3 — Relevant knowledge"]
  n4["L4 — Original files and source code"]
  n0 --> n1
  n1 --> n2
  n2 --> n3
  n3 --> n4
```

</details>

## Document intake

![Document intake](04-document-ingestion.svg)

[PNG](04-document-ingestion.png) · [SVG](04-document-ingestion.svg) · [Mermaid](04-document-ingestion.mmd) · [DOT](04-document-ingestion.dot)

<details><summary>Mermaid source rendered by GitHub</summary>

```mermaid
flowchart TD
  n0["Discover / checksum"]
  n1["Extract content (adapter)"]
  n2["Extract requirements with provenance"]
  n3["Detect conflicts / questions"]
  n4["Propose context delta"]
  n5["Human approval"]
  n6["Versioned baseline"]
  n0 --> n1
  n1 --> n2
  n2 --> n3
  n3 --> n4
  n4 --> n5
  n5 --> n6
```

</details>

## Agent role routing

![Agent role routing](05-agent-team.svg)

[PNG](05-agent-team.png) · [SVG](05-agent-team.svg) · [Mermaid](05-agent-team.mmd) · [DOT](05-agent-team.dot)

<details><summary>Mermaid source rendered by GitHub</summary>

```mermaid
flowchart TD
  o["Owner"]
  m["Master orchestrator"]
  p["Discovery / planning / architect"]
  i["Implementation / UI / database"]
  q["QA / reviewer / security"]
  k["DevOps / documentation / context"]
  o --> m
  m --> p
  m --> i
  m --> q
  m --> k
```

</details>

## Bounded Ralph-style execution

![Bounded Ralph-style execution](06-bounded-loop.svg)

[PNG](06-bounded-loop.png) · [SVG](06-bounded-loop.svg) · [Mermaid](06-bounded-loop.mmd) · [DOT](06-bounded-loop.dot)

<details><summary>Mermaid source rendered by GitHub</summary>

```mermaid
flowchart TD
  s["Select approved task"]
  c["Load scoped context"]
  i["Implement minimal change"]
  v["Run gates / tests"]
  r["Independent review"]
  p["Checkpoint / update state"]
  f["Diagnose / bounded retry"]
  b["BLOCKED / approval / budget stop"]
  s --> c
  c --> i
  i --> v
  v -->|pass| r
  v -->|fail| f
  f -->|retry allowed| i
  f -->|limit reached| b
  r -->|pass| p
  r -->|fail| f
  p -->|next task| s
```

</details>

## Planning hierarchy

![Planning hierarchy](07-planning.svg)

[PNG](07-planning.png) · [SVG](07-planning.svg) · [Mermaid](07-planning.mmd) · [DOT](07-planning.dot)

<details><summary>Mermaid source rendered by GitHub</summary>

```mermaid
flowchart TD
  n0["Product vision"]
  n1["Requirements / evidence"]
  n2["Epics / features"]
  n3["Stories / tasks"]
  n4["Scope + dependencies + acceptance"]
  n5["Owner approval"]
  n6["Execution contract"]
  n0 --> n1
  n1 --> n2
  n2 --> n3
  n3 --> n4
  n4 --> n5
  n5 --> n6
```

</details>

## Verification gates

![Verification gates](08-quality-gates.svg)

[PNG](08-quality-gates.png) · [SVG](08-quality-gates.svg) · [Mermaid](08-quality-gates.mmd) · [DOT](08-quality-gates.dot)

<details><summary>Mermaid source rendered by GitHub</summary>

```mermaid
flowchart TD
  n0["Scope compliance"]
  n1["Build / lint / type checks"]
  n2["Functional / regression tests"]
  n3["Security / accessibility as applicable"]
  n4["Independent review"]
  n5["Documentation reconciliation"]
  n6["Acceptance evidence"]
  n0 --> n1
  n1 --> n2
  n2 --> n3
  n3 --> n4
  n4 --> n5
  n5 --> n6
```

</details>

## Harness improvement loop

![Harness improvement loop](09-learning.svg)

[PNG](09-learning.png) · [SVG](09-learning.svg) · [Mermaid](09-learning.mmd) · [DOT](09-learning.dot)

<details><summary>Mermaid source rendered by GitHub</summary>

```mermaid
flowchart TD
  a["Observe failure"]
  b["Root cause"]
  c["Propose skill / workflow change"]
  d["Regression evaluation"]
  e["Human approval"]
  f["Measure benchmark delta"]
  a --> b
  b --> c
  c --> d
  d --> e
  e --> f
  f --> a
```

</details>

## Diagram skill pipeline

![Diagram skill pipeline](10-diagram-pipeline.svg)

[PNG](10-diagram-pipeline.png) · [SVG](10-diagram-pipeline.svg) · [Mermaid](10-diagram-pipeline.mmd) · [DOT](10-diagram-pipeline.dot)

<details><summary>Mermaid source rendered by GitHub</summary>

```mermaid
flowchart TD
  n0["Inspect approved spec or actual code"]
  n1["Extract semantic model / provenance"]
  n2["Generate Mermaid / DOT"]
  n3["Render SVG and PNG"]
  n4["Validate edges / labels / state"]
  n5["Review and commit"]
  n0 --> n1
  n1 --> n2
  n2 --> n3
  n3 --> n4
  n4 --> n5
```

</details>

## Scheduled development jobs

![Scheduled development jobs](11-automation.svg)

[PNG](11-automation.png) · [SVG](11-automation.svg) · [Mermaid](11-automation.mmd) · [DOT](11-automation.dot)

<details><summary>Mermaid source rendered by GitHub</summary>

```mermaid
flowchart TD
  n0["Schedule / manual trigger"]
  n1["Validate approved task / permissions"]
  n2["Acquire workspace lock"]
  n3["Run with budget / timeout"]
  n4["Persist checkpoint / log"]
  n5["Report status — no auto merge"]
  n0 --> n1
  n1 --> n2
  n2 --> n3
  n3 --> n4
  n4 --> n5
```

</details>

## Harness roadmap

![Harness roadmap](12-roadmap.svg)

[PNG](12-roadmap.png) · [SVG](12-roadmap.svg) · [Mermaid](12-roadmap.mmd) · [DOT](12-roadmap.dot)

<details><summary>Mermaid source rendered by GitHub</summary>

```mermaid
flowchart TD
  n0["V0.1 Foundation"]
  n1["V0.2 Context"]
  n2["V0.3 Planning"]
  n3["V0.4 Execution and verification"]
  n4["V0.5 Automation"]
  n5["V0.6 Skills and agent adapters"]
  n6["V0.7 Diagrams / dashboard"]
  n7["V1.0 Release benchmark"]
  n0 --> n1
  n1 --> n2
  n2 --> n3
  n3 --> n4
  n4 --> n5
  n5 --> n6
  n6 --> n7
```

</details>

## Additional harness architecture and workflow diagrams

These sources fill the component, memory, skill/tool, prompt, dependency, review, approval, recovery, security, and CI/CD gaps. Each Mermaid file includes ID, version, and target-state metadata and renders on GitHub when opened.

| ID | Diagram | Editable / rendered Mermaid source |
|---|---|---|
| HARNESS-D13 | Harness Component Architecture | [13-component-architecture.mmd](13-component-architecture.mmd) |
| HARNESS-D14 | Memory and Context Layers | [14-memory-architecture.mmd](14-memory-architecture.mmd) |
| HARNESS-D15 | Skill Loading Mechanism | [15-skill-loading.mmd](15-skill-loading.mmd) |
| HARNESS-D16 | Tool and MCP Integration | [16-tool-mcp-integration.mmd](16-tool-mcp-integration.mmd) |
| HARNESS-D17 | Prompt Compilation Pipeline | [17-prompt-compilation.mmd](17-prompt-compilation.mmd) |
| HARNESS-D18 | Task Dependency Graph | [18-task-dependency-graph.mmd](18-task-dependency-graph.mmd) |
| HARNESS-D19 | Bounded Debugging Workflow | [19-debugging-workflow.mmd](19-debugging-workflow.mmd) |
| HARNESS-D20 | Independent Review Workflow | [20-independent-review.mmd](20-independent-review.mmd) |
| HARNESS-D21 | Human Approval Boundaries | [21-human-approval.mmd](21-human-approval.mmd) |
| HARNESS-D22 | Checkpoint and Resume Workflow | [22-checkpoint-resume.mmd](22-checkpoint-resume.mmd) |
| HARNESS-D23 | Security and Permission Boundaries | [23-security-permissions.mmd](23-security-permissions.mmd) |
| HARNESS-D24 | CI/CD Validation and Release Boundary | [24-ci-cd-pipeline.mmd](24-ci-cd-pipeline.mmd) |
