import pytest


def START(n): return message("start", n)


def APPEND0(n): return message("append0", n)


def APPEND4(n): return message("append4", n)


def DIVIDE2(n): return message("divide2", n)


def message(state, value): return "%s: %d" % (state, value)


def solve_iterative(n):
    if n < 1:
        raise ValueError("value must be greater than 0")

    path = []

    while True:
        if n == 4:  # solution found
            path.insert(0, START(n))
            break

        prefix, digit = n // 10, n % 10

        if digit == 4:
            path.insert(0, APPEND4(n))
            n = prefix
        elif digit == 0:
            path.insert(0, APPEND0(n))
            n = prefix
        else:
            path.insert(0, DIVIDE2(n))
            n *= 2

    return path


def solve_recursive(n):
    if n < 1:
        raise ValueError("value must be greater than 0")

    return _solve_recursive(n)


def _solve_recursive(n):

    if n == 4:
        return [START(n)]

    prefix, digit = n // 10, n % 10

    if digit == 4:
        path = _solve_recursive(prefix)
        path.append(APPEND4(n))
        return path

    if digit == 0:
        path = _solve_recursive(prefix)
        path.append(APPEND0(n))
        return path

    path = _solve_recursive(n*2)
    path.append(DIVIDE2(n))
    return path


# tests ############################################################

def test_solve_0_should_raise():
    with pytest.raises(ValueError):
        solve_iterative(0)
    with pytest.raises(ValueError):
        solve_recursive(0)


def test_solve_4_should_pass_immediately():
    expect = [
        START(4)
    ]
    assert solve_iterative(4) == expect
    assert solve_recursive(4) == expect


def test_solve_one_digit():
    expect = [
        START(4),
        DIVIDE2(2),
        DIVIDE2(1),
    ]
    assert solve_iterative(1) == expect
    assert solve_recursive(1) == expect


def test_solve_13():
    expect = [
        START(4),
        DIVIDE2(2),
        DIVIDE2(1),
        APPEND0(10),
        APPEND4(104),
        DIVIDE2(52),
        DIVIDE2(26),
        DIVIDE2(13),
    ]
    assert solve_iterative(13) == expect
    assert solve_recursive(13) == expect


def test_solve_17():
    expect = [
        START(4),
        DIVIDE2(2),
        APPEND4(24),
        DIVIDE2(12),
        DIVIDE2(6),
        DIVIDE2(3),
        APPEND4(34),
        DIVIDE2(17),
    ]
    assert solve_iterative(17) == expect
    assert solve_recursive(17) == expect
