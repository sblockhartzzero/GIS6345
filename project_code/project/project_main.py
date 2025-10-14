# -*- coding: utf-8 -*-
"""
Created on Mon Oct 13 17:37:39 2025

@author: s44ba

This is the main program for my GIS6345 project. 
It calls functions in project_functions.py to animate an animal track,
overlaying time-varying oceanographic data i.e. surface temperature and 
velocity,indicating the location of the Gulf Stream.

To do:
    -Replace hard-coded netcdf fullpaths with call to get fullpath of nearest (in time)
     HYCOM netcdf file
"""
# Imports
import pandas as pd
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.animation import FuncAnimation
import project_functions

# Specify fullpath to input csv file containing multiple animal tracks
# i.e. the csv downloaded from movebank.org
# and load it into a pandas DataFrame
input_csv = 'C:/Users/s44ba/git/GIS6345/project_data/track_data/Short_finned_pilot_whales_CRC_NW_Atlantic.csv'
df = pd.read_csv(input_csv)

# We need only a few columns, so create a DataFrame containing only the columns
# that are needed
# Fewer columns
df_subset = df[['event-id','timestamp','location-long','location-lat','individual-local-identifier']]

# Add a new column (initialized to 1/1/1970) to convert the timestamp string to datetime
df_subset["timestamp_datetime"] = datetime(1970,1,1)
format_string = "%Y-%m-%d %H:%M:%S.000"
for k in range(len(df_subset)):
    datetime_string = df_subset.loc[k,"timestamp"]
    df_subset.loc[k,"timestamp_datetime"] = datetime.strptime(datetime_string,format_string)
#endfor
print(df_subset.head())

# Let's look at just one of the tracks
# From data exploration, I found GmTag142 to be interesting i.e. it went through
# my region of interest
tag_id = 'GmTag142'
myTrack = df_subset[df_subset['individual-local-identifier']==tag_id]

# Subset in time
myTrack_in_time_window = myTrack['timestamp_datetime']<datetime(2016,1,1)   # boolean
myTrack_subset = myTrack[myTrack_in_time_window]

# Extract arrays 
df_lat = myTrack_subset['location-lat']
df_lon = myTrack_subset['location-long']
df_timestamp_datetime = myTrack_subset['timestamp_datetime']

# Convert to numpy
lat_array = np.array(df_lat)
lon_array = np.array(df_lon)
timestamp_datetime_array = np.array(df_timestamp_datetime)

# Plot just the track
fig1, ax1 = plt.subplots()
ax1.plot(lon_array,lat_array)

# print min and max timestamp during this period
print("Time from ",df_timestamp_datetime.min()," to ",df_timestamp_datetime.max())

# Animate track, saving mp4 to a file
# First, initialize the data for the initial plot
# Fullpath to ts netCDF file
ts_netcdf_folder= 'C:/Users/s44ba/git/GIS6345/project_data/env_data/CapeHatteras/hycom_TS_CapeHatteras/'
ts_netcdf_filename = 'hycom_glby_930_2019030712_t003_ts3z.nc'
ts_netcdf_fullpath = ts_netcdf_folder+ts_netcdf_filename 
# Update the sea-surface temperature (SST) contour plot
ts_lon_array,ts_lat_array,SST_array = project_functions.get_SST_from_HYCOM_TS(ts_netcdf_fullpath)

# The sea-surface velocity quiver plot (???)
# Get fullpath for the nearest (in time) HYCOM TS netcdf file
# Fudge for now
# Fullpath to uv netCDF file
uv_netcdf_folder= 'C:/Users/s44ba/git/GIS6345/project_data/env_data/CapeHatteras/hycom_UV_CapeHatteras/'
uv_netcdf_filename = 'hycom_glby_930_2019030712_t003_uv3z.nc'
uv_netcdf_fullpath = uv_netcdf_folder+uv_netcdf_filename
# Update the sea-surface velocity quiver plot
uv_lon_array,uv_lat_array,surface_u_array,surface_v_array = project_functions.get_uv_from_HYCOM_UV(uv_netcdf_fullpath)

# Then, initialize the plot
fig2, ax2 = plt.subplots()
line1, = ax2.plot(lon_array,lat_array,'-',color = 'gray')  # Initialize plot
line2, = ax2.plot(lon_array[0],lat_array[0],'ro-',markersize=7)  # Initialize plot
cont = ax2.contourf(ts_lon_array,ts_lat_array,SST_array[0,:,:],levels=15,cmap=cm.PuBu_r)
quiver_plot = ax2.quiver(uv_lon_array, uv_lat_array, surface_u_array[0,:,:], surface_v_array[0,:,:], units='width')
ax2.set(xlim=[-75.0, -73.0],ylim=[35.25, 38.0])
plt.show()
    

# Function for updating plots in the animation
def update(frame_num):
    # For a given frame, update the plot (line2) of the track as well as the overlays of 
    # oceanographic data (???) and (???)
  
    # The position along the track (line2)
    x = lon_array[frame_num-1:frame_num]
    y = lat_array[frame_num-1:frame_num]
    line2.set_data(x,y)
    
    # The sea-surface temperature (SST) contour plot (???)
    # Get fullpath for the nearest (in time) HYCOM TS netcdf file
    # Fudge for now
    # Fullpath to ts netCDF file
    ts_netcdf_folder= 'C:/Users/s44ba/git/GIS6345/project_data/env_data/CapeHatteras/hycom_TS_CapeHatteras/'
    ts_netcdf_filename = 'hycom_glby_930_2019030712_t003_ts3z.nc'
    ts_netcdf_fullpath = ts_netcdf_folder+ts_netcdf_filename 
    # Update the sea-surface temperature (SST) contour plot
    ts_lon_array,ts_lat_array,SST_array = project_functions.get_SST_from_HYCOM_TS(ts_netcdf_fullpath)
     
    # The sea-surface velocity quiver plot (???)
    # Get fullpath for the nearest (in time) HYCOM TS netcdf file
    # Fudge for now
    # Fullpath to uv netCDF file
    uv_netcdf_folder= 'C:/Users/s44ba/git/GIS6345/project_data/env_data/CapeHatteras/hycom_UV_CapeHatteras/'
    uv_netcdf_filename = 'hycom_glby_930_2019030712_t003_uv3z.nc'
    uv_netcdf_fullpath = uv_netcdf_folder+uv_netcdf_filename
    # Update the sea-surface velocity quiver plot
    uv_lon_array,uv_lat_array,surface_u_array,surface_v_array = project_functions.get_uv_from_HYCOM_UV(uv_netcdf_fullpath)
    
    # Remove previous contourf and quiver plot
    for collection in ax2.collections:
        collection.remove()
    #endfor
    #  Create new contour plot    
    cont = ax2.contourf(ts_lon_array,ts_lat_array,SST_array[0,:,:],levels=15,cmap=cm.PuBu_r) 
    # Create new quiver plot
    quiver_plot = ax1.quiver(uv_lon_array, uv_lat_array, surface_u_array[0,:,:], surface_v_array[0,:,:], units='width')
     
    # Return vars
    return line2, quiver_plot, cont 

# Call to animate, where interval is the milliseconds (msec) between frames    
ani = FuncAnimation(fig=fig2, func=update, frames=400, interval=120, blit=False)
mp4_filename = tag_id + '.mp4'
ani.save(mp4_filename)
plt.show()




