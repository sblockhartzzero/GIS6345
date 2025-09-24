# -*- coding: utf-8 -*-
"""
Created on Tue Sep 23 23:51:09 2025

@author: s44ba
"""

# For GIS6345 exercise 9.2
def has_no_e(word):
    if ('e' in word):
        return False
    else:
        return True
    #endif
    
# For GIS6345 exercise 10.1
# Remove a level of nesting from a list
# If there are mulptiple levels of nesting, this function should be called iteratively
# until list is no longer nested. THe callerwill know when to stop--i.e. when the
# output_list has the same length as the input_list
def flatten_list_one_level(input_list):
    # Init output list
    output_list = []
    # Loop on items in input_list
    for k in range(len(input_list)):
        val = input_list[k]
        if (type(val) is int):
           output_list.append(val) 
        elif (type(val) is list):
            # This item in the list is nested
            sub_list = val
            sub_list_len = len(sub_list)
            # Loop on items in sub_list
            for n in range(sub_list_len):
                sub_val = sub_list[n]
                output_list.append(sub_val)
            #endfor
        #endif 
    #endfor 
    return output_list

# For GIS6345 exercise 10.1
# Flatten a list even if it has multiple levels of nesting
def flatten_list(input_list):
    # Initialize lists
    output_list = []
    this_list = input_list
    while (1 == 1):
        print("Calling flatten_list_one_level")
        output_list = flatten_list_one_level(this_list)
        if (len(output_list) == len(this_list)):
            break
        else:
            # Continue looping
            # Prep for next iteration
            this_list = output_list
    #endwhile
    return output_list
    
# For GIS6345 exercise 10.1
# Exercise 10.1. Write a function called nested_sum that takes a list of lists 
# of integers and adds up the elements from all of the nested lists.
# It calls flatten_list, which iteratively calls flatten_list_one_level until
# there is no more nesting
def nested_sum(input_list):
    # First, get rid of nesting
    flattened_list = flatten_list(input_list)
    # Get sum of flattened list
    return_val = sum(flattened_list)
    return return_val
            
# For GIS6345 exercise 10.2
def cumsum(input_list):
    # Assume input_list is a list of integers   
    # Init output list
    output_list = []    
    # Loop on items in input_list
    for k in range(len(input_list)):        
        this_val = sum(input_list[0:k+1])
        print(k, this_val)
        output_list.append(this_val)
    #endfor
    return output_list 
  
            
            
    
    
    
    
     