# 13C — Public API Decision

The API decision phase was read-only. It separated contracts already justified by evidence from behavior that would require new design.

## Accepted Tier-1 decisions

The later API hardening phase defined deliberate contracts for non-negative integer sampler shots, positive integer CHSH shot counts, qubit indices in `0..3`, and finite 16-element fidelity vectors without requiring exact norm one because of Q4.12 drift.

## Deferred decisions

File API error-style consistency was deferred because it is architectural and compatibility-sensitive. The sampler `progress=False` expectation was not converted into an API feature because no surviving implementation, documentation, call site, or history establishes its intended semantics.

## Result

The resulting decision record supported the isolated `df48f3a` Tier-1 hardening commit. No decision in this file should be interpreted as historical source recovery.

## Detailed record

The full decision report is in `reports/qgrim_13c_api_decision_report.md`, with the API inventory and boundary probe in `evidence/` or the source history referenced by the report.
