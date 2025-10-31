# -*- coding: utf-8 -*-
"""
Created on Fri Oct 31 13:45:48 2025

@author: s44ba

For GIS6345 Project

From the MUR SST csv file, save to pkl file for subsequent processing.
"""

# Imports
import project_functions

# Specify csv file for MUR SST
csv_folder = 'C:\\Users\\s44ba\\git\\GIS6345\\project_data\\env_data\\CapeHatteras\\MUR_SST_CapeHatteras\\'
csv_filename = 'jplMURSST41F_de75_def0_78ea.csv';
csv_fullpath = csv_folder + csv_filename

# Specify pickled file
pkl_filename = 'df_short.pkl'

# Convert csv to pandas dataframe and save to pickle file for subsequent runs
project_functions.pickle_from_MUR_csv(csv_fullpath,pkl_filename)