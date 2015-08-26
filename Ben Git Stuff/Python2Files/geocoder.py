__author__ = 'Ben'
import geocoder as gc
import pandas as pd
import time

def gcodeSeg(segment):
   addr = " Chicago IL"

   data = segment.split("/")
   cross1 = data[0]
   cross2 = data[1]

   query = cross1 + ' & ' + cross2 + addr
   latlng = gc.arcgis(query).latlng

   return latlng

print gcodeSeg('Aldine/Broadway')
file = open("C:\\Users\\Ben\\Downloads\\City Data Spreadsheet - Tallies.csv")
file.next()

i=0
i2=0
'''
for line in file:
    if line is not None:
        i2+=1
        data = line.split(',')
        cross_section = data[0]
        print cross_section
        time.sleep(.2)
        latlng = gcodeSeg(cross_section)
        print len(latlng)
        if len(latlng)==0:
            debugDict[str(cross_section)]=i2
        if len(latlng)is not 0 and len(data) is not 0:
            print latlng
            lat.append(latlng[0])
            lng.append(latlng[1])
            i+=1
print i
'''
timev=time.time()
frame=pd.read_csv("C:\\Users\\Ben\\Downloads\\City Data Spreadsheet - Tallies.csv")
data=frame['BlockNameBegin']
lat=[]
i3=0
long=[]
debugDict={}
for point in data:
    latlng = gcodeSeg(point)
    print len(latlng)
    if len(latlng)==0:
        debugDict[str(point)]=i2
        lat.append(None)
        long.append(None)
        i3+=1
    if len(latlng)is not 0 and len(data) is not 0:
        print latlng
        lat.append(latlng[0])
        long.append(latlng[1])
        i+=1
    i2+=1
frame['Latitude']=lat
frame['Longitude']=long
frame.to_csv('C:\\Rdcep Github\\Ben Git Stuff\\MaybeGeocodedTalliesHopefullyPlease.csv')
print 'looped %s times, %s failed and %s successfully geocoded'%(i2,i3,i)
print debugDict
time2=time.time()
print time2-timev