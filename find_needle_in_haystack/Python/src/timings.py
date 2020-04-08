import random
import sys

# https://stackoverflow.com/questions/7370801/measure-time-elapsed-in-python
from timeit import default_timer as timer

from findstring import FindString

REPEAT = 100


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


def test_massive_random_find():

    tlen, qlen = 2**20, 2**13

    time1, time2 = 0, 0

    print("run", REPEAT, "massive random finds")

    for _ in range(REPEAT):
        start = random.randint(0, tlen - qlen)
        target, query = build_strings(tlen, qlen, start)
        finder = FindString(target, query, metrics=True)

        begin = timer()
        finder.binary_find()
        time1 += timer() - begin

        begin = timer()
        finder.margin_find()
        time2 += timer() - begin

    print("binary_find", REPEAT, "iterations",  "%6.4f" % time1, "seconds")
    print("margin_find", REPEAT, "iterations",  "%6.4f" % time2, "seconds")
    print()


test_massive_random_find()
