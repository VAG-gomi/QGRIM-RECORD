# QGRIM Phase 11G — Sampler `progress=False` Contract Archaeology

## Result

Phase 11G is complete as an investigation-only phase. No repository source, test, or configuration file was changed. The recovery branch remains clean at:

```text
72edc13 recovery: validate entropy partitions
```

The historical `main` branch remains unchanged at `a504f6c`.

## The remaining failure

The official suite continues to report:

```text
104 passed, 1 failed
```

The one failure is:

```text
sample_circuit(..., progress=False)
→ TypeError: sample_circuit() got an unexpected keyword argument 'progress'
```

This result is unchanged from the clean `18926db` baseline and from the post-11F checkpoint.

## Evidence inventory

The surviving sampler implementation has this public signature:

```python
def sample_circuit(
    source: str,
    shots: int = 1024,
    seed: int = 0xACE1,
    noise_p: float = 0.0,
) -> Dict[str, int]:
```

Its body assembles the circuit, creates a deterministic random-number generator from `seed`, executes independent fresh simulator instances, records measured four-bit strings, and returns counts. It has no `progress` parameter and performs no progress printing, callback invocation, or progress-state calculation.

The existing test asserts only that `progress=False` is accepted and that the returned counts total the requested number of shots. It does not assert visual output, callbacks, timing, intermediate status, or any distinction between `progress=True` and `progress=False`.

All normal sampler call sites in the engine use only `source`, `shots`, and occasionally `noise_p`; none passes `progress`. The README documents shot sampling and histogram output but contains no `progress` or `progress=False` API description. Repository-wide search found no other reference to the parameter.

The Git history contains only one original repository commit, `a504f6c`. That commit introduced both the sampler implementation and the failing test. Blame assigns the sampler body and the test assertion to the same commit by the original repository author. There is no earlier implementation, later correction, or historical version in the available repository history that establishes what `progress` was intended to do.

| Evidence source | Finding | Strength for historical API recovery |
|---|---|---|
| Current sampler signature | No `progress` parameter | Strong evidence against implemented support |
| Current sampler body | No progress output or hook | Strong evidence that semantics are absent |
| Engine call sites | Never pass `progress` | Evidence against internal reliance |
| README | Describes sampler, omits `progress` | Evidence against documented public API |
| Existing test | Explicitly expects `progress=False` acceptance | Evidence that the test author intended acceptance |
| Git history | Test and implementation introduced together in one commit | Establishes inconsistency, not a recoverable prior design |

## What `progress=False` could mean

If a compatibility parameter were added today, the only observable meaning supported by surviving code would be a **display-control no-op**: accept the flag and leave the returned count dictionary, random stream, and current lack of progress output unchanged. An external adapter demonstrated this behavior: calls with `progress=True` and `progress=False` returned identical seeded Bell histograms and emitted no stdout.

That probe does not recover historical intent. It only shows that a no-op parameter would be a technically coherent new compatibility contract. Other meanings—such as printing progress when true, suppressing progress when false, invoking a callback, or changing execution behavior—have no surviving implementation or documentation evidence.

## Classification

The most defensible classification is:

> **Historically inconsistent and presently ambiguous; not proven to be either a recoverable implementation omission or a stale test.**

It is not appropriate to label the test simply “stale,” because it is part of the original commit and explicitly states an API expectation. It is also not appropriate to claim that the missing parameter is a historically recoverable implementation defect, because the original implementation and test were committed together and no specification explains the intended behavior.

Adding `progress=False` as an ignored keyword would satisfy the test, but that would be a **new compatibility decision**, not historical recovery. Implementing visible progress reporting would be even more clearly new engineering. Neither choice was made in Phase 11G.

## Decision

No sampler code change is authorized by the evidence-first recovery standard. The remaining failure should remain documented as an unresolved API-contract inconsistency until a deliberate product decision is made outside historical recovery.

If a future engineering phase chooses compatibility, its contract should explicitly specify the parameter type, default, whether `True` displays progress, whether `False` suppresses it, whether output is permitted in library use, and whether seeded counts must remain identical. That future decision must be labeled new engineering rather than presented as recovery.

## Final state

| Item | State |
|---|---|
| `main` | Unchanged at `a504f6c` |
| `qgrim-recovery` | Clean at `72edc13` |
| Sampler source changed in 11G | No |
| Tests changed in 11G | No |
| Official suite | `104 passed, 1 failed` |
| Remaining failure | `progress=False` unexpected keyword |
| QFT/Grover | Investigated, unrepaired |
| Next action | Deliberate post-recovery compatibility decision, if desired |

The recovery sequence therefore remains disciplined: demonstrated defects were repaired causally, algorithmic failures were characterized without speculative repairs, entropy input validation was isolated, and the sampler disagreement remains explicitly unresolved rather than being hidden by a test-oriented API addition.
