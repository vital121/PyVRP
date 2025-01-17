from typing import List

import numpy as np
from numpy.testing import assert_, assert_allclose, assert_equal
from pytest import mark

from pyvrp import RandomNumberGenerator


def test_bounds():
    """
    Tests that the minimum and maximum integer value the RNG can produce
    corresponds to the underlying type's maximum range.
    """
    assert_equal(RandomNumberGenerator.min(), 0)
    assert_equal(RandomNumberGenerator.max(), np.iinfo(np.uint32).max)


def test_call():
    """
    Calling the RNG as a function returns random integers, in a fixed sequence
    depending on the seed.
    """
    rng = RandomNumberGenerator(seed=42)

    assert_equal(rng(), 2386648076)
    assert_equal(rng(), 1236469084)

    rng = RandomNumberGenerator(seed=43)

    assert_equal(rng(), 2386648077)
    assert_equal(rng(), 1236469085)


def test_randint():
    """
    The ``randint(high)`` function returns a random integer between
    ``[0, high]``. Internally, this relies on ``__call__`` (see previous test).
    """
    rng = RandomNumberGenerator(seed=42)

    assert_equal(rng.randint(100), 2386648076 % 100)
    assert_equal(rng.randint(100), 1236469084 % 100)


@mark.parametrize("seed", [2, 10, 42])
def test_rand(seed: int):
    """
    Tests that repeatedly calling ``rand()`` should result in a sample that is
    approximately uniformly distributed.
    """
    rng = RandomNumberGenerator(seed)
    sample = np.array([rng.rand() for _ in range(10_000)])

    # The sample should be almost uniform, so mean 1/ 2 and variance 1 / 12,
    # and every realisation needs to be in [0, 1].
    assert_allclose(sample.mean(), 1 / 2, atol=1e-3)
    assert_allclose(sample.var(), 1 / 12, atol=1e-3)
    assert_(0 <= sample.min() < sample.max() <= 1)


@mark.parametrize("state", [[1, 2, 3, 4], [10, 14, 274, 83]])
def test_rng_has_given_state(state: List[int]):
    """
    Tests that setting the RNG with a given state, and then requesting that
    state, returns the same state.
    """
    rng = RandomNumberGenerator(state=state)
    assert_equal(rng.state(), state)
