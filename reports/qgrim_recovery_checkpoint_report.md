# QGRIM Recovery Checkpoint Report

## Scope

Only the missing `conftest.py` test infrastructure was reconstructed. `main`, `QGRIM_ENGINE.py`, all tests, README, metadata, and scaffold files were not edited. The reconstructed file explicitly labels values that cannot be historically recovered from the repository.

## Git state

| Ref | Commit |
|---|---|
| `main` | `a504f6c4769d004a651b58c12666a74c68da4bf1` — original baseline |
| `qgrim-recovery` | `896cc798a03004e806895b3ed6b49721cd920cab` — recovery checkpoint |

The recovery commit is `recovery: reconstruct test infrastructure baseline`. The diff from `a504f6c` contains exactly one added file: `conftest.py`. No commit was pushed.

## Reconstructed infrastructure

`fresh()` returns a new `QGRIMSim()` using the engine constructor defaults. `run(source)` assembles a QASM string and executes it on a fresh simulator. `assert_norm()` computes the sum of squared amplitude magnitudes and checks approximate equality to one. `assert_amp()` compares the complete complex amplitude at an index. `assert_prob()` compares the Born probability `abs(sim.state[index]) ** 2`. `Q412_TOL` is set to `4/4096`, explicitly as a reconstruction choice rather than an alleged historical value. `STAT_TOL` is set to `0.05`, also explicitly marked as a reconstruction choice.

The exact original `conftest.py`, exact tolerance literals, original `fresh()` seed choice, and original assertion-message wording cannot be recovered from the surviving repository. The committed file does not present them as historical facts.

## Official clean-clone test result

The official `pytest -q` run on `qgrim-recovery` cannot collect the suite because `conftest.py` imports `QGRIM_ENGINE`, and the committed engine contains bare non-Python separator/prose lines at line 1. The exact error is:

```text
ImportError while loading conftest '/home/ubuntu/QGRIM_-ENGINE-.PY/conftest.py'.
conftest.py:20: in <module>
    from QGRIM_ENGINE import QGRIMSim, assemble
  File "/home/ubuntu/QGRIM_-ENGINE-.PY/QGRIM_ENGINE.py", line 1
    ===================================================
    ^^
SyntaxError: invalid syntax
```

This is a **repository/package execution barrier**, not a conftest failure. The official suite result is therefore collection failure before test execution.

## Temporary recovery experiment

To classify lower-level failures without rewriting the engine, an external temporary harness copied the repository to a temporary directory, removed only the known non-Python edge lines from the temporary engine copy, copied the committed reconstructed `conftest.py`, and temporarily renamed the extensionless Y test for collection. This did not alter the repository.

Result: **108 passed, 4 failed in 3.69 seconds**.

| Failure | Classification | Exact meaning |
|---|---|---|
| `test_ccx.py::TestToffoli::test_ccx_bounds_error` | Implementation defect | `assemble("CCX 0 1 8")` does not raise `AsmError`; `_encode()` validates 4-bit fields but not the four-qubit domain. |
| `test_cnot.py::TestCNOT::test_cnot_bounds_error` | Implementation defect | Out-of-range CNOT qubits are accepted instead of rejected. |
| `test_entropy.py::TestEntropy::test_entropy_1qubit_faster_than_half_second` | Performance failure | 100 entropy calls took about 1.386 seconds in the sandbox versus the test’s 0.5-second limit. |
| `test_sample.py::TestSampler::test_progress_kwarg_accepted` | API mismatch | `sample_circuit()` does not accept the test’s `progress=False` keyword. |

No additional algorithmic/semantic test failure was exposed by this suite. That does not prove the advanced algorithm claims; the existing tests are not sufficient to establish Grover, QFT, teleportation, or other claims independently.

## Failure categories

| Category | Current status |
|---|---|
| Test infrastructure | Reconstructed and checkpointed; exact historical file remains unrecoverable. |
| Repository/package failure | Engine syntax prevents the official suite from importing. |
| API mismatch | `progress=False` expectation conflicts with `sample_circuit` signature. |
| Implementation defect | Assembler lacks four-qubit bounds validation. |
| Performance failure | Entropy implementation misses the test’s timing threshold in this environment. |
| Algorithmic/semantic uncertainty | Advanced claims remain unverified; no repair was attempted. |

## Final safety statement

The historical baseline `a504f6c` remains intact on `main`. The recovery branch contains only the new `conftest.py` checkpoint. `QGRIM_ENGINE.py`, tests, and all other original files remain unchanged. The repository has not been pushed or rewritten.
