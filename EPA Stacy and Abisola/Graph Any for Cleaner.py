import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')


def graphAny(df, y):
    yName = np.where(df['Type'] == y)[0]                                                                                #finds where the param code is in MasterFile06
    yNamedf = df[(yName[0]):(yName[-1]+1)]                                                                              #creates separate DF from MasterFile06 w/ only param
    print(yNamedf['Date'][:1])                                                                                          #prints first date in yNamedf
    print(yNamedf['Date'][-1:])                                                                                         #prints last date in yNamedf
    print(yNamedf['Type'][:1])                                                                                          #prints parameter description
    yNamedf.plot(x='Date', y='Value', kind='line', color='red')                                                        #plotting the new parameter DF
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
        plt.axhline(y=yRefL, xmin=0, xmax=yRefL, linewidth=1.5, color=lineColor, label=labelRefl)
        plt.legend()
        done = input('Done? ')                                                                                          #are you done w/ reference lines?
        if done == 'yes':
            '''
            verticalRefL = input('Does this graph need a vertical reference line? ')
            while verticalRefL != 'no':
                vRefl = float(input('Enter value for vertical reference line: '))
                labelvRefl = input('Enter vertical reference line description: ')
                vlineColor = input('Enter color for reference line: ')
                plt.axvline(x=vRefl, ymin=0, ymax=1, linewidth=1.5, color=vlineColor, label=labelvRefl)
                plt.legend()
                doneFinal = input('Done with vertical line? ')
                if doneFinal == 'yes':
                    plt.show()
                    break
            plt.show()
            break
    verticalRefL2 = input('Does this graph need a vertical reference line? ')
    while verticalRefL2 != 'no':
        vRefl2 = float(input('Enter value for vertical reference line: '))
        labelvRefl2 = input('Enter vertical reference line description: ')
        vlineColor2 = input('Enter color for reference line: ')
        plt.axvline(x=vRefl2, ymin=0, ymax=1, linewidth=1.5, color=vlineColor2, label=labelvRefl2)
        plt.legend()
        doneFinal2 = input('Done? ')
        if doneFinal2 == 'yes':
        '''
            plt.show()
            break
    plt.show()

allFiles = pd.read_csv(r'/Users/aolawale/Downloads/FinalCSVREAL.csv', parse_dates=['Date'])
allFiles = allFiles.drop(['Unnamed: 0'], axis=1)
allFiles = allFiles.sort(['Type', 'Date'], ascending=[True, True])
#print(allFiles)
s = np.where(allFiles['Type'] == 'Water-Total Coliforms')
print(s)
newFile = allFiles[17496512:17497673]
print(newFile)

'''
y = 'Water-Total Coliforms'
df = allFiles
graphAny(df, y)
'''