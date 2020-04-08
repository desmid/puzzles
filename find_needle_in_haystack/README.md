## Problem

Given a string of length 1048576, find the position of a substring of length
8192 characters, where:

- the substring is the largest substring
- the substring characters are all the same
- there is only one instance of it.

Constraint:

- It is not possible to examine the string, but there is an external function

  `
  int getMaxLength(int startPosition, int endPosition)
  `

  which returns the length of the maximal candidate substring in the interval.

## What is known?

- The 'target' string to be searched is `1048576 = 2^20` characters
- The 'query'  string to be found    is    `8192 = 2^13` characters

The query is 7 orders of magnitude base 2 smaller than the target.

## Three solutions

- *naive_find* (uses a linear scan)
- *binary_find* (eliminates target using a binary search initially)
- *margin_find* (eliminates margins of the target incrementally)

### 1. naive_find

Let:
```
  tlen = length(target)
  qlen = length(query)
```

Scan along target testing each word of length `qlen` starting at every
possible starting position in target:

```
for i = 0 to i = tlen-qlen
  do scan getMaxLength(i, i+qlen-1)
```

Analysis:

Assuming the `getMaxLength` function is at least linear in the length of
input, this is at least `O(tlen * qlen)`, i.e., `O(tlen)` with `qlen` being a
large constant.

### 2. binary_find

Use divide and conquer to eliminate most of the target, similar to binary
search.

Let:
```
  tlen = length(target)
  qlen = length(query)
  slen = length(segment of target)
```

Given a 'segment', there are 6 cases:
```
case 0a:  slen < qlen
          return no match

case 0b:  slen == qlen != getMaxLength(segment_start, segment_stop)
          return no match

case 1:   slen == qlen == getMaxLength(segment_start, segment_stop)
          return solution `[segment_start, segment_stop]`

case 2:   slen > qlen and query lies in left half of segment
          recurse to left

case 3:   slen > qlen and query lies in right half of segment
          recurse to right

case 4:   slen > qlen and query spans the middle of segment
          extract middle and change algorithm to either:
          - return naive_find linear_scan (see above), or
          - return margin_find (see below)
```

Case 4 details:

The query spans the middle of segment so at most `qlen-1` characters lie in
the left half of the segment or at most `qlen-1` in the right half, defining
a region `2*qlen-2` characters wide.

For example:
```
  segment:  xxxxx|xxxxx   query of length 4 spans the midpoint somwhere
              xxx|x       leftmost candidate
                x|xxx     rightmost candidate
              xxx|xxx     new segment to search
```

#### Analysis

*Binary_find* is roughly `O(log2 tlen)` assuming `getMaxLength` is `O(1)`,
with a large constant.

A recursive implementation is not stack limited as the recursion depth will be
at most `log2(tlen/qlen) = 7`.

Most of the cost lies in case 4. If the *naive_find* linear scan approach is
used that will require `(2*qlen - 2 - qlen + 1) = qlen - 1` calls to
`getMaxLength`, or 8191, which is very expensive. The *margin_find* method
described below solves this problem.

### 3. margin_find

For some starting margin size, repeatedly eliminate that margin from either
or both sides of the target string. If there is no reduction possible at
that margin size, divide the margin by 2 and repeat. Stop when the query is
found, or there is no solution possible.

Let:
```
  tlen = length(target)
  qlen = length(query)
  slen = length(segment of target)

  margin = tlen//2  (if searching whole target string)
  margin = qlen//2  (if searching central region after binary_find)
```

Given a 'segment' and a 'margin', there are 6 cases:
```
case 0a:  slen < qlen
          return no match

case 0b:  slen == qlen != getMaxLength(segment_start, segment_stop)
          return no match

case 1:   slen == qlen == getMaxLength(segment_start, segment_stop)
          return solution [segment_start, segment_stop]

case 2:   slen > qlen and query lies in [left, segment_stop - margin]
          recurse to left

case 3:   slen > qlen and query lies in [segment_start + margin, segment_stop]
          recurse to right

case 4:   slen > qlen and no match
          the margin is too big, halve it:
            margin = margin / 2
          and repeat the search.
```

#### Analysis

An iterative implementation is preferable as, if too small an initial margin
is chosen the recursion depth could get very deep with little work done at
each level.

This method is actually similar to *binary_find*, but will be less efficient
in most cases because it does not explicitly discover any central region
containing the query.

## Timings

On an old Intel core2 duo laptop (Python using 1 core), *binary_find* and
*margin_find* can solve the given problem with 100 randomly placed queries in
under five seconds:

```
  binary_find 100 iterations 3.9339 seconds
  margin_find 100 iterations 4.3326 seconds
```

As might be expected, *binary_find* (calling *margin_find* for the final
search) is slighlty faster than *margin_find* alone.

## Examples with (inscrutable) trace output

Search for a 4 character query substring (denoted xxxx) in an 8 character
target string. There are 5 possible starting positions giving 5 traces in each
example below. Without explaining the detailed output, it should be clear how
the algorithms examine boxed [.....] segments and progressively home in on the
query substring, which is found when it is tightly boxed [xxxx].

#### naive_find, uses linear scan

```
  nf in  [xxxx----]  8/4 (0, 7)
  ls in  [xxxx----]  8/4 (0, 7)
  ls >>  [xxxx]....  8/4 (0, 3)

  nf in  [-xxxx---]  8/4 (0, 7)
  ls in  [-xxxx---]  8/4 (0, 7)
  ls >>  .[xxxx]...  8/4 (1, 4)

  nf in  [--xxxx--]  8/4 (0, 7)
  ls in  [--xxxx--]  8/4 (0, 7)
  ls >>  ..[xxxx]..  8/4 (2, 5)

  nf in  [---xxxx-]  8/4 (0, 7)
  ls in  [---xxxx-]  8/4 (0, 7)
  ls >>  ...[xxxx].  8/4 (3, 6)

  nf in  [----xxxx]  8/4 (0, 7)
  ls in  [----xxxx]  8/4 (0, 7)
  ls >>  ....[xxxx]  8/4 (4, 7)
```

#### binary_find, binary search with opportunistic margin_find

Switches algorithm from *binary_find* (bf) to *margin_find* (mf) in
cases when a central region containing the query has been identified.
```
  bf in  [xxxx----]  8/4 (0, 7)
  bf bl  [xxxx]....  8/4 (0, 3)
  bf >>  [xxxx]....  8/4 (0, 3)

  bf in  [-xxxx---]  8/4 (0, 7)
  mf bl  .[xxxx]...  8/4 (1, 4) margin 2
  mf >>  .[xxxx]...  8/4 (1, 4)

  bf in  [--xxxx--]  8/4 (0, 7)
  mf sh  .[-xxxx-].  8/4 (1, 6) margin 1
  mf bl  .[-xxxx]..  8/4 (1, 5) margin 1
  mf br  ..[xxxx]..  8/4 (2, 5) margin 1
  mf >>  ..[xxxx]..  8/4 (2, 5)

  bf in  [---xxxx-]  8/4 (0, 7)
  mf br  ...[xxxx].  8/4 (3, 6) margin 2
  mf >>  ...[xxxx].  8/4 (3, 6)

  bf in  [----xxxx]  8/4 (0, 7)
  bf br  ....[xxxx]  8/4 (4, 7)
  bf >>  ....[xxxx]  8/4 (4, 7)
```

#### margin_find, eats margins
```
  mf in  [xxxx----]  8/4 (0, 7) margin 4
  mf bl  [xxxx]....  8/4 (0, 3) margin 4
  mf >>  [xxxx]....  8/4 (0, 3)

  mf in  [-xxxx---]  8/4 (0, 7) margin 4
  mf sh  [-xxxx---]  8/4 (0, 7) margin 2
  mf bl  [-xxxx-]..  8/4 (0, 5) margin 2
  mf sh  [-xxxx-]..  8/4 (0, 5) margin 1
  mf bl  [-xxxx]...  8/4 (0, 4) margin 1
  mf br  .[xxxx]...  8/4 (1, 4) margin 1
  mf >>  .[xxxx]...  8/4 (1, 4)

  mf in  [--xxxx--]  8/4 (0, 7) margin 4
  mf sh  [--xxxx--]  8/4 (0, 7) margin 2
  mf bl  [--xxxx]..  8/4 (0, 5) margin 2
  mf br  ..[xxxx]..  8/4 (2, 5) margin 2
  mf >>  ..[xxxx]..  8/4 (2, 5)

  mf in  [---xxxx-]  8/4 (0, 7) margin 4
  mf sh  [---xxxx-]  8/4 (0, 7) margin 2
  mf br  ..[-xxxx-]  8/4 (2, 7) margin 2
  mf sh  ..[-xxxx-]  8/4 (2, 7) margin 1
  mf bl  ..[-xxxx].  8/4 (2, 6) margin 1
  mf br  ...[xxxx].  8/4 (3, 6) margin 1
  mf >>  ...[xxxx].  8/4 (3, 6)

  mf in  [----xxxx]  8/4 (0, 7) margin 4
  mf br  ....[xxxx]  8/4 (4, 7) margin 4
  mf >>  ....[xxxx]  8/4 (4, 7)
```

## Implementation
```
Python
├── src
│   ├── findstring.py        # implementation
│   ├── metrics.py           # collect/display metrics
│   ├── timings.py           # run repeated timings
│   └── trace.py             # display traces
└── test
    ├── __init__.py
    └── findstring_test.py
```
