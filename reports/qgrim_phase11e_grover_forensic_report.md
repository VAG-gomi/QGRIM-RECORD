# QGRIM Phase 11E — Grover Forensic Investigation

## Scope and provenance

Phase 11E was forensics-only. No repository files were changed. `qgrim-recovery` remains at `18926db`, and `main` remains at `a504f6c`.

The question was not how to add gates until a Grover test passes. It was:

> What oracle and diffusion operators does the surviving circuit actually implement, and how do they compare with the claimed marked-state Grover iteration?

## Claimed convention

The built-in description says:

```text
Grover search for |0101⟩
qubits 0,1,2,3 = 1,0,1,0 from LSB
```

Under QGRIM’s documented least-significant-bit convention, the marked computational basis index is therefore `5` (`0101₂`). The intended oracle is:

```text
O|5⟩ = -|5⟩
O|x⟩ = |x⟩ for x ≠ 5
```

The ideal four-qubit diffusion operator is:

```text
D = 2|s⟩⟨s| − I
```

where `|s⟩` is the uniform superposition over all 16 basis states.

## Existing circuit decomposition

The surviving source uses the following oracle segment:

```text
X 1
X 3
H 3
CCX 0 1 2
H 3
X 1
X 3
```

The comments describe this as an approximation to a multi-controlled phase flip, but the actual `CCX` has controls q0 and q1 and target q2. It does not use q3 as a control. The surrounding `H 3` pair cancels because the CCX does not act on q3.

Consequently, after the X conjugation on q1 and q3, the oracle is not a phase flip on a single basis state. It is a permutation that swaps basis indices:

```text
1 ↔ 5
9 ↔ 13
```

All other basis states are unchanged. The actual oracle therefore maps `|1⟩` to `|5⟩` and `|5⟩` to `|1⟩`; it does not map `|5⟩` to `-|5⟩`.

The diffusion segment is:

```text
H 0 H 1 H 2 H 3
X 0 X 1 X 2 X 3
H 3
CCX 0 1 2
H 3
X 0 X 1 X 2 X 3
H 0 H 1 H 2 H 3
```

Again, the CCX acts only on q0, q1, and q2. The q3 Hadamard pair cancels around it. This is not the required four-qubit phase inversion about `|0000⟩`; it is a three-qubit Toffoli-based operation tensored with an effectively unaffected q3 path.

## Full operator measurements

The extracted oracle, diffusion, and complete one-iteration operators were each unitary in the simulator’s exact permutation/Hadamard structure; the Q4.12 state arithmetic does not introduce a material operator-norm failure here.

Against the intended operators:

| Operator | Maximum global-phase-aligned error | Process-style fidelity |
|---|---:|---:|
| Existing oracle vs. mark-only phase flip on index 5 | `1.0` | `0.5625` |
| Existing diffusion vs. ideal 16-state diffusion | `0.375` | `0.5625` |

The oracle’s basis action was:

```text
1  → 5
5  → 1
9  → 13
13 → 9
x  → x for all other x
```

This is a direct operator-level contradiction of the claimed phase oracle.

## One-iteration result

Starting from the uniform superposition, the existing complete circuit produces amplitudes of magnitude `0.25` for every basis state. Every probability is therefore `0.0625`, including the claimed target index 5:

```text
P(target = 5) = 0.0625
```

The maximum probability is also `0.0625`, so no target amplification occurs. The norm remains 1.0.

This is stronger than a single failed target assertion: the extracted operator explains why the entire state remains uniform in probability after the purported Grover iteration.

## Test coverage

The existing Grover tests check that the circuit runs, preserves norm, has nonzero amplitudes, has nonnegative probabilities, is deterministic, and has nontrivial instruction depth. They do not check:

- that the oracle is diagonal;
- that only basis index 5 receives a phase flip;
- that the diffusion operator equals `2|s⟩⟨s| − I`;
- that the target probability is amplified;
- that the full operator agrees with an independently specified Grover iteration.

Thus the existing suite can pass while the advertised Grover semantics fail.

## Classification

| Question | Result |
|---|---|
| Does the built-in execute? | Yes |
| Does it preserve norm? | Yes |
| Does the oracle mark only `|0101⟩` by a phase? | No; it performs swaps |
| Does the diffusion implement four-qubit inversion about average? | No |
| Is the target amplified after one iteration? | No; remains `0.0625` |
| Is the failure explained by bit ordering? | No; the operator is non-diagonal |
| Is the failure explained by global phase? | No |
| Is the intended alternate oracle documented? | No |
| Historical exact intention recoverable? | No |
| Repair made in Phase 11E? | No; forensic phase only |

The surviving circuit is therefore an **algorithmic implementation failure**, not a mere convention mismatch. The exact historical intended circuit cannot be proven from the surviving repository, but the claimed marked-state oracle and ideal diffusion are mathematically explicit enough to establish that the current implementation does not realize them.

## Repair gate for a later phase

A later Grover repair must first specify whether the project intends a four-qubit standard Grover iteration. If yes, the verification contract should require an oracle that is diagonal with exactly one `-1` at index 5, a diffusion operator equal to `2|s⟩⟨s| − I`, target amplification after the intended number of iterations, all 16 basis-input operator checks, norm preservation, and unchanged behavior outside the Grover built-in.

No Grover repair was made here. Entropy input validation and the sampler contract remain separate phases.
