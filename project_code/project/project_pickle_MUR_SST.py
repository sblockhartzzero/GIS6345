# -*- coding: utf-8 -*-
"""
Created on Fri Oct 31 13:45:48 2025

@author: s44ba

For GIS6345 Project

From the MUR SST csv file, save to pkl file for subsequent processing.

If adding a new env_scenario, make sure to add it to project_functions.get_MUR_pickle_filename as well.
"""

# Imports
import project_functions

# Specify csv file for MUR SST
csv_folder = 'C:\\Users\\s44ba\\git\\GIS6345\\project_data\\env_data\\CapeHatteras\\MUR_SST_CapeHatteras\\'

# Specify scenario (which determines pickle filename to use for MUR SST)
# Could be 'GIS6345' or 'OS2026_1a', 'OS2026_1b' to 'OS2026_4'
env_scenario = 'OS2026_4'

# Specify scenario (which defines input data file)
match env_scenario:
    case 'GIS6345':
        # Specify input csv filename
        # From 10/15/2015 to 01/06/2016 w/0.04 degree res
        csv_filename = 'jplMURSST41F_56bc_5beb_086c.csv';
    case 'OS2026_1':
        # Specify input csv filename
        # From 01/15/2015 to 04/05/2015 w/0.02 degrees res and wider range of lons (to -76.0)
        csv_filename = 'jplMURSST41F_871e_f8d3_18d4.csv'
    case 'OS2026_1a':
        # Specify input csv filename
        # From 01/15/2015 to 02/15/2015 w/0.02 degrees res and wider range of lons (to -76.0)
        csv_filename = 'jplMURSST41F_d09a_37a2_a2cc.csv'    
    case 'OS2026_1b':
        # Specify input csv filename
        # From 02/15/2015 to 04/01/2015 w/0.02 degrees res and wider range of lons (to -76.0)
        csv_filename = 'jplMURSST41F_aa56_bb6c_1813.csv'
    case 'OS2026_2':
        # Specify input csv filename
        # From 02/15/2016 to 04/01/2016 w/0.02 degrees res and wider range of lons (to -76.0)
        csv_filename = 'jplMURSST41F_2c81_ca33_a3f1.csv'
    case 'OS2026_4':
        # Specify input csv filename
        # From 12/01/2018 to 04/01/2019 w/0.02 degrees res and wider range of lons (to -76.0)
        csv_filename = 'jplMURSST41F_d81f_2e6f_4f60.csv'
#endmatch

csv_fullpath = csv_folder + csv_filename

# Get pickled filename (for MUR SST data) based upon the env_scenario
pkl_filename = project_functions.get_MUR_pickle_filename(env_scenario) 

# Convert csv to pandas dataframe and save to pickle file for subsequent runs
project_functions.pickle_from_MUR_csv(csv_fullpath,pkl_filename)