"""Shared test helpers reconstructed from the surviving QGRIM tests and engine.

This file is recovery infrastructure, not a claim that it is the historical
conftest.py.  The repository does not preserve the original helper source, so
only semantics forced by the tests and engine are implemented here.

Reconstruction choices that cannot be recovered historically:
- Q412_TOL is set to four Q4.12 least-significant steps.  The engine's grid
  step is 1/4096; the original multiple is not present in the repository.
- STAT_TOL is set to 0.05 for finite-shot frequency checks.  Its original
  literal is also not recoverable, but the tests use it only for sampling.
- fresh() uses QGRIMSim() and therefore the engine's constructor default seed.
  The tests do not establish a different historical seed.
"""

from __future__ import annotations

from typing import Union

from QGRIM_ENGINE import QGRIMSim, assemble

# Q4.12 grid step: ONE_Q12 = 1 << 12 = 4096 in QGRIM_ENGINE.py.
# Four steps is an explicit recovery choice, not a recovered historical value.
Q412_TOL = 4 / 4096

# Sampling-only tolerance; no original literal survives in the repository.
STAT_TOL = 0.05


def fresh() -> QGRIMSim:
    """Return a new simulator in the engine constructor's initial state."""
    return QGRIMSim()


def run(source: str) -> QGRIMSim:
    """Assemble QASM source, execute it on a fresh simulator, and return it."""
    sim = fresh()
    sim.run(assemble(source))
    return sim


def assert_norm(sim: QGRIMSim) -> None:
    """Assert that the state-vector probability norm is approximately one."""
    norm = sum(abs(amplitude) ** 2 for amplitude in sim.state)
    assert abs(norm - 1.0) < Q412_TOL, f"state norm {norm!r} is not approximately 1"


def assert_amp(
    sim: QGRIMSim,
    index: int,
    expected: Union[complex, float, int],
) -> None:
    """Assert a full complex amplitude at a basis-state index."""
    actual = sim.state[index]
    assert abs(actual - expected) < Q412_TOL, (
        f"state[{index}]={actual!r}, expected {expected!r}"
    )


def assert_prob(sim: QGRIMSim, index: int, expected: float) -> None:
    """Assert the Born probability derived from one complex amplitude."""
    actual = abs(sim.state[index]) ** 2
    assert abs(actual - expected) < Q412_TOL, (
        f"probability[{index}]={actual!r}, expected {expected!r}"
    )
