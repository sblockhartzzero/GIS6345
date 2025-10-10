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
    
    

    
    

