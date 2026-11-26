# API Design

**State:** Proposed REST resource contracts; no API server, authentication, or endpoints are implemented.

## API conventions

- Versioned prefix candidate: `/api/v1`.
- JSON request/response bodies; UTC timestamps in ISO 8601; opaque IDs.
- Every derived resource includes provenance references and a state.
- Mutations are authenticated and authorized; sensitive actions create audit events.
- Pagination, filtering, idempotency, rate limits, and error format must be specified before implementation.
- External URLs, prompts, and source text are untrusted input. API access must not allow a user to expand connector permissions.

## Proposed resource groups

| Resource | Example routes | Intended behavior |
|---|---|---|
| Sources | `GET /sources`, `POST /sources`, `GET /sources/{id}`, `PATCH /sources/{id}` | List and manage source profiles; activate only after terms/access review. |
| Ingestion | `POST /ingestion-jobs`, `GET /ingestion-jobs/{id}` | Request a bounded permitted run and inspect status; not a public arbitrary URL fetcher. |
| Articles/events | `GET /articles`, `GET /events`, `GET /events/{id}` | Retrieve normalized records with source and version references. |
| Claims/evidence | `GET /claims/{id}`, `GET /claims/{id}/evidence` | Show claim state, source spans, evidence URL, observation/effective dates. |
| Digests | `POST /digests`, `GET /digests/{id}`, `GET /digests/{id}/items` | Create/read a draft for an authorized period and market. |
| Content drafts | `POST /content-drafts`, `GET /content-drafts/{id}`, `POST /content-drafts/{id}/versions` | Create draft versions from selected evidence; edits create new versions. |
| Editorial actions | `POST /content-versions/{id}/reviews`, `POST /content-versions/{id}/approvals` | Review and approve an exact version; authorization and state checks required. |
| Content audit | `POST /content-audits`, `GET /content-audits/{id}` | Audit only authorized published content; return findings for human review. |
| Administration | `GET /health`, `GET /admin/source-health`, `GET /admin/quality` | Operational health and measured metrics; do not expose secrets or private data. |

## Editorial state proposal

`draft → in_review → changes_requested → draft`; or `draft/in_review → approved`. Any content edit creates a new version in `draft` and invalidates approval of the earlier content as current. Export/publish is a separate authorized action and is outside the current scope. State transitions must be enforced server-side, not only in UI.

## Error and evidence rules

- Return explicit `insufficient_evidence`, `unverified`, `stale`, and `source_unavailable` states; never substitute an empty success response.
- Validation errors identify the field and stable error code without leaking internals.
- Generated responses expose citations and supporting claim IDs; citation URLs are validated and rendered safely.
- Record actor, action, resource/version, request ID, and timestamp for review/approval/configuration changes.
- A future OpenAPI document should be generated from implemented contracts and checked against integration tests.
