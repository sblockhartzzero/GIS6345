# -*- coding: utf-8 -*-
"""
Created on Tue Sep 23 22:51:02 2025

@author: s44ba

For GIS6345 Assignment 5
"""

# Exercise 9.1. Write a program that reads words.txt and prints only the words with 
# more than 20 characters (not counting whitespace).

# Issues: Why are spaces not stripped out?

# Imports
import string
import re

# Specify input file words.txt
words_fullpath = "C:/Users/s44ba/Documents/Training/Northeastern/GeospatialProgramming/Week5/week5_deliverables/week5_data/words.txt"

#
fin = open(words_fullpath)
for line in fin:
    # Get word
    word = line.strip()
    # The following command strips nly leading o trailing whitespace
    word_no_ws = word.strip(string.whitespace)
    # The following command is better as it strips all whitespace from the string
    word_no_ws_better = re.sub(r'\s+','',word)
    if len(word_no_ws_better) > 20:
        print(word_no_ws_better)
    #endif 
#endfor 

# Close the file
fin.close() 