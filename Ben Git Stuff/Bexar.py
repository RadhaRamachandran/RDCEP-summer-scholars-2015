__author__ = 'Ben'
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

path =r'C:\Rdcep Github\Ben Git Stuff\DataFilesOzone\DataFilesOzoneTexas'
allFiles = glob.glob(path + "/*.csv")
frame = pd.DataFrame()
list_ = []
for file_ in allFiles:
    df = pd.read_csv(file_,index_col='Date', header=0,parse_dates=['Date'])
    list_.append(df)
frame = pd.concat(list_)






df3=frame['Daily Max 8-hour Ozone Concentration']
#df3=df3.sort_index(by=['PERCENT COMPLETE'], ascending=[True])
df3.plot(label="Measured Ozone Level")
plt.title('Daily Ozone Levels for 1980-1990 in Honolulu County, HI')
plt.xlabel('Date')
plt.ylim(0,.2)
plt.yticks(arange(-.05,.2,.05))
plt.ylabel('Ozone Concentration in Air (ppm)')
plt.axhline(y=.075, xmin=0, xmax=1, linewidth=2, color = 'b',label='Dangerous Ozone Level')
plt.legend()
y = np.sin(2 * np.pi)
plt.plot(y)
plt.show()




