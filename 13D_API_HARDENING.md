# 13D — Tier-1 API Hardening

Commit `df48f3a` introduced deliberate public-boundary validation on a new engineering branch from `05b10eb`. It did not alter QFT, Grover, entropy, noise, teleportation, file APIs, sampler progress behavior, ISA semantics, or historical branches.

## Contracts added

| Surface | Contract |
|---|---|
| `sample_circuit(shots)` | Integer excluding bool; non-negative; zero returns `{}`; wrong type raises `TypeError`; negative raises `ValueError` |
| `chsh_test(shots_per_setting)` | Integer excluding bool; strictly positive; wrong type raises `TypeError`; non-positive raises `ValueError` |
| `bloch_sphere(q)` / `bloch_sphere_str(q)` | Integer excluding bool in `0..3`; wrong type raises `TypeError`; out-of-range raises `ValueError` |
| Fidelity functions | Exactly 16 finite numeric elements; deliberate `TypeError`/`ValueError`; no exact norm-one requirement |

Forty-six focused tests were added. Valid useful behavior was compared before and after the change and remained unchanged.

## Remaining limitation

The historical `progress=False` test remains untouched and continues to be recorded as unresolved. The official suite result is 150 passed and one failed.

## Provenance

This is new API engineering, not recovery. The detailed implementation report, before/after comparison, tests, and verification outputs are preserved in `reports/` and `evidence/`.
