# -*- coding: utf-8 -*-
"""
Created on Sun Sep 21 10:55:43 2025

@author: s44ba
"""
# Imports
import math

# For exercise 6.3 of thinkpython2
def first(word):
    return word[0]

def last(word):
    return word[-1]

def middle(word):
    return word[1:-1]  

def is_palindrome(word: str):
    
    # Get length of input word
    num_chars = len(word)
    
    # If the length is an even number, it cannot be a palindrome
    if (num_chars%2 == 0):
        return False
    # Else proceed to test the word to see it it is a palindrome
    else:
        # Init word_subset
        word_subset = word
        # Determin number of pairs of letters to compare e.g. first, last 
        # letters of a word_subset
        num_pairs =  math.floor(num_chars/2)
        # Iterate over num_pairs, from outside to inside
        for pair_num in range(num_pairs):
            print("pair_num=",pair_num)
            print("word_subset=",word_subset)
            if (first(word_subset) != last(word_subset)):
                return False
            else:
                # Get ready for next iteration by updating 
                # word_subset, lopping off the first and last
                word_subset = middle(word_subset)
        #endfor
        # If we get to this point, it must be a palindrome
        return True
    #endif
    
    
        
        
    
    