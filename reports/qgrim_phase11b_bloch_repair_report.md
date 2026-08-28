# QGRIM Phase 11B — Bloch-Sphere Y Convention Repair

## Scope and provenance

Phase 11B was a localized repair of the Bloch-sphere y-coordinate convention. It began from Phase 11A checkpoint `6d41f78` on `qgrim-recovery`.

Only one executable expression changed in `QGRIM_ENGINE.py`:

```python
y = 2.0 * rho01.imag
```

became:

```python
y = -2.0 * rho01.imag
```

No gates, phase conventions, state representation, Q4.12 quantization, entropy, solver, sampler/API, tests, or algorithms were changed.

## Contract

Under `rho = |psi><psi|`, the standard Bloch coordinates are:

```text
x =  2 Re(rho01)
y = -2 Im(rho01)
z =    rho00 - rho11
```

The previous implementation used the opposite y sign. This reversed the labels of `|+i>` and `|-i>`.

## Independent analytic oracle

The corrected implementation was checked against `|0>`, `|1>`, `|+>`, `|->`, `|+i>`, and `|-i>` constructed from QGRIM gates. The x and z axes remain correct, and the y-axis states now have the expected signs within Q4.12 rounding.

| State | Expected vector | Corrected engine vector | Display |
|---|---|---|---|
| `|0>` | `(0, 0, +1)` | `(0, −0.0, +1)` | `|0>` |
| `|1>` | `(0, 0, −1)` | `(0, −0.0, −1)` | `|1>` |
| `|+>` | `(+1, 0, 0)` | `(0.999786, −0.0, 0)` | `|+>` |
| `|->` | `(−1, 0, 0)` | `(−0.999786, −0.0, 0)` | `|->` |
| `|+i>` | `(0, +1, 0)` | `(0, 0.999786, 0)` | `|+i>` |
| `|-i>` | `(0, −1, 0)` | `(0, −0.999786, 0)` | `|-i>` |

The small magnitude difference from 1 is expected from the existing Q4.12 quantization and was not changed.

## Regression results

`python3 -m py_compile QGRIM_ENGINE.py` passed.

The unchanged official suite produced:

```text
104 passed, 1 failed in 2.02s
```

The only failure remains the pre-existing sampler contract ambiguity:

```text
sample_circuit(..., progress=False)
TypeError: unexpected keyword argument 'progress'
```

No new failure appeared, and no sampler behavior was altered.

## Causal conclusion

The one-line change corrected the demonstrated Bloch y-sign and display-label defect. It did not affect entropy, eigensolver behavior, gate execution, measurement, noise, sampling, QFT, Grover, teleportation, or test discovery.

The repair is therefore causally isolated and independently verified.

## Checkpoint state

```text
6d41f78  Phase 11A numerical solver repair
   ↓
c8aaafd  Phase 11B Bloch Y convention repair
```

`qgrim-recovery` is at `c8aaafd`. `main` remains at `a504f6c`. The working tree is clean, and nothing was pushed.

The remaining Phase 10 findings are unchanged: teleportation correction control, QFT semantics, Grover semantics, entropy input validation, and the ambiguous sampler contract.
