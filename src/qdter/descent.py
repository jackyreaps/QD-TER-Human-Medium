"""Finite descent: executable checks for the mathematics of v10.0.

This module checks the *mathematical* statements of v10.0 Sections 2 and 7.
It does not model physics and makes no claim that the Rank-3 base is any of
the objects below; Fano, Hamming, and the gated fold are candidates (see
theory/finite_topological_descent.md). What is checked here is that the
combinatorial facts the narrative relies on are true:

1. A chain of surjective folds can transmit at most log2 |S_out| bits
   (v10.0 Section 2.3).
2. Under the candidate reading rank = F_2-dimension, S_3 = F_2^3 has eight
   elements (v10.0 Section 2.4).
3. Those eight elements are the syndrome space of the [7,4] Hamming code:
   seven nonzero points of the Fano plane P^2(F_2) plus zero.
4. The weight-3 codewords of that code are exactly the seven Fano lines.
5. Syndrome decoding corrects any single-bit error (the analogy used for
   symbolic gating in v10.0 Section 7.2).

All vectors are over F_2 and are represented as numpy integer arrays.
"""

from __future__ import annotations

import itertools
import math
from typing import FrozenSet, List, Optional, Sequence, Set, Tuple

import numpy as np

#: Number of positions in the Hamming code, and of Fano points.
N_POINTS: int = 7


def rank_f2(matrix: np.ndarray) -> int:
    """Rank of a binary matrix over F_2 (Gaussian elimination)."""
    m = (np.asarray(matrix, dtype=np.uint8) % 2).copy()
    rows, cols = m.shape
    rank = 0
    for col in range(cols):
        pivot = next((r for r in range(rank, rows) if m[r, col]), None)
        if pivot is None:
            continue
        m[[rank, pivot]] = m[[pivot, rank]]
        for r in range(rows):
            if r != rank and m[r, col]:
                m[r] ^= m[rank]
        rank += 1
        if rank == rows:
            break
    return rank


def random_fold(
    n_in: int, n_out: int, rng: Optional[np.random.Generator] = None
) -> np.ndarray:
    """A random surjective linear fold F_2^n_in -> F_2^n_out.

    Draws binary matrices until one has full row rank, so that the map is
    onto. Requires n_out <= n_in.
    """
    if n_out > n_in:
        raise ValueError("A surjective fold needs n_out <= n_in.")
    rng = rng or np.random.default_rng()
    while True:
        a = rng.integers(0, 2, size=(n_out, n_in), dtype=np.uint8)
        if rank_f2(a) == n_out:
            return a


def apply_fold(fold: np.ndarray, x: np.ndarray) -> np.ndarray:
    """Apply a linear fold over F_2."""
    return (np.asarray(fold, dtype=np.uint8) @ np.asarray(x, dtype=np.uint8)) % 2


def compose(first: np.ndarray, second: np.ndarray) -> np.ndarray:
    """Composite fold: apply `first`, then `second`."""
    return (np.asarray(second, dtype=np.uint8) @ np.asarray(first, dtype=np.uint8)) % 2


def image_size(fold: np.ndarray) -> int:
    """Number of distinct outputs of a linear fold over F_2: 2^rank."""
    return 2 ** rank_f2(fold)


def surviving_bits(fold: np.ndarray) -> int:
    """Bits that survive the fold when the input is uniform.

    For a linear map on a uniform input the output is uniform on the image,
    so the output entropy, and hence I(input; output), equals the rank.
    It never exceeds log2 of the output set size.
    """
    return rank_f2(fold)


def descent_bound_bits(sizes: Sequence[int]) -> float:
    """Upper bound log2 |S_out| on the information a fold chain can transmit."""
    return math.log2(sizes[-1])


# ----------------------------------------------------------------------
# The seven points, the Fano plane, and the [7,4] Hamming code
# ----------------------------------------------------------------------


def fano_points() -> List[Tuple[int, int, int]]:
    """The seven nonzero vectors of F_2^3, i.e. the points of P^2(F_2)."""
    return [
        tuple(int(b) for b in format(k, "03b"))  # type: ignore[misc]
        for k in range(1, 8)
    ]


def fano_lines() -> Set[FrozenSet[int]]:
    """The seven lines of the Fano plane, as sets of point labels 1..7.

    Points are labelled by the integer value of the binary vector. Three
    distinct points are collinear exactly when their XOR is zero.
    """
    lines = set()
    for a, b in itertools.combinations(range(1, 8), 2):
        c = a ^ b
        lines.add(frozenset((a, b, c)))
    return lines


def hamming_parity_check() -> np.ndarray:
    """Parity-check matrix H (3 x 7) of the [7,4] Hamming code.

    Column j (1-based) is the binary representation of j, so the columns
    are the seven nonzero vectors of F_2^3.
    """
    cols = [[(j >> bit) & 1 for bit in (2, 1, 0)] for j in range(1, 8)]
    return np.array(cols, dtype=np.uint8).T


def syndrome(word: np.ndarray, h: Optional[np.ndarray] = None) -> int:
    """Syndrome of a 7-bit word as an integer in 0..7."""
    h = hamming_parity_check() if h is None else h
    s = apply_fold(h, np.asarray(word, dtype=np.uint8))
    return int(s[0]) * 4 + int(s[1]) * 2 + int(s[2])


def hamming_codewords() -> List[np.ndarray]:
    """All 16 codewords (words with zero syndrome)."""
    return [
        np.array(bits, dtype=np.uint8)
        for bits in itertools.product((0, 1), repeat=N_POINTS)
        if syndrome(np.array(bits, dtype=np.uint8)) == 0
    ]


def weight3_supports() -> Set[FrozenSet[int]]:
    """Supports (as 1-based positions) of the weight-3 codewords."""
    return {
        frozenset(int(i) + 1 for i in np.flatnonzero(w))
        for w in hamming_codewords()
        if int(w.sum()) == 3
    }


def all_syndromes() -> Set[int]:
    """The set of syndromes over all 128 seven-bit words."""
    return {
        syndrome(np.array(bits, dtype=np.uint8))
        for bits in itertools.product((0, 1), repeat=N_POINTS)
    }


def correct(word: np.ndarray) -> np.ndarray:
    """Syndrome decoding: flip the bit the syndrome points to, if any.

    A syndrome of 0 means no error. A nonzero syndrome j names position j
    (1-based). This is the "symbol selects which of seven channels to
    write, with 'none' as the eighth outcome" analogy of v10.0 Section 7.2.
    """
    w = np.asarray(word, dtype=np.uint8).copy()
    s = syndrome(w)
    if s:
        w[s - 1] ^= 1
    return w


# ----------------------------------------------------------------------
# Gated fold (v10.0 Section 7.1)
# ----------------------------------------------------------------------


class GatedFold:
    """A family of surjective folds F_2^n_in -> F_2^n_out indexed by a symbol.

    Args:
        folds: One fold matrix per symbol. All must be surjective and share
            the same shape.
    """

    def __init__(self, folds: Sequence[np.ndarray]):
        if not folds:
            raise ValueError("A gated fold needs at least one symbol.")
        shape = np.asarray(folds[0]).shape
        for f in folds:
            f = np.asarray(f)
            if f.shape != shape:
                raise ValueError("All folds must share one shape.")
            if rank_f2(f) != shape[0]:
                raise ValueError("Every fold must be surjective.")
        self.folds = [np.asarray(f, dtype=np.uint8) for f in folds]

    @property
    def alphabet_size(self) -> int:
        return len(self.folds)

    @property
    def gate_capacity_bits(self) -> float:
        """The symbol conveys at most log2 |alphabet| bits per use."""
        return math.log2(self.alphabet_size)

    def apply(self, symbol: int, x: np.ndarray) -> np.ndarray:
        return apply_fold(self.folds[symbol], x)
