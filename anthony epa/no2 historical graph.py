import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def historical_no2():
    # loads the data into pandas dataframe
    location = "C:/Anthony/RDCEP things/no2 data"
    filenames_1980 = ['no2 1989', 'no2 1988', 'no2 1987', 'no2 1986', 'no2 1985',
                      'no2 1984', 'no2 1983', 'no2 1982', 'no2 1981', 'no2 1980']
    filenames_1990 = ['no2 2015', 'no2 2014', 'no2 2013', 'no2 2012', 'no2 2011',
                      'no2 2010', 'no2 2009', 'no2 2008', 'no2 2007', 'no2 2006',
                      'no2 2005', 'no2 2004', 'no2 2003', 'no2 2002', 'no2 2001',
                      'no2 2000', 'no2 1999', 'no2 1998', 'no2 1997', 'no2 1996',
                      'no2 1995', 'no2 1994', 'no2 1993', 'no2 1992', 'no2 1991',
                      'no2 1990']
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
        eachdf = pd.read_csv(eachfile, index_col='Date', usecols=['Date', 'Daily Max 1-hour NO2 Concentration'],
                             parse_dates=True)
        dflist_1980.append(eachdf)

    # narrow down the data, and add 80s data to 90s data
    df_1990 = pd.concat(dflist_1990)
    df_1980 = pd.concat(dflist_1980)
    df_1990 = df_1990.loc[df_1990['City Name'] == 'Chicago']
    df_1990 = df_1990.loc[df_1990['Pollutant Standard'] == 'NO2 1-hour']
    df_1990 = df_1990.loc[df_1990['1st Max Value'] >= 0]
    concentration_series = df_1990['1st Max Value'].append(df_1980['Daily Max 1-hour NO2 Concentration'])
    date_series = df_1990.index.append(df_1980.index)
    df = pd.DataFrame(concentration_series, index=date_series, columns=['Daily Max 1 hour NO2 Conc.'])
    df['Date'] = df.index.date
    df['Month'] = df.index.month
    df['Year'] = df.index.year
    df = df.groupby(['Date']).aggregate(np.median)

    # create monthly and yearly averages for all of the months and years respectively
    df_monthly = df.groupby(['Year', 'Month']).aggregate(np.median)
    df_yearly = df.groupby(['Year']).aggregate(np.median)
    df_monthly_avg = df.groupby(['Month']).aggregate(np.median)

    # line of bestfit and r squared for yearly data
    def yearly_bestfit():
        xi = df_yearly.index
        yi = df_yearly['Daily Max 1 hour NO2 Conc.']
        coeffs = np.polyfit(xi, yi, deg=1)
        x = np.array([1980, 2015])
        y = x*coeffs[0] + coeffs[1]
        plt.plot(x, y, color='yellow')
        p = np.poly1d(coeffs)
        print(p)
        yavg = np.mean(yi)
        ssres = np.sum([np.power(yi - p(xi), 2)])
        sstot = np.sum([np.power(yi - yavg, 2)])
        rsquared = 1 - (ssres/sstot)
        print(rsquared)

    # line of bestfit and r squared for daily data
    def daily_bestfit():
        df_wo_dates = df.reset_index()
        yi = df_wo_dates['Daily Max 1 hour NO2 Conc.']
        coeffs = np.polyfit(range(12849), yi, deg=1)
        x = np.array([0, 12848])
        y = x*coeffs[0] + coeffs[1]
        pd.Series.plot(df_wo_dates['Daily Max 1 hour NO2 Conc.'])
        plt.xlabel('days since 1980')
        plt.axvline(3947, linewidth=1, color='yellow')
        plt.axvline(10955, linewidth=1, color='green')
        plt.plot(x, y, color='yellow')
        p = np.poly1d(coeffs)
        yavg = np.mean(yi)
        ssres = np.sum([np.power(yi[i] - p(i), 2) for i in range(12849)])
        sstot = np.sum([np.power(yi - yavg, 2)])
        rsquared = 1 - (ssres/sstot)
        print(rsquared)

    # here is our new model, one that finds the average before, between, and after
    # the clean air act of 1990 and the setting of the new no2 1 hour standard in 2010
    def no2_model(x):
        df_wo_dates = df.reset_index()
        series1 = df_wo_dates['Daily Max 1 hour NO2 Conc.'][:3957]
        series2 = df_wo_dates['Daily Max 1 hour NO2 Conc.'][3957:10955]
        series3 = df_wo_dates['Daily Max 1 hour NO2 Conc.'][10955:12768]
        if x < 3957:
            return np.mean(series1)
        elif 3957 <= x < 10955:
            return np.mean(series2)
        else:
            return np.mean(series3)

    # calculate r squared for our new model;
    def no2_model_daily():
        df_wo_dates = df.reset_index()
        yi = df_wo_dates['Daily Max 1 hour NO2 Conc.']
        yavg = np.mean(yi)
        ssres = np.sum([np.power(yi[i] - no2_model(i), 2) for i in range(12849)])
        sstot = np.sum([np.power(yi - yavg, 2)])
        rsquared = 1 - (ssres/sstot)
        pd.Series.plot(df_wo_dates['Daily Max 1 hour NO2 Conc.'])
        plt.xlabel('days since 1980')
        plt.axvline(3947, linewidth=1, color='yellow')
        plt.axvline(10955, linewidth=1, color='green')
        plt.plot(df_wo_dates.index, [no2_model(i) for i in df_wo_dates.index], color='yellow')
        print(rsquared)

    # plot the various data
    def plot_yearly():
        pd.Series.plot(df_yearly['Daily Max 1 hour NO2 Conc.'])

    def plot_daily():
        pd.Series.plot(df['Daily Max 1 hour NO2 Conc.'])
        plt.axvline('1990-11-15', linewidth=1, color='yellow')
        plt.axvline('2010-01-22', linewidth=1, color='green')

    def plot_monthly():
        pd.Series.plot(df_monthly['Daily Max 1 hour NO2 Conc.'])

    def monthly_avg():
        pd.Series.plot(df_monthly_avg['Daily Max 1 hour NO2 Conc.'])

    no2_model_daily()
    plt.axhline(100, linewidth=4, color='red')
    plt.title('NO2 air concentration in Chicago (red line indicates dangerous levels)')
    plt.ylabel('part per billion')
    plt.show()
historical_no2()
