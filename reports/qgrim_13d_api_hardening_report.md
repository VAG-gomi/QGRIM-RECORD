# QGRIM 13D — Tier-1 Public API Hardening

## Scope and provenance

13D began from `qgrim-api-decision` at `05b10eb` and was implemented on a new branch:

```text
qgrim-api-hardening
```

The isolated implementation was committed as:

```text
df48f3a engineering: harden Tier-1 public API contracts
```

No historical or previously accepted branch was modified.

| Reference | State |
|---|---|
| `main` | `a504f6c`, unchanged |
| `qgrim-recovery` | `72edc13`, unchanged |
| `qgrim-engineering-qft-grover` | `3e88909`, unchanged |
| `qgrim-docs-sync` | `05b10eb`, unchanged |
| `qgrim-api-decision` | `05b10eb`, unchanged |
| 13D branch | `df48f3a`, clean |
| Tests modified | No existing tests; new `test_api_contracts.py` added |
| Pushes | None |

13D is new API engineering. It is not historical recovery and does not alter QFT, Grover, entropy, noise, teleportation, file APIs, sampler progress, ISA semantics, or historical branches.

## Implemented contracts

### `sample_circuit(..., shots=...)`

`shots` must be an integer excluding booleans and must be non-negative. Zero remains a valid empty run returning `{}`. Non-integers raise `TypeError`; negative integers raise `ValueError`.

### `chsh_test(shots_per_setting=...)`

`shots_per_setting` must be an integer excluding booleans and must be at least one. Non-integers raise `TypeError`; zero and negative integers raise `ValueError` rather than leaking `ZeroDivisionError` or producing a meaningless negative-shot result.

### `bloch_sphere(q)` and `bloch_sphere_str(q)`

The qubit index must be an integer excluding booleans in the four-qubit domain `0..3`. Non-integers raise `TypeError`; negative and out-of-range integers raise `ValueError`. Valid coordinate behavior remains unchanged.

### Fidelity functions

Both module-level `fidelity` and `QGRIMSim.fidelity` now require finite numeric state vectors of exactly 16 elements. Invalid types and non-numeric values raise `TypeError`; wrong lengths and non-finite values raise `ValueError`. Exact unit norm is intentionally not required because QGRIM’s Q4.12 representation produces small numerical norm drift.

The existing squared-overlap mathematics is preserved.

## Before/after behavioral table

| Case | 05b10eb before 13D | `df48f3a` after 13D | Classification |
|---|---|---|---|
| `sample_circuit(shots=0)` | Accepted, `{}` | Accepted, `{}` | Unchanged |
| `sample_circuit(shots=10, seed=0)` | `{'1100': 7, '0000': 3}` | Same result | Unchanged |
| `sample_circuit(shots=-1)` | Accepted, `{}` | `ValueError` | Intentional contract change |
| `sample_circuit(shots=False)` | Accepted, `{}` | `TypeError` | Intentional contract change |
| `chsh_test(1)` | Accepted, same formatted result | Same formatted result | Unchanged |
| `chsh_test(0)` | `ZeroDivisionError` | `ValueError` | Intentional contract change |
| `chsh_test(-1)` | Accepted meaningless result | `ValueError` | Intentional contract change |
| `bloch_sphere(q=0..3)` | Accepted, same coordinates | Same coordinates | Unchanged |
| `bloch_sphere(q=-1)` | Low-level negative-shift `ValueError` | Deliberate range `ValueError` | Intentional contract change |
| `bloch_sphere(q=4)` | Accepted meaningless coordinate | Deliberate range `ValueError` | Intentional contract change |
| Global fidelity with valid 16-element vectors | `1.0` | `1.0` | Unchanged |
| Simulator fidelity with valid 16-element vector | `1.0` | `1.0` | Unchanged |
| Global fidelity with one-element vector | Accepted in one short-sequence case | Deliberate length `ValueError` | Intentional contract change |
| Simulator fidelity with one-element vector | `IndexError` | Deliberate length `ValueError` | Intentional contract change |
| `progress=False` | Unsupported `TypeError` | Still unsupported `TypeError` | Intentionally unchanged |

## Verification gate

The new focused contract test module contains 46 tests and passes completely:

```text
46 passed
```

The complete official suite now reports 151 collected tests, with:

```text
150 passed, 1 failed
```

The only failure remains the pre-existing sampler ambiguity:

```text
TestSampler.test_progress_kwarg_accepted
TypeError: sample_circuit() got an unexpected keyword argument 'progress'
```

No change was made to that behavior.

| Verification | Result |
|---|---|
| Syntax compilation | Pass |
| New 13D contract tests | `46/46` pass |
| 12A integration matrix | `18/18` pass |
| QFT audit | Unchanged; process fidelity `0.9986614`, round-trip error `7.96e-4` |
| Grover audit | Unchanged; exact oracle/diffusion, target probability `0.47265625` |
| Noise audit | Unchanged; invalid probabilities rejected and recursion guard passes |
| Before/after valid behavior | Unchanged for sampled valid cases |
| Diff check | Pass |
| Working tree | Clean after commit |

## Causal diff boundary

The committed diff from `05b10eb` contains exactly two files:

| File | Purpose |
|---|---|
| `QGRIM_ENGINE.py` | Four Tier-1 validation contracts plus shared validation helpers |
| `test_api_contracts.py` | New tests for the deliberate contracts |

No QFT, Grover, entropy, noise, teleportation, file API, sampler-progress, ISA, or existing test files were changed.

## Disposition

13D passes as an isolated API-engineering checkpoint. It converts four accidental or low-level boundary behaviors into explicit public contracts while preserving useful valid-input behavior and all previously verified algorithmic audits.

The next step should be a post-13D regression/readiness audit before any packaging cleanup or additional API redesign. The sampler `progress=False` ambiguity remains a separate deliberate decision and was not used as a target for this hardening phase.

## Supporting evidence

- `/home/ubuntu/qgrim_13d_api_contract_decision.md` — 13C contract decisions.
- `/home/ubuntu/qgrim_13d_baseline.txt` — pre-13D baseline.
- `/home/ubuntu/qgrim_13d_tier1_tests.txt` — initial focused and official tests.
- `/home/ubuntu/qgrim_13d_before_after_behavior_final.txt` — independent compatibility comparison.
- `/home/ubuntu/qgrim_13d_postcommit_verification.txt` — post-commit complete verification.
- `/home/ubuntu/qgrim_13d_commit.txt` — commit and branch provenance.
