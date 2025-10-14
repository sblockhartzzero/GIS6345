# -*- coding: utf-8 -*-
"""
Created on Sun Sep 28 15:37:15 2025

@author: s44ba

# For GIS6345 Project
"""

# Imports
import project_functions

# Fullpath to netCDF file
netcdf_folder= 'C:/Users/s44ba/git/GIS6345/project_data/env_data/CapeHatteras/hycom_TS_CapeHatteras/'
netcdf_filename = 'hycom_glby_930_2019030712_t003_ts3z.nc'
netcdf_fullpath = netcdf_folder+netcdf_filename
print("netcdf_fullpath = ",netcdf_fullpath)

# Call function to plot sea surface temperature from this netCDF file
project_functions.plot_HYCOM_TS(netcdf_fullpath)



