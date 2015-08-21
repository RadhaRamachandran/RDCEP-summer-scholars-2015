import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, Polygon, MultiPolygon
import matplotlib.pyplot as plt
import numpy as np
from descartes import PolygonPatch


figure = plt.figure(1, figsize=(28, 16))
subplot = figure.add_subplot(111)
plt.xlim(-130, -60)
plt.ylim(10, 50)
plt.xticks([])
plt.yticks([])
america = gpd.GeoDataFrame.from_file('C:/Anthony/RDCEP things/map of us')

df_main = pd.read_csv('C:/Anthony/RDCEP things/final rdcep thanng/FinalCSVREAL.csv',
                      usecols=['Lat', 'Long', 'Type'])


# color; blue is water, yellow is air
def color(x):
    if x[:2] == 'Ac' or x[:2] == 'Ai' or x[:2] == 'Ca' or x[:2] == 'Oz' or x[:2] == 'PM':
        return 'yellow'
    else:
        return 'blue'


for i in america.index:
    if type(america['geometry'][i]) == Polygon:
        patch = PolygonPatch(america['geometry'][i], fc='white', ec='black', zorder=0)
        subplot.add_patch(patch)
    elif type(america['geometry'][i]) == MultiPolygon and america['STATE_NAME'][i] != 'Alaska' and america['STATE_NAME'][i] != 'Hawaii':
        for polygon in america['geometry'][i]:
            patch = PolygonPatch(polygon, fc='white', ec='black', zorder=0)
            subplot.add_patch(patch)

df_count = df_main.groupby(['Type']).size()
df_count2 = df_main.groupby(['Type']).size()


for eachtype in df_count.index:
    print('loading', eachtype)
    df_type = df_main.loc[df_main['Type'] == eachtype]
    df_lat_index = df_type.groupby(['Lat']).aggregate(np.mean)
    df_coords = df_lat_index.reset_index()
    for i in df_coords.index:
        circle = Point(df_coords['Long'][i], df_coords['Lat'][i]).buffer(0.2)
        patch = PolygonPatch(circle, fc=color(eachtype), ec=color(eachtype))
        subplot.add_patch(patch)
        if i == df_coords.index[-1]:
            print('finished at latitude index', i)

# extra water data location

loc1 = Point(-96.665033, 33.90492).buffer(0.2)
loc2 = Point(-102.506255, 36.035292).buffer(0.2)
loc3 = Point(-95.59051, 33.831166).buffer(0.2)
loc4 = Point(-95.160931, 30.654296).buffer(0.2)
loc5 = Point(-98.005991, 33.888817).buffer(0.2)
points_list = [loc1, loc2, loc3, loc4, loc5]
for i in points_list:
    print('adding extra patches')
    patchloc = PolygonPatch(i, fc='blue', ec='blue')
    subplot.add_patch(patchloc)

plt.show()
