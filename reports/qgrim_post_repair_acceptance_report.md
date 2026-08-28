# QGRIM Post-repair Acceptance Audit — 12A–12C

## Acceptance result

The controlled post-repair acceptance phase is complete. The engineering branch passed the full independent 12A integration matrix, the 12B numerical audit characterized expected Q4.12 behavior and two deferred boundary weaknesses, and 12C explicitly retained the sampler ambiguity without changing code or tests.

The accepted baseline is frozen at:

```text
qgrim-engineering-qft-grover → be28bf0
```

| Reference | State |
|---|---|
| Historical `main` | `a504f6c`, unchanged |
| Recovery branch `qgrim-recovery` | `72edc13`, unchanged |
| Engineering branch | `be28bf0`, clean |
| Repository tests modified during 12A–12C | None |
| Pushes | None |

## 12A — Engineering integration audit

An external integration harness checked the combined repaired system without modifying repository files. All 18 checks passed.

| Area | Result |
|---|---|
| Hadamard state and Q4.12 norm boundary | Pass; one-H norm `0.9997864` within expected tolerance |
| CNOT basis-state evolution | Pass |
| Bell-state entropy | Pass; single-qubit entropy `1.0000945` |
| Entropy internal partition | Pass; approximately zero |
| Entropy invalid-input boundary | Pass; duplicate, negative, and out-of-range indices rejected |
| Bloch `|0⟩`, `|+⟩`, and `|+i⟩` coordinates | Pass |
| Teleportation | Pass; all four measurement branches reached and corrected |
| QFT execution and norm | Pass |
| Grover target amplification | Pass; target probability `0.47265625` |
| Measurement collapse | Pass |
| Seeded sampling reproducibility and shot count | Pass |
| Noise distribution change | Pass |
| Invalid assembler qubit API boundary | Pass |
| `progress=False` status | Correctly preserved as unsupported/ambiguous |

The integration audit summary was:

```text
passed=18 failed=0 total=18
```

This establishes cross-component coherence for the repaired algorithms and previously repaired simulator behavior. It does not claim universal quantum-semantic verification beyond the tested matrix.

## 12B — Q4.12 numerical-boundary audit

The numerical audit deliberately exercised repeated Hadamards, tiny amplitudes, near-zero probabilities, phase wrapping, degenerate and near-degenerate spectra, entropy near zero and one, QFT round trips, Grover amplification, repeated execution, and invalid numeric inputs.

### Expected numerical characteristics

The Q4.12 model produces quantization effects at the expected scale. A single Hadamard has norm `0.999786376953125`; repeated Hadamards in the tested sequence returned to norm 1.0. Tiny amplitudes near the Q4.12 grid can disappear or change the resulting norm by approximately `1e-4`. The near-zero probability probe remained non-negative and had total norm `1.000131666660309`.

Entropy remained stable at the boundaries tested:

| State/cut | Result |
|---|---:|
| Product-state entropy | `0.0` |
| Bell-state entropy | `1.0000945369` |
| Near-product state entropy | `0.0000015165` |

The QFT forward/external-inverse round trip had maximum error `0.000838677` in one random-state trial, with forward norm `0.9995071568` and recovered norm `0.9988668996`. This is a characterized Q4.12 error budget, not the prior semantic transform failure.

Grover reached the exact expected target probability in the quantized run:

```text
P(index 5) = 0.472656250000
norm       = 1.000000000000000
```

Repeated execution of the initialized Grover program produced zero state difference across two runs.

### Boundary weaknesses deferred

The audit identified two separate input-hardening issues and deliberately did not repair them:

| Finding | Classification | Current action |
|---|---|---|
| `noise_p=NaN` is accepted and effectively suppresses all noise branches because comparisons with NaN are false | Input-validation weakness | Document and defer |
| `noise_p=+Inf` recursively re-enters noise application through `_pauli_x` and reaches `RecursionError` | Numerical/input-boundary bug | Document and defer |
| Internal `_phase` accepts/wraps indices through `idx & 0xF`, while public assembly rejects `PHASE 0 16` | Layered API behavior | Characterize; no change |
| `_q(NaN)` / `_q(±Inf)` raise conversion errors | Current numeric behavior | Characterize; no change |

These findings mean that acceptance is **not** a claim of production-ready handling for every invalid numeric input. A future 12D hardening phase should define the legal `noise_p` domain and explicit NaN/Infinity behavior before changing code.

## 12C — Sampler contract decision

The sampler decision is:

> Retain the ambiguity. Do not add `progress=False`, do not modify the original test, and do not change the sampler solely to reach 105/105.

The parameter is historically ambiguous. The current implementation does not support it; documentation, call sites, and prior history provide no semantics; the original test explicitly expects it, but the test and implementation originate from the same historical commit. Therefore neither “stale test” nor “recoverable implementation omission” is established.

A future no-op compatibility parameter could be legitimate new API engineering, but it was not adopted in the acceptance baseline. The official suite consequently remains:

```text
104 passed, 1 unresolved contract failure
```

The remaining failure is the expected `progress=False` unexpected-keyword error and is not an acceptance-critical algorithmic regression.

## Final acceptance statement

> Post-repair integration and numerical-boundary audits are complete. The engineering branch passes all 18 integration checks. Q4.12 numerical behavior and known input-boundary weaknesses have been characterized without modification. QFT and Grover satisfy their explicit engineering contracts within the existing numerical model. The remaining official test failure is preserved as an unresolved historical/API contract ambiguity. No acceptance-critical algorithmic regression was identified.

The branch should now remain frozen as a validated reconstruction. Any future changes should begin in a new branch and be separately labeled, with noise/input hardening as the next technically valuable candidate and sampler compatibility as a later optional API decision.

## Supporting audit artifacts

- `/home/ubuntu/qgrim_12a_integration_audit.txt` — 18/18 integration checks.
- `/home/ubuntu/qgrim_12b_numerical_boundary_audit.txt` — numerical boundary results.
- `/home/ubuntu/qgrim_12c_sampler_contract_decision.md` — explicit sampler policy.
- `/home/ubuntu/qgrim_acceptance_freeze.txt` — branch and provenance verification.
- `/home/ubuntu/qgrim_acceptance_audit_spec.md` — pre-audit scope and boundaries.
