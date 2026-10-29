"""Tests for the Prisoner's Dilemma tournament example (v7.0 spec)."""
import math

import numpy as np

from examples.pd_tournament import (
    PairConfig,
    Strategy,
    experiment_a,
    make_engine,
    recovery_time_estimate,
    select_strategy,
    simulate_pair,
    social_return_rate,
)
from qdter.manifold.rheology import StrategicTopology


def _result(re_eps, phase_locked=True):
    return {"dielectric_reynolds_number": re_eps, "phase_locked": phase_locked}


def test_social_return_rate_matches_spec_formula():
    assert math.isclose(social_return_rate(0.2, 0.5, 1.0), 0.2 * 0.5)
    assert social_return_rate(0.2, 0.2, 0.0) == 0.0


def test_recovery_time_diverges_as_re_goes_to_zero():
    times = [recovery_time_estimate(social_return_rate(0.2, 0.2, re)) for re in (10.0, 1.0, 0.1, 0.01)]
    assert times == sorted(times)
    assert math.isinf(recovery_time_estimate(0.0))


def test_strategy_follows_v7_regime_table():
    ridge = StrategicTopology.RIDGE
    assert select_strategy(_result(0.5), ridge) is Strategy.RIGID_DEFECT
    assert select_strategy(_result(5.0), ridge) is Strategy.TIT_FOR_TAT
    assert select_strategy(_result(15.0), ridge) is Strategy.UNCONDITIONAL_COOPERATE
    assert select_strategy(_result(15.0, phase_locked=False), ridge) is Strategy.TIT_FOR_TAT
    assert select_strategy(_result(15.0), StrategicTopology.ABYSS) is Strategy.FRAGMENTED


def test_simulation_is_deterministic_for_a_seed():
    cfg = PairConfig(nr3c1_a=0.5, nr3c1_b=0.52, oxtr=0.3, rounds=30)
    a = simulate_pair(cfg, make_engine(), np.random.default_rng(1))
    b = simulate_pair(cfg, make_engine(), np.random.default_rng(1))
    assert a == b


def test_cooperation_rises_with_oxytocin_and_nr3c1_match():
    rows = experiment_a(n_pairs=30, rounds=30, rng=np.random.default_rng(3))
    matched = [r["matched_cc"] for r in rows]
    assert matched[0] < matched[2] < matched[-1]
    for r in rows[1:-1]:
        assert r["matched_cc"] >= r["mismatched_cc"]


def test_low_re_pairs_recover_trust_more_slowly():
    def recovery(nr3c1_b):
        cfg = PairConfig(nr3c1_a=0.0, nr3c1_b=nr3c1_b, oxtr=0.2, rounds=300, shock_round=5, noise=0.0)
        return simulate_pair(cfg, make_engine(), np.random.default_rng(0))["recovery_rounds"]

    assert recovery(0.0) < recovery(0.4) < recovery(0.95)
