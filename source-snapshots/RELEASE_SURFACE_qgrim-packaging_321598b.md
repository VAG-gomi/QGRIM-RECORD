# QGRIM Direct-Execution Release Surface

This repository is released as a **direct-execution source artifact**, not as an installer package or pip distribution. The primary runtime is `QGRIM_ENGINE.py`.

## Primary release surface

The following files belong to the intended QGRIM direct-execution and verification surface:

| File or pattern | Role |
|---|---|
| `QGRIM_ENGINE.py` | Primary runtime module, assembler, simulator, CLI, REPL, built-in circuits, and analysis helpers |
| `README.md` | User-facing operating and feature documentation |
| `PROVENANCE.md` | Historical/recovery/reconstruction/hardening provenance map |
| `LICENSE` | MIT release license |
| `conftest.py` | Reconstructed pytest infrastructure required by the surviving tests; not claimed to be historical |
| `test_*.py` | Standard pytest verification files discovered by ordinary pytest |
| `test_y_py` | Additional valid Pauli-Y verification file with no `.py` suffix; ordinary pytest does not discover it unless it is explicitly renamed or loaded by a separate harness |
| `RELEASE_SURFACE.md` | This direct-execution release manifest |

The standard suite currently includes the `test_*.py` files. `test_y_py` is intentionally listed separately because its extensionless filename places it outside ordinary pytest discovery. It should be executed separately when complete historical verification coverage is required; it should not be renamed silently as part of release packaging.

## Not part of the primary release surface

The following tracked artifacts are retained in the repository for historical or workspace context, but are not required to execute the current QGRIM engine directly:

| Artifact | Current classification |
|---|---|
| `main.py` | Generic workspace greeting; not the QGRIM entry point |
| `screen_shot.py` | Captured menu text; not executable Python |
| `QGRIM_Engine _V2.2 ( Future ) ` | One-line future-version placeholder |
| `replit_readme.md` | Stale pnpm/TypeScript workspace and absent hardware-blueprint description |
| `pyproject_toml.` | Nonstandard, inactive generic workspace metadata; not `pyproject.toml` |
| `uv.lock` | Generic workspace lockfile for gdstk/NumPy; not required by the stdlib-only engine path |
| `.npmrc` | Generic npm workspace configuration; not used by QGRIM runtime execution |

These artifacts must not be deleted, renamed, moved, or converted solely because they are not part of the primary release surface. Any future cleanup requires a separate packaging decision and implementation phase.

## Direct execution

From the repository directory:

```text
python3 QGRIM_ENGINE.py --list
python3 QGRIM_ENGINE.py --run bell
python3 QGRIM_ENGINE.py --isa
```

No `pip install` step is implied by this release surface. Formal Python package metadata and installer behavior are separate future engineering decisions.

## Numerical and API boundaries

The runtime uses a four-qubit Q4.12-like fixed-point state-vector model. Small norm and operator errors are expected within the documented numerical budget. Simulator-only extensions such as `IFX`, `IFZ`, `MARK`, and `REFLECT` are not historical hardware ISA instructions and are not sent to FPGA hardware. The sampler `progress=False` behavior remains intentionally unresolved and is not part of the current public API contract.
