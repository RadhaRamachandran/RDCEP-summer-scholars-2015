
#do all of this from swift
__author__ = 'Ben'
import pandas as pd
import glob


#dirtyFrame,outputFrame,dataPossible,latPossible,longPossible,unitPossible

dataColumnsPossible=['Daily Mean Pb Concentration','Daily Max 8-Hour Ozone Concentration','Daily Max 8-hour CO Concentration','Daily Mean PM2.5 Concentration','Result','Values',]
newColumns=['Date','Lat','Long','Type','Value','Unit']
latPossible=['SITE_LATITUDE','Latitude']
longPossible=['SITE_LONGITUDE','Longitude']
unitPossible=['ppm','ppb','ug/m3','DEG C','DEG F','CFS','JTU','IN','M','uS/CM','MG/L','MG/KG','S.U.','PPT','UG/L','NS','NU','#/100ML','MPN/100ML','UG/KG','MMOL/KG','MG/KG','DAYS','CFS','% BY WT','NTU','m']
newColumnsSet=set(newColumns)
dataColumnsPossible=set(dataColumnsPossible)
latPossible=set(latPossible)
longPossible=set(longPossible)
unitPossible=set(unitPossible)

path =r'C:\Rdcep Github\EPADataFiles'
allFiles = glob.glob(path + "/*.csv")
list=[]

argsDict={'file':None,'dirtyFrame':None,'outputFrame':None,'dataPossible':dataColumnsPossible,'latPossible':latPossible,'longPossible':longPossible,'unitPossible':unitPossible,'datePossible':datePossible}

for file in allFiles:
    dfNew=pd.DataFrame(columns=newColumns)
    argsDict['outputFrame']=dfNew
    argsDict['file']=file
    list.append(Cleaner.loadClean(argsDict=argsDict))
path2='C:Ben\Rdcep Github\EPADataFiles\FinalCSV.csv'
pd.concat(list).to_csv(path2)

#in swift, run the php script