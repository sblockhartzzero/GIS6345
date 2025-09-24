# -*- coding: utf-8 -*-
"""
Spyder Editor

For GIS6345 Assignment 5, Part 2
"""
# To do:
# Multiple plots, labeled
    
# Imports
import xarray as xr
import pandas as pd
import geopandas as gpd
#import netcdf4
import matplotlib.pyplot as plt

# Fullpath to netCDF file
netcdf_folder= 'C:/Users/s44ba/Documents/Training/Northeastern/GeospatialProgramming/Project/project_deliverables/project_data/'
netcdf_filename = 'atn_85568_short-finned-pilot-whale_trajectory_20080705-20080802.nc'
netcdf_fullpath = netcdf_folder+netcdf_filename
print("netcdf_fullpath = ",netcdf_fullpath)

# Open netcdf file
ds_loaded = xr.open_dataset(netcdf_fullpath)
print(ds_loaded)

# Unpack
sample_datetime = ds_loaded.time
depth = ds_loaded.z
lon = ds_loaded.lon
lat = ds_loaded.lat

# Preliminary plots
#plt.plot(depth)
#plt.plot(lon,lat)

# Create a pandas DataFrame from the data extracted from netcdf by xarray
# Add columns for:
#    Distance_btwn_points, 
#    Time_btwn_pts,
#    Speed
# (all initialized to 0)
df = pd.DataFrame({
    'Sample_datetime': sample_datetime,
    'Longitude': lon,
    'Latitude': lat,
    'Distance_btwn_points': 0*lon,
    'Time_btwn_points': 0*lon,
    'Speed': 0*lon})
print("pandas df.info() = ",df.info())

# Create a geopandas GeoDataFrame from the pandas DataFrame
# The coordinate reference system is WGS84 i.e. crs='EPSG:4326'
df_geo = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude, z=None, crs='EPSG:4326'))
print("geopandas df_geo.info() = ",df_geo.info())

# Calculate Distance_btwn_points,Time_btwn_points, Speed
num_pts = len(lon)
for k in range(num_pts-1):
    # Two consecutive points (pt1,pt2) along track 
    pt1 = df_geo.loc[k, 'geometry']
    pt2 = df_geo.loc[k+1, 'geometry']
    # Distance between pt1 and pt2
    # My understanding is that the distance is in meters
    distance = pt1.distance(pt2)
    df_geo.loc[k,'Distance_btwn_points'] = distance
    # Time between points
    t1 = df_geo.loc[k, 'Sample_datetime']
    t2 = df_geo.loc[k+1, 'Sample_datetime']
    delta_t_secs = (t2 - t1).seconds
    df_geo.loc[k,'Time_btwn_points'] = delta_t_secs
    # Speed in m/s
    if (delta_t_secs>0):
        df_geo.loc[k,'Speed'] = distance/delta_t_secs
    #endif    
#endfor

# Plot Speed
plt.plot(df_geo.Speed)    
    
    






