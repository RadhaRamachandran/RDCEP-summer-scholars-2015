import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, Polygon, MultiPolygon
import matplotlib.pyplot as plt
import numpy as np
from descartes import PolygonPatch


def choropleth(startyear, endyear, polutant_type, measure, annotation):
    print('Loading Choropleth...')
    black = '#000000'
    # creates a fgure for our maps
    figure = plt.figure(1, figsize=(24, 14))
    subplot_key = 1
    yeardif = (int(endyear) - int(startyear)) + 1

    # calculates the amount of columns and rows needed for our map
    if yeardif <= 4:
        rows = 2
        columns = 2
    elif 4 < yeardif <= 9:
        rows = 3
        columns = 3
    elif 9 < yeardif <= 16:
        rows = 4
        columns = 4
    elif 16 < yeardif <= 25:
        rows = 5
        columns = 5
    elif 25 < yeardif:
        rows = 6
        columns = 6

    # loop which draws each map one by one
    for year in range(int(startyear), int(endyear) + 1):
        choropleth_map = figure.add_subplot(rows, columns, subplot_key)
        subplot_key += 1
        plt.xlim(-180, -60)
        plt.ylim(10, 80)
        plt.xticks([])
        plt.yticks([])
        danger_level = {'so2': 75, 'no2': 100, 'pm10': 150}

        # gets the data from files based on the parameters specified in the function
        america = gpd.GeoDataFrame.from_file('C:/Anthony/RDCEP things/map of us')
        df = pd.read_csv('C:/Anthony/RDCEP things/' + polutant_type + ' data/' + polutant_type + ' ' + str(year) + '.csv',
                         usecols=['Longitude', 'Latitude', 'Arithmetic Mean'])
        dflocation = df.groupby(['Latitude']).aggregate(np.mean)

        measure_df = dflocation.reset_index()

        # creates point object for each data point in the dflocation, at the same latitude/longitude
        points = []
        for i in range(len(dflocation.index)):
            if dflocation['Arithmetic Mean'][dflocation.index[i]] > 0:
                pt = Point(dflocation['Longitude'][dflocation.index[i]], dflocation.index[i])
                points.append(pt)

        # adds various columns to pointsdf including latitude and longitude, and mean
        pointsdf = gpd.GeoDataFrame(points, columns=['points'])
        pointsdf['Arithmetic Mean'] = measure_df['Arithmetic Mean']
        pointsdf['Longitude'] = measure_df['Longitude']
        pointsdf['Latitude'] = measure_df['Latitude']
        mean_list = []

        # create a column for each state for whether or not every point is in that state; averages the values for
        # each column and adds an annotation. also accounts for states with no points in them
        for i in america.index:
            eachstate = america['STATE_NAME'][i]
            state_geom = america['geometry'][i]
            pointsdf['in' + eachstate] = gpd.GeoSeries(pointsdf['points']).intersects(state_geom)
            pointsdf['in' + eachstate] = pointsdf['Arithmetic Mean'].loc[pointsdf['in' + eachstate] == True]
            if measure == 'mean':
                datum = np.mean(pointsdf['in' + eachstate])
                if annotation == 'yes':
                    mean_val = np.mean(pointsdf['in' + eachstate])
                    occurance = pointsdf['in' + eachstate].idxmax(skipna=True)
                    if type(occurance) != float:
                        plt.annotate(float("{0:.1f}".format(mean_val)), xy=(state_geom.centroid.x, state_geom.centroid.y),
                                     bbox=dict(boxstyle='round', color='k', fc='w', alpha=0.8))
            elif measure == 'max':
                datum = np.max(pointsdf['in' + eachstate])
                if annotation == 'yes':
                    max_val = np.max(pointsdf['in' + eachstate])
                    occurance = pointsdf['in' + eachstate].idxmax(skipna=True)
                    if type(occurance) != float:
                        plt.annotate(float("{0:.1f}".format(max_val)), xy=(state_geom.centroid.x, state_geom.centroid.y),
                                     bbox=dict(boxstyle='round', color='k', fc='w', alpha=0.8))
            elif measure == 'min':
                datum = np.min(pointsdf['in' + eachstate])
                if annotation == 'yes':
                    min_val = np.min(pointsdf['in' + eachstate])
                    occurance = pointsdf['in' + eachstate].idxmin(skipna=True)
                    if type(occurance) != float:
                        plt.annotate(float("{0:.1f}".format(min_val)), xy=(state_geom.centroid.x, state_geom.centroid.y),
                                     bbox=dict(boxstyle='round', color='k', fc='w', alpha=0.8))
            mean_list.append(datum)

        # after calculating a value (datum) for each state, add that value to the america df, well use it to calculate
        # the color of each state
        america['Arithmetic Mean'] = pd.Series(mean_list)
        america['Arithmetic Mean'] = america['Arithmetic Mean'].fillna(value=0)

        # calculate color based on value
        def color(value):
            danger = danger_level[polutant_type]
            if value >= danger:
                return '#ea440d'
            elif value >= 0.25 * danger:
                return '#f6b49e'
            elif value >= 0.05 * danger:
                return '#fcece6'
            elif value < 0.05 * danger:
                return '#ffffff'

        # create a polygon patch for each state, taking into account that some states are
        # Polygons and some are MultiPolygons (ie. collections of polygons)
        patch_list = []
        for i in america.index:
            if type(america['geometry'][i]) == Polygon:
                patch = PolygonPatch(america['geometry'][i], fc=color(america['Arithmetic Mean'][i]), ec=black, zorder=0)
                patch_list.append(patch)
                choropleth_map.add_patch(patch)
            elif type(america['geometry'][i]) == MultiPolygon:
                for polygon in america['geometry'][i]:
                    patch = PolygonPatch(polygon, fc=color(america['Arithmetic Mean'][i]), ec=black, zorder=0)
                    choropleth_map.add_patch(patch)

        # finally, create a title for each sub plot
        plt.title(year)
    # create a title for the whole figure
    figure.suptitle(measure + ' ' + polutant_type + ' concentration from ' + startyear + ' to ' + endyear,
                    family='serif', fontsize=30)
    print('Choropleth Loaded; enjoy!')
    plt.show()


# various inputs including year range, annotations, type of pollutant, etc.
start_year_input = input('Enter a start year from 1990 to 2015: ')
end_year_input = input('Enter an end year from ' + start_year_input + ' to 2015: ')
pollutant_input = input('Enter one of the following pollutants: so2, no2, or pm10: ')
measure_type = input('Enter one of the following measures: mean, std dev, or max: ')
annotation_boolean = input('Annotations? Enter yes or no: ')
choropleth(start_year_input, end_year_input, pollutant_input, measure_type, annotation_boolean)
