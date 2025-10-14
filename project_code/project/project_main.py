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
from celluloid import Camera
import project_functions

#==============LOAD DATA INTO PANDAS DATAFRAME========================
# Specify fullpath to input csv file containing multiple animal tracks
# i.e. the csv downloaded from movebank.org and load it into a pandas DataFrame
input_csv = 'C:/Users/s44ba/git/GIS6345/project_data/track_data/Short_finned_pilot_whales_CRC_NW_Atlantic.csv'
df = pd.read_csv(input_csv)

# We need only a few columns, so create a DataFrame containing only the columns
# that are needed
df_subset = df[['event-id','timestamp','location-long','location-lat','individual-local-identifier']]

# Add a new column (initialized to 1/1/1970) to convert the timestamp string to datetime
df_subset["timestamp_datetime"] = datetime(1970,1,1)
format_string = "%Y-%m-%d %H:%M:%S.000"
for k in range(len(df_subset)):
    datetime_string = df_subset.loc[k,"timestamp"]
    df_subset.loc[k,"timestamp_datetime"] = datetime.strptime(datetime_string,format_string)
#endfor
print(df_subset.head())

# Let's look at just one of the tracks. From data exploration, I found GmTag142 to be 
# interesting i.e. it went through my region of interest
tag_id = 'GmTag142'
myTrack = df_subset[df_subset['individual-local-identifier']==tag_id]

# Subset in time
myTrack_in_time_window = myTrack['timestamp_datetime']<datetime(2016,1,1)   # boolean
myTrack_subset = myTrack[myTrack_in_time_window]

#===============CONVERT TO NUMPY ARRAYS=====================
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

#============SAMPLE PLOTS===========
# Plot just the track
fig1, ax1 = plt.subplots()
ax1.plot(lon_array,lat_array)

# Plot track with overlays of oceanographic data
# Get fullpath for the nearest (in time) HYCOM TS netcdf file
ts_netcdf_fullpath = project_functions.get_HYCOM_TS_fullpath(timestamp_datetime_array[0]) 
# Get data for sea-surface temperature (SST) contour plot
ts_lon_array,ts_lat_array,SST_array = project_functions.get_SST_from_HYCOM_netcdf(ts_netcdf_fullpath)
# Get fullpath for the nearest (in time) HYCOM uv netcdf file
uv_netcdf_fullpath = project_functions.get_HYCOM_UV_fullpath(timestamp_datetime_array[0])
# Get data for  the sea-surface velocity quiver plot
uv_lon_array,uv_lat_array,surface_u_array,surface_v_array = project_functions.get_uv_from_HYCOM_netcdf(uv_netcdf_fullpath)
# Plot track with overlays 
fig2, ax2 = plt.subplots()
line1, = ax2.plot(lon_array,lat_array,'-',color = 'gray')        # Track
line2, = ax2.plot(lon_array[0],lat_array[0],'ro-',markersize=7)  # Position along track
cont = ax2.contourf(ts_lon_array,ts_lat_array,SST_array[0,:,:],levels=15,cmap=cm.PuBu_r)  # Contour SST
quiver_plot = ax2.quiver(uv_lon_array, uv_lat_array, surface_u_array[0,:,:], surface_v_array[0,:,:], units='width') # Quiver u,v
ax2.set(xlim=[-75.0, -73.0],ylim=[35.25, 37.5])
plt.show()

#===========ANIMATE USING CELLULOID==============================
fig3, ax3 = plt.subplots()
camera = Camera(fig3)
for frame_num in range(len(timestamp_datetime_array)):
    # Track (static)
    line1, = ax3.plot(lon_array,lat_array,'-',color = 'gray')  
    ax3.set(xlim=[-75.0, -73.0],ylim=[35.25, 38.0])      
    # Update the position along the track (line2)
    x = lon_array[frame_num-1:frame_num]
    y = lat_array[frame_num-1:frame_num]
    line2, = ax3.plot(x,y,'ro-',markersize=7)
    # Update SST contour
    # Get fullpath for the nearest (in time) HYCOM TS netcdf file
    ts_netcdf_fullpath = project_functions.get_HYCOM_TS_fullpath(timestamp_datetime_array[frame_num]) 
    # Get data for sea-surface temperature (SST) contour plot
    ts_lon_array,ts_lat_array,SST_array = project_functions.get_SST_from_HYCOM_netcdf(ts_netcdf_fullpath)
    # Contour plot of SST
    cont = ax3.contourf(ts_lon_array,ts_lat_array,SST_array[0,:,:],levels=15,cmap=cm.PuBu_r)
    # Update quiver of u,v
    # Get fullpath for the nearest (in time) HYCOM uv netcdf file
    uv_netcdf_fullpath = project_functions.get_HYCOM_UV_fullpath(timestamp_datetime_array[frame_num])
    # Get data for  the sea-surface velocity quiver plot
    uv_lon_array,uv_lat_array,surface_u_array,surface_v_array = project_functions.get_uv_from_HYCOM_netcdf(uv_netcdf_fullpath)
    # Quiver plot
    quiver_plot = ax3.quiver(uv_lon_array, uv_lat_array, surface_u_array[0,:,:], surface_v_array[0,:,:], units='width') # Quiver u,v
    # Snap picture of this frame
    camera.snap()
#endfor
animation = camera.animate(interval=120)
mp4_filename = tag_id + '.mp4' 
animation.save(mp4_filename)   

    
"""
Attempt at animation using Matplotlib animation
It worked fine for line plot but ran into issues with contour plot
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
"""





