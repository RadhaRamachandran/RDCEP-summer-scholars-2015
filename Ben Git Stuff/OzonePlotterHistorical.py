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

path =r'C:\Users\Ben\Desktop\DataFiles'
allFiles = glob.glob(path + "/*.csv")
frame = pd.DataFrame()
list_ = []
for file_ in allFiles:
    df = pd.read_csv(file_,index_col='Date', header=0,parse_dates=['Date'])
    list_.append(df)
frame = pd.concat(list_)



df3=frame['Daily Max 8-hour Ozone Concentration']
#df3=df3.sort_index(by=['PERCENT COMPLETE'], ascending=[True])
df3.plot(label="Measured Lead Level")
plt.title('Daily Ozone Levels for 1980-2015 in Cook County, IL')
plt.xlabel('Date')
plt.ylabel('Ozone Concentration in Air (ppm)')
plt.axhline(y=.075, xmin=0, xmax=1, linewidth=2, color = 'b',label='Dangerous Ozone Level')
plt.legend()
plt.show()




