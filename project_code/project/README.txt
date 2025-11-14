GIS 6345 PROJECT CODE:
-project_main.py > project_functions.py 
-project_pickle_MUR_SST.py pickles MUR_SST data (as df_MUR_SST.pkl) before running project_main.py
-project_plot_distance.py plots distance from point on track to one of the hydrophone locations
-other project_plot_* are for data exploration

GIS 6345 PROJECT OUTPUT:
*.mp4 are outputs from running project_main.py

GIS 6345 ASSIGNMENT #9
-prep_MUR_SST_data (which saves MUR SST data as df_short.pkl) and generates new_scaled_int.tif
-verify_MUR_SST_data

OS2026:
project_pickle_MUR_SST.py, project_functions.py, and project_main.py modified to support OS2026 scenarios (i.e. env_scenario) 
os2026_main.py calls project_functions.py (after running project_pickle_MUR_SST.py to save pickle file)
