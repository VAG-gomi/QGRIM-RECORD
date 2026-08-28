# QGRIM 13G-A — Packaging Disposition Decision

## Scope and baseline

13G-A was a strictly read-only packaging disposition audit of frozen `df48f3a` on `qgrim-api-hardening`. No repository files were moved, deleted, renamed, edited, or regenerated.

| Reference | State |
|---|---|
| `main` | `a504f6c`, unchanged |
| `qgrim-recovery` | `72edc13`, unchanged |
| `qgrim-engineering-qft-grover` | `3e88909`, unchanged |
| `qgrim-docs-sync` | `05b10eb`, unchanged |
| 13D artifact | `df48f3a`, clean |
| 13G-A changes | None |

## Release model

QGRIM is currently coherent as a **single-file/direct-execution distribution**, not as a conventional installable Python package. The primary runtime is `QGRIM_ENGINE.py`, whose actual entry point is `if __name__ == "__main__": cli()`. Direct commands such as `python3 QGRIM_ENGINE.py --list`, `--run bell`, and `--isa` work, and the module imports as `QGRIM_ENGINE` when the repository directory is on `PYTHONPATH`.

There is no recognized `pyproject.toml`, `setup.py`, or `setup.cfg`. The tracked file `pyproject_toml.` is not recognized Python packaging metadata; it describes a generic `repl-nix-workspace` and lists `gdstk` and NumPy dependencies that are not required by the stdlib-only QGRIM runtime. `uv.lock` locks those same unrelated workspace dependencies, and `.npmrc` contains generic npm settings. These files should not be treated as the QGRIM installation recipe.

The tracked `main.py` is not the QGRIM entry point: it only prints `Hello from repl-nix-workspace!`. The current release instruction should therefore name `QGRIM_ENGINE.py` explicitly rather than relying on `main.py`.

## File disposition

| Surface | Evidence-based classification | 13G-A decision |
|---|---|---|
| `QGRIM_ENGINE.py` | Primary runtime, CLI, REPL, assembler, simulator, built-ins | Retain |
| `test_*.py` / `conftest.py` | Verification and reconstructed test infrastructure | Retain |
| `test_y_py` | Seven valid but extensionless tests, not discovered by ordinary pytest | Retain and document separately |
| `README.md` / `PROVENANCE.md` / `LICENSE` | Primary documentation, provenance, and release metadata | Retain |
| `main.py` | Generic workspace greeting; not a QGRIM launcher | Preserve pending explicit entry-point decision |
| `screen_shot.py` | Captured menu text, not executable Python | Preserve pending archival decision |
| `QGRIM_Engine _V2.2 ( Future )` | One-line `Future version` placeholder | Preserve pending historical review |
| `replit_readme.md` | pnpm/TypeScript monorepo and absent `qgrim/` blueprint | Preserve pending cleanup decision |
| `pyproject_toml.` | Nonstandard, inactive generic metadata | Do not rename/delete yet |
| `uv.lock` | Unrelated workspace dependency lockfile | Do not delete yet |
| `.npmrc` | Generic npm workspace residue | Do not delete yet |
| `.pytest_cache/`, `__pycache__/` | Ignored generated artifacts | Exclude from release artifacts |

Every suspicious tracked file was introduced in the original baseline commit `a504f6c` and has no later independent history. That establishes common provenance but does not prove whether each was intended as runtime, workspace, or archival material. Therefore deletion is not justified by appearance alone.

## Documentation and packaging inconsistencies

The synchronized README and `PROVENANCE.md` correctly describe the main history → recovery → reconstruction → hardening boundary and identify the auxiliary files. The primary module docstring and generated `--help` output remain partially stale: they say there are 16 built-in circuits while the live registry and `--list` output contain 19. The `--isa` output correctly lists simulator-only `IFX`, `IFZ`, `MARK`, and `REFLECT`; the `--chip` output still refers to an absent `qgrim/rtl/` and `qgrim/host/` tree, which should be treated as a retained hardware blueprint claim rather than included package content.

## 13G-B recommendations

The next implementation stage should be a new branch from `df48f3a`. The smallest justified packaging work is documentation and release-surface clarification: correct the module docstring’s feature count and obsolete wording, and define a distribution manifest containing the primary engine, README, provenance map, license, tests, reconstructed `conftest.py`, and explicitly documented `test_y_py` status.

Do not create `pyproject.toml` or convert QGRIM into a pip package yet. That would be a separate packaging architecture decision. Do not delete or move `main.py`, `screen_shot.py`, the future placeholder, `replit_readme.md`, `pyproject_toml.`, `uv.lock`, or `.npmrc` until a dedicated cleanup implementation phase obtains sufficient historical or owner evidence.

## Disposition

13G-A establishes a conservative packaging decision: distribute QGRIM as a direct-execution source artifact centered on `QGRIM_ENGINE.py`; retain suspicious tracked files pending explicit cleanup decisions; exclude ignored caches; and postpone formal Python packaging metadata. 13G-B may implement only explicitly approved documentation or release-surface changes.

> The repository has been classified, not cosmetically cleaned. No file is disposable solely because it looks like workspace residue.

## References

[1]: /home/ubuntu/qgrim_13g_disposition_trace.txt "13G-A history, references, imports, metadata, and branch trace"
[2]: /home/ubuntu/qgrim_13f_packaging_inventory.txt "13F tracked-file, ignored-artifact, and repository inventory"
[3]: /home/ubuntu/qgrim_13f_packaging_entrypoints.txt "13F CLI, import, and auxiliary-entry audit"
[4]: /home/ubuntu/qgrim_13f_final_provenance.txt "13F clean-tree and frozen-branch verification"
[5]: /home/ubuntu/QGRIM_-ENGINE-.PY/QGRIM_ENGINE.py "Primary QGRIM runtime and CLI source"
[6]: /home/ubuntu/QGRIM_-ENGINE-.PY/README.md "Synchronized QGRIM documentation"
[7]: /home/ubuntu/QGRIM_-ENGINE-.PY/PROVENANCE.md "QGRIM provenance and auxiliary-file map"
