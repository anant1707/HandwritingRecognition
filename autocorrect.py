# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 16:34:26 2020

@author: Anant
"""
import nltk
from nltk.corpus import words
from nltk.metrics.distance import (
    edit_distance,
    jaccard_distance,
    )
from nltk.util import ngrams
#nltk.download('words')
import pandas

correct_spellings = words.words()
spellings_series = pandas.Series(correct_spellings)

print(spellings_series)