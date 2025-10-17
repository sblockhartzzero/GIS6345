# -*- coding: utf-8 -*-
"""
Created on Tue Sep 23 22:51:02 2025

@author: s44ba

For GIS6345 Assignment 11
"""

# Imports
import string

# For exercise 11.1
def convert_words_file_to_dict(words_fullpath):
    
    # Set the word to be the key. Add the line_count (of the word in the words.txt file) so we can 
    # verify it's working

    # Define dictionary
    this_dictionary = dict()
    
    # Initialize  line count
    line_count = 1
    
    # Open words.txt and loop through it
    fin = open(words_fullpath)
    for line in fin:
        # Get word
        word = line.strip()
        # The following command strips nly leading or trailing whitespace
        word_no_ws = word.strip(string.whitespace)
        # Add this word to dictionary as the key. Also add the line count, so when
        # I check the program using the key, I get the line count of that key
        this_dictionary[word]=line_count
        # Increment line_count
        line_count = line_count + 1
    #endfor 
    
    # Close the file
    fin.close()
    
    # Return
    return this_dictionary

# For exercise 12.1
def histogram_for_string(s):
    d = dict()
    for c in s:
        if c not in d:
            d[c] = 1
        else:
            d[c] += 1    
        #endif
    #endfor
    
    return d 