import pandas as pd

from matplotlib import pyplot as plt
import numpy as np
import matplotlib
import vincent as vc


import glob


matplotlib.style.use('ggplot')


path =r'C:\Rdcep Github\Ben Git Stuff\DataFilesLead'
allFiles = glob.glob(path + "/*.csv")
frame = pd.DataFrame()
list_ = []
list2=[]
for file_ in allFiles:
    df = pd.read_csv(file_,index_col=['Date'],parse_dates=['Date'])
    df2 = pd.read_csv(file_)
    list_.append(df)
    list2.append(df2)
frame = pd.concat(list_)
frame['Type']=['Air-Lead']*len(frame.index)
print(frame.head())


def makeYearlyAverage(frame):
    columns = ['Year', 'Avezrage']
    averageDict=pd.DataFrame(data=np.zeros((0,len(columns))), columns=columns)
    for year in range(1980,2015,1):
        tempAverage=0
        i2=0
        for f in range(len(frame.index)):
            print(frame['Date'][f][-4:])
            if str(frame['Date'][f][-4:])==str(year):
                tempAverage+=frame['Daily Mean Pb Concentration'][f]
                i2+=1
        tempAverage=tempAverage/i2
        averageDict['Year'][year-1980] = year
        averageDict['Average'][year-1980]=tempAverage
    return averagesDict


def meanYearly(frame):
    averageList=[]
    for year in range(1980,2015,1):
        for f in range(len(frame.index)):
            tempAverage=np.empty(0)
            if str(frame['Date'][f][-4:])==str(year):
                np.append(tempAverage,frame['Daily Mean Pb Concentration'][f])
                averageList.append(np.mean(tempAverage))
                print(tempAverage)
    return averageList

#meanYearly(frame=frame2)


'''
i=0
frame['Year']=''
years=[]
for a in frame.iterrows():
    if not i>=1955:
        frame['Year'][i]=
    i+=1
print(years)

#frame['Year']=years
'''
df3=frame['Daily Mean Pb Concentration']
df3.plot(label="Measured Lead Level")
plt.title('Daily Lead Levels for 1980-2015 in Cook County, IL')
plt.xlabel('Date')
plt.ylabel('Lead Concentration in Air (ug/m3)')
plt.axhline(y=.15, xmin=0, xmax=1, linewidth=2, color = 'b',label='Dangerous Lead Level')
plt.legend()
plt.show()
df4=pd.read_csv('C:\\Users\Ben\Desktop\leadGas.csv',index_col='year')
df4.plot()
plt.show()
#df5=frame.as_matrix(columns=['Date','Daily Mean Pb Concentration'])


