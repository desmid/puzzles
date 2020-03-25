import pytest


def solve(n):
    # assume n is int with unlimited upper bound
    if n < 0:
        raise ValueError("number must be at least 0")

    digits = _split_digits(n)

    i = _find_transition(digits)

    if i == -1:
        return i

    digits = _reorder(digits, i)

    return _merge_digits(digits)


def _split_digits(n):
    """Split an unsigned integer into digits and return the list."""
    return list(str(n))


def _merge_digits(digits):
    """Merge a list of digits and return the unsigned integer value."""
    return int("".join(digits))


def _find_transition(digits):
    """Given an ordered list of digits, find the rightmost index in the interval
    [0, size-1] where adjacent digits increase in magnitude. The returned
    value is the index of the left item of the pair or -1 if there is no pair.
    """

    size = len(digits)
    if size > 1:
        for i in range(size-1, 0, -1):
            if digits[i-1] < digits[i]:
                return i-1
    return -1


def _reorder(digits, transition):
    """Given a list of digits and a transition index, find the next highest digit
     afer the transition and swap these two, then sort the tail of the
     list ascending.
    """

    end = len(digits)
    pivot = digits[transition]

    # find the index of the rightwards smallest element above pivot
    swap = _find_least_above(digits, transition+1, end, pivot)

    # exchange
    digits[transition], digits[swap] = digits[swap], pivot

    # sort tail
    digits = digits[:transition+1] + sorted(digits[transition+1:])

    return digits


def _find_least_above(digits, start, end, threshold):
    """Given a list of digits and range [start, end), find the least element
    larger than threshold, and return its index, or -1 if no such element
    exists.
    """

    j = start
    winner = digits[start]

    for i in range(start+1, end):
        digit = digits[i]
        if digit < winner and digit > threshold:
            winner, j = digit, i

    if winner > threshold:
        return j
    return -1


# tests ############################################################

def test_raises_with_negative_input():
    with pytest.raises(ValueError):
        solve(-1)


def test_single_digit_has_no_solution():
    assert solve(1) == -1


def test_uniform_digits_have_no_solution():
    assert solve(11) == -1


def test_descending_edge_case_has_no_solution():
    assert solve(21) == -1


def test_solves_ascending_edge_case():
    assert solve(12) == 21


def test_only_changes_rightmost_transition():
    assert solve(1212) == 1221


def test_sorts_tail():
    assert solve(121221) == 122112


# examples

def test_solve_example_11123():
    assert solve(11123) == 11132


def test_solve_example_1234321():
    assert solve(1234321) == 1241233


def test_solve_example_123987():
    assert solve(123987) == 127389
