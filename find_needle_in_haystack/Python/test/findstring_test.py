import pytest
import random
import sys

from findstring import FindString

"""
Tests all three solutions exhaustively over a range of short even and odd
sized target and query sequences.

Tests the full scale problem with binary_find and margin_find using randomly
generated target/query pairs.

  pytest --setup-plan

Examples:

  pytest -v
  pytest -s
  pytest -v src/test_findstring.py::test_naive_find_in_even_length_target
  pytest -v 'src/test_findstring.py::test_naive_find_in_even_length_target[8-4]'
  pytest -v -m 'not random'
  pytest -v -m random
"""


def build_strings(tsize, qsize, qstart, marker='x'):
    """Generate and return a pair of test strings for target and query using
    the supplied lengths and query start position inside target.
    """
    if tsize < 1:
        print("ERROR: target size less than 1", file=sys.stderr)
        return [], []
    if qsize < 1:
        print("ERROR: query size less than 1", file=sys.stderr)
        return [], []
    if qstart + qsize > tsize:
        print("ERROR: query overshoots target", file=sys.stderr)
        return [], []
    if qstart < 0:
        print("ERROR: query start is negative", file=sys.stderr)
        return [], []
    target, query = ['-'] * tsize, [marker] * qsize
    for i in range(qstart, qstart + qsize):
        target[i] = marker
    return target, query


def is_query(target, query, start, stop):
    """Return true if the target range (start stop) inclusive equals the
    query."""
    return target[start:stop + 1] == query


def run_one_find(find_method, tlen, qlen, start, trace=True, metrics=True):
    if trace or metrics:
        print()
    stop = start + qlen - 1
    target, query = build_strings(tlen, qlen, start)
    finder = FindString(target, query, trace=trace, metrics=metrics)
    assert find_method(finder) == (start, stop)
    assert is_query(target, query, start, stop)

# the tests


# lists of pairs (target_length, query_length) for build_strings()
EVEN_TESTS = [(8, 8), (8, 7), (8, 6), (8, 5), (8, 4), (8, 3), (8, 2), (8, 1)]
ODD_TESTS = [(7, 7), (7, 6), (7, 5), (7, 4), (7, 3), (7, 2), (7, 1)]


# naive_find

@pytest.mark.parametrize(['tlen', 'qlen'], EVEN_TESTS)
def test_naive_find_in_even_length_target(tlen, qlen):
    print("\n\nnaive_find, uses linear scan")
    for start in range(tlen - qlen + 1):
        run_one_find(FindString.naive_find, tlen, qlen, start)


@pytest.mark.parametrize(['tlen', 'qlen'], ODD_TESTS)
def test_naive_find_in_odd_length_target(tlen, qlen):
    print("\n\nnaive_find, uses linear scan")
    for start in range(tlen - qlen + 1):
        run_one_find(FindString.naive_find, tlen, qlen, start)


# binary_find

@pytest.mark.parametrize(['tlen', 'qlen'], EVEN_TESTS)
def test_binary_find_in_even_length_target(tlen, qlen):
    print("\n\nbinary_find, binary search with opportunistic margin_find")
    for start in range(tlen - qlen + 1):
        run_one_find(FindString.binary_find, tlen, qlen, start)


@pytest.mark.parametrize(['tlen', 'qlen'], ODD_TESTS)
def test_binary_find_in_odd_length_target(tlen, qlen):
    print("\n\nbinary_find, binary search with opportunistic margin_find")
    for start in range(tlen - qlen + 1):
        run_one_find(FindString.binary_find, tlen, qlen, start)


# binary_find, random massive target/query

@pytest.mark.random
def test_massive_random_binary_find():
    print("\n\nmassive random binary_find")
    tlen, qlen = 2**20, 2**13
    for _ in range(10):
        start = random.randint(0, tlen - qlen)
        run_one_find(FindString.binary_find, tlen,
                     qlen, start, trace=False, metrics=True)


# margin_find

@pytest.mark.parametrize(['tlen', 'qlen'], EVEN_TESTS)
def test_margin_find_in_even_length_target(tlen, qlen):
    print("\n\nmargin_find, eats margins")
    for start in range(tlen - qlen + 1):
        run_one_find(FindString.margin_find, tlen, qlen, start)


@pytest.mark.parametrize(['tlen', 'qlen'], ODD_TESTS)
def test_margin_find_in_odd_length_target(tlen, qlen):
    print("\n\nmargin_find, eats margins")
    for start in range(tlen - qlen + 1):
        run_one_find(FindString.margin_find, tlen, qlen, start)


# margin_find, random massive target/query

@pytest.mark.random
def test_massive_random_margin_find():
    print("\n\nmassive random margin_find")
    tlen, qlen = 2**20, 2**13
    for _ in range(10):
        start = random.randint(0, tlen - qlen)
        run_one_find(FindString.margin_find, tlen,
                     qlen, start, trace=False, metrics=True)
