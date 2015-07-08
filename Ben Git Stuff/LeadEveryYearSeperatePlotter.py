import pandas as pd
import numpy as np
from pandas import DataFrame
import datetime
import pandas.io.data
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.pyplot import text
from numpy import arange
matplotlib.style.use('ggplot')

import glob

path =r'C:\Users\Ben\Desktop\DataFilesLead'
allFiles = glob.glob(path + "/*.csv")
list=[]
integer=0
for file in allFiles:
    if integer<=50:
        df = pd.read_csv(file,)# index_col=0)# header=0,)#parse_dates=['Date'])
        print(df.index)
        list.append(df)
        integer+=1



for frame in list:
    year=frame['Date'][5][-4:]
    plt.ylim([0, 7])
    frame=frame.sort_index(by=['Date'], ascending=[True])
    frame.plot(label="Measured Lead Level", y='Daily Mean Pb Concentration', x='Date')
    plt.title("Daily Lead Levels for Year {0}".format(str(year))+" in Cook County, IL")
    plt.xlabel('Date')
    plt.ylabel('Lead Concentration in Air (ug/m3)')
    plt.yticks(arange(0,7,.5))
    plt.axhline(y=.15, xmin=0, xmax=1, linewidth=2, color = 'b',label='Dangerous Lead Level')
    plt.legend()
plt.show()

