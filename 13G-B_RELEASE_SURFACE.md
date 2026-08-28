# 13G-B — Direct-Execution Release Surface

Commit `321598b` synchronized the documented release surface without changing runtime behavior. The release model is direct execution from a source checkout.

## Primary surface

```text
QGRIM_ENGINE.py
README.md
PROVENANCE.md
LICENSE
RELEASE_SURFACE.md
conftest.py
test_*.py
test_y_py
```

`test_y_py` is an extensionless test file. Ordinary pytest discovery does not necessarily collect it; its coverage must be executed separately and documented as such.

## Outside the primary surface

`main.py`, `screen_shot.py`, `QGRIM_Engine _V2.2 ( Future )`, `replit_readme.md`, `pyproject_toml.`, `uv.lock`, and `.npmrc` remain retained workspace or archival surfaces pending a separate cleanup decision.

## Verification

The synchronized artifact passed direct `--help`, `--list`, `--isa`, and representative direct execution checks. The official suite remained 150 passed and one unresolved sampler failure.
