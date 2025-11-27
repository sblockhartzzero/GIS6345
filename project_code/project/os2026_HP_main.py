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

The HP is for high-pass filter of the SST data...but, instead of using the HP-filtered SST image,
I decided to use a temperature range to define the western boundary of the Gulf Stream in winter

To  do:
    -Support for OS2026_3
    -Save min distance plus save as time series (i.e. with timestamp)--perhaps as a mat file?
    -Use longer scenarios, corresponding to the time series in the poster
"""
# Imports
import pandas as pd
from datetime import datetime, timedelta
import geopandas as gpd
from shapely.geometry import Point
import numpy as np
import math
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
# Could be 'GIS6345' or 'OS2026_1' to 'OS2026_4'
env_scenario = 'OS2026_1'

# Specify scenario (which defines time frame as well as input data file)
match env_scenario:
    case 'OS2026_1':
        start_datetime = datetime(2015,2,15)  
        num_days = 40
    case 'OS2026_2':
        start_datetime = datetime(2016,2,15)  
        num_days = 40
    case 'OS2026_3':
        start_datetime = datetime(2018,2,15)  
        num_days = 40        
#endmatch

# Specify temperature range in F (to define the western edge of Gulf Stream)
temperature_F_range = [64.5,65.5]

# Specify UTM zone (for conversion to UTM)
my_UTM_crs = "EPSG:32618"

# Specify reference point in UTM (from project_plot_distance.py)
ref_point_utm = Point(490343.697, 3888451.864)


#====================MUR SST PICKLE FILE====================================================
pkl_filename = project_functions.get_MUR_pickle_filename(env_scenario) 


#===========CREATE ARRAY OF DATETIMES========================================================
timestamp_datetime_array = [start_datetime + timedelta(days=x) for x in range(num_days)]


#===========TEST CALL============================================================================
# Get timestamp_datetime_range for this day
timestamp_datetime_range = project_functions.get_datetime_range_for_the_day(timestamp_datetime_array[0])
# Call to get points in range for this pickle file, this timestamp
df_points_in_T_range = os2026_functions.points_in_T_range(pkl_filename, timestamp_datetime_range, temperature_F_range)
# Unpack
lon = df_points_in_T_range['longitude']
lat = df_points_in_T_range['latitude']
# Convert to numpy
lat_array = np.array(lat)
lon_array = np.array(lon)

# Convert track to geopandas
# First, specify geometry
geometry = gpd.points_from_xy(df_points_in_T_range['longitude'],df_points_in_T_range['latitude'])
gdf_boundary = gpd.GeoDataFrame(df_points_in_T_range,geometry=geometry,crs="EPSG:4326")
#print(gdf_boundary.geometry.iloc[7])

# Convert track to UTM zone 18
gdf_boundary_utm = gdf_boundary.to_crs(my_UTM_crs)

# Distance and bearing (in degrees ccw from N) to reference point
gdf_boundary_utm['distance_to_reference'] = gdf_boundary_utm.geometry.distance(ref_point_utm)
#print(gdf_boundary_utm.geometry.iloc[7])

# Extract arrays
distance_km = gdf_boundary_utm['distance_to_reference']/1000.0
min_distance_km = distance_km.min()
min_distance_km_index_val = distance_km.idxmin()
print("Min distance (in km) = ",min_distance_km)

# Bearing between points i.e. between boundary (closest approach) and reference point
boundary_point_utm = gdf_boundary_utm.geometry.loc[min_distance_km_index_val]
delta_y = ref_point_utm.y - boundary_point_utm.y
delta_x = ref_point_utm.x - boundary_point_utm.x
bearing = (180/np.pi)*math.atan2(delta_y, delta_x)
print("bearing = ",bearing)

# Plot
gdf_boundary_utm.plot()
plt.show()


#===========LOOP ON MUR SST DAYS==================================================
# Init
num_frames = len(timestamp_datetime_array)
distance_to_boundary_km = np.zeros(num_frames)
bearing_to_boundary_degrees = np.zeros(num_frames)
fig3, ax3 = plt.subplots()
camera = Camera(fig3)
for frame_num in range(num_frames):  
    #ax3.set(xlim=[-76.0, -73.0],ylim=[34.25, 37.5])      
    # Update SST boundary
    # Get timestamp_datetime_range for this day
    timestamp_datetime_range = project_functions.get_datetime_range_for_the_day(timestamp_datetime_array[frame_num])
    # Call to get points in range for this pickle file, this timestamp
    df_points_in_T_range = os2026_functions.points_in_T_range(pkl_filename, timestamp_datetime_range, temperature_F_range)
    # Unpack
    lon = df_points_in_T_range['longitude']
    lat = df_points_in_T_range['latitude']
    # Convert to numpy
    lat_array = np.array(lat)
    lon_array = np.array(lon)
    
    # Plot points in T range
    line3, = ax3.plot(lon_array,lat_array,'ro',markersize=7)
    
    # Update plot title
    title_string = env_scenario
    plt.title(title_string)
    
    # Labels 
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    # Snap picture of this frame
    camera.snap()
    
    # Calc min distance to front
    # Convert track to geopandas
    # First, specify geometry
    geometry = gpd.points_from_xy(df_points_in_T_range['longitude'],df_points_in_T_range['latitude'])
    gdf_boundary = gpd.GeoDataFrame(df_points_in_T_range,geometry=geometry,crs="EPSG:4326")

    # Convert track to UTM zone 18
    gdf_boundary_utm = gdf_boundary.to_crs(my_UTM_crs)

    # Distance to reference point
    gdf_boundary_utm['distance_to_reference'] = gdf_boundary_utm.geometry.distance(ref_point_utm)

    # Extract arrays and get min distance 
    distance_km = gdf_boundary_utm['distance_to_reference']/1000.0
    min_distance_km = distance_km.min()
    min_distance_km_index_val = distance_km.idxmin()
    
    # Bearing between points i.e. between boundary (closest approach) and reference point
    boundary_point_utm = gdf_boundary_utm.geometry.loc[min_distance_km_index_val]
    delta_y = ref_point_utm.y - boundary_point_utm.y
    delta_x = ref_point_utm.x - boundary_point_utm.x
    bearing = (180/np.pi)*math.atan2(delta_y, delta_x)
    
    # Save
    distance_to_boundary_km[frame_num] = min_distance_km
    bearing_to_boundary_degrees[frame_num] = bearing
    
#endfor
animation = camera.animate(interval=120)
mp4_filename = env_scenario + '_HP.mp4' 
animation.save(mp4_filename) 

# Plot distance_to_boundary_km
fig4, ax4 = plt.subplots()
ax4.plot(distance_to_boundary_km)
plt.show()
fig5, ax5 = plt.subplots()
ax5.plot(bearing_to_boundary_degrees)
plt.show()
print(distance_to_boundary_km)
 






