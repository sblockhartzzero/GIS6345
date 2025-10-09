# -*- coding: utf-8 -*-
"""
Created on Tue Sep 23 22:51:02 2025

@author: s44ba

For GIS6345 Assignment 7

Write a function called sed that takes as arguments a pattern string, a replacement
string, and two filenames; it should read the first file and write the contents into the second file
(creating it if necessary). If the pattern string appears anywhere in the file, it should be replaced
with the replacement string.

If an error occurs while opening, reading, writing or closing files, your program should catch the
exception, print an error message, and exit.
"""

# Imports
import string
import re

def sed(pattern_string, replacement_string, input_file_fullpath, output_file_fullpath):
    
    # Open files
    # Open input file for reading
    try:
        fin = open(input_file_fullpath,'r')
    except:
        print("ERROR: Could not open input file: ",input_file_fullpath)
        return
        
    # Open output file for writing (overwriting if exists)
    try:
        fout = open(output_file_fullpath,'w')
    except:
        print("ERROR: Could not open output file: ",output_file_fullpath)
        return
               
    # Loop through lines of input file, replacing pattern_string with replacement_string
    for line in fin:
        line_mod = re.sub(pattern_string, replacement_string, line)
        print(line_mod)
        try:
            fout.write(line_mod)
        except:
            print("ERROR: Could not write to output file: ",output_file_fullpath)
            return
    #endfor

    # Close files
    try:
        fin.close()
    except:
        print("ERROR: Could not close input file: ",input_file_fullpath)
        return
    try:
        fout.close()
    except:
        print("ERROR: Could not close output file: ",output_file_fullpath)
        return
