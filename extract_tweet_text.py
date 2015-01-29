#!/usr/bin/python

# Author: David Ackerson

import json
import sys

for line in sys.stdin:
    text = json.loads(line)["text"]
    print(text.encode('unicode_escape'))
