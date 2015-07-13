__author__ = 'Ben'
__author__ = 'Ben'
import pandas as pd
import numpy as np
from pandas import DataFrame
import datetime
import pandas.io.data
import matplotlib.pyplot as plt
import matplotlib
from numpy import arange
matplotlib.style.use('ggplot')

import glob

path =r'C:\Rdcep Github\Ben Git Stuff\DataFilesPM2'
allFiles = glob.glob(path + "/*.csv")
list=[]
integer=0
for file in allFiles:
    if integer<=50:
        df = pd.read_csv(file)# index_col=0)# header=0,)#parse_dates=['Date'])
        print(df.index)
        list.append(df)
        integer+=1



for frame in list:
    year=frame['Date'][5][-4:]
    plt.ylim([0, .2])
    frame=frame.sort_index(by=['Date'], ascending=[True])
    frame.plot(label="Measured PM2.5 Level", y='Daily Mean PM2.5 Concentration', x='Date')
    plt.title("Daily Small Particulate Matter Levels for Year {0}".format(str(year))+" in Cook County, IL")
    plt.xlabel('Date')
    plt.ylabel('PM2.5 Concentration in Air Close to Surface (ug/m^3)')
    plt.yticks(arange(0,55,5))
    plt.axhline(y=35, xmin=0, xmax=1, linewidth=2, color = 'b',label='Dangerous PM2.5 Level')
    plt.legend()
plt.show()

