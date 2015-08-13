__author__ = 'Ben'
import pandas as pd


class cleaner:
    def loadClean(argsDict):
        dfClean=clean(load(argsDict))
        return dfClean

    def load(argsDict):
        df=pd.read_csv(argsDict['file'])
        argsDict['dirtyFrame']=pd.read_csv(argsDict['file'])
        return argsDict

    def clean(argsDict):
        generalSet=set(argsDict['dirtyFrame'].columns.values)
        valueSet=generalSet.intersection(argsDict['dataPossible'])
        latSet=generalSet.intersection(argsDict['latPossible'])
        lonSet=generalSet.intersection(argsDict['longPossible'])
        unitSet=generalSet.intersection(argsDict['unitPossible'])
        if valueSet is not None:
            newColumn=valueSet
            argsDict['outputFrame']['Value']=argsDict['dirtyFrame'][str(newColumn)]
        if latSet is not None:
            newLatitude=latSet
            argsDict['outputFrame']['Lat']=argsDict['dirtyFrame'][str(newLatitude)]
        if lonSet is not None:
            newLongitude=lonSet
            argsDict['outputFrame']['Lon']=argsDict['dirtyFrame'][str(newLongitude)]
        if argsDict['dirtyFrame']['Type'] is not None:
            argsDict['outputFrame']['Type']=argsDict['dirtyFrame']['Type']
        if unitSet is not None:
            newUnit=unitSet
            argsDict['outputFrame']['Unit']=argsDict['dirtyFrame'][str(newUnit)]

        return argsDict['outputFrame']

    path =r'C:\Rdcep Github\EPADataFiles'
    allFiles = glob.glob(path + "/*.csv")
    list=[]

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

    argsDict={'file':None,'dirtyFrame':None,'outputFrame':None,'dataPossible':dataColumnsPossible,'latPossible':latPossible,'longPossible':longPossible,'unitPossible':unitPossible}

    for file in allFiles:
        dfNew=pd.DataFrame(columns=newColumns)
        argsDict['outputFrame']=dfNew
        argsDict['file']=file
        list.append(loadClean(argsDict=argsDict))
    path2='C:Ben\Rdcep Github\EPADataFiles\FinalCSV.csv'
    pd.concat(list).to_csv(path2)
