import os
import sys

uselib = os.path.dirname(__file__)
uselib = os.path.join(uselib, '..', "src")
uselib = os.path.abspath(uselib)

sys.path.insert(0, uselib)
