## Problem

A proof exists that any natural number P can be generated from the natural
number N' = 4 by successive application of a rule chosen from:

- rule 1: if N' ends with 1, append 0
- rule 2: if N' does not end with 1, append 4
- rule 3: divide N' by 2

Constraints:

- natural numbers start with 1
- time < 1s

Examples:
<pre>
  target:  13        target:  17

  start:   4         start:   4
  divide2: 2         divide2: 2
  divide2: 1         append4: 24
  append0: 10        divide2: 12
  append4: 104       divide2: 6
  divide2: 52        divide2: 3
  divide2: 26        append4: 34
  divide2: 13        divide2: 17
</pre>

## Observations

0. There is an implicit "rule 0": if N == N' == 4, stop

1. Rules 1 and 2 are mutually exclusive.

2. Rules 1 and 3 or 2 and 3 are not mutually exclusive.

3. There is no preferred order of rule application.

4. An approach exploring forwards from the starting value 4 is impracticable
   due to the branching factor (insight 2).

5. Instead, work backwards from the target number N, reversing rule
   applications.

This can be solved iteratively or recursively.

## Recursive algorithm

Construct a 'path' of rule applications:

1. base case:

   1a. if the input N is 4, return trivial path "rule 0".

2. general case:

   2a. split the input N into most significant digits (prefix) and least
       significant digit (digit).

   2b. examine digit:

   - if digit == 4: discard it, and append "rule 2" to the path returned by
     recursing on prefix.

   - if digit == 0: discard it, and append "rule 1" to the path returned by
     recursing on prefix.

   - otherwise: append "rule 3" to the path returned by recursing on 2 * N.
