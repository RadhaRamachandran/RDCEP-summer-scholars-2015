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

df = pd.read_csv("C:\\Users\Ben\Desktop\d_viz_plotval_data.csv", index_col='Date', parse_dates=True)
df.head()
df2 = df[['AQS_SITE_ID', 'STATE', 'Daily Max 8-hour Ozone Concentration','UNITS']]
print(df2.head())
df3=df['Daily Max 8-hour Ozone Concentration']
df3.plot()
plt.title('Daily Ozone Levels for Year 2014 in Cook County, IL')
plt.axhline(y=.075, xmin=0, xmax=1, linewidth=2, color = 'b',label='Dangerous Ozone Level')
plt.legend()
plt.show()



