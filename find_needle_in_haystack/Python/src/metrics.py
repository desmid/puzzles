class metrics:
    name = ""
    calls = 0   # number of calls
    cumlen = 0  # cumulative length of target scanned

    def __init__(self, name=""):
        self.name = name
        self.calls = 0
        self.cumlen = 0

    def update(self, left, right):
        self.calls += 1
        self.cumlen += right - left + 1

    def print(self, msg=""):
        """
        Print metrics.

        Example:

          margin_find: funcalls: 6, targetsum: 26

        Key:

          funcalls  = number of calls to getMaxLength
          targetsum = cumulative length of target examined by getMaxLength
        """

        if self.name:
            print(self.name, end=": ")

        print("funcalls: %d, targetsum: %d %s" % (self.calls, self.cumlen, msg))
