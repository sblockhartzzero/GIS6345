# -*- coding: utf-8 -*-
"""
Created on Sat Sep 20 23:03:46 2025

@author: s44ba

Test case for thinkpython2 exercise 5.2.1
"""

# Imports
import week3_functions

# User input
x = input('Enter integer a=\n')
a = int(x)

x = input('Enter integer b=\n')
b = int(x)

x = input('Enter integer c=\n')
c = int(x)

x = input('Enter integer n=\n')
n = int(x)

# Call check_fermat
week3_functions.check_fermat(a,b,c,n)