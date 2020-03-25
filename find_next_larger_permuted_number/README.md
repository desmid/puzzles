# Problem

Given a natural number N, find the next number P > N that that reuses the same
set of digits (if P exists). If there is no solution, return -1.

Constraints:

  0 <= N <= 2e12
  time < 1s

Examples:

  11123   -> 11132
  1234321 -> 1241233
  1111    -> no solution
  4321    -> no solution

# Observations:

1. If the number consists of uniform digits (like 1, 11, 111) there is no
   solution, since all permutations are identical.

2. If the digits of the number are monotonically decreasing (like 4321)
   there is no solution, since no permutation can be larger.

3. Otherwise a number must contain at least one transition from low digit to
   higher digit (like 12, transition at 1) or (123, transitions at 1 and at
   2), so that a rightwards larger digit can always be exchanged with it.

4. Only the rightmost such transition affecting the least significant digits
   can generate a smallest number that is higher than the input value.

5. The choice of rightwards digit to exchange should be the least rightward
   value that is also greater than the transition digit.

6. After the exchange, the rightwards digits should be sorted (increasing)
   to produce the lowest possible number.

# Algorithm:

1. Split the number into digits.

2. Find the rightmost transition index, if any.

3. If there is no transition, report no solution and stop.

4. Let the digit at the transition index be 'pivot'. Logically partition the
   digits into { head, pivot, tail }. Exchange pivot with the next highest
   digit in tail, then sort tail ascending.

5. Join the digits back together and return the result.
