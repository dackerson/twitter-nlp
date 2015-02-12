#!/bin/python

# Author: David Ackerson

import sys
from llr import llr2
from pmi import pmi
from dice import dice

with open(sys.argv[1], 'r') as f:
    freqs = {}
    collocs = []
    N = 0
    for line in f:
        tokens = line.strip().split()
        if len(tokens) == 2:
            freqs[tokens[1]] = int(tokens[0])
            N += 1
        else:
            collocs.append({'freq': int(tokens[0]), 'words': tokens[1:]})
    
    for colloc in collocs:
        f12 = colloc['freq']
        f1 = freqs[colloc['words'][0]]
        f2 = freqs[colloc['words'][1]]
        colloc['pmi_rank'] =  pmi(f12, f1, f2, N)
        colloc['llr_rank'] =  llr2(f12, f1, f2, N)
        colloc['dice_rank'] =  dice(f12, f1, f2, N)

    for colloc in sorted(collocs, key = lambda x: x['rank']):
        print colloc['rank'], colloc['words']
