# QGRIM Phase 11D — QFT Forensic Investigation

## Scope and provenance

Phase 11D was forensics-only. No repository source, tests, configuration, or tolerances were changed. `qgrim-recovery` remains at `18926db`, and `main` remains at `a504f6c`.

The question was not how to make a QFT test pass. It was:

> What complete 8×8 operator does the surviving QFT circuit implement, and can that operator be explained by standard QFT conventions?

## Surviving circuit

The built-in is labelled “Quantum Fourier Transform on 3 qubits” and contains:

```text
H 0
PHASE 1 4
CNOT 0 1
PHASE 2 2
CNOT 0 2
PHASE 2 4
CNOT 1 2
H 1
PHASE 2 4
CNOT 1 2
H 2
SWAP 0 2
```

The simulator uses Q4.12 state arithmetic. The complete operator was obtained by applying this circuit to each of the eight computational basis states while holding q3 at zero. The result is a unitary up to the expected fixed-point norm error; the maximum observed `U†U − I` entrywise error was approximately `2.14×10⁻⁴`.

## Complete operator evidence

Rows are output basis indices and columns are input basis indices. The matrix is shown in Q4.12-rounded form:

```text
row 0:  [ 0.353516,  0.353516, -0.353516, -0.353516, -0.25-0.25i, -0.25-0.25i, -0.25-0.25i, -0.25-0.25i ]
row 1:  [ 0.353516,  0.353516,  0.353516,  0.353516,  0.25+0.25i,  0.25+0.25i, -0.25-0.25i, -0.25-0.25i ]
row 2:  [ 0.353516,  0.353516,  0.353516,  0.353516, -0.25-0.25i, -0.25-0.25i,  0.25+0.25i,  0.25+0.25i ]
row 3:  [-0.353516, -0.353516,  0.353516,  0.353516, -0.25-0.25i, -0.25-0.25i, -0.25-0.25i, -0.25-0.25i ]
row 4:  [ 0+0.353516i, 0-0.353516i, 0-0.353516i, 0+0.353516i, -0.25+0.25i, 0.25-0.25i, -0.25+0.25i, 0.25-0.25i ]
row 5:  [ 0+0.353516i, 0-0.353516i, 0+0.353516i, 0-0.353516i, 0.25-0.25i, -0.25+0.25i, -0.25+0.25i, 0.25-0.25i ]
row 6:  [ 0-0.353516i, 0+0.353516i, 0-0.353516i, 0+0.353516i, 0.25-0.25i, -0.25+0.25i, -0.25+0.25i, 0.25-0.25i ]
row 7:  [ 0+0.353516i, 0-0.353516i, 0-0.353516i, 0+0.353516i, 0.25-0.25i, -0.25+0.25i, 0.25-0.25i, -0.25+0.25i ]
```

For `|000>`, the output is not a uniform positive-real vector. It contains sign and imaginary-phase differences. Therefore the fact that all output probabilities are approximately `1/8` does not establish QFT correctness.

## Convention search

The actual operator was compared with standard forward and inverse 3-qubit QFT matrices. The search included all input and output wire permutations, including bit-reversal-equivalent arrangements, and optimized away one possible global phase.

The best tested convention was an inverse-QFT sign with input permutation `(1,2,0)` and output permutation `(0,2,1)`. Its process-style fidelity was only approximately `0.07031`, with maximum global-phase-aligned entrywise error approximately `0.69692`.

Other best candidates remained below approximately `0.04621` fidelity, and the direct forward-QFT plus standard reversal candidate was approximately `0.03582`. No tested combination approached unitary equivalence.

The prior `|000>` state comparison also found global-phase residual approximately `0.65325`; for `|000>` a correct standard QFT or inverse QFT should be uniform up to a single global phase. This is already sufficient to rule out a mere global-phase explanation.

## Interpretation

The surviving circuit is a valid executable unitary-like transformation under QGRIM’s numerical model, but it is not the standard 3-qubit QFT or inverse QFT under the tested conventions. The discrepancy is not explained by:

- forward versus inverse sign;
- input bit ordering;
- output bit ordering;
- final bit reversal;
- a single global phase;
- Q4.12 rounding alone.

The source’s use of individual `PHASE` gates interleaved with CNOTs may be intended as a hand-built decomposition, but the complete operator does not match the standard QFT family under the tested convention space. The source does not document an alternative transform definition.

## Classification

| Question | Result |
|---|---|
| Does the built-in execute? | Yes |
| Is it norm/unitary-like? | Yes, within Q4.12 error |
| Does it match standard forward QFT? | No |
| Does it match inverse QFT? | No |
| Can ordering/reversal explain it? | No, not in the tested permutation space |
| Can global phase explain it? | No |
| Is the intended alternative transform documented? | No |
| Historical exact intention recoverable? | No |
| Repair authorized in Phase 11D? | No; forensic decision only |

The current evidence supports classifying the advertised QFT example as an **implementation/algorithmic claim failure**, not as a simple convention mismatch. The exact historical intention remains bounded because the repository does not specify the intended decomposition or an alternative unitary.

## Repair gate for a later phase

A later QFT repair should first specify one explicit convention and then verify the complete operator, not only probabilities. The minimum verification matrix should include all eight basis inputs, forward/inverse selection, wire-ordering documentation, bit reversal, global-phase alignment, QFT followed by inverse QFT, norm preservation, and unchanged regression behavior.

No QFT repair was made here. The next separate forensic phase should analyze the Grover oracle and diffusion operators.
