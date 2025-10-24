# -*- coding: utf-8 -*-
"""
Created on Mon Oct 20 09:37:51 2025

@author: s44ba

For GIS6345 Project

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
frame_num = 8
    
# Specify desired timestamp_datetime_range
timestamp_datetime_range = [datetime(2015,1,day_num), datetime(2015,1,day_num+1)]

# Call function in project_functions module
lon_array, lat_array, SST_array = project_functions.get_SST_from_MUR_pkl(pkl_filename, timestamp_datetime_range)
    
# Verify
with rasterio.open('new_scaled_int.tif') as src:
    image_data = src.read(1)
    
    # Plot contour
    fig3, ax3 = plt.subplots()
    cont = ax3.contourf(lon_array,lat_array,image_data,levels=20,cmap=cm.jet)  # Contour SST
    fig3.colorbar(cont)
    plt.show()
    
    







  