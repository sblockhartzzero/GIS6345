#!/usr/bin/env python
# coding: utf-8

# In[1]:


# From thinkpython2.pdf:
# Exercise 8.2. There is a string method called count that is similar to the function in Section 8.7.
# Read the documentation of this method and write an invocation that counts the number of a’s in
#'banana'.


# In[2]:


myString = 'banana'
num_chars = myString.count('a')


# In[3]:


num_chars


# In[4]:


# From thinkpython2.pdf:
# Exercise 8.3:
# A step size of -1 goes through the word backwards, so the slice [::-1] generates a reversed string.
# Use this idiom to write a one-line version of is_palindrome from Exercise 6.3.


# In[5]:


def is_palindrome(word):
    if (word == word[::-1]):
        return True
    else:
        return False
    #endif    


# In[6]:


# Test is_palindrome
is_palindrome('ABCDEDCBA')


# In[7]:


# Test is_palindrome
is_palindrome('GIS6345')


# In[ ]:




