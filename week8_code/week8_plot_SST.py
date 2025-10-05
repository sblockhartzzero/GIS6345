# -*- coding: utf-8 -*-
"""
Created on Sun Sep 28 15:37:15 2025

@author: s44ba

# For GIS6345 Week 8
"""

# Imports
import week8_functions

# Fullpath to netCDF file
netcdf_folder= '../week8_data/'
netcdf_filename = 'hycom_glby_930_2019030712_t003_ts3z.nc'
netcdf_fullpath = netcdf_folder+netcdf_filename
print("netcdf_fullpath = ",netcdf_fullpath)

# Call function to plot sea surface temperature from this netCDF file
(lon_array,lat_array,SST_array) = week8_functions.plot_HYCOM_TS(netcdf_fullpath)



