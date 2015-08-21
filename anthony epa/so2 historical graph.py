import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def historical_so2():
    # loads the data into pandas dataframe
    location = "C:/Anthony/RDCEP things/so2 data"
    filenames_1980 = ['so2 1989', 'so2 1988', 'so2 1987', 'so2 1986', 'so2 1985',
                      'so2 1984', 'so2 1983', 'so2 1982', 'so2 1981', 'so2 1980',]
    filenames_1990 = ['so2 2015', 'so2 2014', 'so2 2013', 'so2 2012', 'so2 2011',
                      'so2 2010', 'so2 2009', 'so2 2008', 'so2 2007', 'so2 2006',
                      'so2 2005', 'so2 2004', 'so2 2003', 'so2 2002', 'so2 2001',
                      'so2 2000', 'so2 1999', 'so2 1998', 'so2 1997', 'so2 1996',
                      'so2 1995', 'so2 1994', 'so2 1993', 'so2 1992', 'so2 1991',
                      'so2 1990']
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
        eachdf = pd.read_csv(eachfile, index_col='Date', usecols=['Date', 'Daily Max 1-hour SO2 Concentration'],
                             parse_dates=True)
        dflist_1980.append(eachdf)

    # narrow down the data, and add 80s data to 90s data
    df_1990 = pd.concat(dflist_1990)
    df_1980 = pd.concat(dflist_1980)
    df_1990 = df_1990.loc[df_1990['City Name'] == 'Chicago']
    df_1990 = df_1990.loc[df_1990['Pollutant Standard'] == 'SO2 1-hour 2010']
    df_1990 = df_1990.loc[df_1990['1st Max Value'] >= 0]
    concentration_series = df_1990['1st Max Value'].append(df_1980['Daily Max 1-hour SO2 Concentration'])
    date_series = df_1990.index.append(df_1980.index)
    df = pd.DataFrame(concentration_series, index=date_series, columns=['Daily Max 1 hour SO2 Conc.'])
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
        pd.Series.plot(df_yearly['Daily Max 1 hour SO2 Conc.'])

    def plot_daily():
        df_wo_dates = df.reset_index()
        pd.Series.plot(df_wo_dates['Daily Max 1 hour SO2 Conc.'])
        plt.axvline(3966, linewidth=1, color='yellow')  # number of days from 1980 to 1990,
        # when the clean air ammendments were passed
        plt.axvline(10953, linewidth=1, color='green')  # number of days from 1980 to 2010,
        # when the new SO2 1 hr standards were placed
        plt.axvline(5474, linewidth=1, color='black')  # number of days from 1980 to 1995,
        # when the acid rain program started

    def plot_monthly():
        df_wo_months = df_monthly.reset_index()
        pd.Series.plot(df_wo_months['Daily Max 1 hour SO2 Conc.'])
        plt.axvline(131, linewidth=1, color='yellow')  # number of months till caa
        plt.axvline(180, linewidth=1, color='green')  # number of months till arp
        plt.axvline(360, linewidth=1, color='black')  # number of months till standard
        plt.xlabel('months since January, 1980')

    def monthly_avg():
        pd.Series.plot(df_monthly_avg['Daily Max 1 hour SO2 Conc.'])

    def null_hyp():  # This calculates the null hypothesis, ie, that concentration does not change
        df_wo_dates = df.reset_index()
        yi = df_wo_dates['Daily Max 1 hour SO2 Conc.']
        x =[0, 12768]
        y = [np.mean(df['Daily Max 1 hour SO2 Conc.']), np.mean(df['Daily Max 1 hour SO2 Conc.'])]
        plt.plot(x, y, color='yellow')
        yavg = np.mean(yi)
        ssres = np.sum([np.power(yi[i] - np.mean(df['Daily Max 1 hour SO2 Conc.']), 2) for i in range(12768)])
        sstot = np.sum([np.power(yi - yavg, 2)])
        rsquared = 1 - (ssres/sstot)
        print(rsquared)  # the rsquared for the null hypothesis will always be zero
        # because the model is simply the average

    def our_model(x):  # this is our model, which assumes that the concentration is lower after key EPA regulations
        df_wo_dates = df.reset_index()
        series1 = df_wo_dates['Daily Max 1 hour SO2 Conc.'][:3966]
        series2 = df_wo_dates['Daily Max 1 hour SO2 Conc.'][3966:5474]
        series3 = df_wo_dates['Daily Max 1 hour SO2 Conc.'][5747:10953]
        series4 = df_wo_dates['Daily Max 1 hour SO2 Conc.'][10953:12768]
        if x < 3966:
            return np.mean(series1)
        elif 3966 <= x < 5474:
            return np.mean(series2)
        elif 5474 <= x < 10953:
            return np.mean(series3)
        else:
            return np.mean(series4)

    def model_rsqr():  # calculate r squared and plot our model
        df_wo_dates = df.reset_index()
        yi = df_wo_dates['Daily Max 1 hour SO2 Conc.']
        yavg = np.mean(yi)
        ssres = np.sum([np.power(yi[i] - our_model(i), 2) for i in range(12768)])
        print(ssres)
        sstot = np.sum([np.power(yi - yavg, 2)])
        print(sstot)
        rsquared = 1 - (ssres/sstot)
        print(rsquared)
        plt.plot(df_wo_dates.index, [our_model(i) for i in df_wo_dates.index], color='yellow')

    monthly_avg()
    plt.axhline(75, linewidth=4, color='red')
    plt.title('SO2 air concentration in Chicago (red line indicates dangerous levels)')
    plt.ylabel('part per billion')
    plt.show()

historical_so2()