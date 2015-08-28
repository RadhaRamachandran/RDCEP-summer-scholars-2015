__author__ = 'Ben Glick'
__Co__Author__='John Gueringer'
import geocoder as gc
import pandas as pd
import time


def gcodeSeg(segment):
    addr = " Chicago IL"
    if '/' in segment:
        data = segment.split("/")
    else:
        data=None
    if data is not None:
        cross1 = data[0]
        cross2 = data[1]
        query = cross1 + ' & ' + cross2 + addr
        latlng = gc.google(query).latlng
        time.sleep(.1)
        return latlng

print gcodeSeg('Aldine/Broadway')


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
frame=pd.read_csv("C:\\Users\\Ben\\Downloads\\City Data Spreadsheet - LawnConditions.csv")
data=frame['BlockNameBegin']

i=0
i2=0
i3=0

lats=[]
longs=[]
debugDict={}

lat=[]
long=[]
i4=1
for point in data:
    latlng = gcodeSeg(point)
    print i4
    if latlng is None:
        print None
    if latlng is None:
        debugDict[str(point)]=i2
        lat.append(None)
        long.append(None)
        i3+=1
    if latlng is not None and len(latlng)is not 0 and len(data) is not 0:
        print latlng
        lat.append(latlng[0])
        long.append(latlng[1])
        i+=1
    i4+=1
i2+=1
lats.append(lat)
longs.append(long)
frame['Latitude']=lats[0]
frame['Longitude']=longs[0]
frame.to_csv('C:\Rdcep Github\Ben Git Stuff\LawnsGeocoded.csv')
print 'looped %s times, %s failed and %s successfully geocoded'%(i2,i3,i)
print debugDict
print len(debugDict)
time2=time.time()
print time2-timev
