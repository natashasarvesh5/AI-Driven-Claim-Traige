# AI-Driven Claims Triage Prototype

A dependency-free, local-first proof of concept that classifies insurance claims by **urgency**, **complexity**, and **risk**, then recommends a handling queue with transparent reason codes.

## Why this project matches the brief
- No external APIs, cloud calls, keys, databases, or package installation.
- Working end-to-end demo using mock JSON/CSV data and local processing.
- Dashboard, single-claim intake, bulk CSV simulation, routing, explanations, confidence, and audit logging.
- Clear future-state roadmap while keeping the prototype safe and demonstrable.

## Run
Requires Python 3.9+.

```bash
cd claims_triage_project
python -m app.server
```
Open http://localhost:8000

## Test
```bash
python -m unittest discover -s tests -v
```

## Demo flow
1. Open **Dashboard** and show prioritized queues.
2. Filter to Critical or High claims.
3. Open **Triage a claim**, change the description or amount, and run triage.
4. Explain urgency, complexity, risk, route, confidence, and reason codes.
5. Open **Bulk CSV**, use `data/sample_claims.csv`, and show local batch processing.
6. Open **Roadmap** to contrast current and future states.
7. Show `data/audit_log.jsonl` as the decision trail.

## Prototype logic
This is a hybrid baseline: deterministic text signals plus structured business features. It is intentionally explainable and easy to validate before labeled historical data is available. It makes a routing recommendation only. It does not approve, deny, reserve, or settle claims.

## Project structure
- `app/triage_engine.py`: local scoring and routing engine
- `app/server.py`: dependency-free web server and API
- `static/`: interface
- `data/`: synthetic sample input and audit log
- `tests/`: unit tests
- `docs/`: requirements, architecture, model card, and demo script

## Research basis
Claims triage commonly evaluates severity/complexity, risk, and routing, with simple claims directed to fast-track handling and exceptions to specialist review. NIST's AI RMF emphasizes valid/reliable, accountable/transparent, explainable/interpretable, privacy-enhanced, and fair AI. The prototype therefore includes reason codes, confidence, human accountability, and audit records.

Sources:
- NIST AI RMF: https://www.nist.gov/itl/ai-risk-management-framework
- NIST AI RMF Core: https://airc.nist.gov/airmf-resources/airmf/5-sec-core/
- Scikit-learn text classification example for the future ML baseline: https://scikit-learn.org/stable/auto_examples/text/plot_document_classification_20newsgroups.html
