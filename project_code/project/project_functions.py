# -*- coding: utf-8 -*-
"""
Spyder Editor

For GIS6345 Project

"""
# To do:
# Multiple plots, labeled
    
# Imports
import xarray as xr
import pandas as pd
from datetime import datetime
import netCDF4
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

"""
Assumptions
-Only one HYCOM netcdf file per day
"""

"""
movebank data for tracks
"""
def get_movebank_tracks_from_csv(csv_fullpath):
    # Convert csv to dataframe
    df = pd.read_csv(csv_fullpath)

    # We need only a few columns, so create a DataFrame containing only the columns
    # that are needed
    df_subset = df[['event-id','timestamp','location-long','location-lat','individual-local-identifier']]

    # Add a new column (initialized to 1/1/1970) to convert the timestamp string to datetime
    df_subset["timestamp_datetime"] = datetime(1970,1,1)
    format_string = "%Y-%m-%d %H:%M:%S.000"
    for k in range(len(df_subset)):
        datetime_string = df_subset.loc[k,"timestamp"]
        df_subset.loc[k,"timestamp_datetime"] = datetime.strptime(datetime_string,format_string)
    #endfor
    print(df_subset.head())
    
    # Return
    return df_subset
    
def get_movebank_track_from_csv(csv_fullpath, tag_id):    
    # Convert from csv to pandas dataframe, enriching with datetime
    df_movebank_tracks = get_movebank_tracks_from_csv(csv_fullpath)

    # Let's look at just one of the tracks.
    myTrack = df_movebank_tracks[df_movebank_tracks['individual-local-identifier']==tag_id]
    
    # Return
    return myTrack

"""
HYCOM-related functions for environmental data
"""
def get_HYCOM_TS_fullpath(timestamp_datetime):
    # Convert timestamp_datetime to string
    datetime_str = timestamp_datetime.strftime("%Y%m%d")
    ts_netcdf_folder= 'C:/Users/s44ba/git/GIS6345/project_data/env_data/CapeHatteras/hycom_TSUV_CapeHatteras/'
    #ts_netcdf_filename = 'hycom_GLBv0.08_563_2015102112_t003.nc'
    ts_netcdf_filename =  'hycom_GLBv0.08_563_'+datetime_str+'12_t003.nc'
    ts_netcdf_fullpath = ts_netcdf_folder+ts_netcdf_filename
    #print(ts_netcdf_fullpath)
    return ts_netcdf_fullpath

def get_HYCOM_UV_fullpath(timestamp_datetime):
    # Convert timestamp_datetime to string
    datetime_str = timestamp_datetime.strftime("%Y%m%d")
    uv_netcdf_folder= 'C:/Users/s44ba/git/GIS6345/project_data/env_data/CapeHatteras/hycom_TSUV_CapeHatteras/'
    #uv_netcdf_filename = 'hycom_GLBv0.08_563_2015102112_t003.nc'
    uv_netcdf_filename =  'hycom_GLBv0.08_563_'+datetime_str+'12_t003.nc'
    uv_netcdf_fullpath = uv_netcdf_folder+uv_netcdf_filename
    #print(uv_netcdf_fullpath)
    return uv_netcdf_fullpath

def get_SST_from_HYCOM_netcdf(netcdf_fullpath):
    # Open netcdf file
    ds_loaded = netCDF4.Dataset(netcdf_fullpath)
    #print(ds_loaded.variables.keys())
    
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
    #print("Shape of SST_array is ",np.shape(SST_array))
    
    # Return
    return lon_array,lat_array,SST_array
    
def get_uv_from_HYCOM_netcdf(netcdf_fullpath):
    # Open netcdf file
    ds_loaded = netCDF4.Dataset(netcdf_fullpath)
    #print(ds_loaded.variables.keys())
    
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
    #print("Shape of surface_u_array is ",np.shape(surface_u_array))
    surface_v_array = water_v_array[0,:,:]   # [lat,lon]
    #print("Shape of surface_v_array is ",np.shape(surface_v_array))
    
    # Return
    return lon_array,lat_array,surface_u_array,surface_v_array
    
    
def plot_HYCOM_TS(netcdf_fullpath):
    
    # Call get_SST_from_HYCOM_netcdf
    lon_array,lat_array,SST_array = get_SST_from_HYCOM_netcdf(netcdf_fullpath)
    
    # Plot
    fig, ax = plt.subplots()
    contourf_plot = ax.contourf(lon_array,lat_array,SST_array[0,:,:],levels=15,cmap=cm.PuBu_r)
    cbar = fig.colorbar(contourf_plot)
    plt.show()

    return
  

def plot_HYCOM_UV(netcdf_fullpath):
    
    # Call get_uv_from_HYCOM_netcdf
    lon_array,lat_array,surface_u_array,surface_v_array = get_uv_from_HYCOM_netcdf(netcdf_fullpath)
    
    # Plot
    fig1, ax1 = plt.subplots()
    ax1.set_title('Arrows scale with plot width, not view')
    quiver_plot = ax1.quiver(lon_array, lat_array, surface_u_array[0,:,:], surface_v_array[0,:,:], units='width')
    qk = ax1.quiverkey(quiver_plot, 0.9, 0.9, 2, r'$2 \frac{m}{s}$', labelpos='E',
                   coordinates='figure')

    return


def plot_HYCOM_TS_and_UV(ts_netcdf_fullpath, uv_netcdf_fullpath):
    
    # Call get_SST_from_HYCOM_netcdf
    ts_lon_array,ts_lat_array,SST_array = get_SST_from_HYCOM_netcdf(ts_netcdf_fullpath)
    
    # Call get_uv_from_HYCOM_netcdf
    uv_lon_array,uv_lat_array,surface_u_array,surface_v_array = get_uv_from_HYCOM_netcdf(uv_netcdf_fullpath)
    
    # Plot with overlay
    # Plot
    fig, ax = plt.subplots()
    ax.set_title('SST and surface velocity')
    # countorf of SST
    contourf_plot = ax.contourf(ts_lon_array,ts_lat_array,SST_array[0,:,:],levels=12,cmap=cm.PuBu_r)
    cbar = fig.colorbar(contourf_plot)
    # quiver of surface velocity vectors
    quiver_plot = ax.quiver(uv_lon_array, uv_lat_array, surface_u_array[0,:,:], surface_v_array[0,:,:], units='width')
    qk = ax.quiverkey(quiver_plot, 0.9, 0.9, 2, r'$2 \frac{m}{s}$', labelpos='E',
                   coordinates='figure')
    plt.show()
    
    return


"""
MUR SST analysis-related functions
"""
def pickle_from_MUR_csv(csv_fullpath, pkl_filename):
    # Load csv file into pandas dataframe
    df = pd.read_csv(csv_fullpath, skiprows = [1])
       
    # Temporarily shorten
    #df_short = df.iloc[0:655260]
    df_short = df

    # Add a new column (initialized to 1/1/1970) to convert the timestamp string to datetime
    df_short["timestamp_datetime"] = datetime(1970,1,1)
    format_string = "%Y-%m-%dT%H:%M:%SZ"
    for k in range(len(df_short)):
        datetime_string = df_short.loc[k,"time"]
        df_short.loc[k,"timestamp_datetime"] = datetime.strptime(datetime_string,format_string)
    #endfor
    print(df_short.head())
    
    # Save to pickle
    df_short.to_pickle(pkl_filename)
    
def get_SST_from_MUR_pkl(pkl_filename, timestamp_datetime_range):
    # Note that the temporal resolution of this dataset is daily. Therefore, to get the same
    # interface as get_SST_from_HYCOM_netcdf, the caller should make sure that the timestamp_datetime_range
    # is a single day
    
    # Load from pickle
    df_short = pd.read_pickle(pkl_filename)

    # Subset in time to get a single i.e. unique timestamp
    df_in_time_window = (df_short['timestamp_datetime']>timestamp_datetime_range[0]) & (df_short['timestamp_datetime']<=timestamp_datetime_range[1])   # boolean
    df_subset = df_short[df_in_time_window]
    df_subset.info()
    
    # What is date range in this short file?
    print(df_subset["timestamp_datetime"].unique())
     
    # Grid
    # Since we already have repeating lon values for each lat, try pivot and to_xarray
    grid_df = df_subset.set_index(['latitude','longitude' ])
    x_coords = df_subset['longitude'].unique()
    y_coords = df_subset['latitude'].unique()
    SST = grid_df['analysed_sst'].values.reshape(len(y_coords),len(x_coords))

    # Convert to numpy
    lat_array = np.array(y_coords)
    lon_array = np.array(x_coords)
    SST_array = np.array(SST)
      
    return lon_array, lat_array, SST_array
    
 






