import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from descartes import PolygonPatch
from shapely.geometry import Point
import numpy as np


def chicago_plotter():
    beat_shp = gpd.GeoDataFrame.from_file('C:/Anthony/RDCEP things/chicago beats')
    tract_shp = gpd.GeoDataFrame.from_file('C:/Anthony/RDCEP things/illinois tracts')
    ward_shp = gpd.GeoDataFrame.from_file('C:/Anthony/RDCEP things/chicago wards 2')
    print(beat_shp)
    print(tract_shp)
    print(ward_shp)
    df_tallies = pd.read_csv('C:/Anthony/RDCEP things/MaybeGeocodedTalliesHopefullyPlease.csv')
    df_tallies = df_tallies.reset_index()
    df_tallies = gpd.GeoDataFrame(df_tallies)
    crime_data = pd.read_csv('C:/Anthony/RDCEP things/Crimes_-_2014-ex file.csv')
    crime_data_count = crime_data.groupby('Beat').count()
    target_crs = {'init': 'epsg:4269'}
    tract_shp.to_crs(crs=target_crs, inplace=True)
    beat_shp.to_crs(crs=target_crs, inplace=True)
    ward_shp.to_crs(crs=target_crs, inplace=True)
    print(beat_shp.crs)
    print(tract_shp.crs)
    print(ward_shp.crs)
    point_coord_list = [Point(df_tallies['Longitude'][k], df_tallies['Latitude'][k])for k in df_tallies.index]
    pointseries = gpd.GeoSeries(point_coord_list)
    df_tallies['beat_number'] = pd.Series([0]*len(df_tallies.index))
    df_tallies['ward_number'] = pd.Series([0]*len(df_tallies.index))
    df_tallies['census_tract'] = pd.Series([0]*len(df_tallies.index))

    for i in beat_shp.index:
        print('filling in cells with beat index', i)
        df_tallies['in' + beat_shp['BEAT_NUM'][i]] = pointseries.intersects(beat_shp['geometry'][i])
        in_beat_series = df_tallies['in' + beat_shp['BEAT_NUM'][i]][df_tallies['in' + beat_shp['BEAT_NUM'][i]] == True]
        for g in in_beat_series.index:
            df_tallies['beat_number'][g] = beat_shp['BEAT_NUM'][i]
        del df_tallies['in' + beat_shp['BEAT_NUM'][i]]

    for i in tract_shp.index:
        print('filling in cells with tract index', i)
        df_tallies['in' + tract_shp['TRACTCE'][i]] = pointseries.intersects(tract_shp['geometry'][i])
        in_tract_series = df_tallies['in' + tract_shp['TRACTCE'][i]][df_tallies['in' + tract_shp['TRACTCE'][i]] == True]
        for g in in_tract_series.index:
            df_tallies['census_tract'][g] = tract_shp['TRACTCE'][i]
        del df_tallies['in'+ tract_shp['TRACTCE'][i]]

    for i in ward_shp.index:
        print('filling in cells with ward index', i)
        df_tallies['in' + ward_shp['District_N'][i]] = pointseries.intersects(ward_shp['geometry'][i])
        in_ward_series = df_tallies['in' + ward_shp['District_N'][i]][df_tallies['in' + ward_shp['District_N'][i]] == True]
        for g in in_ward_series.index:
            df_tallies['ward_number'][g] = ward_shp['District_N'][i]
        del df_tallies['in' + ward_shp['District_N'][i]]

    df_tallies['CrimeCount'] = pd.Series([0]*len(df_tallies.index))
    for j in df_tallies.index:
        crime = crime_data_count['ID'][crime_data_count.index == df_tallies['beat_number'][j]]
        print(crime)
        df_tallies['CrimeCount'][j] = crime

    print(df_tallies)
    df_tallies.to_csv('C:/Anthony/TalliesWithCrimeBeatTractAndWard2.csv')

chicago_plotter()
