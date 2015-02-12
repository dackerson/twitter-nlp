#!/bin/python

# Author: David Ackerson

import math

def pmi(f12, f1, f2, N):
    return math.log((f12 * N) / (f1 * f2))
