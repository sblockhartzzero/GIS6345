#!/usr/bin/env python
# coding: utf-8

# In[1]:


# For Part2 of Homework4 in GIS6345


# In[1]:


# Imports
import arcgis


# In[2]:


from arcgis.gis import GIS
gis = GIS()


# In[3]:


map1 = gis.map('Chicago, IL')


# In[4]:


map1


# In[7]:


chicago_item = gis.content.get('ee16f399fb8e469aacfc48a0f2fc9f02')
chicago_layer = chicago_item.layers[0]
chicago_layer


# In[8]:


map1.content.add(chicago_layer)


# In[ ]:




