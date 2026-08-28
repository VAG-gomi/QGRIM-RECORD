# QGRIM Phase 11A — Solver-Level Eigenvalue Repair

## Scope and provenance

Phase 11A was intentionally treated as a **numerical-solver repair**, not merely an entropy patch. The affected shared primitive is `_hermitian_eigenvalues()`, which is called by `entanglement_entropy()`.

The repair began from `af21a5c` on `qgrim-recovery`. `main` remained at the historical baseline `a504f6c`. No tests, `conftest.py`, entropy matrix selection, gate implementations, sampler/API code, Bloch code, QFT, Grover, teleportation, or other algorithms were modified.

The final causal checkpoint is:

```text
6d41f78 recovery: replace degenerate eigenvalue solver
```

## Pre-repair evidence

The former routine used power iteration followed by rank-one deflation. Its comments claimed that varied starting vectors handled degeneracy, but controlled-spectrum testing disproved that claim.

Examples of the old behavior included:

| Input spectrum | Old solver result | Problem |
|---|---|---|
| `[0.25, 0.25, 0.25, 0.25]` | One or two `0.25` values plus zeros | Exact degeneracy lost |
| `[1, 1, 1, 1]` | Partial spectrum in some orientations | Exact degeneracy unstable |
| `[2, 2, 2, 2]` | Partial spectrum in some orientations | Exact degeneracy unstable |
| `[0.7, 0.1, 0.1, 0.1]` | Occasionally lost a repeated eigenvalue | Partial degeneracy lost |
| `[0.5, 0.5, 0, 0]` | Generally recovered | Non-degenerate/zero structure could appear correct |
| Near-degenerate spectra | Approximate values with small errors | Stability depended on separation and orientation |

The cluster-state `[0,2]` entropy defect was localized to this solver: the independent 4×4 spectrum was four `0.25` values, while the old routine returned two `0.25` values and two zeros.

## Repair selected

The power-iteration/deflation routine was replaced with a stdlib-only complex-Hermitian Jacobi diagonalization. The replacement:

- copies the input matrix before operating;
- preserves Hermitian complex entries;
- applies complex Jacobi similarity rotations;
- iterates over full off-diagonal sweeps;
- handles exact and near-degenerate eigenvalues without selecting one vector from a degenerate eigenspace at a time;
- returns the real diagonal of the converged Hermitian form;
- preserves the existing function signature and the entropy caller;
- does not introduce NumPy, caching, or a new public API.

The returned ordering remains intentionally unspecified because the entropy caller only needs the eigenvalue multiset.

## Controlled-spectrum verification

The replacement was tested against independently generated Hermitian matrices with known spectra. The matrices included random unitary rotations so the test was not limited to diagonal inputs.

| Spectrum class | Maximum absolute eigenvalue error |
|---|---:|
| `I₄/4` | `1.11×10⁻¹⁶` |
| `[1,1,1,1]` | `5.55×10⁻¹⁶` |
| `[2,2,2,2]` | `8.88×10⁻¹⁶` |
| `[0.5,0.5,0,0]` | `3.33×10⁻¹⁶` |
| `[0.5,0.5000001,0.25,0.2499999]` | `5.55×10⁻¹⁶` |
| `[0.7,0.1,0.1,0.1]` | `3.33×10⁻¹⁶` |
| `[0.7,0.2,0.08,0.02]` | `8.88×10⁻¹⁶` |

Additional random Hermitian matrices of dimensions 1, 2, 4, and 8 agreed with NumPy’s independent reference eigensolver to at most approximately `7.1×10⁻¹⁵` in the tested samples.

The `I₄/4` invariant now returns exactly four `0.25` eigenvalues, with trace `1.0` and all eigenvalues non-negative. The partial-rank and near-degenerate cases also preserve their full spectrum and trace.

## Entropy verification

The post-repair entropy audit matched an independent reduced-density calculation for every subset of a deliberately asymmetric normalized four-qubit state. The maximum entropy difference across all 16 partitions was approximately `1.11×10⁻¹⁵`.

Canonical checks also passed:

| State/cut | Result |
|---|---:|
| Product state, all partitions | `0` bits |
| Bell single-qubit cut | `1.000094536943` bits |
| Bell internal two-qubit cut | `0.000308159989` bits |
| Cluster contiguous 2+2 cut | `1` bit |
| Cluster non-contiguous 2+2 cut `[0,2]` | `2` bits |
| Cluster non-contiguous 2+2 cuts generally | `2` bits |

The Phase 8 smaller-side matrix optimization remains intact. The solver repair corrected the deeper degeneracy issue without reverting that performance improvement.

## Performance verification

For 100 Bell-state single-qubit entropy calls, the post-repair elapsed time was approximately:

```text
0.001384885 seconds
```

The existing `0.5`-second test threshold remains satisfied by a wide margin. No caching or unrelated optimization was added.

## Regression results

`python3 -m py_compile QGRIM_ENGINE.py` passed.

The unchanged official test suite produced:

```text
104 passed, 1 failed in 2.01s
```

The single remaining failure is unchanged and is the previously unresolved sampler contract question:

```text
TestSampler.test_progress_kwarg_accepted
TypeError: sample_circuit() got an unexpected keyword argument 'progress'
```

The external complete regression harness, which temporarily made the extensionless `test_y_py` discoverable outside the repository, produced:

```text
111 passed, 1 failed in 2.08s
```

It reported the same sampler failure and no new failure. The Y test was not renamed in the repository.

The external core audit completed 1,121 checks with zero failures after the solver repair. These checks covered direct gate truth tables, assembled execution, measurement invariants, seeded sampling, noise boundaries, and canonical entropy spot checks.

## Causal conclusion

The solver replacement removed the degenerate-spectrum entropy defect while preserving the prior successful behavior. The result supports the following causal statement:

> Replacing power iteration plus rank-one deflation with complex-Hermitian Jacobi diagonalization fixed the demonstrated repeated-eigenvalue loss. It did not repair or alter the sampler API, test discovery, Bloch convention, teleportation, QFT, Grover, or other outstanding Phase 10 findings.

## Remaining risks

The implementation is a small-matrix solver intended for the entropy path, with supported matrices no larger than the current four-qubit partition limit. It was verified on controlled spectra, random Hermitian matrices, positive-semidefinite reduced states, and the full regression suite. It was not presented as a historically recovered implementation; it is a documented engineering reconstruction.

Invalid entropy partition inputs remain unresolved. The Bloch-sphere y-sign defect, teleportation correction defect, QFT semantic failure, Grover semantic failure, and sampler `progress=False` contract ambiguity remain unchanged and must be handled in separate causal phases.

## Final safety state

| Reference | State |
|---|---|
| `main` | Unchanged at `a504f6c` |
| `qgrim-recovery` | `6d41f78` |
| Working tree | Clean |
| Files changed in Phase 11A | `QGRIM_ENGINE.py` only, restricted to `_hermitian_eigenvalues()` |
| Tests changed | None |
| Push performed | None |
