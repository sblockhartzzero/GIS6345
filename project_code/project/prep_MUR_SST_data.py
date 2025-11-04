# -*- coding: utf-8 -*-
"""
Created on Mon Oct 20 09:37:51 2025

@author: s44ba

For GIS6345 Project

From the MUR SST csv file, create a set of geotiff  files (one per day) for a 
specified date range. This demonstrates conversion from csv to pandas dataframe
to numpy array to geotiff (the last step using rasterio)

To do:
    -Set to time window that matches animal tracks e.g. 10/20/2015-01/06/2016
"""

# Imports
import pandas as pd
from datetime import datetime
import numpy as np
import rasterio
import matplotlib.pyplot as plt
from matplotlib import cm
import project_functions

# Specify csv file for MUR SST
csv_folder = 'C:\\Users\\s44ba\\git\\GIS6345\\project_data\\env_data\\CapeHatteras\\MUR_SST_CapeHatteras\\'
csv_filename = 'jplMURSST41F_de75_def0_78ea.csv';
csv_fullpath = csv_folder + csv_filename

# Specify pickled file
pkl_filename = 'df_short.pkl'

# Convert csv to pandas dataframe and save to pickle file for subsequent runs
#project_functions.pickle_from_MUR_csv(csv_fullpath,pkl_filename)

# Loop over days
day_num = 1
for frame_num in range(9):
    
    print(frame_num)
    
    # Specify desired timestamp_datetime_range
    timestamp_datetime_range = [datetime(2015,1,day_num), datetime(2015,1,day_num+1)]
    
    # Call function in project_functions module
    lon_array, lat_array, SST_array = project_functions.get_SST_from_MUR_pkl(pkl_filename, timestamp_datetime_range)
    
    # Plot contour
    fig2, ax2 = plt.subplots()
    cont = ax2.contourf(lon_array,lat_array,SST_array,levels=20,cmap=cm.jet)  # Contour SST
    fig2.colorbar(cont)
    plt.show()
    
    # Create transform, using (x,y) of upper left corner and (res_x,res_y). 
    # Note res_y is negative for north up
    min_lon = np.min(lon_array)
    max_lat = np.max(lat_array)
    this_transform = rasterio.transform.from_origin(min_lon,max_lat,0.01,-0.01)
    
    # Scale to 0-65536 (from standard SST Fahrenheit range of 40-80)
    min_SST_val = np.min(SST_array)
    max_SST_val = np.max(SST_array)
    new_min_val = 40
    new_max_val = 80
    standard_SST_range_F = new_max_val-new_min_val   # range of temperature from min to max in Farenheit
    new_dynamic_range = 2**16   # full-scale range of integer values per pixel
    scale_factor = new_dynamic_range/standard_SST_range_F
    SST_array_scaled = ((SST_array-new_min_val)*scale_factor)
    SST_array_scaled_int = SST_array_scaled.astype(np.uint16)
    print("Min SST_array_scaled_int =", np.min(SST_array_scaled_int))
    print("Max SST_array_scaled_int =", np.max(SST_array_scaled_int))
       
    # Export as geotiff i.e. convert to raster using  rasterio
    # Following example at https://rasterio.readthedocs.io/en/stable/quickstart.html
    # with different transform, different crs
    # Create raster dataset
    new_dataset = rasterio.open(
    'new_scaled_int.tif',
    'w',
    driver='GTiff',
    height=SST_array_scaled_int.shape[0],
    width=SST_array_scaled_int.shape[1],
    count=1,
    dtype=SST_array_scaled_int.dtype,
    crs=rasterio.crs.CRS.from_epsg(4326),
    transform=this_transform,
    )
    
    # Save raster dataset
    new_dataset.write(SST_array_scaled_int, 1)
    
    # Close raster dataset
    new_dataset.close()
    
    # Increment day for next iteration
    day_num = day_num + 1
    
#endfor    



    







  