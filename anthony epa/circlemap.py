import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import matplotlib.pyplot as plt
import numpy as np


def circlemap(state_name, year, polutant_type):
    pollutant_size = {'so2': 0.1, 'no2': 0.05, 'pm10': 0.01}
    pollutant_unit = {'so2': 'ppb', 'no2': 'ppb', 'pm10': 'ug/m3'}
    america = gpd.GeoDataFrame.from_file('C:/Anthony/RDCEP things/map of us')
    state_list = [america['geometry'][i] for i in america.index if america['STATE_NAME'][i] == state_name]
    state = gpd.GeoSeries(state_list)
    df = pd.read_csv('C:/Anthony/RDCEP things/' + polutant_type + ' data/' + polutant_type + ' ' + str(year) + '.csv',
                     usecols=['Longitude', 'Latitude', 'Arithmetic Mean'])
    dflocation = df.groupby('Latitude').aggregate(np.median)

    points = []
    for i in range(len(dflocation.index)):
        if dflocation['Arithmetic Mean'][dflocation.index[i]] > 0:
            pt = Point(dflocation['Longitude'][dflocation.index[i]], dflocation.index[i]).buffer(dflocation['Arithmetic Mean'][dflocation.index[i]]*pollutant_size[polutant_type])
            points.append(pt)

    pointsdf = gpd.GeoDataFrame(points, columns=['points'])
    pointsdf['point_coords'] = gpd.GeoSeries(pointsdf['points']).centroid
    if state_name != 'country':
        pointsdf['in_state'] = gpd.GeoSeries(pointsdf['point_coords']).intersects(state[0])
        state_circle_list = [pointsdf['points'][i] for i in pointsdf.index if pointsdf['in_state'][i] == True]
        state_point_list = [pointsdf['point_coords'][i] for i in pointsdf.index if pointsdf['in_state'][i] == True]
        state_circle_series = gpd.GeoSeries(state_circle_list)
        state_point_series = gpd.GeoSeries(state_point_list)
        state_circle_series.plot()
        state_point_series.plot()
        state.plot(colormap='winter_r')
        plt.title(polutant_type + ' conc in ' + state_name + ' ' + str(year)
                  + ' (magnitude of each circle represents conc. in ' + pollutant_unit[polutant_type] + ')')

    else:
        america.plot(colormap='Blues')
        gpd.GeoSeries.plot(pointsdf['points'])
        gpd.GeoSeries.plot(pointsdf['point_coords'])
        plt.title(polutant_type + ' conc in ' + state_name + ' ' + str(year)
                  + ' (magnitude of each circle represents conc. in ' + pollutant_unit[polutant_type] + ')')

    plt.show()
circlemap('country', 2009, 'no2')
