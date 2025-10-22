# -*- coding: utf-8 -*-
"""
Created on Mon Oct 20 09:37:51 2025

@author: s44ba

For GIS6345 Project

From the MUR SST csv file, create a set of geotiff  files (one per day) for a 
specified date range. This demonstrates conversion from csv to pandas dataframe
to numpy array to geotiff (the last step using rasterio)

To do:
    -Convert to geotiff
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
csv_filename = 'jplMURSST41F_960e_f25d_3a04.csv';
csv_fullpath = csv_folder + csv_filename

# Specify pickled file
pkl_filename = 'df_short.pkl'

# Loop over days
day_num = 1
for frame_num in range(9):
    
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
    
    # Export as geotiff i.e. convert to raster using  rasterio
    # Following example at https://rasterio.readthedocs.io/en/stable/quickstart.html
    # with different transform, different crs
    # Create raster dataset
    new_dataset = rasterio.open(
    'new.tif',
    'w',
    driver='GTiff',
    height=SST_array.shape[0],
    width=SST_array.shape[1],
    count=1,
    dtype=SST_array.dtype,
    crs=rasterio.crs.CRS.from_epsg(4326),
    transform=this_transform,
    )
    
    # Save raster dataset
    new_dataset.write(SST_array, 1)
    
    # Close raster dataset
    new_dataset.close()
    
    # Increment day for next iteration
    day_num = day_num + 1
    
#endfor    
    







  