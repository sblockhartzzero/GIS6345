# -*- coding: utf-8 -*-
"""
Created on Sat Sep 20 22:36:28 2025

@author: s44ba

Functions for week3 of GIS6345
"""

# For exercise 5.2.1 of thinkpython2
def check_fermat(a: int,b: int,c: int,n: int):
    if ( ((a**n)+(b**n)) == c**n) and (n>2):
        print("Holy smokes, Fermat was wrong!")
    else:
        print("No, that doesn’t work.")
        
    

      
            
        
    