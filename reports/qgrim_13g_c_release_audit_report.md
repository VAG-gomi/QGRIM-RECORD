# QGRIM 13G-C — Release Artifact and Packaging Readiness Audit

## Scope and baseline

13G-C was a strictly read-only release audit of `qgrim-packaging` at `321598b`. No source, test, documentation, packaging, branch, or historical artifact was modified.

| Reference | Verified state |
|---|---|
| `main` | `a504f6c`, unchanged |
| `qgrim-recovery` | `72edc13`, unchanged |
| `qgrim-engineering-qft-grover` | `3e88909`, unchanged |
| `qgrim-docs-sync` | `05b10eb`, unchanged |
| `qgrim-api-hardening` | `df48f3a`, unchanged |
| Release-surface branch | `qgrim-packaging` at `321598b` |
| Working tree | Clean |
| 13G-C repository changes | None |
| Pushes | None |

## Release-surface integrity

Every file declared by `RELEASE_SURFACE.md` exists and is represented in the manifest:

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

The manifest separately identifies `test_y_py` because its extensionless name is not discovered by ordinary pytest. The audit confirmed that the listed workspace artifacts are explicitly classified as outside the primary release surface: `main.py`, `screen_shot.py`, `QGRIM_Engine _V2.2 ( Future )`, `replit_readme.md`, `pyproject_toml.`, `uv.lock`, and `.npmrc`.

No excluded workspace artifact is referenced as a required primary runtime file. No suspicious artifact was deleted, moved, renamed, or converted.

## Direct-execution reproducibility

The runtime is reproducible as a direct source checkout. The following commands completed successfully:

```text
python3 QGRIM_ENGINE.py --help
python3 QGRIM_ENGINE.py --list
python3 QGRIM_ENGINE.py --isa
python3 QGRIM_ENGINE.py --run bell
```

The CLI help identifies the reconstructed engineering edition and 19 built-in circuits. The live registry contains exactly 19 circuits, and `--list` reports 19. `--isa` exposes the documented simulator-only `IFX`, `IFZ`, `MARK`, and `REFLECT` extensions. A representative Bell execution completed and produced measurement output.

The module imports successfully as `QGRIM_ENGINE`. Static import analysis found no non-standard-library runtime imports. The direct execution model therefore does not require the unrelated dependencies listed by the inert `pyproject_toml.` and `uv.lock` workspace residue.

## Documentation consistency

The README links to `RELEASE_SURFACE.md` and explicitly discloses the `test_y_py` discovery boundary. The manifest repeats that disclosure. `PROVENANCE.md` contains the auxiliary-file map and the historical → recovery → reconstruction → hardening stage terminology. The README and manifest document the simulator-only extensions and preserve the unresolved `progress=False` behavior.

The module docstring, `--help`, and registry agree on the reconstructed edition and the 19-circuit count. The CLI ISA output contains all four simulator-only extensions. The direct-execution release model is consistently described as source execution rather than pip installation.

## Verification surface

| Gate | Result |
|---|---|
| Focused API tests | `46 passed` |
| Integration matrix | `18/18 passed` |
| QFT independent audit | Pass; process fidelity `0.9986614`, round-trip error `7.96e-4` |
| Grover independent audit | Pass; target probability `0.47265625` |
| Noise boundary audit | Pass; invalid values rejected and recursion guard passes |
| Official pytest | `150 passed, 1 failed` |

The sole remaining official failure is exactly the unresolved sampler contract:

```text
TestSampler.test_progress_kwarg_accepted
TypeError: sample_circuit() got an unexpected keyword argument 'progress'
```

13G-C did not reinterpret or repair this behavior. `test_y_py` remains explicitly accounted for but is not part of ordinary pytest collection.

## Provenance and cleanliness

The verified provenance chain is:

```text
a504f6c  historical baseline
   ↓
72edc13  evidence-driven recovery
   ↓
3e88909  engineering reconstruction + numerical hardening
   ↓
05b10eb  documentation/provenance synchronization
   ↓
df48f3a  Tier-1 API hardening
   ↓
321598b  release-surface synchronization
   ↓
13G-C    read-only release audit
```

The working tree is clean at `321598b`. The audit found no unintended diff, no branch movement, and no historical mutation.

## Decision

13G-C passes. `321598b` is suitable to freeze as the release-oriented engineering baseline for the current direct-execution model.

This decision does not imply pip packaging, formal installer support, or resolution of every future engineering question. It establishes that the declared source release surface is complete, directly executable, documented, independently verified, and provenance-preserving.

> QGRIM has crossed the release boundary: recovery is complete, reconstruction and Tier-1 hardening are complete, the direct-execution surface is synchronized, and remaining ambiguity is explicit rather than hidden.

Future work should be a new independent track: Tier-2 API design, sampler policy, extended verification, formal packaging, or historical cleanup. None is part of 13G-C.

## References

[1]: /home/ubuntu/qgrim_13g_c_static_audit.txt "13G-C manifest, runtime, documentation, and stdlib audit"
[2]: /home/ubuntu/qgrim_13g_c_full_audit.txt "13G-C complete verification and provenance output"
[3]: /home/ubuntu/qgrim_13g_b_postcommit_verification.txt "13G-B post-commit CLI and regression verification"
[4]: /home/ubuntu/QGRIM_-ENGINE-.PY/RELEASE_SURFACE.md "Direct-Execution Release Surface manifest"
[5]: /home/ubuntu/QGRIM_-ENGINE-.PY/README.md "Synchronized README"
[6]: /home/ubuntu/QGRIM_-ENGINE-.PY/PROVENANCE.md "Provenance and auxiliary-file map"
