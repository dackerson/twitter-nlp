#!/bin/bash
# Author: David Ackerson

bash -c "\
  zcat -f $1 |\
./extract_tweet_text.py |\
./parser_run.sh /dev/stdin |\
  tee $1.parsed |\
./collocations.py |\
  grep -x '[[:alnum:][:space:]]' |\
  sort |\
  uniq -c > $1.colloc"
