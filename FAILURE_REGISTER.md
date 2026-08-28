# Failure Register

## Remaining failure

| Field | Record |
|---|---|
| Test | `TestSampler.test_progress_kwarg_accepted` |
| Source | `test_sample.py`, lines 85–87 in the implementation repository |
| Call | `sample_circuit(BELL_SRC, shots=10, seed=0, progress=False)` |
| Observed result | `TypeError: sample_circuit() got an unexpected keyword argument 'progress'` |
| Execution point | Python argument binding, before `sample_circuit()` executes |
| Current classification | Unresolved historical/API contract mismatch |

## Technical mechanism

The surviving sampler accepts `source`, `shots`, `seed`, and `noise_p`. It has no `progress` parameter and no `**kwargs` catch-all. The failing call therefore never enters the sampler body. The sampler’s actual supported behavior—fresh simulator per shot, seeded execution, measurement collection, and count aggregation—is unrelated to the failure.

## Evidence

The test was introduced in the original baseline commit `a504f6c`, together with the sampler implementation. Repository history contains no earlier alternate signature or progress mechanism. The current README, PROVENANCE, and release-surface documents preserve the mismatch rather than reinterpret it.

A read-only suite run with only this test deselected produced:

```text
150 passed, 1 deselected
```

This demonstrates that the test is the sole remaining official failure and that its exclusion changes verification status, not runtime behavior.

## Current decision

Do not delete the test, silently reclassify it, or add a no-op parameter merely to obtain a green suite. Preserve it as historical evidence until a deliberate API decision defines whether `progress` should be unsupported, removed from the test contract, or implemented with observable semantics.

## Non-inferable intent

The surviving material cannot establish whether `progress=False` was intended to suppress output, control logging, invoke a callback, drive a progress bar, or act as a no-op. None of these meanings should be presented as historical fact.

## Author and date

Manus AI, 2026-08-28.
