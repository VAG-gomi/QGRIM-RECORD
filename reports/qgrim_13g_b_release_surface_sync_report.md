# QGRIM 13G-B — Release Surface Synchronization

## Scope and provenance

13G-B began from the frozen Tier-1 API-hardening artifact `df48f3a` and was implemented on the new branch `qgrim-packaging`.

The isolated commit is:

```text
321598b docs: synchronize direct-execution release surface
```

This phase changed only documentation and release-surface description. No algorithm, API, test behavior, dependency, package metadata, or suspicious auxiliary artifact was changed.

| Reference | State |
|---|---|
| `main` | `a504f6c`, unchanged |
| `qgrim-recovery` | `72edc13`, unchanged |
| `qgrim-engineering-qft-grover` | `3e88909`, unchanged |
| `qgrim-docs-sync` | `05b10eb`, unchanged |
| `qgrim-api-hardening` | `df48f3a`, unchanged |
| 13G-B branch | `qgrim-packaging` at `321598b`, clean |
| Pushes | None |

## Changes made

### QGRIM module documentation

The module docstring, which is also the source of the CLI `--help` output, now identifies the artifact as a reconstructed engineering edition, reports 19 built-in circuits rather than 16, and clarifies that direct built-in execution requires no installation or internet access while tests and provenance are separate files.

### Direct-Execution Release Surface

A new `RELEASE_SURFACE.md` defines the intended source distribution surface:

```text
QGRIM_ENGINE.py
README.md
PROVENANCE.md
LICENSE
conftest.py
test_*.py
test_y_py
RELEASE_SURFACE.md
```

The manifest explicitly distinguishes `test_y_py` from the ordinary `test_*.py` suite because its extensionless filename is not discovered by ordinary pytest. It must be executed separately for complete verification and must not be silently renamed.

The manifest also classifies `main.py`, `screen_shot.py`, `QGRIM_Engine _V2.2 ( Future )`, `replit_readme.md`, `pyproject_toml.`, `uv.lock`, and `.npmrc` as retained non-primary workspace or historical artifacts. None was deleted, moved, renamed, or converted.

### README synchronization

The README now links to the direct-execution manifest, states the exact `test_y_py` discovery boundary, and clarifies that the suspicious workspace artifacts remain pending a separate cleanup decision.

## Verification

The post-commit checks completed successfully:

| Check | Result |
|---|---|
| Syntax compilation | Pass |
| `QGRIM_ENGINE.py --help` | Pass; reconstructed edition and 19 circuits shown |
| `QGRIM_ENGINE.py --list` | Pass; 19 circuits listed |
| `QGRIM_ENGINE.py --isa` | Pass; `IFX`, `IFZ`, `MARK`, `REFLECT` shown |
| Direct `--run bell` | Pass; executable completes normally |
| Test collection | 151 tests; extensionless `test_y_py` remains undiscovered |
| Official pytest | `150 passed, 1 failed` |
| 12A integration | `18/18 passed` |
| QFT audit | Unchanged; process fidelity `0.9986614`, round-trip error `7.96e-4` |
| Grover audit | Unchanged; target probability `0.47265625` |
| Noise audit | Unchanged; all hardening checks pass |
| Diff check | Pass |

The sole official failure remains intentionally unchanged:

```text
TestSampler.test_progress_kwarg_accepted
TypeError: sample_circuit() got an unexpected keyword argument 'progress'
```

No compatibility behavior was invented for `progress=False`.

## Exact diff boundary

The complete 13G-B diff from `df48f3a` contains exactly three files:

| File | Change |
|---|---|
| `QGRIM_ENGINE.py` | Module-docstring/help-text synchronization only |
| `README.md` | Release-surface and `test_y_py` documentation |
| `RELEASE_SURFACE.md` | New direct-execution release manifest |

The explicitly excluded files were verified unchanged: `main.py`, `screen_shot.py`, `QGRIM_Engine _V2.2 ( Future )`, `replit_readme.md`, `pyproject_toml.`, `uv.lock`, `.npmrc`, and `test_sample.py`.

## Disposition

13G-B passes as a narrow release-surface synchronization phase. QGRIM now has an explicit direct-execution release manifest without implying pip packaging or installer support. The historical/API sampler ambiguity remains visible and unchanged, and all prior algorithmic, numerical, and API verification results are preserved.

The next appropriate phase is a read-only 13G-C release audit from `321598b`, followed by any separately authorized Tier-2 API design. No general cleanup was performed.

## References

[1]: /home/ubuntu/qgrim_13g_b_postcommit_verification.txt "Post-commit CLI and regression verification"
[2]: /home/ubuntu/qgrim_13g_b_commit.txt "13G-B commit and excluded-artifact verification"
[3]: /home/ubuntu/qgrim_13g_b_branch_baseline.txt "13G-B branch baseline and prior test result"
[4]: /home/ubuntu/QGRIM_-ENGINE-.PY/RELEASE_SURFACE.md "Direct-Execution Release Surface manifest"
[5]: /home/ubuntu/QGRIM_-ENGINE-.PY/README.md "Synchronized README"
[6]: /home/ubuntu/QGRIM_-ENGINE-.PY/QGRIM_ENGINE.py "Primary QGRIM runtime and CLI source"
