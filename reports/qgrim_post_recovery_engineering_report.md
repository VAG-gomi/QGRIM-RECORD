# Post-recovery QFT and Grover Engineering Report

## Executive result

The QFT and Grover fixes were implemented as **new engineering reconstructions**, not as historical recovery. The recovery branch and historical baseline remain frozen.

| Reference | Commit/state |
|---|---|
| Historical `main` | `a504f6c` — unchanged |
| Frozen recovery branch `qgrim-recovery` | `72edc13` — unchanged |
| Engineering branch | `qgrim-engineering-qft-grover` |
| QFT engineering repair | `a57f8a7 engineering: reconstruct standard forward QFT` |
| Grover engineering repair | `be28bf0 engineering: reconstruct standard Grover iteration` |
| Working tree | Clean |
| Tests modified | None |
| Pushes | None |

The two engineering repairs were made in separate commits. QFT was implemented and verified before the Grover repair began.

## Explicit engineering contracts

QGRIM’s state-vector convention is preserved: qubit q is bit position q, so q0 is the least significant bit. The QFT repair acts on q0, q1, and q2; q3 remains untouched. The Grover target is index 5, representing `|0101⟩` under this convention.

The QFT contract is the three-qubit forward transform:

```text
F|x⟩ = 1/√8 · Σ_y exp(+2πi x y / 8)|y⟩
```

The Grover contract is one standard iteration with:

```text
O = I − 2|5⟩⟨5|
D = 2|s⟩⟨s| − I
```

The expected target probability after preparation and one iteration is:

```text
(11/16)^2 = 0.47265625
```

## QFT repair

### Implementation

The previous QFT circuit used local `PHASE` gates and incomplete CNOT patterns. The engineering reconstruction replaces it with a standard forward-QFT decomposition adapted to QGRIM’s LSB convention.

Controlled phase rotations are synthesized using existing gates:

```text
CP(c,t,θ) = P_c(θ/2) P_t(θ/2) CNOT(c,t)
           P_t(-θ/2) CNOT(c,t)
```

The repaired sequence prepares q2 first, applies controlled rotations `CP(q1,q2,π/2)`, `CP(q0,q2,π/4)`, and `CP(q0,q1,π/2)`, then applies the final `SWAP 0 2` required by the declared integer-index convention. No new ISA opcode or simulator primitive was needed.

### Verification

An independent mathematical oracle constructed the exact 8×8 forward-QFT matrix. The QGRIM implementation was applied independently to all eight computational basis inputs and compared column-by-column.

| Check | Result |
|---|---:|
| Maximum Q4.12 operator entry error | `3.4527e-4` |
| Q4.12 operator Frobenius error | `2.1150e-3` |
| Process-style fidelity | `0.9986614` |
| Maximum basis-column error | `3.4527e-4` |
| QGRIM operator unitarity deviation | `1.7731e-3` |
| Arbitrary-state forward/inverse round-trip error | `7.9617e-4` |

The exact reference matrix was unitary to approximately `1.03e-15`. The remaining QGRIM deviations are consistent with the simulator’s existing Q4.12 quantization and repeated gate rounding, not with a transform-construction mismatch.

The inverse-round-trip audit constructed the inverse externally by reversing the forward sequence and conjugating the phase angles. This avoided adding an unrequested public inverse built-in while still verifying the inverse property.

## Grover repair

### Implementation

The previous circuit attempted to construct a four-qubit phase oracle and diffusion operator using `CCX 0 1 2` surrounded by Hadamards on q3. That omitted the required control and produced swaps rather than a phase oracle.

The engineering reconstruction uses two explicitly documented simulator-only basis operators encoded through reserved NOP fields:

```text
MARK basis     — multiply exactly one basis amplitude by -1
REFLECT basis  — multiply every basis amplitude by -1 except the selected basis
```

These are new software extensions and are not claimed to be historical QGRIM ISA operations.

The repaired oracle is:

```text
X 1
X 3
MARK 15
X 1
X 3
```

The X conjugation maps target index 5 to index 15, so `MARK 15` implements `I − 2|5⟩⟨5|` after conjugation.

The repaired diffusion is:

```text
H 0 H 1 H 2 H 3
X 0 X 1 X 2 X 3
REFLECT 15
X 0 X 1 X 2 X 3
H 0 H 1 H 2 H 3
```

Since `REFLECT 15 = 2|1111⟩⟨1111| − I`, conjugation by X and H gives exactly `2|s⟩⟨s| − I`.

### Verification

The independent operator audit checked every oracle and diffusion entry.

| Check | Result |
|---|---:|
| Oracle off-diagonal maximum | `0.0` |
| Oracle indices with diagonal `-1` | `[5]` |
| Oracle diagonal `+1` count | `15` |
| Oracle vs. reference maximum error | `0.0` |
| Diffusion vs. reference maximum error | `5.55e-16` |
| Exact oracle unitarity error | `0.0` |
| Exact diffusion unitarity error | `1.22e-15` |
| Full exact iteration vs. reference maximum error | `4.44e-16` |
| Q4.12 oracle vs. reference maximum error | `0.0` |
| Q4.12 diffusion vs. reference maximum error | `0.0` |
| Target probability at index 5 | `0.47265625` |
| Expected target probability | `0.47265625` |
| Maximum output probability | `0.47265625` |
| Final state norm | `1.0` |

The oracle is exactly diagonal with one and only one negative entry. The diffusion matches the ideal 16-dimensional reflection. The target is the unique maximum-probability output after one iteration.

## Regression and isolation

The official suite was run before the engineering branch changes and after both repairs. The result after both repairs is:

```text
104 passed, 1 failed
```

The remaining failure is unchanged:

```text
sample_circuit(..., progress=False)
→ TypeError: unexpected keyword argument 'progress'
```

This is the previously classified historical API inconsistency and was intentionally not altered. The existing QFT and Grover tests pass, and no test files were modified.

The engineering branch has `72edc13` as its merge base with `qgrim-recovery`. The recovery branch still points to `72edc13`, and `main` still points to `a504f6c`. The engineering branch has not been pushed.

## Final classification

The repaired QFT and Grover implementations satisfy their newly explicit mathematical contracts within QGRIM’s existing numerical model. These are **post-recovery engineering choices**. They do not establish what the original author intended internally, and they do not rewrite the historical evidence that the surviving circuits were defective.

The recovery branch remains the correct historical/reconstruction record. The engineering branch is a separate, auditable implementation path that adds standard algorithmic behavior only after the forensic failures were established.

## Supporting evidence

- `/home/ubuntu/qgrim_post_recovery_engineering_spec.md` — explicit engineering contracts.
- `/home/ubuntu/qgrim_qft_engineering_audit_final.txt` — all-eight-basis QFT and inverse-round-trip audit.
- `/home/ubuntu/qgrim_grover_engineering_audit_final.txt` — full Grover oracle/diffusion/iteration audit.
- `/home/ubuntu/qgrim_engineering_final_pytest.txt` — final official regression output.
- `/home/ubuntu/qgrim_engineering_final_verification.txt` — final branch and provenance verification.
