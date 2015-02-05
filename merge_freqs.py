#!/bin/python

# Author: David Ackerson

import sys
import os

colloc_counts = []

for file_name in sys.argv[1:]:
    file = open(file_name, 'r')
    line = file.readline().strip()
    if not line == '':
        tokens = line.split()
        freq = int(tokens[0])
        words = " ".join(tokens[1:])
        line = {'freq': freq, 'words': words}
        colloc_count = {'file': file, 'line': line}
        colloc_counts.append(colloc_count)

while True:
    if colloc_counts == []:
        break

    sorted_ccs = sorted(colloc_counts, key=lambda cc: cc['line']['words'])
    top_cc = sorted_ccs[0]
    top_ccs = [cc for cc in colloc_counts if cc['line']['words'] == top_cc['line']['words']]
    freqs = 0
    for cc in top_ccs:
        freqs += cc['line']['freq']

    print "{0:>7} {1}".format(freqs, top_cc['line']['words'])
    
    for cc in top_ccs:
        line = cc['file'].readline().strip()
        if line == '':
            cc['line']['words'] = ''
        else:
            tokens = line.split()
            freq = int(tokens[0])
            words = " ".join(tokens[1:])
            cc['line']['freq'] = freq
            cc['line']['words'] = words
    
    colloc_counts = [cc for cc in colloc_counts if not cc['line']['words'] == '']
