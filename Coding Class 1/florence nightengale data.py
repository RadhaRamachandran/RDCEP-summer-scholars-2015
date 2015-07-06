import matplotlib.pyplot as plt
import pandas as pd


def bargraph2():
    location = 'FlorenceN.csv'
    df = pd.read_csv(location, names=['deaths', 'dates'], index_col='dates', skiprows=1)
    deaths = df['deaths']
    pd.Series.plot(deaths, kind='bar', color='red')
    plt.ylabel('deaths from zymotic diseases')
    plt.xlabel('date')
    plt.show()
bargraph2()
