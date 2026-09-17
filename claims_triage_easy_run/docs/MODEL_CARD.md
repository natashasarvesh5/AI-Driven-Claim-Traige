# Prototype model card

## Intended use
Decision support for initial queue assignment using synthetic demonstration data.

## Not intended for
Coverage decisions, claim denial, settlement, reserve estimation, fraud accusations, medical decisions, or fully autonomous handling.

## Method
Version `prototype-rules-1.0` is a deterministic scoring engine, not a trained AI model. It processes structured inputs and transparent keyword signals locally.

## Key risks
- Illustrative thresholds may not reflect actual operations.
- Keyword matching can miss context, negation, spelling variants, or multilingual text.
- Synthetic data cannot establish accuracy or business impact.
- Historical labels may reproduce prior inconsistencies or bias.
- Risk flags are review signals, not evidence of wrongdoing.

## Controls
Human review, reason codes, missing-field disclosure, confidence reduction, engine versioning, audit log, test cases, and no automated adverse action.

## Required production evaluation
Confusion matrices per priority/route, class-level precision/recall/F1, urgent-claim recall, calibration, subgroup error analysis where legally and ethically appropriate, override rate, routing rework, and time-to-assignment.
