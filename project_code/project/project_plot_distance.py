# -*- coding: utf-8 -*-
"""
Created on Mon Oct 13 17:37:39 2025

@author: s44ba

For GIS6345 Project

This program calls functions in project_functions.py to calculate and plot the distance
of an animal from a reference location as a function of time

The animal tracks are from a specified file downloaded from movebank.org.

TO do:
    -Loop on tags

"""
# Imports
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.animation import FuncAnimation
import project_functions

#==============CREATE REFERENCE POINT AS PANDAS DATAFRAME===================================
ncroep_loc = {'location-long': [-75.106], 'location-lat': [35.1389]}
reference_loc = ncroep_loc
df_reference = pd.DataFrame(reference_loc)

#==============CONVERT REFERENCE POINT TO UTM===============================================
# Convert reference point to geopandas
# First, specify geometry
geometry = gpd.points_from_xy(df_reference['location-long'],df_reference['location-lat'])
gdf_reference = gpd.GeoDataFrame(df_reference,geometry=geometry,crs="EPSG:4326")

# Convert track to UTM zone 18
my_UTM_crs = "EPSG:32618"
gdf_reference_utm = gdf_reference.to_crs(my_UTM_crs)
print(gdf_reference_utm)

# Use this UTM point
ref_point_utm = Point(490343.697, 3888451.864)


#==============LOAD ANIMAL TELEMETRY DATA INTO PANDAS DATAFRAME==============================
# Specify fullpath to input csv file containing multiple animal tracks
# i.e. the csv downloaded from movebank.org and load it into a pandas DataFrame
track_csv_fullpath = 'C:/Users/s44ba/git/GIS6345/project_data/track_data/Short_finned_pilot_whales_CRC_NW_Atlantic.csv'

# Let's look at just one of the tracks. From data exploration, I found GmTag142 to be 
# interesting i.e. it went through my region of interest
tag_id = 'GmTag142'  # e.g. 'GmTag142' or 'GmTag137'

# Call function to get the individual track, as apndas dataframe
myTrack = project_functions.get_movebank_track_csv(track_csv_fullpath, tag_id)

# Subset myTrack in time
myTrack_in_time_window = myTrack['timestamp_datetime']<datetime(2021,1,6)   # boolean
myTrack_subset = myTrack[myTrack_in_time_window]

#==============CONVERT TRACK TO UTM================================================================
# Convert track to geopandas
# First, specify geometry
geometry = gpd.points_from_xy(myTrack_subset['location-long'],myTrack_subset['location-lat'])
gdf_myTrack = gpd.GeoDataFrame(myTrack_subset,geometry=geometry,crs="EPSG:4326")

# Convert track to UTM zone 18
my_UTM_crs = "EPSG:32618"
gdf_myTrack_utm = gdf_myTrack.to_crs(my_UTM_crs)


# ==============DISTANCE TO REFERENCE=========================================================
gdf_myTrack_utm['distance_to_reference'] = gdf_myTrack_utm.geometry.distance(ref_point_utm)


#===============CONVERT TO NUMPY ARRAYS AND PLOT==============================================
# Extract arrays
distance_km = gdf_myTrack_utm['distance_to_reference']/1000.0
df_timestamp_datetime = gdf_myTrack_utm['timestamp_datetime']

# Convert to numpy
distance_km_array = np.array(distance_km)
timestamp_datetime_array = np.array(df_timestamp_datetime)

# Plot distance
fig1, ax1 = plt.subplots()
ax1.plot(timestamp_datetime_array,distance_km_array)
plt.yscale('log')
