#!/bin/bash
# Author: David Ackerson

bash -c "\
  cat $1 |\
./collocations.py |\
  grep -x '[[:alnum:][:space:]]\+' |\
  sort |\
  uniq -c > $1.colloc"
