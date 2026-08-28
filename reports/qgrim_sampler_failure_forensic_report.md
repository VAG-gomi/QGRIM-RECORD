# QGRIM — Sampler `progress=False` Failure Forensic Report

## Scope and baseline

This was a read-only forensic investigation on `qgrim-packaging` at `321598b`, the release-oriented engineering baseline. No source file, test, documentation, branch, or commit was modified.

| Reference | State |
|---|---|
| Current branch | `qgrim-packaging` |
| Current head | `321598b` |
| Working tree | Clean |
| Historical main | `a504f6c`, unchanged |
| Recovery branch | `72edc13`, unchanged |

The investigation concerns the one remaining official pytest failure:

```text
TestSampler.test_progress_kwarg_accepted
TypeError: sample_circuit() got an unexpected keyword argument 'progress'
```

## A. Exact failing test

The failure is in `test_sample.py`, method `TestSampler.test_progress_kwarg_accepted`:

```python
def test_progress_kwarg_accepted(self):
    """sample_circuit accepts progress=False without error."""
    counts = sample_circuit(BELL_SRC, shots=10, seed=0, progress=False)
    assert sum(counts.values()) == 10
```

The test expects two things: first, that the call accepts a keyword named `progress` with value `False`; second, that the resulting counts contain ten samples. The assertion does not specify whether progress should suppress output, control a callback, alter timing, or have any other observable effect.

The test imports `sample_circuit` directly from `QGRIM_ENGINE`; no wrapper or decorator is involved.

## B. Exact exception mechanism

The current signature is:

```python
def sample_circuit(
    source: str,
    shots: int = 1024,
    seed: int = 0xACE1,
    noise_p: float = 0.0,
) -> Dict[str, int]:
```

The complete relevant signature is therefore:

```text
(source: str, shots: int = 1024, seed: int = 44257, noise_p: float = 0.0) -> Dict[str, int]
```

`progress` is not one of the named parameters, and the function has no `**kwargs` collection. Python rejects the unexpected keyword during call argument binding, before the function body begins. A tracing probe recorded no `call`, `line`, `return`, or `exception` event for `sample_circuit` when the failing invocation was made:

```text
sample_circuit_trace_events=[]
entered_sample_circuit=False
```

Thus the failure is not caused by assembler execution, simulator execution, sampling, measurement, a wrapper, or a later assertion. The exact mechanism is an argument-binding `TypeError` before entry into `sample_circuit`.

## C. Actual `sample_circuit` behavior

The current implementation is:

```python
def sample_circuit(
    source: str,
    shots: int = 1024,
    seed: int = 0xACE1,
    noise_p: float = 0.0,
) -> Dict[str, int]:
    """
    Run the circuit `shots` times (independent fresh state each run).
    `shots` must be a non-negative integer; zero returns an empty dictionary.
    Returns a dict: 4-bit bitstring → count.
    """
    shots = _validate_nonnegative_integer(shots, "shots")
    program = assemble(source)
    counts: Dict[str, int] = {}
    rng = random.Random(seed)
    for _ in range(shots):
        sim = QGRIMSim(seed=rng.randint(0, 0xFFFFFFFF), noise_p=noise_p)
        sim.run(program)
        bits = "".join(str(sim.measurements.get(q, 0)) for q in range(QUBITS))
        counts[bits] = counts.get(bits, 0) + 1
    return counts
```

Its actual behavior is as follows:

| Aspect | Observed implementation |
|---|---|
| Circuit input | QGRIM source text, assembled once before the shot loop |
| Shot input | Non-negative integer validated at entry; zero returns `{}` |
| State isolation | Creates a fresh `QGRIMSim` for every shot |
| Per-shot seed | Derives a seed from a local `random.Random(seed)` instance |
| Default seed | `0xACE1`, equal to `44257` |
| Noise | Passes `noise_p` into each fresh simulator |
| Execution | Runs the assembled program once per fresh simulator |
| Measurement | Reads `sim.measurements[q]` for q0 through q3, defaulting missing entries to 0 |
| Return value | `Dict[str, int]`, mapping four-bit strings to counts |
| Output | No progress output, callback, status update, or display-control branch |

Observed calls confirm the documented core behavior. A measured one-qubit superposition produced one four-bit result for one shot and two possible results for ten shots. Identical `(source, shots, seed)` inputs produced identical dictionaries; changing the seed changed the sampled result in the probe. `shots=0` returned `{}`.

There is no `progress` parameter, no `**kwargs`, and no code path that refers to progress reporting.

## D. Complete repository occurrences of `progress`

On the frozen release branch, the word appears only in these tracked repository locations:

| File | Occurrence type | Meaning |
|---|---|---|
| `test_sample.py:85-87` | Historical test | Method name, docstring, and call requiring `progress=False` |
| `README.md:72`, `85-86` | Maintenance documentation | Describes the preserved ambiguity and displays the exact failure |
| `PROVENANCE.md:39` | Maintenance/provenance documentation | Labels the mismatch intentionally unresolved |
| `RELEASE_SURFACE.md:52` | Release-surface documentation | States that `progress=False` is not part of the current API contract |

There are no `progress` occurrences in `QGRIM_ENGINE.py`, `conftest.py`, the API contract tests, or other runtime implementation files.

The search also found no `callback`, `tqdm`, `percentage`, `spinner`, or progress-specific mechanism. The word `status` occurs only in the README heading `Verification status`. The word `iteration` refers to numerical eigenvalue comments and a Grover test description, not sampler progress. The word `bar` refers to histogram/probability display bars, not progress reporting.

The sampler and CLI do produce ordinary result and histogram output, but those are completed-result displays. They are not an iteration progress API and do not establish what a hypothetical `progress=False` flag would control.

## E. Historical evidence

The historical evidence is limited but precise:

1. `git blame` assigns the failing test method and its assertion to the original baseline commit `a504f6c`.
2. `git log -Ssample_circuit -- QGRIM_ENGINE.py test_sample.py --all` finds only the original baseline commit `a504f6c`.
3. `git log -Sprogress --all` finds the original baseline commit and later documentation commits `05b10eb` and `321598b`.
4. The original implementation and the failing test were introduced together in `a504f6c`.
5. No earlier version, later implementation, callback, display loop, or alternate sampler signature exists in the repository history examined.

The test is therefore historical evidence that someone expected the keyword to be accepted. It is not evidence of the keyword’s intended semantics. The implementation is equally historical evidence that the surviving function did not accept it in the same baseline snapshot.

The later README, `PROVENANCE.md`, and `RELEASE_SURFACE.md` statements are recovery/maintenance documentation. They accurately preserve the ambiguity, but they do not recover an original meaning.

## F. What is known

The following facts are established directly from source, execution, and history:

- The exact failing call is `sample_circuit(BELL_SRC, shots=10, seed=0, progress=False)`.
- The test expects the call to succeed and return ten samples.
- The current function signature has no `progress` parameter and no `**kwargs`.
- Python raises the `TypeError` before entering `sample_circuit`.
- The current sampler assembles once, executes fresh simulator state per shot, uses seeded per-shot RNG derivation, reads measurement storage, and returns a count dictionary.
- The current sampler has no progress callback, progress bar, percentage, spinner, or progress-specific output mechanism.
- `progress=False` occurs in one historical test and in later explanatory documentation, not in the runtime implementation.
- The official suite’s only failure is this call-binding error.

## G. What is unknown

The surviving repository does not establish:

- Whether `progress` was intended to suppress an output display.
- Whether it was intended to enable a progress bar or callback.
- Whether it was intended to control per-shot status output, logging, or a CLI-only feature.
- Whether `True` should display anything.
- Whether a callback, frequency, stream, or return-value change was ever planned.
- Whether the test was written ahead of an omitted implementation, copied from another version, or left stale in the original snapshot.
- Whether a compatible implementation should be a no-op flag, an output-control flag, a callback API, or something else.

## H. Can the semantics be reconstructed?

No. The acceptance of the keyword can be established from the test, but its semantics cannot be reconstructed with confidence from surviving evidence.

The most that can be inferred is that the test author expected accepting `progress=False` not to prevent the sampler from returning ten counts. That does not determine whether `progress` should have any behavior when set to `True`, whether output should be suppressed, or whether a progress mechanism existed outside the surviving snapshot.

## I. What must not be inferred

The following conclusions would exceed the evidence:

- That the test is definitely stale.
- That the implementation definitely omitted a planned parameter.
- That `progress=False` was intended as a no-op.
- That it was intended to suppress the ASCII histogram.
- That it was intended to suppress per-shot output, even though no such output exists in the current sampler.
- That adding a defaulted parameter would recover historical behavior.
- That modifying or removing the test would correct the repository.
- That making pytest green would establish semantic correctness.

## J. Recommended next decision

Keep the current behavior unchanged in the forensic/release baseline. The evidence supports classifying the failure as an **original historical/API inconsistency with unrecoverable progress semantics**.

Any future change should be a separately named public API decision. It must first define the intended observable contract—accepted values, output behavior, callback or display semantics if any, interaction with seeded sampling, and tests—before implementation. A no-op parameter should not be added merely to change the test count from `150 passed, 1 failed` to green.

> Known fact: `sample_circuit()` does not accept `progress`.
>
> Known consequence: Python rejects the keyword before the sampler executes.
>
> Unknown: what historical behavior, if any, `progress=False` was meant to control.

## References

[1]: /home/ubuntu/qgrim_sampler_failure_forensic.txt "Read-only source, behavior, occurrence, and history probe"
[2]: /home/ubuntu/QGRIM_-ENGINE-.PY/test_sample.py "Historical sampler tests"
[3]: /home/ubuntu/QGRIM_-ENGINE-.PY/QGRIM_ENGINE.py "Current sample_circuit implementation"
[4]: /home/ubuntu/QGRIM_-ENGINE-.PY/README.md "Maintained sampler ambiguity documentation"
[5]: /home/ubuntu/QGRIM_-ENGINE-.PY/PROVENANCE.md "Provenance classification of unresolved behavior"
[6]: /home/ubuntu/QGRIM_-ENGINE-.PY/RELEASE_SURFACE.md "Current direct-execution API boundary"
