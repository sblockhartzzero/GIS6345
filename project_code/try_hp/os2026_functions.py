# -*- coding: utf-8 -*-
"""
Created on Wed Nov 26 12:58:36 2025

@author: s44ba
"""

# Imports
import imageio
import numpy as np
from scipy import ndimage
import pandas as pd

# Function to high-pass filter an image (given a file e.g. jpg or png)
def hpfilter_band_from_file(image_fullpath, band_num):
    # Read image file
    im = imageio.imread(image_fullpath)
    # Convert to numpy array
    data = np.array(im,dtype=float)
    #np.shape(data)
    # Hp filter
    kernel = np.array([[-1.0,-1.0,-1.0],[-1.0,8.0,-1.0],[-1.0,-1.0,-1.0]])
    if (band_num<0):
        # Already a single-band image
        hp33 = ndimage.convolve(data[:,:],kernel)
    else:
        hp33 = ndimage.convolve(data[:,:,band_num],kernel)
    # Return
    return hp33

# Function to high-pass filter a 2-D image (given a numpy array)
def hpfilter_band_from_array(image_array):
    # Assign data
    data = image_array
    # Hp filter
    kernel = np.array([[-1.0,-1.0,-1.0],[-1.0,8.0,-1.0],[-1.0,-1.0,-1.0]])
    hp33 = ndimage.convolve(data[:,:],kernel)
    # Return
    return hp33
    
# Function to get a set of points corresponding to the locations where SST 
# (in the MUR SST pkl file) is in a specified range. The set of points is 
# returned in a pandas dataframe. This will be used by the caller to identify the 
# western edge of the Gulf Stream for the specified datetime range 
def points_in_T_range(pkl_filename, timestamp_datetime_range, temperature_F_range):
    # Load from pickle
    df_short = pd.read_pickle(pkl_filename)

    # Subset in time to get a single i.e. unique timestamp
    df_in_time_window = (df_short['timestamp_datetime']>timestamp_datetime_range[0]) & (df_short['timestamp_datetime']<=timestamp_datetime_range[1])   # boolean
    df_subset = df_short[df_in_time_window]
    df_subset.info()
    
    # What is date range in this short file?
    print(df_subset["timestamp_datetime"].unique())
    
    # Subset further, based upon T range
    df_in_T_range = (df_subset['analysed_sst']>temperature_F_range[0]) & (df_subset['analysed_sst']<=temperature_F_range[1])
    df_subset_T = df_subset[df_in_T_range]
    df_subset_T.info()
    
    # Return
    return df_subset_T
    