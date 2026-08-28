# QGRIM Phase 10 — Read-Only Behavioral Audit

## Audit question and boundary

The governing question was:

> What does QGRIM actually implement, independently of what its README, tests, or apparent aspirations claim it implements?

This was a read-only audit on `qgrim-recovery` at `af21a5c`. No source, test, tolerance, or configuration file was modified. The external audit scripts used temporary files only.

For each capability, the audit separated four questions:

1. Does the code execute?
2. Does the implementation correspond to the claimed mathematics?
3. Does an independent reference/oracle agree?
4. Is the claim covered by the existing tests?

## Executive result

The core four-qubit gate, measurement, sampling, noise-boundary, entropy-canonical-state, persistence, and visualization paths are substantially executable and locally consistent. However, the full quantum-semantic claim is **not established**. Several advertised algorithms are either only weakly tested or fail independent semantic checks.

The strongest newly identified findings are:

- **Grover does not amplify the advertised target**: the target basis index 5 remains at probability `1/16`, with all basis states tied.
- **The built-in teleportation circuit does not deterministically deliver `|+⟩` to q2**: across measurement branches, q2 has fidelity 0 or approximately 0.999786 with `|+⟩`, consistent with unconditional rather than classically controlled corrections.
- **The QFT circuit does not match the standard three-qubit QFT on `|000⟩`**: its fidelity to the standard uniform reference is approximately `0.124973`, even though its probabilities are uniform.
- **The generic eigenvalue solver mishandles degenerate spectra**: cluster-state non-contiguous 2+2 partitions should have entropy 2 bits but return 1 bit.
- **The Bloch-sphere y coordinate is sign-reversed**: `|+i⟩` is reported as y≈−1 and displayed as `|−i⟩`; `|−i⟩` is reported as y≈+1.
- **Entropy partition input is not validated**: duplicates are silently accepted, out-of-range positive indices are ignored, and negative indices raise a raw shift error.

## Capability classification matrix

| Capability | Executes? | Independent mathematical/reference result | Existing test coverage | Classification |
|---|---|---|---|---|
| Q4.12 state engine | Yes | Norm and canonical states agree within quantization error | Broad gate/norm tests | Verified with bounded numerical error |
| X, Y, H, PHASE gates | Yes | Exhaustive basis checks and analytic matrices agree within Q4.12 tolerance | X indirectly, Y/H/phase-related tests | Verified with bounded numerical error |
| CNOT, CZ, SWAP, CCX | Yes | Exhaustive valid-basis truth tables agree | Strong direct tests; bounds now repaired | Verified with bounded numerical error |
| Measurement/collapse | Yes | Born-rule and Bell-correlation checks agree locally | Broad direct and assembled tests | Verified with bounded numerical error |
| Noise | Yes | Boundary/statistical behavior agrees with stated local model | Broad statistical tests | Partially verified; full channel semantics unproven |
| Sampling/QRNG | Yes | Counts, seeded reproducibility, Bell support, and 16-outcome QRNG checks agree | Broad sampler tests | Verified for tested behavior; `progress=False` contract ambiguous |
| Entropy canonical states | Yes | Independent reduced-density oracle agrees | Product, Bell, GHZ, cluster single-qubit tests | Verified with bounded numerical error for covered cuts |
| Entropy arbitrary partitions | Yes | Random normalized state matched independent oracle to max difference ≈`8.9×10⁻¹⁶` | Not covered | Verified for sampled arbitrary states |
| Entropy degenerate cluster cuts | Yes | Independent spectrum is `[0.25,0.25,0.25,0.25]`; engine returns only two `0.25` eigenvalues | Not covered | Implementation defect in eigensolver degeneracy handling |
| Entropy partition validation | Partly | Invalid inputs have undefined/accidental behavior | Not covered | Implementation/input-validation defect |
| Bloch sphere x/z axes | Yes | Analytic checks agree within Q4.12 error | Not covered | Verified locally |
| Bloch sphere y axis | Yes | `|+i⟩` and `|−i⟩` have reversed y sign and reversed labels | Not covered | Implementation defect |
| Deutsch constant oracle | Yes | q0=0 in 100/100 seeded runs | Not covered by dedicated test | Verified for the fixed built-in example |
| Deutsch balanced oracle | Yes | q0=1 in 100/100 seeded runs | Not covered by dedicated test | Verified for the fixed built-in example |
| Bernstein–Vazirani | Yes | hidden string `(1,0,1)` in 100/100 runs | Direct tests exist | Verified for the fixed example |
| Grover | Yes | Advertised target index 5 remains at probability 0.0625; no amplification | Tests check execution, norm, nonzero amplitudes, and depth only | Implementation/algorithmic claim failure |
| QFT | Yes | Standard QFT(`|000⟩`) reference fidelity ≈`0.124973`; output phases differ | No QFT semantic test | Implementation/algorithmic claim failure |
| Teleportation | Yes | q2 `|+⟩` fidelity ranges from 0 to ≈0.999786 across measurement branches | No teleportation test | Implementation defect in advertised circuit |
| Superdense coding | Yes | fixed message `11` measured as `(1,1)` in 100/100 runs | No dedicated test | Verified for the fixed example |
| Phase kickback | Yes | q0=1 in 100/100 fixed-example runs | No dedicated test | Verified for the fixed example |
| QPE | Yes | fixed Z-eigenphase sketch returns q0=1 in 100/100 runs | No QPE test | Narrow example verified; general QPE unverified |
| CHSH | Yes | finite-shot S≈2.896 at 500 and 2.8396 at 5000 versus theory 2.8284; violation remains | No dedicated test | Verified with bounded statistical error; output has finite-shot overshoot caveat |
| Save/load, disassembly, hex, diagrams, listing, histogram | Yes | Temporary-directory round trip and nine public-surface checks pass | Limited/no direct tests | Verified locally |

## Core gate, measurement, noise, and sampling findings

An external core sweep performed 1,121 checks across direct gate truth tables, assembled paths, measurement invariants, sampling reproducibility, noise boundaries, and canonical entropy spot checks. After correcting an error in the external PHASE test setup—not in QGRIM—the sweep completed with **0 failures**.

The measurement checks covered deterministic basis states, collapse, repeated measurement, Bell correlations, and norm preservation. The sampler checks covered requested shot totals, same-seed reproducibility, Bell support, and QRNG support. The noise checks covered zero-noise identity, distribution change under noise, and norm preservation. These are meaningful positive results, but they do not constitute a complete proof of the noise channel or all measurement semantics.

The implementation applies independent X, Y, or Z errors to each listed qubit when a per-gate random draw falls into one of three `noise_p/3` intervals. This is consistent with a local single-qubit Pauli depolarizing model, but the audit did not perform complete process tomography.

## Entropy findings

The Phase 8 smaller-side repair is mathematically justified and remains correct for a deliberately asymmetric normalized four-qubit state: all 16 partitions, including `[0,2]` and complementary 3+1 cuts, matched an independent reduced-density calculation with maximum difference approximately `8.9×10⁻¹⁶`.

A separate cluster-state check exposed a remaining defect in `_hermitian_eigenvalues()`. For non-contiguous 2+2 cuts `[0,2]`, `[0,3]`, `[1,2]`, and `[1,3]`, the independent reduced spectrum is four eigenvalues of `0.25`, yielding entropy 2 bits. The engine’s power-iteration/deflation routine returns only two `0.25` eigenvalues and two zeros, yielding entropy 1 bit. The partition mapping itself is correct; the discrepancy is localized to degenerate-eigenvalue recovery.

The entropy method also has no explicit validation for `partition_a`. Duplicate entries are silently accepted, `[4]` and `[0,4]` are effectively treated as if the invalid positive index were absent, and `[-1]` raises `ValueError: negative shift count`. These are untested input-contract defects, separate from the Phase 8 performance repair.

## Algorithmic findings

### Grover

The built-in description says it searches for `|0101⟩`, which corresponds to basis index 5 under the stated qubit ordering. The independent run finds probability `0.0625` at index 5 and the same `0.0625` probability for every basis state. Thus the circuit executes and preserves norm, but it performs no target amplification. The existing tests do not assert the target probability or marked-state behavior; they therefore cannot support the Grover claim.

### QFT

For `|000⟩` on the three active qubits, the standard QFT reference is uniform with equal positive real amplitudes. The built-in circuit also produces equal probabilities, but its amplitudes include sign and imaginary-phase differences. The fidelity to the standard reference is approximately `0.124973`, not close to 1. Uniform probabilities alone do not establish a correct QFT because the relative phases are part of the unitary transformation. The QFT claim is therefore not verified and the fixed example fails the independent reference check.

### Teleportation

The built-in circuit advertises teleportation of `|+⟩` from q0 to q2. The audit reduced q2’s final state independently for 100 measurement branches. The q2 fidelity to `|+⟩` was either 0 or approximately 0.999786, with branches `(m0,m1)=(0,0)` and `(0,1)` producing fidelity 0 and branches `(1,0)` and `(1,1)` producing fidelity approximately 0.999786. The source comment says corrections are “always applied in software model,” and the circuit unconditionally applies both `X 2` and `PHASE 2 8` rather than conditioning them on the measurement bits. This is consistent with a real correction-control defect, not merely weak testing.

### CHSH

The CHSH implementation uses four settings, independent fresh Bell-state runs, `Ry` basis rotations, and the standard correlation estimator. At 5,000 shots per setting it reports `S=2.8396` versus theoretical `2.8284`, a plausible finite-shot deviation. The estimator can exceed the theoretical bound because it is sampled; the output should be interpreted statistically rather than as a literal violation of the Tsirelson bound. The Bell violation itself is locally supported, but complete statistical confidence intervals were not added in this audit.

### Deutsch, BV, superdense coding, phase kickback, and QPE

The fixed built-in Deutsch, balanced Deutsch, Bernstein–Vazirani, superdense, phase-kickback, and one-clock-qubit QPE examples execute and match their narrow expected outputs in repeated seeded runs. These results verify those examples, not the general algorithms or arbitrary oracles, messages, phases, or circuit sizes.

## Bloch-sphere finding

The gate-state construction was corrected in the external audit to create `|+i⟩` as H followed by the `k=4` (`π/2`) phase and `|-i⟩` with the `k=12` (`−π/2`) phase. The engine returns:

| State | Analytic expected | Engine result |
|---|---|---|
| `|+i⟩` | `(0,+1,0)` | `(0,−0.999786,0)` |
| `|−i⟩` | `(0,−1,0)` | `(0,+0.999786,0)` |

The x and z axes agree within Q4.12 rounding. The y sign is reversed because the implementation uses `y = +2 Im(ρ01)` under a density-matrix convention where the standard Bloch coordinate is `y = -2 Im(ρ01)`. The human-readable labels reverse with it. No existing test covers this helper.

## Test coverage and discovery

The official suite currently discovers 105 tests and, at the current checkpoint, reports 104 passed and one sampler API failure. The extensionless `test_y_py` is not collected; an external temporary rename discovers 112 tests and reports 111 passed and one sampler failure. This distinction must remain explicit.

Existing tests are strong for basic gates, Bell/GHZ, measurement, noise boundaries, sampling statistics, entropy single-qubit cuts, SWAP, and Y. They are weak or absent for Grover target amplification, QFT phases, teleportation correction control, CHSH statistical bounds, QPE generality, superdense arbitrary messages, Bloch coordinates, invalid entropy partitions, and non-contiguous entropy cuts.

The test suite’s passing count therefore cannot establish full quantum-semantic correctness.

## Final status

| Layer | Status | Confidence |
|---|---|---|
| Repository recoverability | Substantially restored | High, historical exactness limited |
| Test infrastructure | Reconstructed | High, but not historically exact |
| Python importability | Repaired | High |
| Four-qubit operand domain | Repaired | High |
| Entropy dimensionality/performance | Repaired | High locally |
| Core gates and basic measurement | Locally verified | High within tested domain |
| Noise | Partially verified | Moderate |
| Sampler API `progress=False` | Ambiguous; correctly unresolved | Moderate |
| Entropy general partitions | Mostly verified, with degenerate-spectrum defect | High for observed cases |
| Bloch-sphere y semantics | Defect found | High |
| Grover/QFT/teleportation advertised behavior | Not verified; concrete failures found | High for observed fixed examples |
| Narrow Deutsch/BV/superdense/phase-kickback/QPE examples | Verified | Moderate to high for those examples |
| Full numerical correctness | Partially established | Moderate |
| Full quantum-semantic correctness | Not established | Open |
| Historical fidelity | Fundamentally incomplete | Explicitly bounded |

The recovery branch remains clean at `af21a5c`, and `main` remains at `a504f6c`. No repair was made during Phase 10. The next action should be a deliberate decision about which independently demonstrated semantic defects to repair, preserving the same causal-checkpoint discipline.
