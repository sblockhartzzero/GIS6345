# -*- coding: utf-8 -*-
"""
Created on Sat Sep 20 23:15:54 2025

@author: s44ba

Exercise 5.1 of thinkpython2
"""
# Imports
import time

# Get current time (in seconds since epoch)
secs_since_epoch = time.time()

# Convert to a string
timestamp_str = time.ctime(secs_since_epoch)
print(timestamp_str)

# Convert to days since epoch
secs_per_day = 24*60*60
days_since_epoch = secs_since_epoch/secs_per_day
print("Days since epoch = ", days_since_epoch)


