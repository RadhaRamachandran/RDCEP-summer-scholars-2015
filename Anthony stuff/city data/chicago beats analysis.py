import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from descartes import PolygonPatch
from shapely.geometry import Point
import numpy as np


def chicago_plotter():
    beat_shp = gpd.GeoDataFrame.from_file('C:/Anthony/RDCEP things/chicago beats')
    df_tallies = pd.read_csv('C:/Anthony/RDCEP things/MaybeGeocodedTalliesHopefullyPlease.csv')
    df_tallies = df_tallies.reset_index()
    target_crs = {'init': 'epsg:4269'}
    beat_shp.to_crs(crs=target_crs, inplace=True)
    point_coord_list = [Point(df_tallies['Longitude'][k], df_tallies['Latitude'][k])for k in df_tallies.index]
    df_tallies['point_coords'] = pd.Series(point_coord_list)
    df_tallies['beat_number'] = pd.Series([0]*len(df_tallies.index))
    for i in beat_shp.index:
        df_tallies['in' + beat_shp['BEAT_NUM'][i]] = gpd.GeoSeries(df_tallies['point_coords']).intersects(beat_shp['geometry'][i])
        in_beat_series = df_tallies['in' + beat_shp['BEAT_NUM'][i]][df_tallies['in' + beat_shp['BEAT_NUM'][i]] == True]
        # print(df_tallies['in' + beat_shp['BEAT_NUM'][i]])
        print('beat number', i)
        for g in in_beat_series.index:
            df_tallies['beat_number'][g] = beat_shp['BEAT_NUM'][i]
        del df_tallies['in' + beat_shp['BEAT_NUM'][i]]

    print(df_tallies)
    df_tallies.to_csv('C:/Anthony/RDCEP things/UpdatedTalliesWithBeatNumbers.csv')

chicago_plotter()