# Sampler Test Impact Analysis

## Scope

This is a read-only analysis of `TestSampler.test_progress_kwarg_accepted` on the frozen QGRIM release-oriented branch. No repository files, tests, or branches were modified.

## Exact failure

The historical test calls:

```python
sample_circuit(BELL_SRC, shots=10, seed=0, progress=False)
```

The surviving function signature accepts `source`, `shots`, `seed`, and `noise_p`, but not `progress` and not arbitrary keyword arguments. Python rejects the unknown keyword during argument binding, before `sample_circuit()` begins execution.

## Dependency findings

The test is an isolated test method. No runtime code imports or calls the test. The only runtime call graph is through the other sampler tests and production callers that use the supported parameters. The repository contains no progress callback, progress bar, logging loop, or other sampler progress mechanism.

The test was introduced in the original baseline commit `a504f6c`, together with the sampler implementation. No earlier alternate sampler signature or progress implementation was found. Later README, provenance, and release-surface references document the mismatch; they do not establish historical semantics.

## Consequence comparison

| Policy | Runtime behavior | Test result | Evidence/provenance consequence |
|---|---|---|---|
| Preserve test | No change | `150 passed, 1 failed` | Historical expectation remains visible |
| Deselect/reclassify test without deleting it | No change | `150 passed, 1 deselected` | Failure is hidden from ordinary suite unless separately recorded |
| Remove test from repository | No change | Likely `150 passed` | Historical evidence is lost unless archived elsewhere |
| Implement `progress` | New API behavior | Could become `151 passed` | Requires inventing semantics; not historical recovery |

A read-only pytest deselection confirmed that excluding only this test produces `150 passed, 1 deselected`. This demonstrates that removing or reclassifying the expectation changes suite status and coverage accounting, not QGRIM runtime behavior.

## Conclusion

There is no working `progress` feature in the engine to remove. Removing the failing test would be safe for current runtime behavior, but it would be a deliberate test-suite and provenance change. The scientifically conservative policy is to preserve the test and classify it as an unresolved historical/API contract expectation. Any future reclassification or API implementation must be an explicit post-reconstruction engineering decision.

## Provenance boundary

The historical branch and release-oriented artifacts remain unchanged. This analysis does not authorize or perform a test modification, sampler change, or API compatibility addition.

## References

- `test_sample.py`, historical sampler test and failing expectation.
- `QGRIM_ENGINE.py`, surviving `sample_circuit` signature and implementation.
- `qgrim_sampler_test_impact_trace.txt`, repository references and Git blame.
- `qgrim_sampler_test_impact_final.txt`, historical trace and deselected-suite result.
- `README.md`, `PROVENANCE.md`, and `RELEASE_SURFACE.md`, current explicit documentation of the unresolved behavior.
- Git baseline commit `a504f6c`, original source/test provenance.

## Author

Manus AI

## Date

2026-08-28

---

## Note on evidence

This report uses only local repository files, local Git history, and read-only test execution. No external web sources were required.
