import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def historical_no2():
    location = "C:/Anthony/RDCEP things/PM 10 data"
    filenames = ['pm10 2015', 'pm10 2014', 'pm10 2013', 'pm10 2012', 'pm10 2011',
                 'pm10 2010', 'pm10 2009', 'pm10 2008', 'pm10 2007', 'pm10 2006',
                 'pm10 2005', 'pm10 2004', 'pm10 2003', 'pm10 2002', 'pm10 2001',
                 'pm10 2000', 'pm10 1999', 'pm10 1998', 'pm10 1997', 'pm10 1996',
                 'pm10 1995', 'pm10 1994', 'pm10 1993', 'pm10 1992', 'pm10 1991',
                 'pm10 1990']
    filetype = '.csv'
    files =[location + '/' + eachfile + filetype for eachfile in filenames]

    dflist = []
    for eachfile in files:
        eachdf = pd.read_csv(eachfile, index_col='Date Local', usecols=['Date Local', 'Arithmetic Mean', 'Method Name', 'Address'], parse_dates = True)
        dflist.append(eachdf)
    df = pd.concat(dflist)
    df = df.loc[np.logical_or(df['Address'] == 'WASHINGTON ELEM. SCH., 3611 E. 114TH ST.', df['Address'] == '3535 E. 114TH ST.')]
    df = df.loc[df['Arithmetic Mean'] >= 0]
    df['Month'] = df.index.month
    df['Year'] = df.index.year
    dfmonthly = df.groupby(['Year', 'Month']).aggregate(np.median)
    print(dfmonthly[:40])

    pd.Series.plot(dfmonthly['Arithmetic Mean'])
    plt.axhline(150, linewidth=4, color='red')
    plt.title('PM 10 air concentration in Chicago(red line indicates dangerous levels)')
    plt.ylabel('ug/m3')
    plt.show()
historical_no2()


