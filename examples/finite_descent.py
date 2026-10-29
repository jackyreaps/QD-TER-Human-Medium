"""Print the checked mathematics behind v10.0 Sections 2 and 7.

Usage (from the repository root)::

    python -m examples.finite_descent
"""

import numpy as np

from qdter.descent import (
    GatedFold,
    all_syndromes,
    compose,
    correct,
    fano_lines,
    hamming_codewords,
    random_fold,
    surviving_bits,
    syndrome,
    weight3_supports,
)


def _flip(word, j):
    w = word.copy()
    w[j] ^= 1
    return w


def main() -> None:
    rng = np.random.default_rng(0)
    chain = compose(random_fold(12, 6, rng), random_fold(6, 3, rng))
    print("Fold chain F2^12 -> F2^6 -> F2^3")
    print(f"  bits surviving a uniform input : {surviving_bits(chain)} (bound: 3)")
    print()
    print("Rank-3 candidate: syndrome space of the [7,4] Hamming code")
    print(f"  syndromes over all words       : {sorted(all_syndromes())}")
    print(f"  Fano lines                     : {len(fano_lines())}")
    print(f"  weight-3 codewords == lines    : {weight3_supports() == fano_lines()}")
    ok = all(
        np.array_equal(correct(_flip(cw, j)), cw)
        for cw in hamming_codewords()
        for j in range(7)
    )
    print(f"  all single-bit errors corrected: {ok}")
    word = _flip(hamming_codewords()[5], 3)
    print(f"  example: error at position 4 gives syndrome {syndrome(word)}")
    print()
    gate = GatedFold([random_fold(6, 3, rng) for _ in range(4)])
    print("Gated fold on F2^6 -> F2^3")
    print(f"  symbols: {gate.alphabet_size}; gate capacity: {gate.gate_capacity_bits:.1f} bits per use")
    print()
    print("These are mathematical facts, not evidence about biology.")


if __name__ == "__main__":
    main()
