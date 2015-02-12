#!/usr/bin/python

# Author: David Ackerson

import json
import sys
import nltk

conll_fields = {
    "ID": 0,
    "FORM": 1,
    "LEMMA": 2,
    "CPOSTAG": 3,
    "POSTAG": 4,
    "FEATS": 5,
    "HEAD": 6,
    "DEPREL": 7,
}

parse = []
my_lemmatizer = nltk.stem.WordNetLemmatizer()

for line in sys.stdin:
    if line != "\n":
        parse.append(line.split('\t'))
    else:
        for row in parse:
            if row[conll_fields["CPOSTAG"]] == 'N' or row[conll_fields["POSTAG"]] == 'N':
                head = int(row[conll_fields["HEAD"]])
                if head > 0:
                    head_row = parse[head - 1]
                    if head_row[conll_fields["CPOSTAG"]] == 'V' or head_row[conll_fields["POSTAG"]] == 'V':
                        verb_form = head_row[conll_fields["FORM"]]
                        noun_form = row[conll_fields["FORM"]]

                        # Lemmatize the word forms first
                        verb_form = my_lemmatizer.lemmatize(verb_form, 'v')
                        noun_form = my_lemmatizer.lemmatize(noun_form, 'n')

                        print("%s %s" % (verb_form, noun_form))
                        print(verb_form)
                        print(noun_form)
        parse = []
