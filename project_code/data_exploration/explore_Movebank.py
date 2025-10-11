# -*- coding: utf-8 -*-
"""
Created on Thu Oct  9 16:24:43 2025

@author: s44ba

Explore shapefile downloaded from movebank.org
"""
# Imports
import fiona
from shapely.geometry import shape
import geopandas as gpd
import pandas as pd
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

# Specify fullpath to input shapefile
# i.e. shapefile downloaded from movebank.org
input_shp = 'C:/Users/s44ba/git/GIS6345/project_data/track_data/Short_finned_pilot_whales_CRC_NW_Atlantic/lines.shp'

# Explore with fiona
# Get info about shapefile contents i.e. schema, crs
with fiona.open(input_shp,"r") as my_shapefile:
    print(my_shapefile.crs)
    print(my_shapefile.schema)

    # Explore features
    for feature in my_shapefile:
        shapely_geometry = shape(feature['geometry'])
        #print(shapely_geometry)
    #endfor
#endwith

# Alternatively, load into geopandas (instead of fiona)
input_gdf = gpd.read_file(input_shp)

# Preview
print(input_gdf.head())

# Since shapefile does not contain timestamps, use csv instead, starting
# with a pandas dataframe

# Specify fullpath to csv
# i.e. csv downloaded from movebank.org
input_csv = 'C:/Users/s44ba/git/GIS6345/project_data/track_data/Short_finned_pilot_whales_CRC_NW_Atlantic.csv'
df = pd.read_csv(input_csv)
print(df.info())

# Fewer columns
df_subset = df[['event-id','timestamp','location-long','location-lat','individual-local-identifier']]

# Convert to datetime
# Add new column, derived timestamp_datetime, initialized to 1/1/1970
df_subset["timestamp_datetime"] = datetime(1970,1,1)
# Convert
format_string = "%Y-%m-%d %H:%M:%S.000"
for k in range(len(df_subset)):
    datetime_string = df_subset.loc[k,"timestamp"]
    df_subset.loc[k,"timestamp_datetime"] = datetime.strptime(datetime_string,format_string)
#endfor
print(df_subset.head())

# group by individual-local-identifier
grouped_series = df_subset.groupby('individual-local-identifier').describe()

# Print timestamp_datetime min, max
print(grouped_series['timestamp_datetime']['min'])
print(grouped_series['timestamp_datetime']['max'])

# Print location-lat min, max
print(grouped_series['location-lat']['min'])
print(grouped_series['location-lat']['max'])
  
# Print location-long min, max
print(grouped_series['location-long']['min'])
print(grouped_series['location-long']['max'])

# Is time of interest in data range of track?
datetime_of_interest = datetime(2016, 3, 15)
is_datetime_of_interest_in_range = (grouped_series['timestamp_datetime']['min']<datetime_of_interest)&(grouped_series['timestamp_datetime']['max']>datetime_of_interest)
print(grouped_series[is_datetime_of_interest_in_range])

# Two tags look good i.e. include 3/15/2016: GmTag137 and GmTag142
df_subset[df_subset['individual-local-identifier']=='GmTag137'].describe()
df_subset[df_subset['individual-local-identifier']=='GmTag142'].describe()

# Let's look at one of these tracks:
tag_id = 'GmTag142'
myTrack = df_subset[df_subset['individual-local-identifier']==tag_id]
df_lat = myTrack['location-lat']
df_lon = myTrack['location-long']
lat_array = np.array(df_lat)
lon_array = np.array(df_lon)

plt.plot(lon_array,lat_array)
    


    
    

    
    

