"""Tests for qdter.descent: the mathematics behind v10.0 Sections 2 and 7."""
import itertools

import numpy as np
import pytest

from qdter.descent import (
    GatedFold,
    all_syndromes,
    apply_fold,
    compose,
    correct,
    descent_bound_bits,
    fano_lines,
    fano_points,
    hamming_codewords,
    hamming_parity_check,
    image_size,
    random_fold,
    rank_f2,
    surviving_bits,
    syndrome,
    weight3_supports,
)


def test_rank_f2_basic():
    assert rank_f2(np.eye(3, dtype=np.uint8)) == 3
    assert rank_f2(np.array([[1, 1], [1, 1]], dtype=np.uint8)) == 1
    assert rank_f2(np.zeros((2, 4), dtype=np.uint8)) == 0


def test_random_fold_is_surjective():
    rng = np.random.default_rng(0)
    for _ in range(5):
        f = random_fold(12, 6, rng)
        assert f.shape == (6, 12)
        assert image_size(f) == 2 ** 6


def test_chain_12_6_3_transmits_at_most_three_bits():
    rng = np.random.default_rng(1)
    f126 = random_fold(12, 6, rng)
    f63 = random_fold(6, 3, rng)
    chain = compose(f126, f63)
    assert chain.shape == (3, 12)
    assert surviving_bits(chain) <= 3
    assert surviving_bits(chain) == 3  # full rank for a generic chain
    assert descent_bound_bits([2 ** 12, 2 ** 6, 2 ** 3]) == pytest.approx(3.0)


def test_surviving_bits_never_exceeds_bound_even_when_rank_drops():
    # a composite of surjections can only lose information
    a = np.array([[1, 0, 0, 0], [0, 1, 0, 0]], dtype=np.uint8)
    b = np.array([[1, 1]], dtype=np.uint8)
    chain = compose(a, b)
    assert surviving_bits(chain) <= descent_bound_bits([16, 4, 2])


def test_the_composite_output_set_has_eight_elements_under_rank_reading():
    rng = np.random.default_rng(2)
    chain = compose(random_fold(12, 6, rng), random_fold(6, 3, rng))
    outputs = {
        tuple(apply_fold(chain, np.array(bits, dtype=np.uint8)))
        for bits in itertools.product((0, 1), repeat=12)
    }
    assert len(outputs) == 8


def test_fano_plane_has_seven_points_and_seven_lines():
    assert len(fano_points()) == 7
    lines = fano_lines()
    assert len(lines) == 7
    assert all(len(line) == 3 for line in lines)
    # every pair of distinct points lies on exactly one line
    for a, b in itertools.combinations(range(1, 8), 2):
        assert sum(1 for line in lines if a in line and b in line) == 1


def test_p3_over_f2_has_fifteen_points_not_seven():
    # the memo correction: P^3(F_2) is not the Fano plane
    assert 2 ** 4 - 1 == 15
    assert 2 ** 3 - 1 == 7


def test_parity_check_columns_are_the_seven_nonzero_vectors():
    h = hamming_parity_check()
    assert h.shape == (3, 7)
    cols = {tuple(h[:, j]) for j in range(7)}
    assert len(cols) == 7
    assert (0, 0, 0) not in cols


def test_syndrome_space_has_eight_elements():
    assert all_syndromes() == set(range(8))


def test_hamming_code_has_sixteen_codewords():
    assert len(hamming_codewords()) == 16


def test_weight3_codewords_are_exactly_the_fano_lines():
    assert weight3_supports() == fano_lines()


def test_single_bit_error_syndrome_names_the_position():
    word = np.zeros(7, dtype=np.uint8)
    for j in range(7):
        w = word.copy()
        w[j] ^= 1
        assert syndrome(w) == j + 1


def test_syndrome_decoding_corrects_every_single_bit_error():
    for cw in hamming_codewords():
        assert syndrome(cw) == 0
        for j in range(7):
            bad = cw.copy()
            bad[j] ^= 1
            assert np.array_equal(correct(bad), cw)
        assert np.array_equal(correct(cw), cw)  # "none" leaves the word alone


def test_gated_fold_capacity_and_surjectivity():
    rng = np.random.default_rng(3)
    gate = GatedFold([random_fold(6, 3, rng) for _ in range(4)])
    assert gate.alphabet_size == 4
    assert gate.gate_capacity_bits == pytest.approx(2.0)
    x = np.array([1, 0, 1, 1, 0, 0], dtype=np.uint8)
    outs = {tuple(gate.apply(s, x)) for s in range(4)}
    assert len(outs) <= 4
    assert all(len(o) == 3 for o in outs)


def test_gated_fold_rejects_non_surjective_member():
    bad = np.zeros((3, 6), dtype=np.uint8)
    with pytest.raises(ValueError):
        GatedFold([bad])
