# -*- coding: utf-8 -*-
"""
Created on Mon Oct 13 17:37:39 2025

@author: s44ba

For Ocean Sciences 2026

This program calls functions in project_functions.py to animate oceanographic data.

The oceanographic data is either:
    -temperature and velocity from HYCOM hindcasts (not yet supported for OS2026)
    -SST from MUR

The env_scenario corresponds to a date range (and download file) for the OS2026 analysis. See the README.txt file
at C:\\Users\\s44ba\\git\\GIS6345\\project_data\\env_data\\CapeHatteras\\MUR_SST_CapeHatteras. Before adding a 
new env_scenario, you need to add it to project_pickle_MUR_SST.py and to project_functions.get_MUR_pickle_filename. 

To  do:
    -support for OS2026_3 
"""
# Imports
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from celluloid import Camera
import project_functions

# Custom import from a different folder
import sys
sys.path.append('../try_hp')
import os2026_functions

#==============USER INPUT===================================================================
# Specify whether oceanographic data is from 'HYCOM' opr 'MUR'
env_data_src  = 'MUR'

# Specify scenario (which ultimately determines which pickle file to use for MUR SST)
# Could be 'GIS6345' or 'OS2026_1a','OS2026_1b' to 'OS2026_4'
env_scenario = 'OS2026_1a'

# Specify scenario (which defines time frame as well as input data file)
match env_scenario:
    case 'OS2026_1':
        start_datetime = datetime(2015,1,15)  
        num_days = 70
    case 'OS2026_1a':
        start_datetime = datetime(2015,1,15)  
        num_days = 30
    case 'OS2026_1b':
        start_datetime = datetime(2015,2,15)  
        num_days = 40
    case 'OS2026_2':
        start_datetime = datetime(2016,2,15)  
        num_days = 40
    case 'OS2026_3':
        start_datetime = datetime(2018,2,15)  
        num_days = 40
    case 'OS2026_4':
        start_datetime = datetime(2018,12,1)  
        num_days = 119         
#endmatch

#===========CREATE ARRAY OF DATETIMES========================================================
timestamp_datetime_array = [start_datetime + timedelta(days=x) for x in range(num_days)]

#============PLOT OCEANOGRAPHIC DATA (STATIC)================================================
# Get data for the SST plot
ts_lon_array,ts_lat_array,SST_array = project_functions.get_SST(timestamp_datetime_array[0],env_data_src,env_scenario)

# Data source-specific stuff
if (env_data_src=='HYCOM'):
    # Set custom levels for SST (degrees C)
    custom_SST_levels = np.linspace(8,29,num=22)
else:
    # Set custom levels for SST (degrees F)
    #custom_SST_levels = 25
    custom_SST_levels = np.linspace(40,81,num=40)
#endif

# Plot SST image and HP-filtered SST image
HP_SST_array = os2026_functions.hpfilter_band_from_array(SST_array)
# Plot HP-filtered SST image
plt.imshow(SST_array)
plt.show() 
plt.imshow(HP_SST_array)
plt.colorbar()
plt.show()
#plt.hist(HP_SST_array,bins='auto')
#plt.show()

# Plot track with overlays 
fig1, ax1 = plt.subplots()
cont = ax1.contourf(ts_lon_array,ts_lat_array,HP_SST_array)  # Contour SST
fig1.colorbar(cont)
plt.show()

# Plot track with overlays 
fig2, ax2 = plt.subplots()
cont = ax2.contourf(ts_lon_array,ts_lat_array,SST_array,levels=custom_SST_levels,cmap=cm.jet)  # Contour SST
fig2.colorbar(cont)
ax2.set(xlim=[-76.0, -73.0],ylim=[34.25, 37.5])
# Set plot title
title_string = env_scenario
plt.title(title_string)
# Labels 
plt.xlabel('Longitude')
plt.ylabel('Latitude')
# Update text
text_string = timestamp_datetime_array[0].strftime("%Y-%m-%d")
ax2.text(0.8,0.8,text_string)
# Show
plt.show()


#===========ANIMATE OCEANOGRAPHIC DATA==================================================
fig3, ax3 = plt.subplots()
camera = Camera(fig3)
for frame_num in range(len(timestamp_datetime_array)):  
    ax3.set(xlim=[-76.0, -73.0],ylim=[34.25, 37.5])      
    # Update SST contour 
    # Get data for the SST plot
    ts_lon_array,ts_lat_array,SST_array = project_functions.get_SST(timestamp_datetime_array[frame_num],env_data_src,env_scenario)
    
    # Contour plot of SST   
    cont = ax3.contourf(ts_lon_array,ts_lat_array,SST_array,levels=custom_SST_levels,cmap=cm.jet)
    #fig3.colorbar(cont) # Including this causes problems
    
    # Update plot title
    title_string = env_scenario
    plt.title(title_string)
    # Update text
    text_string = timestamp_datetime_array[frame_num].strftime("%Y-%m-%d")
    plt.text(0.8,0.8,text_string)
    # Labels 
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    # Snap picture of this frame
    camera.snap()
#endfor
animation = camera.animate(interval=120)
mp4_filename = env_scenario + '.mp4' 
animation.save(mp4_filename)  






