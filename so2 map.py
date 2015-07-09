from tkinter import Tk, Canvas
import numpy as np
import pandas as pd

tk = Tk()
canvas = Canvas(tk, width=1000, height=600)
canvas.pack()

location = 'C:\Anthony\RDCEP things\so2 2015.csv'
df = pd.read_csv(location, usecols=['Longitude', 'Latitude', 'Arithmetic Mean'])
dflocation = df.groupby('Latitude').aggregate(np.median)


def lat_to_ycoord(lat):
    ycoord = (70 - lat)* 10
    return ycoord


def long_to_xcoord(long):
    xcoord = -(-160 - long) * 10
    return xcoord

mean_list = []
lat_list = []
long_list = []
mainlist = []

for item in dflocation['Arithmetic Mean']:
    mean = item
    mean_list.append(item)

for item in dflocation.index:
    lat = lat_to_ycoord(item)
    lat_list.append(lat)

for item in dflocation['Longitude']:
    long = long_to_xcoord(item)
    long_list.append(long)

for item in range(len(lat_list)):
    mainitem = [long_list[item], lat_list[item], mean_list[item]]
    mainlist.append(mainitem)

for item in mainlist:
    if item[2] >= 0:
        radius = 2*item[2]
        canvas.create_oval(item[0] - radius, item[1] - radius,
                           item[0] + radius, item[1] + radius,
                           fill='blue')

tk.mainloop()