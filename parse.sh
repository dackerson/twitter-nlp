#!/bin/python

# Author: David Ackerson

zcat $1 | python extract_tweet_text.py | TweeboParser/run.sh /dev/stdin
