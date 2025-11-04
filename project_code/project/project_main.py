# -*- coding: utf-8 -*-
"""
Created on Mon Oct 13 17:37:39 2025

@author: s44ba

For GIS6345 Project

This program calls functions in project_functions.py to animate an animal track, 
overlaying time-varying oceanographic data.

The animal track is from a specified file downloaded from movebank.org.

The oceanographic data is either:
    -temperature and velocity from HYCOM hindcasts
    -SST from MUR
     
"""
# Imports
import pandas as pd
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from celluloid import Camera
import project_functions

#==============SPECIFY DATA SOURCE FOR OCEANOGRAPHIC DATA====================================
# Specify whether oceanographic data is from 'HYCOM' opr 'MUR'
env_data_src  = 'MUR'

# Specify scenario (which ultimately determines which pickle file to use for MUR SST)
env_scenario = 'GIS6345'

#==============LOAD ANIMAL TELEMETRY DATA INTO PANDAS DATAFRAME==============================
# Specify fullpath to input csv file containing multiple animal tracks
# i.e. the csv downloaded from movebank.org and load it into a pandas DataFrame
track_csv_fullpath = 'C:/Users/s44ba/git/GIS6345/project_data/track_data/Short_finned_pilot_whales_CRC_NW_Atlantic.csv'

# Let's look at just one of the tracks. From data exploration, I found GmTag142 to be 
# interesting i.e. it went through my region of interest
tag_id = 'GmTag137'  # e.g. 'GmTag142' or 'GmTag137'

# Call function to get the individual track, as apndas dataframe
myTrack = project_functions.get_movebank_track_from_csv(track_csv_fullpath, tag_id)

# Subset myTrack in time
myTrack_in_time_window = myTrack['timestamp_datetime']<datetime(2016,1,6)   # boolean
myTrack_subset = myTrack[myTrack_in_time_window]

#===============CONVERT ANIMAL TELEMETRY DATA TO NUMPY ARRAYS================================
# Extract arrays 
df_lat = myTrack_subset['location-lat']
df_lon = myTrack_subset['location-long']
df_timestamp_datetime = myTrack_subset['timestamp_datetime']

# Convert to numpy
lat_array = np.array(df_lat)
lon_array = np.array(df_lon)
timestamp_datetime_array = np.array(df_timestamp_datetime)

# print min and max timestamp during this period
print("Time from ",df_timestamp_datetime.min()," to ",df_timestamp_datetime.max())

#============INTEGRATE ANIMAL TELEMETRY DATA WITH OCEANOGRAPHIC DATA AND PLOT (STATIC)=======
# Plot just the track
fig1, ax1 = plt.subplots()
ax1.plot(lon_array,lat_array)

# Plot track with overlays of oceanographic data
# Get data for the SST plot
# Note use of .item() to convert numpy datetime back to datetime.datetime
ts_lon_array,ts_lat_array,SST_array = project_functions.get_SST(timestamp_datetime_array[0].item(),env_data_src,env_scenario)

# Data source-specific stuff
if (env_data_src=='HYCOM'):
    # Set custom levels for SST (degrees C)
    custom_SST_levels = np.linspace(8,29,num=22)
    # Get fullpath for the nearest (in time) HYCOM uv netcdf file
    uv_netcdf_fullpath = project_functions.get_HYCOM_UV_fullpath(timestamp_datetime_array[0].item())
    # Get data for  the sea-surface velocity quiver plot
    uv_lon_array,uv_lat_array,surface_u_array,surface_v_array = project_functions.get_uv_from_HYCOM_netcdf(uv_netcdf_fullpath)
else:
    # Set custom levels for SST (degrees F)
    #custom_SST_levels = 22
    custom_SST_levels = np.linspace(55,83,num=40)
#endif

# Plot track with overlays 
fig2, ax2 = plt.subplots()
line1, = ax2.plot(lon_array,lat_array,'-',color = 'gray',alpha=0.5)        # Track
line2, = ax2.plot(lon_array[0],lat_array[0],'ro-',markersize=7)  # Position along track
cont = ax2.contourf(ts_lon_array,ts_lat_array,SST_array,levels=custom_SST_levels,cmap=cm.jet)  # Contour SST
fig2.colorbar(cont)
if (env_data_src=='HYCOM'):
    quiver_plot = ax2.quiver(uv_lon_array, uv_lat_array, surface_u_array[0,:,:], surface_v_array[0,:,:], units='width') # Quiver u,v
#endif
ax2.set(xlim=[-75.0, -73.0],ylim=[35.25, 37.5])
# Set plot title
title_string = tag_id
plt.title(title_string)
# Labels 
plt.xlabel('Longitude')
plt.ylabel('Latitude')
# Update text
text_string = timestamp_datetime_array[0].item().strftime("%Y-%m-%d")
ax2.text(0.8,0.8,text_string)
# Show
plt.show()


#===========INTEGRATE ANIMAL TELEMETRY DATA WITH OCEANOGRAPHIC DATA AND ANIMATE==============
fig3, ax3 = plt.subplots()
camera = Camera(fig3)
for frame_num in range(len(timestamp_datetime_array)):
    # Plot the static track, 50% transparent
    line1, = ax3.plot(lon_array,lat_array,'-',color = 'gray',alpha=0.5)  
    ax3.set(xlim=[-75.0, -73.0],ylim=[35.25, 37.5])      
    # Update the position (red dot) along the track (line2)
    x = lon_array[frame_num-1:frame_num]
    y = lat_array[frame_num-1:frame_num]
    line2, = ax3.plot(x,y,'ro-',markersize=7)
    # Update SST contour
    
    # Get data for the SST plot
    # Note use of .item() to convert numpy datetime back to datetime.datetime
    ts_lon_array,ts_lat_array,SST_array = project_functions.get_SST(timestamp_datetime_array[frame_num].item(),env_data_src,env_scenario)
    
    # Contour plot of SST   
    cont = ax3.contourf(ts_lon_array,ts_lat_array,SST_array,levels=custom_SST_levels,cmap=cm.jet)
    #fig3.colorbar(cont) # Including this causes problems
    
    # Update quiver of u,v
    if (env_data_src=='HYCOM'):
        # Get fullpath for the nearest (in time) HYCOM uv netcdf file
        uv_netcdf_fullpath = project_functions.get_HYCOM_UV_fullpath(timestamp_datetime_array[frame_num].item())
        # Get data for  the sea-surface velocity quiver plot
        uv_lon_array,uv_lat_array,surface_u_array,surface_v_array = project_functions.get_uv_from_HYCOM_netcdf(uv_netcdf_fullpath)
        # Quiver plot
        quiver_plot = ax3.quiver(uv_lon_array, uv_lat_array, surface_u_array[0,:,:], surface_v_array[0,:,:], units='width') # Quiver u,v
    #endif
    
    # Update plot title
    title_string = 'Animal track for '+tag_id
    plt.title(title_string)
    # Update text
    text_string = timestamp_datetime_array[frame_num].item().strftime("%Y-%m-%d")
    plt.text(0.8,0.8,text_string)
    # Labels 
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    # Snap picture of this frame
    camera.snap()
#endfor
animation = camera.animate(interval=120)
mp4_filename = tag_id + '.mp4' 
animation.save(mp4_filename)  






