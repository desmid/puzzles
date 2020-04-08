"""
FindString

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
"""

from metrics import metrics
from trace import trace


class FindString:
    """Class implements search methods to find a substring using the black box
    getMaxLength() function (see problem specification). Three public search
    methods are defined:

    - naive_find()  - performs a linear scan.
    - binary_find() - performs a binary search eliminating left or right
                      branches of the target sequence, followed by margin_find
                      in the central region if necessary.
    - margin_find() - performs a margin shinkage search eliminating marginal
                      pieces of the target sequence from both sides.
    """

    # return value if search finds no match
    NO_MATCH = (-1, -1)

    # call metrics for getMaxLength
    show_metrics = False
    metrics = None

    # tracing
    show_trace = False
    trace = None

    # "black box" method
    def getMaxLength(self, startPosition, endPosition):
        """A model implementation of getMaxLength as defined in the
        specification. Rather than return the length of the longest substring,
        it returns the query string length (if found) or zero (if not found).
        """
        segment = self.target[startPosition:endPosition+1]
        return self.qlen if self.query_string in "".join(segment) else 0

    # initialisation

    def __init__(self, target, query, trace=False, metrics=False):
        """Construct a FindString instance. Throws ValueError for bad target or
        query sequence lengths (query bigger than target, target or query
        shorter than 1).
        """
        tlen, qlen = len(target), len(query)

        if tlen < qlen:
            raise ValueError("query is bigger than target")
        if tlen < 1:
            raise ValueError("target length less than 1")
        if qlen < 1:
            raise ValueError("query length less than 1")

        self._initialise(target, query, tlen, qlen, trace, metrics)

    def _initialise(self, target, query, tlen, qlen, trace, metrics):
        self.target = target
        self.query_string = "".join(query)  # for getMaxLength
        self.tlen = tlen
        self.qlen = qlen
        self.show_trace = trace
        self.show_metrics = metrics
        self._trace_start()

    def _trace_start(self):
        if self.show_trace:
            self.trace = trace(self)

    def _trace(self, text, left, right, margin=None):
        if self.show_trace:
            self.trace.print(text, left, right, margin)

    def _metrics_start(self, name=""):
        if self.show_metrics:
            self.metrics = metrics(name)

    def _metrics_print(self, msg=""):
        if self.show_metrics:
            self.metrics.print(msg)

    # public methods

    def naive_find(self):
        """naive_find performs a linear scan for query in target and returns
        (start, stop) inclusive if found, or NO_MATCH otherwise.
        """
        self._metrics_start("naive_find")
        self._trace("nf in", 0, self.tlen - 1)
        solution = self._linear_scan(0, self.tlen - 1)
        self._metrics_print()
        return solution

    def binary_find(self):
        """binary_find performs a binary search for query in target and returns
        (start, stop) inclusive if found, or NO_MATCH otherwise.
        """
        self._metrics_start("binary_find")
        self._trace("bf in", 0, self.tlen - 1)
        solution = self._binary_find(0, self.tlen - 1)
        self._metrics_print()
        return solution

    def margin_find(self):
        """margin_find performs a margin-reducing search for query in target
        and returns (start, stop) inclusive if found, or NO_MATCH otherwise.
        """
        self._metrics_start("margin_find")
        self._trace("mf in", 0, self.tlen - 1, self.tlen//2)
        solution = self._margin_find(0, self.tlen - 1, self.tlen//2)
        self._metrics_print()
        return solution

    # private methods

    def _contains(self, left, right):
        """Returns True if target exactly contains query in (left, right)
        inclusive.
        """
        if self.show_metrics:
            self.metrics.update(left, right)
        return self.getMaxLength(left, right) == self.qlen

    def _linear_scan(self, left, right):
        """
        Performs a linear scan for query in target, scanning rightwards from
        successive start positions. Returns (start, stop) inclusive if found,
        or NO_MATCH otherwise.
        """
        self._trace("ls in", left, right)
        for start in range(left, right + 1):
            stop = start + self.qlen - 1
            if self._contains(start, stop):
                self._trace("ls >>", start, stop)
                return (start, stop)
        self._trace("ls ee", left, right)
        return self.NO_MATCH

    def _binary_find(self, left, right):
        """
        Performs a binary search for query in target eliminating left or right
        sides by successive halvings of the search space. Resorts to another
        algorithm (margin_find) if the target can no longer be halved. Returns
        (left, right) inclusive if found, or NO_MATCH otherwise.
        """
        slen = right - left + 1
        margin = slen//2

        # case 0a
        if slen < self.qlen:
            self._trace("bf ee", left, right)
            return self.NO_MATCH

        # cases 0b and 1
        if slen == self.qlen:
            if self._contains(left, right):  # case 1
                self._trace("bf >>", left, right)
                return (left, right)
            else:                            # case 0b
                self._trace("bf ee", left, right)
                return self.NO_MATCH

        # case 2: examine left side
        if self._contains(left, right - margin):
            right -= margin
            self._trace("bf bl", left, right)
            return self._binary_find(left, right)

        # case 3: examine right side
        if self._contains(left + margin, right):
            left += margin
            self._trace("bf br", left, right)
            return self._binary_find(left, right)

        # case 4: examine centre
        split = right - margin
        left = max(left, (split - self.qlen + 2))
        right = min((split + self.qlen - 1), right)
        # return self._linear_scan(left, right)  # linear scan is slow
        return self._margin_find(left, right, self.qlen//2)

    def _margin_find(self, left, right, margin):
        """
        Performs an iterative search for query in target, eliminating the ends
        of the segment from either side by a margin amount that is successively
        halved when that margin is exhausted. Returns (left, right) inclusive
        if found, or NO_MATCH otherwise.
        """
        while True:
            slen = right - left + 1

            # case 0a
            if slen < self.qlen:
                self._trace("mf ee", left, right, margin)
                return self.NO_MATCH

            # cases 0b and 1
            if slen == self.qlen:
                if self._contains(left, right):  # case 1
                    self._trace("mf >>", left, right)
                    return (left, right)
                else:                            # case 0b
                    self._trace("mf ee", left, right)
                    return self.NO_MATCH

            # case 2: examine left side
            if self._contains(left, right - margin):
                right -= margin
                self._trace("mf bl", left, right, margin)
                continue

            # case 3: examine right side
            if self._contains(left + margin, right):
                left += margin
                self._trace("mf br", left, right, margin)
                continue

            # case 4: margin was too big
            margin = max(margin//2, 1)
            self._trace("mf sh", left, right, margin)
