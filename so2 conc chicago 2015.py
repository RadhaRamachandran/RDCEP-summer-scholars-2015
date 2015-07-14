import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def lineplot():
    location = 'C:\Anthony\RDCEPrepository\daily_42401_2015.csv'
    df = pd.read_csv(location, index_col='Date Local', usecols=["Date Local", 'Arithmetic Mean', 'Method Name', 'Address'])
    df = df.loc[df["Address"] == "7801 LAWNDALE"]
    df = df.loc[np.logical_or(df["Method Name"] == "INSTRUMENTAL - ULTRA VIOLET FLUORESCENCE", df["Method Name"] == "INSTRUMENTAL - ULTRAVIOLET FLUORESCENCE")]
    df = df.loc[df['Arithmetic Mean'] >= 0]
    pd.Series.plot(df['Arithmetic Mean'])
    plt.title('SO2 air concentration in Chicago, January - March, 2015')
    plt.ylabel('part per billion')
    plt.show()

lineplot()
