import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def historical_pm10():
    # loads the data into pandas dataframe
    location = "C:/Anthony/RDCEP things/pm10 data"
    filenames_1980 = ['pm10 1989', 'pm10 1988']
    filenames_1990 = ['pm10 2015', 'pm10 2014', 'pm10 2013', 'pm10 2012', 'pm10 2011',
                      'pm10 2010', 'pm10 2009', 'pm10 2008', 'pm10 2007', 'pm10 2006',
                      'pm10 2005', 'pm10 2004', 'pm10 2003', 'pm10 2002', 'pm10 2001',
                      'pm10 2000', 'pm10 1999', 'pm10 1998', 'pm10 1997', 'pm10 1996',
                      'pm10 1995', 'pm10 1994', 'pm10 1993', 'pm10 1992', 'pm10 1991',
                      'pm10 1990']
    filetype = '.csv'
    files_1990 = [location + '/' + eachfile + filetype for eachfile in filenames_1990]
    files_1980 = [location + '/' + eachfile + filetype for eachfile in filenames_1980]
    dflist_1990 = []
    dflist_1980 = []
    for eachfile in files_1990:
        eachdf = pd.read_csv(eachfile, index_col='Date Local',
                             usecols=['Date Local', '1st Max Value', 'Pollutant Standard', 'City Name'],
                             parse_dates=True)
        dflist_1990.append(eachdf)

    for eachfile in files_1980:
        eachdf = pd.read_csv(eachfile, index_col='Date', usecols=['Date', 'Daily Mean PM10 Concentration'],
                             parse_dates=True)
        dflist_1980.append(eachdf)

    # narrow down the data, and add 80s data to 90s data
    df_1990 = pd.concat(dflist_1990)
    df_1980 = pd.concat(dflist_1980)
    df_1990 = df_1990.loc[df_1990['City Name'] == 'Chicago']
    df_1990 = df_1990.loc[df_1990['Pollutant Standard'] == 'PM10 24-hour 2006']
    df_1990 = df_1990.loc[df_1990['1st Max Value'] >= 0]
    concentration_series = df_1990['1st Max Value'].append(df_1980['Daily Mean PM10 Concentration'])
    date_series = df_1990.index.append(df_1980.index)
    df = pd.DataFrame(concentration_series, index=date_series, columns=['Daily Mean PM10 Concentration'])
    df['Date'] = df.index.date
    df['Month'] = df.index.month
    df['Year'] = df.index.year
    df = df.groupby(['Date']).aggregate(np.median)
    # create monthly and yearly averages for all of the months and years respectively
    df_monthly = df.groupby(['Year', 'Month']).aggregate(np.median)
    df_yearly = df.groupby(['Year']).aggregate(np.median)
    df_monthly_avg = df.groupby(['Month']).aggregate(np.median)

    # plot the data
    def plot_yearly():
        pd.Series.plot(df_yearly['Daily Mean PM10 Concentration'])

    def plot_daily():
        df_wo_dates = df.reset_index()
        print(df_wo_dates[8200:8250])
        pd.Series.plot(df_wo_dates['Daily Mean PM10 Concentration'])
        plt.axvline(886, linewidth=1, color='yellow')  # number of days from 1988 to 1990,
        # when the clean air ammendments were passed
        plt.axvline(6129, linewidth=1, color='yellow')  # number of days from 1988 to 2006,
        # when the annual standard was revoked
        plt.xlabel('days since January 03, 1988')

    def plot_monthly():
        df_wo_months = df_monthly.reset_index()
        pd.Series.plot(df_wo_months['Daily Mean PM10 Concentration'])
        plt.xlabel('months since January, 1988')

    def month_avg():
        pd.Series.plot(df_monthly_avg['Daily Mean PM10 Concentration'])

    def pm10_model(x):
        df_wo_dates = df.reset_index()
        series1 = df_wo_dates['Daily Mean PM10 Concentration'][:886]
        series2 = df_wo_dates['Daily Mean PM10 Concentration'][886:6129]
        if x < 886:
            return np.mean(series1)
        else:
            return np.mean(series2)

    def model_rsqr(function):  # calculate r squared and plot our model
        df_wo_dates = df.reset_index()
        yi = df_wo_dates['Daily Mean PM10 Concentration']
        yavg = np.mean(yi)
        ssres = np.sum([np.power(yi[i] - function(i), 2) for i in range(9332)])
        print(ssres)
        sstot = np.sum([np.power(yi - yavg, 2)])
        print(sstot)
        rsquared = 1 - (ssres/sstot)
        print(rsquared)
        plt.plot(df_wo_dates.index, [function(i) for i in df_wo_dates.index], color='yellow')

    month_avg()
    plt.axhline(150, linewidth=4, color='red')
    plt.title('PM10 air concentration in Chicago (red line indicates dangerous levels)')
    plt.ylabel('ug/m^3')
    plt.show()

historical_pm10()
