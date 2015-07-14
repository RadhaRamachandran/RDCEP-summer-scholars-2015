import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def histrorical_so2():
    location = "C:\RDCEP Github"
    filenames = ["so2 2015", "so2 2014", "so2 2013", "so2 2012", "so2 2011",
                 "so2 2010", "so2 2009", "so2 2008", "so2 2007", "so2 2006",
                 "so2 2005", "so2 2004", "so2 2003", "so2 2002", "so2 2001",
                 "so2 2000"]
    files = []
    filetype = '.csv'
    for eachfile in filenames:
        eachfile = location + r'\\' + eachfile + filetype
        files.append(eachfile)

    dflist = []
    for eachfile in files:
        eachdf = pd.read_csv(eachfile, index_col='Date Local', usecols=['Date Local', 'Arithmetic Mean', 'Method Name', 'Address'], parse_dates = True)
        dflist.append(eachdf)
    df = pd.concat(dflist)
    df = df.loc[np.logical_or(df["Address"] == "7801 LAWNDALE", df["Address"] == "103RD AND LUELLA")]
    df = df.loc[np.logical_or(df["Method Name"] == "INSTRUMENTAL - ULTRA VIOLET FLUORESCENCE", df["Method Name"] == "INSTRUMENTAL - ULTRAVIOLET FLUORESCENCE")]
    df = df.loc[df['Arithmetic Mean'] >= 0]

    pd.Series.plot(df['Arithmetic Mean'])
    plt.axhline(15, linewidth=4, color='red')
    plt.title('SO2 air concentration in Chicago (red line is 1/5th of dangerous levels)')
    plt.ylabel('part per billion')
    plt.show()
histrorical_so2()
