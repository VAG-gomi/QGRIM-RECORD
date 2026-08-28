# QGRIM Release Record

## Release-oriented artifact

The release-oriented QGRIM artifact is the direct-execution engineering branch at `321598b`, built from the frozen recovery and engineering sequence. It is a source checkout, not a pip-installable distribution.

Run the primary program with:

```bash
python3 QGRIM_ENGINE.py --help
python3 QGRIM_ENGINE.py --list
python3 QGRIM_ENGINE.py --isa
python3 QGRIM_ENGINE.py --run bell
```

The runtime is stdlib-only. The primary executable is `QGRIM_ENGINE.py`. The complete direct-execution surface is specified in `RELEASE_SURFACE.md` in the implementation repository and copied into `source-snapshots/` here.

## Verified state

| Verification surface | Result |
|---|---|
| Tier-1 API tests | 46 passed |
| Integration matrix | 18/18 passed |
| QFT | Independent operator audit passed; Q4.12 error budget recorded |
| Grover | Independent oracle/diffusion audit passed; target probability `0.47265625` |
| Noise | Finite probability validation and recursion guard passed |
| Official pytest | 150 passed, 1 failed |
| Extensionless `test_y_py` | Separately executed; not ordinary pytest discovery |

## Remaining limitation

The one official failure is intentionally preserved in `FAILURE_REGISTER.md`. It is a historical/API contract ambiguity, not evidence of a broken sampler execution path.

## Engineering status

The source behavior is considered a validated reconstructed engineering baseline, not a claim of exact historical author intent. QFT and Grover are explicit standard-contract reconstructions. `IFX`, `IFZ`, `MARK`, and `REFLECT` are simulator-only engineered extensions. Historical `main` remains separate and immutable.

## Release decision

The artifact is suitable for preservation as a release-oriented engineering baseline under the direct-execution model. Formal package installation, file-API redesign, sampler progress semantics, and additional cleanup remain future engineering tracks.

## Author and date

Manus AI, 2026-08-28.
