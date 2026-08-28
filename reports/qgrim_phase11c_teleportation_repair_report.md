# QGRIM Phase 11C — Teleportation Correction-Control Repair

## Scope and provenance

Phase 11C began from the accepted Bloch checkpoint `c8aaafd` on `qgrim-recovery`. The repair addressed only the built-in teleportation correction control. It did not change the measurement engine, gate implementations, phase convention, eigenvalue solver, entropy code, sampler/API, tests, QFT, Grover, or other algorithms.

The final checkpoint is:

```text
18926db recovery: control teleportation corrections
```

The exact historical conditional-control mechanism could not be recovered because the surviving assembler had no conditional instruction or branch facility. The new `IFX` and `IFZ` forms are therefore explicitly a **documented reconstruction choice**, not a claim about the original source.

## Measurement semantics established before repair

The measurement implementation computes the Born-rule result for a requested qubit, collapses the state, stores the integer result in `sim.measurements[q]`, and returns the same result. In the built-in teleportation circuit, the first measured qubit is q0 and the second is q1:

```text
m0 = sim.measurements[0]
m1 = sim.measurements[1]
```

The assembled pre-repair program confirmed this order directly:

```text
MEASURE q0
MEASURE q1
```

## Correction contract

For the conventional teleportation circuit used by the built-in example, the required corrections are:

```text
X on q2 if m1 == 1
Z on q2 if m0 == 1
```

QGRIM’s existing phase representation expresses Z as `PHASE q2 8`, corresponding to a π phase.

## Minimum implementation choice

Two simulator-only pseudo-instructions were added through reserved nonzero fields of the existing NOP opcode:

```text
IFX m q  → apply X(q) if measurements.get(m, 0) == 1
IFZ m q  → apply Z(q) if measurements.get(m, 0) == 1
```

The raw `0x0000` NOP remains a no-op. The new forms do not add a hardware opcode or change the 16-bit instruction layout.

The built-in teleportation source now uses:

```text
IFX 1 2
IFZ 0 2
```

The assembler validates both operands as members of the existing four-qubit domain. The disassembler labels the forms as simulator-only extensions.

## Exhaustive branch verification

An external harness forced each possible pair of measurement results, executed the actual repaired built-in program, and independently computed q2’s reduced density matrix and fidelity to `|+>`.

| Forced `(m0,m1)` | Stored `(q0,q1)` | q2 fidelity to `|+>` | Final norm |
|---|---|---:|---:|
| `(0,0)` | `(0,0)` | `0.999786376953` | `0.999786376953` |
| `(0,1)` | `(0,1)` | `0.999786376953` | `0.999786376953` |
| `(1,0)` | `(1,0)` | `0.999786376953` | `0.999786376953` |
| `(1,1)` | `(1,1)` | `0.999786376953` | `0.999786376953` |

The residual difference from 1 is the existing Q4.12 quantization behavior. The independent reduced density matrix for every branch is approximately:

```text
[[0.499893188, 0.499893188],
 [0.499893188, 0.499893188]]
```

This verifies both the measurement storage mapping and the correction rule.

## Regression results

`python3 -m py_compile QGRIM_ENGINE.py` passed.

The unchanged official test suite produced:

```text
104 passed, 1 failed in 2.07s
```

The only failure remains the known sampler contract ambiguity:

```text
sample_circuit(..., progress=False)
TypeError: unexpected keyword argument 'progress'
```

The complete external regression harness, with the extensionless Y test temporarily discoverable outside the repository, produced:

```text
111 passed, 1 failed in 2.05s
```

It reported the same sampler failure and no new failure. The Y test was not renamed, and no test was modified.

## Causal conclusion

The repair changed only the teleportation correction-control path and its minimum simulator-only instruction support. The advertised `|+>` teleportation example now delivers q2 in the correct state for all four measurement branches while preserving existing quantization and norm behavior.

The sampler failure remains untouched, as required. No evidence suggests that the 11C change affected entropy, Bloch coordinates, core gates, noise, sampling, QFT, Grover, or test discovery.

## Final checkpoint state

```text
6d41f78  11A eigenvalue solver repair
   ↓
c8aaafd  11B Bloch Y convention repair
   ↓
18926db  11C teleportation correction-control repair
```

`qgrim-recovery` is at `18926db`. `main` remains at `a504f6c`. The working tree is clean, and nothing was pushed.

The remaining separate work is: QFT convention/implementation forensics, Grover oracle/diffusion forensics, entropy invalid-partition validation, and the sampler `progress=False` contract decision.
