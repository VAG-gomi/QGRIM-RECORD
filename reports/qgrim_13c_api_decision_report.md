# QGRIM 13C — API Contract Decision and Prioritization

## Decision-only scope

13C was conducted as a read-only post-reconstruction engineering decision phase from `05b10eb` on the isolated `qgrim-api-decision` branch. No implementation, test, documentation, or historical branch was modified.

The purpose was to distinguish APIs that need stronger public contracts from behaviors that should remain documented or unresolved.

| Reference | State |
|---|---|
| `main` | `a504f6c`, unchanged |
| `qgrim-recovery` | `72edc13`, unchanged |
| Engineering baseline | `3e88909`, unchanged |
| Documentation baseline | `05b10eb` |
| 13C branch | `qgrim-api-decision` at `05b10eb`, clean |
| Code/test changes | None |

## Tier 1 decisions

### Shot counts

`sample_circuit(..., shots=...)` should accept non-negative integers, including zero. Zero should return an empty count dictionary. Boolean values should be rejected rather than treated as shot counts. Non-integers should raise `TypeError`, and negative integers should raise `ValueError`.

The current implementation accepts negative counts as an empty run and leaks native errors for some non-integers. This is a new API engineering contract, not a recovered historical one.

### CHSH shot counts

`chsh_test(shots_per_setting=...)` should accept positive integers only. Boolean values and non-integers should raise `TypeError`; zero and negative values should raise `ValueError`.

The current zero-input `ZeroDivisionError` and acceptance of negative values are accidental low-level behavior rather than a defensible public contract.

### Bloch qubit indices

`QGRIMSim.bloch_sphere(q)` and `bloch_sphere_str(q)` should accept integer q indices in `0..QUBITS-1`, excluding booleans. Non-integers should raise `TypeError`; negative and out-of-range integers should raise `ValueError`.

The current behavior is inconsistent: `q=-1` leaks `ValueError: negative shift count`, while `q=4` is accepted and produces a meaningless result outside the four-qubit domain.

### Fidelity state vectors

The module-level and simulator fidelity functions should require finite numeric state vectors of exactly `STATES` elements. Wrong-length or non-sequence inputs should raise deliberate `TypeError` or `ValueError` rather than `IndexError` or accidental short-sequence behavior.

The decision does not require exact norm-one inputs because QGRIM’s Q4.12 model intentionally produces small norm drift. Fidelity remains squared overlap evaluated under the existing numerical model.

## Tier 2 decision: file APIs

Do not change `save_program` or `load_program` in the next hardening phase. Their current return-value error style is compatibility-sensitive but coherent enough to document:

- `save_program` returns a success or error string.
- `load_program` returns `(source_text, error_message)`, with `source_text=None` on failure.

Normalizing these into exceptions or a common result type should be a separate library-facing API redesign.

## Tier 3 decision: sampler progress

Keep `progress=False` unsupported and unresolved. The original test expects the keyword, but the implementation, documentation, call sites, and history do not establish its intended semantics. Do not add a no-op parameter merely to reach a green test count.

A future compatibility feature may define real progress semantics, but it must be introduced as a separately named API engineering change with tests and documentation.

## Priority for 13D API hardening

The recommended next implementation phase is limited to the four Tier 1 surfaces:

| Priority | Surface | Contract | Compatibility risk |
|---|---|---|---|
| 1 | `shots` | Non-negative integer; `TypeError` for non-integer, `ValueError` for negative | Low |
| 2 | `chsh_test` shots | Positive integer; deliberate errors for invalid values | Low |
| 3 | Bloch q index | Integer in `0..3`; deliberate errors outside domain | Low |
| 4 | Fidelity vectors | Finite, exactly 16-element sequences; deliberate errors | Medium-low |

Noise validation is already hardened and should not be reopened. Entropy partitions are already explicit. QFT, Grover, teleportation, and historical branches are out of scope.

## Additional observed contract weaknesses

The audit recorded, but did not prioritize for immediate implementation, several additional issues:

| Surface | Observation | Decision |
|---|---|---|
| `QGRIMSim` constructor | Dataclass exposes state, program counter, measurement, trace, and RNG fields | Consider narrowing or documenting in future API design |
| `QGRIMSim.run` | Empty program is a no-op; invalid program leaks native type errors | Document or harden later |
| `step` | Low-level invalid words leak native errors | Treat as low-level API unless promoted |
| `render_histogram` | Does not validate count-total versus supplied shots | Future validation candidate |
| `sample_circuit` | Zero/negative shots currently return `{}` | Change only under 13D contract |
| `chsh_test` | Zero divides; negative accepts | Change only under 13D contract |
| File operations | Return-value errors differ from exception APIs | Defer to Tier 2 redesign |

These findings do not indicate a failure of the reconstructed algorithms. They indicate that QGRIM currently serves both as a user-facing tool and as a low-level simulator/debug surface without a fully formalized library API.

## Provenance and no-change verification

The 13C branch remains exactly at `05b10eb`, with no working-tree changes. `qgrim-docs-sync` also remains `05b10eb`; `qgrim-engineering-qft-grover` remains `3e88909`; `qgrim-recovery` remains `72edc13`; and `main` remains `a504f6c`.

The API decisions recorded here are new engineering choices. They are not historical recovery and must not be applied retroactively to `main` or `qgrim-recovery`.

## Final decision

13C is complete. The next implementation, if authorized, should be 13D Tier 1 API hardening only. File API normalization and sampler progress remain separate decisions. No code changes should be made until the 13D scope is explicitly opened.

## Supporting artifacts

- `/home/ubuntu/qgrim_13c_api_contract_decision.md` — full decision record.
- `/home/ubuntu/qgrim_13c_api_inventory.txt` — interface inventory.
- `/home/ubuntu/qgrim_13c_boundary_reconfirmation.txt` — boundary observations.
- `/home/ubuntu/qgrim_13c_branch_baseline.txt` — branch/provenance baseline.
- `/home/ubuntu/qgrim_13c_no_change_verification.txt` — final no-change verification.
