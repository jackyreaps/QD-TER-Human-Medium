"""Iterated Prisoner's Dilemma tournament on QD-TER organism profiles (v7.0 spec).

This example turns the strategic-interaction passages of Part II (v7.0, sections
3 and 4.6) into a runnable simulation. It is an illustration of the model, not
an empirical result: every parameter below is a choice made for the example.

What it implements
------------------
1. Pair-level dielectric Reynolds number Re_eps, computed by
   ``process_interaction_node`` from NR3C1 alignment, bioelectric alignment,
   gap-junction density, and the external oxytocin stimulus.
2. A strategy-selection layer that applies the v7.0 Re_eps regime table
   literally:

       Re_eps < 1         rigid commitment        -> always defect
       1 <= Re_eps < 10   partial belief updating -> tit-for-tat
       Re_eps >= 10       cross-brain phase-lock  -> unconditional cooperation

   Unconditional cooperation additionally requires the scalar phase-lock
   criterion from ``process_interaction_node``; otherwise the pair plays
   tit-for-tat. A player whose coherence credit has fallen into the Abyss
   (credit < 0.3) plays a fragmented 50/50 mix.
3. The social return rate from v7.0 section 4.6,

       r_social = min(r_self, r_partner) * Re_eps / (1 + Re_eps),

   which governs how fast coherence credit is restored after a defection
   shock. Recovery time therefore diverges as Re_eps -> 0.

Experiments
-----------
Both experiments use a small execution-error rate (A) so that tit-for-tat pairs and
phase-locked pairs behave differently; B turns it off.

A. Cooperation vs. oxytocin stimulus for NR3C1-matched and mismatched pairs
   (the qualitative shape behind falsification Protocol 66).
B. Trust repair after a mutual-defection shock, as a function of Re_eps
   (varied through NR3C1 mismatch at fixed oxytocin).

Usage (from the repository root)::

    python -m examples.pd_tournament
    python -m examples.pd_tournament --pairs 500 --rounds 80 --seed 7
    python -m examples.pd_tournament --oxtr 0.001   # watch recovery time grow
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional

import numpy as np

from qdter.manifold.rheology import (
    AetherSubstrateConstants,
    BioelectricState,
    ChiralManifoldRheology,
    OrganismProfile,
    StrategicTopology,
    process_interaction_node,
)

COOPERATE, DEFECT = "C", "D"

# Standard PD payoffs: temptation > reward > punishment > sucker.
PAYOFF = {
    (COOPERATE, COOPERATE): (3, 3),
    (COOPERATE, DEFECT): (0, 5),
    (DEFECT, COOPERATE): (5, 0),
    (DEFECT, DEFECT): (1, 1),
}

RE_RIGID_MAX = 1.0       # v7.0 table: Re_eps < 1 is the rigid regime
RE_PHASE_LOCK_MIN = 10.0  # v7.0 table: Re_eps > 10 is the phase-locked regime
RIDGE_CREDIT = 0.7       # coherence credit needed to count as recovered


class Strategy(Enum):
    RIGID_DEFECT = "rigid defect"
    TIT_FOR_TAT = "tit-for-tat"
    UNCONDITIONAL_COOPERATE = "unconditional cooperate"
    FRAGMENTED = "fragmented (Abyss)"


def select_strategy(result: Dict, topology: StrategicTopology) -> Strategy:
    """Map one interaction-node result to a strategy (v7.0 Re_eps table)."""
    if topology is StrategicTopology.ABYSS:
        return Strategy.FRAGMENTED
    re_eps = result["dielectric_reynolds_number"]
    if re_eps < RE_RIGID_MAX:
        return Strategy.RIGID_DEFECT
    if re_eps >= RE_PHASE_LOCK_MIN and result["phase_locked"]:
        return Strategy.UNCONDITIONAL_COOPERATE
    return Strategy.TIT_FOR_TAT


def choose_action(strategy: Strategy, opponent_last: Optional[str], rng: np.random.Generator) -> str:
    if strategy is Strategy.RIGID_DEFECT:
        return DEFECT
    if strategy is Strategy.UNCONDITIONAL_COOPERATE:
        return COOPERATE
    if strategy is Strategy.FRAGMENTED:
        return COOPERATE if rng.random() < 0.5 else DEFECT
    return DEFECT if opponent_last == DEFECT else COOPERATE  # tit-for-tat


def _execute(action: str, noise: float, rng: np.random.Generator) -> str:
    """Apply execution error: with probability ``noise`` the other action is played."""
    if rng.random() < noise:
        return DEFECT if action == COOPERATE else COOPERATE
    return action


def social_return_rate(r_self: float, r_partner: float, re_eps: float) -> float:
    """r_social = min(r_self, r_partner) * Re / (1 + Re)  (v7.0 section 4.6)."""
    return min(r_self, r_partner) * re_eps / (1.0 + re_eps)


def recovery_time_estimate(r_social: float, start: float = 0.1, target: float = RIDGE_CREDIT) -> float:
    """Rounds for credit to climb from ``start`` to ``target`` under
    credit <- credit + r_social * (1 - credit). Infinite when r_social is 0."""
    if r_social <= 0.0:
        return math.inf
    return math.log((1.0 - target) / (1.0 - start)) / math.log(1.0 - r_social)


@dataclass(frozen=True)
class PairConfig:
    nr3c1_a: float
    nr3c1_b: float
    oxtr: float
    gap_junction: float = 0.5
    potential_a_mv: float = 0.0
    potential_b_mv: float = 0.0
    rounds: int = 50
    r_self: float = 0.2
    shock_round: Optional[int] = None  # mutual-defection shock at this round
    shock_credit: float = 0.1
    noise: float = 0.03  # probability an intended action is flipped (execution error)


def make_engine() -> ChiralManifoldRheology:
    # 0.5 m is the face-to-face node dimension used in v7.0 section 3.
    return ChiralManifoldRheology(
        substrate=AetherSubstrateConstants(), characteristic_node_dimension=0.5
    )


def simulate_pair(cfg: PairConfig, engine: ChiralManifoldRheology, rng: np.random.Generator) -> Dict:
    credit_a = credit_b = 1.0
    bio_a = BioelectricState(cfg.potential_a_mv, cfg.gap_junction)
    bio_b = BioelectricState(cfg.potential_b_mv, cfg.gap_junction)
    last_a = last_b = None
    cc = 0
    payoff_total = 0.0
    re_eps = 0.0
    recovery_round: Optional[int] = None

    for t in range(cfg.rounds):
        if cfg.shock_round is not None and t == cfg.shock_round:
            credit_a = credit_b = cfg.shock_credit  # debt-field perturbation
            last_a = last_b = DEFECT

        pa = OrganismProfile(cfg.nr3c1_a, credit_a, bio_a)
        pb = OrganismProfile(cfg.nr3c1_b, credit_b, bio_b)
        res_ab = process_interaction_node(pa, pb, cfg.oxtr, engine)
        res_ba = process_interaction_node(pb, pa, cfg.oxtr, engine)
        re_eps = res_ab["dielectric_reynolds_number"]

        s_a = select_strategy(res_ab, res_ab["topology_status"])
        s_b = select_strategy(res_ba, res_ba["topology_status"])
        act_a = _execute(choose_action(s_a, last_b, rng), cfg.noise, rng)
        act_b = _execute(choose_action(s_b, last_a, rng), cfg.noise, rng)

        gain_a, gain_b = PAYOFF[(act_a, act_b)]
        payoff_total += gain_a + gain_b
        cc += (act_a, act_b) == (COOPERATE, COOPERATE)
        last_a, last_b = act_a, act_b

        r_soc = social_return_rate(cfg.r_self, cfg.r_self, re_eps)
        credit_a += r_soc * (1.0 - credit_a)
        credit_b += r_soc * (1.0 - credit_b)

        if (
            cfg.shock_round is not None
            and t >= cfg.shock_round
            and recovery_round is None
            and min(credit_a, credit_b) >= RIDGE_CREDIT
        ):
            recovery_round = t - cfg.shock_round + 1

    return {
        "cc_rate": cc / cfg.rounds,
        "mean_payoff": payoff_total / (2 * cfg.rounds),
        "re_eps": re_eps,
        "recovery_rounds": recovery_round,
        "final_credit": min(credit_a, credit_b),
    }


def sample_pair_config(rng: np.random.Generator, matched: bool, oxtr: float, rounds: int, **kw) -> PairConfig:
    """Draw a pair. Matched pairs share an NR3C1 density; mismatched pairs differ by ~0.6."""
    base = rng.uniform(0.3, 0.7)
    if matched:
        a, b = base, float(np.clip(base + rng.normal(0, 0.02), 0, 1))
    else:
        a, b = base - 0.3, base + 0.3
    return PairConfig(
        nr3c1_a=float(a),
        nr3c1_b=float(b),
        oxtr=oxtr,
        potential_a_mv=float(rng.normal(0, 0.5)),
        potential_b_mv=float(rng.normal(0, 0.5)),
        rounds=rounds,
        **kw,
    )


def experiment_a(n_pairs: int, rounds: int, rng: np.random.Generator) -> List[Dict]:
    """Mutual-cooperation rate vs. oxytocin stimulus, matched vs. mismatched NR3C1."""
    engine = make_engine()
    rows = []
    for oxtr in (0.0, 0.01, 0.05, 0.2, 0.5, 1.0):
        row = {"oxtr": oxtr}
        for label, matched in (("matched", True), ("mismatched", False)):
            out = [simulate_pair(sample_pair_config(rng, matched, oxtr, rounds), engine, rng) for _ in range(n_pairs)]
            row[label + "_cc"] = float(np.mean([o["cc_rate"] for o in out]))
            row[label + "_re"] = float(np.median([o["re_eps"] for o in out]))
        rows.append(row)
    return rows


def experiment_b(rounds: int, rng: np.random.Generator, oxtr: float = 0.2) -> List[Dict]:
    """Rounds to recover coherence credit after a mutual-defection shock.

    Re_eps is varied through NR3C1 mismatch at fixed oxytocin stimulus. Execution
    noise is switched off so the observed recovery matches the closed-form estimate.
    """
    engine = make_engine()
    rows = []
    for delta in (0.0, 0.1, 0.2, 0.4, 0.7, 0.95):
        cfg = PairConfig(
            nr3c1_a=0.025 + 0.0, nr3c1_b=0.025 + delta, oxtr=oxtr, rounds=rounds,
            shock_round=5, noise=0.0,
        )
        out = simulate_pair(cfg, engine, rng)
        r_soc = social_return_rate(cfg.r_self, cfg.r_self, out["re_eps"])
        rows.append(
            {
                "delta": delta,
                "re_eps": out["re_eps"],
                "r_social": r_soc,
                "predicted": recovery_time_estimate(r_soc, cfg.shock_credit),
                "observed": out["recovery_rounds"],
            }
        )
    return rows


def _fmt(x, nd=2):
    if x is None:
        return "not within horizon"
    if isinstance(x, float) and math.isinf(x):
        return "inf"
    return f"{x:.{nd}f}" if isinstance(x, float) else str(x)


def main(argv: Optional[List[str]] = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--pairs", type=int, default=200, help="pairs per cell in experiment A")
    ap.add_argument("--rounds", type=int, default=50, help="rounds per pair")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--oxtr", type=float, default=0.2, help="oxytocin stimulus for experiment B")
    args = ap.parse_args(argv)
    rng = np.random.default_rng(args.seed)

    print("QD-TER Prisoner's Dilemma tournament (illustrative simulation of v7.0)")
    print(f"pairs/cell={args.pairs}  rounds={args.rounds}  seed={args.seed}\n")

    print("A. Mutual-cooperation rate vs. oxytocin stimulus")
    print(f"{'OXTR':>6} | {'matched C,C':>11} {'median Re':>10} | {'mismatched C,C':>14} {'median Re':>10}")
    for r in experiment_a(args.pairs, args.rounds, rng):
        print(
            f"{r['oxtr']:>6.2f} | {r['matched_cc']:>11.3f} {r['matched_re']:>10.2f} | "
            f"{r['mismatched_cc']:>14.3f} {r['mismatched_re']:>10.2f}"
        )

    horizon = max(args.rounds, 300)
    print(f"\nB. Trust repair after a mutual-defection shock (horizon {horizon} rounds)")
    print(f"{'NR3C1 gap':>9} {'Re_eps':>9} {'r_social':>9} {'predicted':>10} {'observed':>20}")
    for r in experiment_b(horizon, rng, args.oxtr):
        print(
            f"{r['delta']:>9.2f} {r['re_eps']:>9.2f} {r['r_social']:>9.4f} "
            f"{_fmt(r['predicted'], 1):>10} {_fmt(r['observed']):>20}"
        )
    print(
        "\nThese numbers illustrate the model's structure under the example's"
        "\nparameter choices. They are not empirical predictions of effect size."
    )


if __name__ == "__main__":
    main()
