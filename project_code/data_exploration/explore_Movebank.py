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



    
    

    
    

