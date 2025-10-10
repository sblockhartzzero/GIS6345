# -*- coding: utf-8 -*-
"""
Created on Fri Oct 10 10:46:31 2025

@author: s44ba

Plot SST and surface velocity as overlay
"""

# Imports
import project_functions

# Fullpath to ts netCDF file
ts_netcdf_folder= 'C:/Users/s44ba/git/GIS6345/project_data/env_data/CapeHatteras/hycom_TS_CapeHatteras/'
ts_netcdf_filename = 'hycom_glby_930_2019030712_t003_ts3z.nc'
ts_netcdf_fullpath = ts_netcdf_folder+ts_netcdf_filename
print("ts_netcdf_fullpath = ",ts_netcdf_fullpath)

# Fullpath to uv netCDF file
uv_netcdf_folder= 'C:/Users/s44ba/git/GIS6345/project_data/env_data/CapeHatteras/hycom_UV_CapeHatteras/'
uv_netcdf_filename = 'hycom_glby_930_2019030712_t003_uv3z.nc'
uv_netcdf_fullpath = uv_netcdf_folder+uv_netcdf_filename
print("uv_netcdf_fullpath = ",uv_netcdf_fullpath)

# Call function to plot sea surface temperature overlayed with surface velocity
project_functions.plot_HYCOM_TS_and_UV(ts_netcdf_fullpath, uv_netcdf_fullpath)