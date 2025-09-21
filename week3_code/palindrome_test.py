# -*- coding: utf-8 -*-
"""
Created on Sun Sep 21 10:28:10 2025

@author: s44ba
"""

# For thinkpython exercise 6.3, testing for palindrome
 
# What about the empty string, which is written '' and contains no letters?

# Imports
import palindrome

# What happens if you call middle with a string with three letters?
print('Calling middle with the following three letters: WHY') 
this_string = palindrome.middle('WHY')
print(this_string)

# What happens if you call middle with a string with two letters?
print('Calling middle with only the following two letters: WH') 
this_string = palindrome.middle('WH')
print(this_string)

# What happens if you call middle with only one letter?
print('Calling middle with only the following single letter: W') 
this_string = palindrome.middle('W')
print(this_string)

# What happens if you call middle with an empty string?
print('Calling middle with an empty string') 
this_string = palindrome.middle('')
print(this_string)