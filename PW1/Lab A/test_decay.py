"""
Tests for the decay simulation.
"""
import numpy as np
import pytest
from decay import simulate, simulate_loop

def test_starts_at_N0():
    # at time zero, no atoms have decayed yet
    assert simulate(1000, 0.4)[0] == 1000

def test_rejects_negative_rate():
    # Check that calling simulate(...) with a negative lam raises a ValueError
    with pytest.raises(ValueError):
        simulate(1000, -0.1)

def test_matches_law():
    # Check that the simulation's AVERAGE over many seeds is close to the physical law
    n0 = 1000
    lam = 0.2
    dt = 0.05
    steps = 100
    t = steps * dt
    expected = n0 * np.exp(-lam * t)

    runs = [simulate(n0, lam, dt=dt, steps=steps, seed=s)[-1] for s in range(300)]
    avg_remaining = np.mean(runs)

    assert avg_remaining == pytest.approx(expected, rel=0.05)