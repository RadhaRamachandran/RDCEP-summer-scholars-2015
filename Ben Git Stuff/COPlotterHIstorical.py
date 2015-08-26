__author__ = 'Ben'
import pandas as pd
import numpy as np
from numpy import random
from pandas import DataFrame
import datetime
import pandas.io.data
import matplotlib.pyplot as plt
import matplotlib
from numpy import arange
import random
matplotlib.style.use('ggplot')

import glob

path =r'C:\Rdcep Github\Ben Git Stuff\DataFilesCO'
allFiles = glob.glob(path + "/*.csv")
frame = pd.DataFrame()
list_ = []
for file_ in allFiles:
    df = pd.read_csv(file_,index_col='Date', header=0,parse_dates=['Date'])
    list_.append(df)
frame = pd.concat(list_)



df3=frame['Daily Max 8-hour CO Concentration']
#df3=df3.sort_index(by=0, ascending=[True])
df3.plot(label="Measured CO Level")

plt.title('Daily Carbon Monoxide Levels for 1980-2015 (Excluding 2013) in Cook County, IL')
plt.xlabel('Date')
plt.ylabel('CO Concentration in Air (ppm)')
plt.axhline(y=15, xmin=0, xmax=1, linewidth=2, color = 'b',label='Dangerous CO Level')
plt.axvline(.25,linewidth=4,color='g')

plt.title('Daily Carbon Monoxide Levels for 1980-2015 in Cook County, IL')
plt.xlabel('Date')
plt.ylabel('CO Concentration in Air (ppm)')
plt.axhline(y=15, xmin=0, xmax=1, linewidth=2, color = 'b',label='Dangerous CO Level')

plt.legend()
plt.show()






