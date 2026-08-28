# QGRIM Reconstruction Map — Read-Only Baseline

## Baseline

The repository is currently at commit `a504f6c4769d004a651b58c12666a74c68da4bf1`, abbreviated `a504f6c`, with subject `Create QGRIM_Engine _V2.2 ( Future )`. It is the root commit authored by `VAG-gomi <polerbear939@gmail.com>` on 2026-07-25 15:58:40 UTC. The local recovery branch `qgrim-recovery` points to this exact commit. The historical `main` branch remains at the same commit. No branch was pushed.

## Repository map

```text
QGRIM
├── CORE
│   └── QGRIM_ENGINE.py
├── TESTS
│   ├── test_bell.py
│   ├── test_ccx.py
│   ├── test_cnot.py
│   ├── test_cz.py
│   ├── test_entropy.py
│   ├── test_ghz.py
│   ├── test_grover.py
│   ├── test_measure.py
│   ├── test_noise.py
│   ├── test_sample.py
│   ├── test_swap.py
│   └── test_y_py
├── DOCUMENTATION
│   └── README.md
├── REPLIT / SCAFFOLD RESIDUE
│   ├── main.py
│   ├── replit_readme.md
│   ├── .npmrc
│   └── uv.lock
└── INVALID / UNCERTAIN
    ├── raw non-Python text embedded in QGRIM_ENGINE.py
    ├── raw display/banner content stored as screen_shot.py
    ├── pyproject_toml. (misnamed project metadata)
    └── QGRIM_Engine _V2.2 ( Future )  (placeholder artifact)
```

## Current read-only findings

`QGRIM_ENGINE.py` is the intended core simulator, but the committed file contains bare separator and attribution lines outside Python syntax. The first parse barrier occurs at line 1, so the exact committed file cannot be imported until those lines are resolved. I have not resolved them.

The test suite expects a missing `conftest.py` containing helpers such as `fresh`, `run`, `assert_norm`, `assert_amp`, `assert_prob`, and `Q412_TOL`. The helper must be reconstructed from test semantics rather than invented merely to make assertions pass. I have not created it.

The test named `test_y_py` has no `.py` extension. `test_sample.py` expects `sample_circuit(..., progress=False)`, while the engine signature does not accept `progress`. Bounds tests expect invalid qubit indices to raise `AsmError`, while the current assembler accepts wider encoded fields. These are recorded failures, not repaired.

`main.py` is a placeholder that prints a Replit workspace greeting. `pyproject_toml.` is not named `pyproject.toml`. `replit_readme.md`, `.npmrc`, and `uv.lock` are scaffold residue or inconsistent metadata relative to the standalone Python engine. They have not been deleted or changed.

## Safety and status

The repository is on the local `qgrim-recovery` branch at the original baseline. The working tree is clean. No tracked file was edited, deleted, renamed, reformatted, committed, or pushed. The next safe phase is to reconstruct the intended `conftest.py` semantics and establish a clean baseline execution path before changing algorithm behavior.
