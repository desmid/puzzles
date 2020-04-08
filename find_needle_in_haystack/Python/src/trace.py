class trace:

    MAX_TRACE_WIDTH = 80

    target = None
    tlen = None
    qlen = None
    marker = None

    def __init__(self, finder):
        self.target = finder.target
        self.tlen = finder.tlen
        self.qlen = finder.qlen
        self.marker = finder.query_string[0]

    def print(self, text, left, right, margin=None):
        if self.tlen > self.MAX_TRACE_WIDTH:
            return
        self._pretty_print(text, left, right, margin)

    def _pretty_print(self, text, left, right, margin):
        """Pretty print a stage of a search on one line.

        Example after repeated calls:

          mf in  [--xxxx--]  8/4 (0, 7) margin 4
          mf sh  [--xxxx--]  8/4 (0, 7) margin 2
          mf bl  [--xxxx]..  8/4 (0, 5) margin 2
          mf br  ..[xxxx]..  8/4 (2, 5) margin 2
          mf >>  ..[xxxx]..  8/4 (2, 5)

        Key:

          [xxxx--] the query 'xxxx' with brackets showing the margins of the
                   search segment also containing '--' as part of the target

          nf = naive_find
          bf = binary_find
          mf = margin_find

          in = enter function
          bl = branch left
          br = branch right
          sh = shrink margin by 2
          >> = return solution
        """

        prefix = self.target[0:left]
        middle = self.target[left:right + 1]
        suffix = self.target[right + 1:self.tlen]
        out = ""

        if left != 0:
            out += "".join(prefix).replace('-', '.').replace(self.marker, '*')

        out += '[' + "".join(middle) + ']'

        if right != self.tlen - 1:
            out += "".join(suffix).replace('-', '.').replace(self.marker, '*')

        out = "%s  %s  %d/%d (%d, %d)" % \
            (text, out, self.tlen, self.qlen, left, right)

        out += " margin %d" % margin if margin is not None else ""

        print(out)
