# QGRIM 13F — Packaging and Repository Cleanup Audit

## Scope and baseline

13F was a read-only audit of the frozen engineering artifact `df48f3a` on `qgrim-api-hardening`. No files were moved, deleted, renamed, edited, or regenerated in the repository.

The purpose was to determine what an external user actually receives, which files are active runtime surfaces, which are historical or auxiliary artifacts, and which cleanup actions require a separate engineering decision.

| Reference | State |
|---|---|
| `main` | `a504f6c`, unchanged |
| `qgrim-recovery` | `72edc13`, unchanged |
| `qgrim-engineering-qft-grover` | `3e88909`, unchanged |
| `qgrim-docs-sync` | `05b10eb`, unchanged |
| 13D hardening baseline | `df48f3a`, clean |
| Current branch | `qgrim-api-hardening` |
| 13F repository changes | None |

## What an external user receives

The repository is not currently a conventional installable Python package. It contains one primary runtime module, a collection of pytest files, a reconstructed `conftest.py`, documentation, license, lock/workspace residue, and several auxiliary artifacts. There is no normal `pyproject.toml`, `setup.py`, or `setup.cfg`; the tracked metadata file is named `pyproject_toml.` and is therefore not recognized as standard Python project metadata.

The primary execution path is direct invocation of `QGRIM_ENGINE.py`:

```text
python3 QGRIM_ENGINE.py --list
python3 QGRIM_ENGINE.py --run bell
python3 QGRIM_ENGINE.py --isa
```

The module also imports successfully as `QGRIM_ENGINE` when the repository directory is on `PYTHONPATH`. The actual module entry point ends with `if __name__ == "__main__": cli()`. In contrast, `python3 main.py` prints only `Hello from repl-nix-workspace!` and does not launch QGRIM. This is the most important external entry-point distinction.

The synchronized README now points developers toward `QGRIM_ENGINE.py`, but the module docstring still contains older self-description, including a 16-circuit count while the live registry has 19 circuits. This is a documentation inconsistency inside the primary runtime file, not a packaging failure in execution.

## Surface classification

| Surface | Evidence | Classification | 13F action |
|---|---|---|---|
| `QGRIM_ENGINE.py` | Contains assembler, simulator, CLI, REPL, built-ins, and `__main__` CLI entry point | Primary runtime | Retain |
| `test_*.py` | Imported by pytest and exercise the engine | Primary verification surface | Retain |
| `test_y_py` | Seven valid tests but extensionless and not discovered by ordinary pytest | Test-discovery auxiliary | Retain; document separately |
| `conftest.py` | Supplies reconstructed test fixtures and tolerances | Recovery test infrastructure | Retain; provenance is documented |
| `README.md` | User/developer instructions and current feature/provenance documentation | Primary documentation | Retain |
| `PROVENANCE.md` | History → recovery → reconstruction → hardening map | Primary maintenance documentation | Retain |
| `LICENSE` | MIT license with `VAG-gomi` copyright | Release metadata | Retain |
| `main.py` | Prints a generic repl-nix workspace greeting | Stale/non-primary entry point | Do not delete without owner decision |
| `screen_shot.py` | Markdown-like captured menu text; not syntactically valid Python | Captured/stale artifact | Do not delete without owner decision |
| `QGRIM_Engine _V2.2 ( Future )` | Contains only `Future version` | Placeholder artifact | Do not delete without owner decision |
| `replit_readme.md` | Describes a pnpm/TypeScript monorepo and absent `qgrim/` tree | Stale workspace blueprint | Do not delete without owner decision |
| `pyproject_toml.` | Generic `repl-nix-workspace` metadata with gdstk/numpy dependencies; nonstandard filename | Inert packaging residue | Do not rename without packaging decision |
| `uv.lock` | Locks gdstk/numpy dependencies not used by QGRIM and has no recognized pyproject partner | Generic workspace residue | Do not delete without dependency decision |
| `.npmrc` | Generic npm peer-dependency settings; no QGRIM runtime use | Workspace residue | Retain pending cleanup decision |
| `.pytest_cache/` | Ignored pytest cache directory | Generated artifact | Safe to omit from releases; not tracked |
| `__pycache__/` | Ignored Python bytecode cache | Generated artifact | Safe to omit from releases; not tracked |

## Packaging and installation findings

The repository’s actual runtime is dependency-free in the engine path: `QGRIM_ENGINE.py` imports Python standard-library modules, and direct execution works without installing the dependencies named by the inert `pyproject_toml.`/`uv.lock` workspace residue. The metadata therefore does not describe the QGRIM runtime accurately and should not be used as an installation recipe.

There is no recognized package metadata defining a distribution name, version, console script, or install-time dependency set. An external user receives a source checkout rather than a pip-installable package. This is coherent with the README’s single-file/Pydroid model but not with the generic TypeScript/uv workspace artifacts.

The recommended current release instruction is direct execution of `QGRIM_ENGINE.py`. A future packaging track may choose between preserving the single-file model, adding real Python package metadata, or removing inert workspace metadata. 13F does not choose among those options.

## README and source consistency

The README and `PROVENANCE.md` correctly describe the current engineering branch, Q4.12 limitations, QFT/Grover reconstruction status, simulator-only extensions, unresolved sampler behavior, and primary versus auxiliary files.

The primary module’s top-level docstring remains partially stale. It says `16 built-in circuits`, while the actual registry and synchronized README report 19. It also uses older wording about the original eigenvalue approach and omits the complete post-recovery provenance context. The CLI `--help` output is generated from that module docstring, so an external user sees stale feature-count text there even though `--list` shows the correct 19 circuits.

The CLI `--isa` output now lists `IFX`, `IFZ`, `MARK`, and `REFLECT` as simulator-only extensions. The source and README agree that these are not hardware-compatible historical ISA instructions. The `--chip` output still describes an absent `qgrim/rtl/` and `qgrim/host/` hardware tree; that is best treated as a retained hardware blueprint claim, not proof that those directories are included in this repository.

## Cleanup recommendations for 13G

13F does not authorize deletion or movement. The evidence supports the following future options:

| Candidate | Recommended next action | Reason |
|---|---|---|
| `main.py` | Retain temporarily or replace only after explicit entry-point decision | It is an ineffective generic entry point, but may be workspace scaffolding |
| `screen_shot.py` | Preserve or move to an archival/docs location | It may retain visual/history value despite not being code |
| Future placeholder | Preserve until historical value is resolved | Its content is too small to infer intent |
| `replit_readme.md` | Mark as historical/inert or archive after review | It describes a different monorepo layout |
| `pyproject_toml.` and `uv.lock` | Audit dependency provenance before removal/renaming | They may be workspace metadata, but are not active QGRIM packaging |
| `.npmrc` | Exclude from a Python release artifact; no code action yet | Generic npm residue |
| caches | Exclude from releases and remove only from local workspace if desired | Already ignored and untracked |
| module docstring | Documentation-only maintenance candidate | Feature count and historical algorithm wording are stale |

A future 13G cleanup should be a new branch from `df48f3a` and should use file-level evidence or user confirmation before deleting, renaming, or moving any tracked artifact.

## Final disposition

13F is complete as a read-only packaging audit. The engineering artifact is executable and importable as a source checkout, but it is not yet a conventional installable package with a declared console entry point. The primary runtime is unambiguous once `QGRIM_ENGINE.py` is identified; `main.py` and the generic workspace metadata are not reliable QGRIM entry points.

The safe immediate release posture is to distribute the primary engine, tests, README, provenance map, license, and explicitly selected supporting files while excluding ignored caches. Packaging cleanup and formal distribution metadata should remain separate 13G work.

> No cleanup action is justified solely by appearance. 13F has classified the artifacts and preserved them; 13G may act only after an explicit packaging decision.

## Supporting evidence

- `/home/ubuntu/qgrim_13f_packaging_inventory.txt` — tracked files, ignored artifacts, sizes, and tree.
- `/home/ubuntu/qgrim_13f_packaging_entrypoints.txt` — direct CLI, import, metadata, and auxiliary-entry behavior.
- `/home/ubuntu/qgrim_13f_quality_notes.txt` — static quality and generated-artifact observations.
- `/home/ubuntu/qgrim_13f_documentation_notes.txt` — README/source layout comparison.
- `/home/ubuntu/qgrim_13f_provenance_audit.txt` — commit/branch provenance.
