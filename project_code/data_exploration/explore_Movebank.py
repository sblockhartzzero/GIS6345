# -*- coding: utf-8 -*-
"""
Created on Thu Oct  9 16:24:43 2025

@author: s44ba

"""
# Imports
import fiona
from shapely.geometry import shape
import geopandas as gpd
import pandas as pd
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

"""
Explore shapefile downloaded from movebank.org
"""
# Specify fullpath to input shapefile
# i.e. shapefile downloaded from movebank.org
input_shp = 'C:/Users/s44ba/git/GIS6345/project_data/track_data/Short_finned_pilot_whales_CRC_NW_Atlantic/lines.shp'

# Explore with fiona
# Get info about shapefile contents i.e. schema, crs
with fiona.open(input_shp,"r") as my_shapefile:
    print(my_shapefile.crs)
    print(my_shapefile.schema)

    # Explore features
    for feature in my_shapefile:
        shapely_geometry = shape(feature['geometry'])
        #print(shapely_geometry)
    #endfor
#endwith

# Alternatively, load into geopandas (instead of fiona)
input_gdf = gpd.read_file(input_shp)

# Preview
print(input_gdf.head())

"""
Since shapefile does not contain timestamps, use csv instead, starting
with a pandas dataframe
"""

# Specify fullpath to csv
# i.e. csv downloaded from movebank.org
input_csv = 'C:/Users/s44ba/git/GIS6345/project_data/track_data/Short_finned_pilot_whales_CRC_NW_Atlantic.csv'
df = pd.read_csv(input_csv)
print(df.info())

# Fewer columns
df_subset = df[['event-id','timestamp','location-long','location-lat','individual-local-identifier']]

# Convert to datetime
# Add new column, derived timestamp_datetime, initialized to 1/1/1970
df_subset["timestamp_datetime"] = datetime(1970,1,1)
# Convert
format_string = "%Y-%m-%d %H:%M:%S.000"
for k in range(len(df_subset)):
    datetime_string = df_subset.loc[k,"timestamp"]
    df_subset.loc[k,"timestamp_datetime"] = datetime.strptime(datetime_string,format_string)
#endfor
print(df_subset.head())

"""
Explore by group by tag id and describe
"""
# group by individual-local-identifier
grouped_series = df_subset.groupby('individual-local-identifier').describe()

# Print timestamp_datetime min, max
print(grouped_series['timestamp_datetime']['min'])
print(grouped_series['timestamp_datetime']['max'])

# Print location-lat min, max
print(grouped_series['location-lat']['min'])
print(grouped_series['location-lat']['max'])
  
# Print location-long min, max
print(grouped_series['location-long']['min'])
print(grouped_series['location-long']['max'])

# Is time of interest in data range of track?
datetime_of_interest = datetime(2016, 3, 15)
is_datetime_of_interest_in_range = (grouped_series['timestamp_datetime']['min']<datetime_of_interest)&(grouped_series['timestamp_datetime']['max']>datetime_of_interest)
print(grouped_series[is_datetime_of_interest_in_range])

# Two tags look good i.e. include 3/15/2016: GmTag137 and GmTag142
df_subset[df_subset['individual-local-identifier']=='GmTag137'].describe()
df_subset[df_subset['individual-local-identifier']=='GmTag142'].describe()

"""
Inspect a single track
"""
# Let's look at one of these tracks:
tag_id = 'GmTag142'
myTrack = df_subset[df_subset['individual-local-identifier']==tag_id]

# Subset in time
myTrack_in_time_window = myTrack['timestamp_datetime']<datetime(2016,1,1)
myTrack_subset = myTrack[myTrack_in_time_window]

# Extract arrays 
df_lat = myTrack_subset['location-lat']
df_lon = myTrack_subset['location-long']
df_timestamp_datetime = myTrack_subset['timestamp_datetime']

# Convert to numpy
lat_array = np.array(df_lat)
lon_array = np.array(df_lon)
timestamp_datetime_array = np.array(df_timestamp_datetime)

ax1 = plt.plot(lon_array,lat_array)

"""
Try animating via matplotlib animation
"""
fig2, ax2 = plt.subplots()
line1, = ax2.plot(lon_array,lat_array,'-',color = 'gray')  # Initialize plot
line2, = ax2.plot(lon_array[0],lat_array[0],'ro-',markersize=7)  # Initialize plot
ax2.set(xlim=[-75.0, -73.0],ylim=[35.25, 38.0])
plt.show()

def update(frame_num):
    x = lon_array[frame_num-1:frame_num]
    y = lat_array[frame_num-1:frame_num]
    line2.set_data(x,y)
    return line2

# Call to animate, where interval is msec between frames    
ani = FuncAnimation(fig=fig2, func=update, frames=400, interval=120)
ani.save('GmTag142.mp4')
plt.show()

# print min and max timestamp during this period
print("Time from ",df_timestamp_datetime.min()," to ",df_timestamp_datetime.max())


"""
Experiment with clipping
Shows multiple periods in ROI
# Clip to region of interest
myTrack_in_ROI = (df_subset['location-long']>-75.7)&(df_subset['location-long']>-74.4)&(df_subset['location-lat']>34.2)&(df_subset['location-lat']<35.8)
myTrack_clipped = df_subset[myTrack_in_ROI]

# Convert to numpy arrays
df_lat = myTrack_clipped['location-lat']
df_lon = myTrack_clipped['location-long']
"""
    
    

    
    

