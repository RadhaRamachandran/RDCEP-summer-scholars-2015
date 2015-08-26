import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import matplotlib.pyplot as plt
import numpy as np

# plots pollutant data points on a map of the united states
def circlemap(state_name, year, polutant_type):
	# create pollutant size dictionary, which determines how big the data points will be on the map
    pollutant_size = {'so2': 0.1, 'no2': 0.05, 'pm10': 0.01}
    pollutant_unit = {'so2': 'ppb', 'no2': 'ppb', 'pm10': 'ug/m3'}
	# load united states shapefile
    america = gpd.GeoDataFrame.from_file('C:/Anthony/RDCEP things/map of us')
	# create a state geoseries, consisting of one state specified in the function's parameters
    state_list = [america['geometry'][i] for i in america.index if america['STATE_NAME'][i] == state_name]
    state = gpd.GeoSeries(state_list)
	# load our data and groupby latitude
    df = pd.read_csv('C:/Anthony/RDCEP things/' + polutant_type + ' data/' + polutant_type + ' ' + str(year) + '.csv',
                     usecols=['Longitude', 'Latitude', 'Arithmetic Mean'])
    dflocation = df.groupby('Latitude').aggregate(np.median)

	# create a circle object for our map at every data point we have, the larger the radius, the higher levels of pollutant there is.  
    points = []
    for i in range(len(dflocation.index)):
        if dflocation['Arithmetic Mean'][dflocation.index[i]] > 0:
            pt = Point(dflocation['Longitude'][dflocation.index[i]], dflocation.index[i]).buffer(dflocation['Arithmetic Mean'][dflocation.index[i]]*pollutant_size[polutant_type])
            points.append(pt)

	#put our points/circles in a data frame, and make another column for the coordinates of the points 
    pointsdf = gpd.GeoDataFrame(points, columns=['points'])
    pointsdf['point_coords'] = gpd.GeoSeries(pointsdf['points']).centroid
	#If the function is given a state name as a parameter(eg. Illinois), then plot only the state, and all points in that state
	# If the function is given the word 'country' as a parameter, plot the entire country, and all the points in it.
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
