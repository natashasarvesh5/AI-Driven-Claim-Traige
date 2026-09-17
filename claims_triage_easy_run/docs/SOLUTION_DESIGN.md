# Solution design

## Problem interpretation
At first notice of loss, claims arrive with structured fields and free-text descriptions. Manual review delays assignment and may create inconsistent routing. The prototype converts the intake into three independent scores, assigns a priority, and recommends a queue.

## Functional requirements
1. Accept one claim or a local CSV.
2. Score urgency, complexity, and potential risk separately.
3. Assign Critical, High, Medium, or Low priority.
4. Route to Fast Track, General Adjuster, Urgent Response, Senior/Complex, or Special Investigation Review.
5. Explain every decision with reason codes and confidence.
6. Preserve an append-only local audit line for each submitted claim.
7. Keep a human reviewer accountable for downstream actions.

## Current-state architecture
Browser UI -> local HTTP server -> deterministic triage engine -> result + local JSONL audit log.

### Why rules first
The brief asks for a functional prototype without integrations. A transparent rules baseline demonstrates the full workflow immediately, allows business users to challenge thresholds, and avoids claiming model accuracy without labeled data. The next iteration can compare this baseline with a trained classifier.

## Scoring
- Urgency: time since loss, injuries, and emergency terms.
- Complexity: amount bands, parties, documents, claim context, and dispute/specialist terms.
- Risk: selected anomaly indicators, prior claims, amount, and missing evidence.
- Priority: maximum operational pressure across the three dimensions.
- Routing: risk exceptions first, then complexity, urgency, fast track, and general queue.

All thresholds in this prototype are illustrative and must be calibrated with claims SMEs and historical outcomes.

## Non-functional requirements
- Offline operation
- Deterministic results for identical inputs
- No secrets or customer data in the repository
- Accessible, responsive interface
- Human-in-the-loop
- Traceability through engine version and timestamp

## Future-state architecture
Channels/FNOL -> secure API gateway -> document ingestion/OCR -> feature service -> model endpoint + rules engine -> workflow orchestrator -> core claims platform/workforce queues. Cross-cutting services: identity, encryption, observability, model registry, drift/fairness monitoring, approval workflow, and audit warehouse.

## Production roadmap
1. Agree taxonomy, queues, SLA definitions, and ground-truth labels.
2. De-identify and profile historical claims.
3. Train interpretable baselines for priority and route; compare against current rules.
4. Measure per-class precision/recall, routing rework, time-to-assignment, calibration, and subgroup error rates.
5. Pilot in shadow mode, then recommendation mode with overrides.
6. Integrate APIs only after security, privacy, model-risk, and operational approvals.
7. Monitor drift, overrides, false escalations, missed urgent claims, and feedback.
