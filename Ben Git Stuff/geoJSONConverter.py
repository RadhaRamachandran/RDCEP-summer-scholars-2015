__author__ = 'Ben'
import csv
import pandas as pd

#concatenate csvs
import glob

path =r'C:\Rdcep Github\Ben Git Stuff\DataFilesLead'
allFiles = glob.glob(path + "/*.csv")
frame = pd.DataFrame()
list_ = []
list2=[]
for file_ in allFiles:
    df = pd.read_csv(file_,index_col='Date', header=0,parse_dates=['Date'])
    list_.append(df)
frame = pd.concat(list_)
frame.to_csv('C:\\Users\\Ben\\Desktop\\output.csv')




rawData = csv.reader(open('C:\\Users\Ben\Desktop\leadDataTotal.csv'))

# the template. where data from the csv will be formatted to geojson
template = \
    ''' \
    { "type" : "Feature",
        "id" : %s,
            "geometry" : {
                "type" : "Point",
                "coordinates" : ["%s","%s"]},
        "properties" : { "name" : "%s", "value" : "%s"}
        },
    '''

# the head of the geojson file
output = \
    ''' \
{ "type" : "Feature Collection",
    {"features" : [
    '''

# loop through the csv by row skipping the first
iter = 0
for row in rawData:
    iter += 1
    if iter >= 2:
        id = row[0]
        lat = row[18]
        lon = row[19]
        name = row[0]
        pop = row[3]
        output += template % (row[0], row[18], row[19], row[0], row[3])

# the tail of the geojson file
output += \
    ''' \
    ]
}
    '''

# opens an geoJSON file to write the output to
outFileHandle = open("C:\\Users\Ben\Desktop\output.geojson", "w")
outFileHandle.write(output)
outFileHandle.close()