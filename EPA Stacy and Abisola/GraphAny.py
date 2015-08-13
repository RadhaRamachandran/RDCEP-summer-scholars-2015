import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('ggplot')

MasterFile06 = pd.read_csv(r'/Users/aolawale/Downloads/MasterFile06.csv', sep=',')
MasterFile06['Date'] = pd.to_datetime(MasterFile06['Date'])
print(MasterFile06)

MFcount = MasterFile06['Parameter Code'].value_counts()                                                                 #counts how many of each parameter there are
print(MFcount)                                                                                                          #shows count of each parameter

def graphAny(df, y):
    yName = np.where(df['Parameter Code'] == y)[0]                                                                      #finds where the param code is in MasterFile06
    yNamedf = df[(yName[0]):(yName[-1]+1)]                                                                              #creates separate DF from MasterFile06 w/ only param
    print(yNamedf['Date'][:1])                                                                                          #prints first date in yNamedf
    print(yNamedf['Date'][-1:])                                                                                         #prints last date in yNamedf
    print(yNamedf['Parameter Description'][:1])                                                                         #prints parameter description
    yNamedf.plot(x='Date', y='Values', kind='line', color='red')                                                        #plotting the new parameter DF
    plt.xlabel('Date')
    yax = input('Enter y-axis label: ')                                                                                 #input whatever you want for y-axis label
    plt.ylabel(yax)                                                                                                     #whatever the input is is what y-axis label is
    #plt.ylabel(yNamedf['Parameter Description'][:1])
    gTitle = input('Enter title: ')                                                                                     #similar to y-axis label...
    plt.title(gTitle)                                                                                                   #whatever the input is is what title is
    referenceLine = input('Does this graph need a reference line? ')
    while referenceLine != 'no':                                                                                        #while statement loops if user doesn't enter 'no'
        yRefL = float(input('Enter y value for reference line: '))                                                      #input whatever number you want ref line to be
        labelRefl = input('Enter reference line description: ')                                                         #input description of line color
        lineColor = input('Enter color for reference line: ')                                                           #input color of reference line
        plt.axhline(y=yRefL, xmin=0, xmax=1, linewidth=1.5, color=lineColor, label=labelRefl)
        plt.legend()
        done = input('Done? ')                                                                                          #are you done w/ reference lines?
        if done == 'yes':                                                                                               #if yes show plot and stop looping through statement
            plt.show()
            break

    plt.show()


df = MasterFile06
y= 530
graphAny(df, y)








