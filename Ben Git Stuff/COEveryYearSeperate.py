__author__ = 'Ben'
import pandas as pd
import numpy as np
from pandas import DataFrame
import datetime
import pandas.io.data
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.pyplot import text
from numpy import arange
#import geopandas.geoseries as gp


matplotlib.style.use('ggplot')


import glob


path='C:\Rdcep Github\Ben Git Stuff\DataFilesPM2'
path2 ='C:\Rdcep Github\EPADataFiles\DataFilesPM2.csv'

allFiles = glob.glob(path + "/*.csv")
list=[]
integer=0
for file in allFiles:
    if integer<=50:

        df = pd.read_csv(file)# index_col=0)# header=0,)#parse_dates=['Date'])
        list.append(df)
        integer+=1
    frame=pd.concat(list)
    frame['Type']=['Air-PM2']*len(frame.index)
    frame.to_csv(path=path2)

    #df2=gp.from_file()
    df = pd.read_csv(file)# index_col=0)# header=0,)#parse_dates=['Date'])
    print(df.index)
    list.append(df)
    integer+=1




for frame in list:
    year=frame['Date'][5][-4:]
    plt.ylim([0, .2])
    frame=frame.sort_index(by=['Date'], ascending=[True])
    frame.plot(label="Measured CO Level", y='Daily Max 8-hour CO Concentration', x='Date')
    plt.title("Daily Carbon Monoxide Levels for Year {0}".format(str(year))+" in Cook County, IL")
    plt.xlabel('Date')
    plt.ylabel('CO Concentration in Air Close to Surface (ppm)')
    plt.yticks(arange(0,20,1))
    plt.axhline(y=15, xmin=0, xmax=1, linewidth=2, color = 'b',label='Dangerous CO Level')
    plt.legend()
plt.show()

