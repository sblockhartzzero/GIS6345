# -*- coding: utf-8 -*-
"""
Spyder Editor

For GIS6345 Project

Assumption: the input netCDF files (from HYCOM) are for a single sample time
"""
# To do:
# Multiple plots, labeled
    
# Imports
import xarray as xr
import pandas as pd
import geopandas as gpd
import netCDF4
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

def get_SST_from_HYCOM_TS(netcdf_fullpath):
    # Open netcdf file
    ds_loaded = netCDF4.Dataset(netcdf_fullpath)
    print(ds_loaded.variables.keys())
    
    # Unpack
    lon = ds_loaded.variables['lon'][:]
    lat = ds_loaded.variables['lat'][:]
    depth = ds_loaded.variables['depth'][:]
    water_temp = ds_loaded.variables['water_temp'][:,:,:,:]  # [t,depth,lat,lon]
    
    # Convert to numpy arrays
    lat_array = np.array(lat)
    lon_array = np.array(lon)
    T_array = np.array(water_temp)   #[depth,lat,lon]
    
    # Use only the surface temperature (i.e. depth index 0)
    SST_array = T_array[0,:,:]   # [lat,lon]
    print("Shape of SST_array is ",np.shape(SST_array))
    
    # Return
    return lon_array,lat_array,SST_array
    
def get_uv_from_HYCOM_UV(netcdf_fullpath):
    # Open netcdf file
    ds_loaded = netCDF4.Dataset(netcdf_fullpath)
    print(ds_loaded.variables.keys())
    
    # Unpack
    lon = ds_loaded.variables['lon'][:]
    lat = ds_loaded.variables['lat'][:]
    depth = ds_loaded.variables['depth'][:]
    water_u = ds_loaded.variables['water_u'][:,:,:,:]  # [t,depth,lat,lon]
    water_v = ds_loaded.variables['water_v'][:,:,:,:]  # [t,depth,lat,lon]
    
    # Convert to numpy arrays
    lat_array = np.array(lat)
    lon_array = np.array(lon)
    water_u_array = np.array(water_u)   #[depth,lat,lon]
    water_v_array = np.array(water_v)   #[depth,lat,lon]
    
    # Use only the surface velocity (i.e. depth index 0)
    surface_u_array = water_u_array[0,:,:]   # [lat,lon]
    print("Shape of surface_u_array is ",np.shape(surface_u_array))
    surface_v_array = water_v_array[0,:,:]   # [lat,lon]
    print("Shape of surface_v_array is ",np.shape(surface_v_array))
    
    # Return
    return lon_array,lat_array,surface_u_array,surface_v_array
    
    
def plot_HYCOM_TS(netcdf_fullpath):
    
    # Call get_SST_from_HYCOM_TS
    lon_array,lat_array,SST_array = get_SST_from_HYCOM_TS(netcdf_fullpath)
    
    # Plot
    fig, ax = plt.subplots()
    cs = ax.contourf(lon_array,lat_array,SST_array[0,:,:],levels=15,cmap=cm.PuBu_r)
    cbar = fig.colorbar(cs)
    plt.show()

    return lon_array,lat_array,SST_array
  

def plot_HYCOM_UV(netcdf_fullpath):
    
    # Call get_uv_from_HYCOM_UV
    lon_array,lat_array,surface_u_array,surface_v_array = get_uv_from_HYCOM_UV(netcdf_fullpath)
    
    # Plot
    fig1, ax1 = plt.subplots()
    ax1.set_title('Arrows scale with plot width, not view')
    Q = ax1.quiver(lon_array, lat_array, surface_u_array[0,:,:], surface_v_array[0,:,:], units='width')
    qk = ax1.quiverkey(Q, 0.9, 0.9, 2, r'$2 \frac{m}{s}$', labelpos='E',
                   coordinates='figure')

    return lon_array,lat_array,surface_u_array,surface_v_array  


def plot_HYCOM_TS_and_UV(ts_netcdf_fullpath, uv_netcdf_fullpath):
    
    # Call get_SST_from_HYCOM_TS
    ts_lon_array,ts_lat_array,SST_array = get_SST_from_HYCOM_TS(ts_netcdf_fullpath)
    
    # Call get_uv_from_HYCOM_UV
    uv_lon_array,uv_lat_array,surface_u_array,surface_v_array = get_uv_from_HYCOM_UV(uv_netcdf_fullpath)
    
    # Plot with overlay
    # Plot
    fig, ax = plt.subplots()
    ax.set_title('SST and surface velocity')
    # countorf of SST
    cs = ax.contourf(ts_lon_array,ts_lat_array,SST_array[0,:,:],levels=12,cmap=cm.PuBu_r)
    cbar = fig.colorbar(cs)
    # quiver of surface velocity vectors
    Q = ax.quiver(uv_lon_array, uv_lat_array, surface_u_array[0,:,:], surface_v_array[0,:,:], units='width')
    qk = ax.quiverkey(Q, 0.9, 0.9, 2, r'$2 \frac{m}{s}$', labelpos='E',
                   coordinates='figure')
    plt.show()
    
    






