# -*- coding: utf-8 -*-
"""
Created on Tue Sep 23 22:51:02 2025

@author: s44ba

For GIS6345 Assignment 11
"""

# Exercise 11.1. Convert words.txt to a dict where the word is the key


# Imports
import string
import week11_functions

# Specify input file words.txt
words_fullpath = "C:/Users/s44ba/Documents/Training/Northeastern/GeospatialProgramming/Week5/week5_deliverables/week5_data/words.txt"

# Call the function  
this_dictionary = week11_functions.convert_words_file_to_dict(words_fullpath)

# Verify that it worked
print("Original line_count for the word xylophone = ",this_dictionary['xylophone']) 