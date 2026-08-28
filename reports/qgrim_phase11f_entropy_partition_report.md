# QGRIM Phase 11F — Entropy Partition Input Validation

## Result

Phase 11F is complete. The entropy partition-input contract was investigated and repaired in one causally isolated source change on `qgrim-recovery`.

The new checkpoint is:

```text
72edc13 recovery: validate entropy partitions
```

`main` remains the immutable historical baseline at `a504f6c`. No changes were pushed to GitHub.

## Scope

This phase addressed only invalid `partition_a` inputs to `QGRIMSim.entanglement_entropy`. It did not change the reduced-density construction, smaller-side Gram selection, Jacobi eigensolver, entropy definition, numerical tolerance, sampler behavior, QFT, Grover, tests, or unrelated simulator behavior.

## Evidence and recovered contract

The surviving method documents entropy for a subsystem A of QGRIM’s four-qubit state, with default partition `[0, 1]`. The engine defines the qubit domain as `0..3`. Existing tests establish singleton cuts, contiguous and non-contiguous two-qubit cuts, three-qubit cuts, and the default cut. The README describes the operation as a bipartite von Neumann entropy but does not specify behavior for malformed partitions.

The pre-repair implementation had three contract problems. Duplicate entries were accepted even though a partition is set-like and duplicates distort the subsystem dimension. Positive out-of-range entries such as `4` or `16` were accepted silently. Negative entries failed indirectly with `ValueError: negative shift count`, exposing an internal bit-shift failure rather than a deliberate API response.

The smallest defensible contract is now:

| Input | Result |
|---|---|
| `None` | Uses the documented default `[0, 1]` |
| Unique integer indices in `0..3` | Accepted |
| Empty list `[]` | Accepted as the valid zero-qubit subsystem; entropy is zero |
| All qubits `[0, 1, 2, 3]` | Accepted; entropy is zero |
| Complementary valid partition | Accepted and yields the same entropy |
| Duplicate index | Raises `ValueError` |
| Negative or positive out-of-range index | Raises `ValueError` |
| Non-integer element, including `bool` | Raises `TypeError` |
| Non-iterable partition argument | Raises `TypeError` |

Acceptance of empty and all-qubit partitions is a mathematical/API reconstruction choice made in this phase, not a claim that the exact historical implementation had explicit handling for those edge cases. Likewise, exception types and messages are new deliberate contract behavior, not historically recovered literals.

## Implementation change

The repair converts a supplied partition to a list, checks that every entry is an integer qubit index, checks the four-qubit domain, and rejects duplicates. The existing entropy matrix construction and eigensolver begin immediately afterward and are unchanged.

The resulting source diff is limited to 18 inserted lines in `QGRIM_ENGINE.py` within `entanglement_entropy`. No test file or configuration file was modified.

## Independent verification

An external NumPy-based oracle constructed the reduced density matrix independently for every one of the 16 valid partitions of a random normalized four-qubit state. The maximum absolute entropy difference was:

```text
1.776e-15 bits
```

Complementary cuts also matched exactly within the audit precision:

| A | Complement B | Entropy difference |
|---|---|---:|
| `[0]` | `[1, 2, 3]` | `0.000e+00` |
| `[0, 2]` | `[1, 3]` | `0.000e+00` |
| `[0, 1, 3]` | `[2]` | `0.000e+00` |
| `[]` | `[0, 1, 2, 3]` | `0.000e+00` |

The focused invalid-input audit confirmed deliberate failures for duplicate, negative, positive out-of-range, mixed out-of-range, floating-point, Boolean, and non-iterable inputs.

## Regression and causal comparison

Syntax compilation passed. The official suite was run both before the commit from a clean `18926db` worktree and after the Phase 11F change:

| Run | Result |
|---|---|
| Before, clean `18926db` | `104 passed, 1 failed` |
| After, `72edc13` | `104 passed, 1 failed` |
| Remaining failure | `sample_circuit(..., progress=False)` unexpected keyword argument |

The failure is identical and remains intentionally untouched because it is the separate sampler API-contract question identified in Phase 9 and carried into the 11G scope. The unchanged result supports causal isolation: entropy partition validation introduced no new official-suite failures and did not alter the unresolved sampler behavior.

The working tree is clean at `72edc13` on `qgrim-recovery`. The QFT and Grover implementations remain unrepaired, as required.

## Classification

Phase 11F is a **conventional API/input-contract repair**, not a mathematical entropy repair. The prior entropy mathematics had already been repaired and independently verified in Phase 11A; this phase prevents malformed partition descriptions from reaching that computation through accidental or silent behavior.

The next separate phase is 11G: sampler `progress=False` contract archaeology. It should begin with evidence gathering and should not be resolved merely by adding a keyword to eliminate the remaining test failure.
