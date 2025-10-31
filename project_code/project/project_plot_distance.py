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
import project_functions

#==============CREATE REFERENCE POINT AS PANDAS DATAFRAME===================================
ncroep_loc = {'location-long': [-75.106], 'location-lat': [35.1389]}
adeon_loc = {'location-long': [-75.0204167], 'location-lat': [35.1997833]}
reference_loc = adeon_loc
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

# Specify date range
#min_datetime = datetime(2014,6,1)
#max_datetime = datetime(2015,4,1)
#min_datetime = datetime(2015,10,1)
#max_datetime = datetime(2015,11,1)
min_datetime = datetime(2018,1,1)
max_datetime = datetime(2020,4,1)

#==============LOAD ANIMAL TELEMETRY DATA INTO PANDAS DATAFRAME==============================
# Specify fullpath to input csv file containing multiple animal tracks
# i.e. the csv downloaded from movebank.org and load it into a pandas DataFrame
track_csv_fullpath = 'C:/Users/s44ba/git/GIS6345/project_data/track_data/Short_finned_pilot_whales_CRC_NW_Atlantic.csv'

# Convert from csv to pandas dataframe, enriching with datetime
df_movebank_tracks = project_functions.get_movebank_tracks_from_csv(track_csv_fullpath)

# Get unique list of tag_ids
unique_tag_ids = df_movebank_tracks['individual-local-identifier'].unique()

# Let's look at just one of the tracks. From data exploration, I found GmTag142 to be 
# interesting i.e. it went through my region of interest
#tag_id = 'GmTag142'  # e.g. 'GmTag142' or 'GmTag137'

# Init
fig1, ax1 = plt.subplots()
# Loop on tag_ids
for tag_id in unique_tag_ids:
    # Get the individual track, as pandas dataframe
    print(tag_id)
    myTrack = df_movebank_tracks[df_movebank_tracks['individual-local-identifier']==tag_id]

    # Subset myTrack in time
    myTrack_in_time_window = (myTrack['timestamp_datetime']>min_datetime) & (myTrack['timestamp_datetime']<=max_datetime)   # boolean
    myTrack_subset = myTrack[myTrack_in_time_window]
        
    # Convert track to geopandas
    # First, specify geometry
    geometry = gpd.points_from_xy(myTrack_subset['location-long'],myTrack_subset['location-lat'])
    gdf_myTrack = gpd.GeoDataFrame(myTrack_subset,geometry=geometry,crs="EPSG:4326")

    # Convert track to UTM zone 18
    my_UTM_crs = "EPSG:32618"
    gdf_myTrack_utm = gdf_myTrack.to_crs(my_UTM_crs)

    # Distance to reference point
    gdf_myTrack_utm['distance_to_reference'] = gdf_myTrack_utm.geometry.distance(ref_point_utm)

    # Extract arrays
    distance_km = gdf_myTrack_utm['distance_to_reference']/1000.0
    df_timestamp_datetime = gdf_myTrack_utm['timestamp_datetime']
    
    # Convert to numpy
    distance_km_array = np.array(distance_km)
    timestamp_datetime_array = np.array(df_timestamp_datetime)

    # Plot distance
    ax1.plot(timestamp_datetime_array,distance_km_array)
    plt.yscale('log')
#endfor    
