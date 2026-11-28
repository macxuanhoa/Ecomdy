# Documentation Portal

## Start here

1. [Comprehensive project audit](setup/COMPREHENSIVE_AUDIT.md)
2. [Repository map](repository-map.md)
3. [Project Owner guide](project-owner-guide.md)
4. [Developer onboarding and playbook](developer-onboarding.md)
5. [Phase 0 acceptance and controlled continuation](setup/PHASE_0_ACCEPTANCE.md)
6. [Phase 1 transition checkpoint](setup/PHASE_1_TRANSITION.md)
7. [Capability coverage matrix](setup/CAPABILITY_COVERAGE.md)
8. [Jira-first setup plan](setup/JIRA_SETUP_PLAN.md) and [import-ready backlog](setup/JIRA_IMPORT_BACKLOG.csv)
9. [Phase 1 requirements delta](phase1-requirements-delta.md)
10. [Phase 1 architecture delta](phase1-architecture-delta.md)
11. [First vertical-slice implementation plan](vertical-slice-01-plan.md)
12. [VS01 owner approval pack](vs01-owner-approval-pack.md)
13. [Team development readiness](team-development-readiness.md)
14. [Project context and current state](project-context.md)
15. [Official requirements register](01-requirements.md)
16. [Environment and capability audit](setup/00_ENVIRONMENT_AND_CAPABILITY_AUDIT.md)
17. [Requirements traceability](requirements-traceability.md)
18. [Implementation roadmap](05-roadmap.md)

## Product specification

- [Product Requirements Document](product-requirements.md)
- [Software Requirements Specification](software-requirements-specification.md)
- [Project Constitution](project-constitution.md)
- [Product vision and capability registry](02-product-vision.md)
- [Target architecture and candidate stack](03-architecture.md)
- [Phase 1 requirements delta](phase1-requirements-delta.md)
- [Phase 1 architecture delta](phase1-architecture-delta.md)
- [Workflows](04-workflows.md)
- [Validation strategy](06-validation.md)
- [Module specifications](module-specifications.md)
- [Database design](database-design.md)
- [API design](api-design.md)
- [Security and governance](security-governance.md)
- [Agent and tool registry](agent-tool-registry.md)
- [Automation specification](automation-specification.md)
- [Context engineering](context-engineering.md)
- [Deployment strategy](deployment-strategy.md)
- [Risk register](risk-register.md)
- [Sprint planning](sprint-planning.md)
- [Product task register](task-register.md)
- [Technology and harness evaluation](technology-evaluation.md)
- [Definition of Ready / Done](definition-of-ready-done.md)
- [Repository map](repository-map.md)
- [Project Owner guide](project-owner-guide.md)
- [Developer onboarding and playbook](developer-onboarding.md)
- [Developer operations matrix](developer-operations.md)
- [Minimum Viable DevHarness plan](minimum-viable-harness-plan.md)
- [Team development readiness](team-development-readiness.md)
- [First vertical-slice plan](vertical-slice-01-plan.md)
- [VS01 owner approval pack](vs01-owner-approval-pack.md)
- [Target user guide](user-guide.md)
- [Harness installation guide](harness-installation-guide.md)
- [Constraints and assumptions](constraints-assumptions.md)
- [Conflict reconciliation](conflict-report.md)
- [Open questions](open-questions.md)
- [Source registry and input inventory](source-registry.md)

## Diagrams and setup

- [Ecomdy diagram gallery](diagrams/README.md)
- [DevHarness diagram gallery](../.harness/docs/diagrams/README.md)
- [Setup plan](setup/SETUP_PLAN.md)
- [Task registry](setup/TASK_REGISTRY.md)
- [Phase 1 transition checkpoint](setup/PHASE_1_TRANSITION.md)
- [Execution status](setup/EXECUTION_STATUS.md)
- [Decision log](setup/DECISION_LOG.md)
- [Blockers](setup/BLOCKERS.md)
- [Verification report](setup/VERIFICATION_REPORT.md)
- [Diagram tooling and contributor guide](setup/DIAGRAM_TOOLING.md)
- [Handoff](setup/HANDOFF.md)

## Source authority and confidentiality

`docs/00-original/` stores local source files and is ignored by Git except for its README. The public challenge workbook is the authority for official requirements. The blueprint, business plan, and image notes inform proposed target design only. Check the [source registry](source-registry.md) and [source manifest](source-manifest.json) before using an input or changing its publication status.

## Current-state reminder

The repository is currently a documentation and diagram scaffold with a local validator. Product runtime, deployment, interviews, feedback, and benchmarks are not evidenced. Target architecture is not as-built architecture. The [Phase 0 verdict](setup/PHASE_0_ACCEPTANCE.md) and [comprehensive audit](setup/COMPREHENSIVE_AUDIT.md) conditionally accept the documentation/setup baseline only. Default `main` remains unusable for onboarding until PR #1 merges; authenticated governance read-back is complete, while Jira, real ownership, CI-safe Mermaid rendering and harness enforcement remain open.
