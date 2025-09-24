# -*- coding: utf-8 -*-
"""
Created on Tue Sep 23 23:53:12 2025

@author: s44ba
"""

# Imports
import week5_functions

# Specify input file words.txt
words_fullpath = "C:/Users/s44ba/Documents/Training/Northeastern/GeospatialProgramming/Week5/week5_deliverables/week5_data/words.txt"

# Open file
fin = open(words_fullpath)

# Init counters
no_e_cnt = 0
word_cnt = 0

# Loop on words
for line in fin:
    # Get word
    word = line.strip()
    # Test for e
    if week5_functions.has_no_e(word.lower()):
        no_e_cnt = no_e_cnt + 1
        # Inspect a few
        if word_cnt<100:
            print(word)
        #endif    
    #endif 
    word_cnt = word_cnt + 1
#endfor 

# Close the file
fin.close() 

# Report number and pct of words with no e
print("Number of words w/o letter e = ",no_e_cnt)
pct_no_e = 100*float(no_e_cnt)/float(word_cnt)
print("Percentage of words w/o letter e = ",pct_no_e,"%")

