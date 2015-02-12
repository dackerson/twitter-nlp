#!/bin/bash
# Author: David Ackerson

bash -c "\
  cat -f $1 |\
./collocations.py |\
  grep -x '[[:alnum:][:space:]]' |\
  sort |\
  uniq -c > $1.colloc"
