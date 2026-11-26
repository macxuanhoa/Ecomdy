# Business and technical workflows

> Target design / v0.1 / 2026-11-26. Not verified as-built.

## Collection
Scheduler → permitted connectors → raw provenance → normalize → hash/exact and semantic duplicate detection → classify/cluster → claim extraction → verify → rank/store → alert rules. Use freshness timestamps and retries; do not imply real-time coverage.

## Assistant
Intent/permission → database retrieval → targeted authorized fetch only if needed → grounded answer → evidence validation → response or draft. Insufficient evidence must be disclosed.

## Editorial
Select event → evidence/brand guidance → format-specific draft → validate figures and claims → review/edit → human approves exact version → export. Editing approved content invalidates approval. No auto-publish.

## Freshness audit
Import authorized published content → extract claims → compare current authoritative evidence and dates → flag conflict/expired/unverified → draft revision → human review.

## Trend ranking (extension)
Capture timestamped signals, market and source scope. Compare normalized volume, velocity, acceleration, recency, diversity and seller relevance. Example weights 30% velocity, 30% relevance, 15% recency, 10% diversity, 15% commercial potential; uncalibrated design hypothesis, not a forecast. Never equate limited observations with market-wide trends.

## Scheduling (proposal)
30–60 minutes for approved sources if limits allow; process new items on arrival; trend scoring hourly; digest weekly; freshness daily/weekly; source health and backups periodically. Disabled until deployment/configuration. Model use must be benchmarked by accuracy, latency, cost and Vietnamese quality, not vendor reputation.

[Diagram catalogue](diagrams/README.md).
