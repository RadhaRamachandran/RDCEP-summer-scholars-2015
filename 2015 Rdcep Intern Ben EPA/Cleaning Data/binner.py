__author__ = 'Ben'
import pandas as pd

frame1=pd.read_csv("C:\Rdcep Github\Rdcep-summer-scholars-2015\Ben Git Stuff\MaybeGeocodedTalliesHopefullyPleaseFinal.csv")
frame2=pd.read_csv("C:\\Users\Ben\Downloads\City Data Spreadsheet - LawnConditions.csv")
grouped = frame2.groupby(['BlockNameBegin','LawnCondition'])
grouped2 = frame1.groupby(['BlockNameBegin'])
newColumns=['Location','0','1','2']
dfNew=pd.DataFrame(columns=newColumns)

for index, group in grouped:
    number=str(len(group))
    type='0'
    location=group['BlockNameBegin']
    if type=='0':
        dfNew.append([[location,number,'0','0']],ignore_index=True)
    elif type=='1':
        dfNew.append([[location,'0',number,'0']],ignore_index=True)
    elif type=='2':
        dfNew.append([[location,'0','0',number]],ignore_index=True)
print dfNew
