# QGRIM Status

## Status at archive creation

QGRIM has completed evidence-driven recovery, explicitly scoped algorithmic reconstruction, numerical/input hardening, documentation synchronization, API hardening, and release-artifact audits. The release-oriented engineering artifact is frozen at commit `321598b` on the `qgrim-packaging` branch of `VAG-gomi/QGRIM_-ENGINE-`.

## Verification state

| Surface | Result |
|---|---|
| Focused Tier-1 API tests | 46 passed |
| Integration matrix | 18/18 passed |
| QFT independent audit | Passed under explicit forward-QFT contract; Q4.12 residuals documented |
| Grover independent audit | Passed; exact oracle/diffusion comparison and target probability `0.47265625` |
| Noise boundary audit | Passed after finite `[0,1]` input validation and recursion prevention |
| Official pytest | 150 passed, 1 failed |
| `test_y_py` extensionless coverage | Present but not discovered by ordinary pytest |

## Remaining failure

The sole official failure is `TestSampler.test_progress_kwarg_accepted`. The call supplies `progress=False`, but the surviving `sample_circuit()` signature has no `progress` parameter. Python rejects the keyword before sampler execution. This is recorded in [`FAILURE_REGISTER.md`](FAILURE_REGISTER.md).

## What is verified

The accepted engineering artifact has verified core gate/state behavior, measurement and seeded sampling behavior, entropy partition validation and solver behavior, Bloch coordinates, teleportation correction branches, forward QFT construction and round trip, Grover oracle/diffusion construction, finite noise input handling, and Tier-1 public API boundaries.

## What is not claimed

This archive does not claim that the surviving source exactly represents historical author intent. QFT and Grover are explicitly engineered reconstructions. `IFX`, `IFZ`, `MARK`, and `REFLECT` are simulator-only reconstructed extensions. The unresolved sampler expectation is not silently converted into a feature.

## Release model

QGRIM is currently a direct-execution source artifact rather than a conventional pip-installable package. The primary runtime is `QGRIM_ENGINE.py`; the direct-execution manifest is preserved in the source repository’s `RELEASE_SURFACE.md` snapshot.

## Frozen implementation references

- Historical baseline: `main` at `a504f6c`.
- Recovery branch: `qgrim-recovery` at `72edc13`.
- Engineering reconstruction/hardening: `3e88909`.
- Documentation synchronization: `05b10eb`.
- Tier-1 API hardening: `df48f3a`.
- Release-surface synchronization: `321598b`.

## Author and date

Manus AI, 2026-08-28.
