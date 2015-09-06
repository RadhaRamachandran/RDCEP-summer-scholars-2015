__author__ = 'Ben Glick'
import geocoder as gc
import pandas as pd
import time

def compare(pothole,knownPothole):
    ffff=0

def truncate(f, n):#4 digits is 11 meters of accuracy
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '%.12f' % f
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

def gcodeSeg(lat,long):
    data=[lat,long]
    if data is not None and not data==['0','0'] and not data==[0,0]:
        cross1 = data[0]
        cross2 = data[1]
        g = gc.reverse(data,provider='google')
        city=g.city
        street=g.street
        number=g.housenumber
        print number,street
        if number is not None and street is not None:
            addr=number+" "+street
        else:
            addr=[]
        time.sleep(.2)
        return addr
    else:
        addr=[]
        return addr

timev=time.time()
frame=pd.read_csv("C:\Users\Ben\Downloads\potholes.csv.csv")
data=frame['loc_lat']
data2=frame['loc_lon']

i=0
i2=0
i3=0

addrs=[]
debugDict={}

lat=[]
i4=1
i6=0

for point in data:
    print data[i6],data2[i6]
    address = gcodeSeg(data[i6],data2[i6])
    i6+=1
    print i4
    if address is None or len(address)is 0:
        debugDict[str(point)]=i2
        lat.append(None)
        i3+=1
    if address is not None and len(address)is not 0 and len(data) is not 0:
        print address
        lat.append(address)
        i+=1
    i4+=1
i2+=1


frame['address']=lat
frame.to_csv('C:\Rdcep Github\Ben Git Stuff\potholesGeocoded.csv')
print 'looped %s times, %s failed and %s successfully geocoded'%(i2,i3,i)
print debugDict
print len(debugDict)
time2=time.time()
print time2-timev