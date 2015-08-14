__author__ = 'Ben'
import pandas as pd
import glob


def loadClean(argsDict):
    """This function is a wrapper function that loads a file and cleans it, then returns a clean dataFrame.  Takes an args dictionary,
    the makeup of which is described below
    Takes an args dict, with every key populated, except for dirtyFrame and  returns a cleaned frame."""

    #sets a variable to be the result of cleaning a loaded file
    dfClean=clean(load(argsDict))
    #returns the clean data frame
    return dfClean


def load(argsDict):
    """This function loads the file from a CSV into a pandas DataFrame, it ues the path supplied in the argsDictionary to load a file
    takes an args dict, returns an updated args dict"""

    #In one line, reads a CSV and ads it to the dictionary
    argsDict['dirtyFrame']=pd.read_csv(argsDict['file'])
    #returns the dictionary
    return argsDict


def clean(argsDict):
    """the clean function is really the heart of this program.  Using sets in order to cover all possibilities, it sorts and cleans all CSVs
    that are in a format the EPA data is(and with minimal modification, the urban data as well), and puts it into a clean format, before
    returning the pandas DataFrame.  The format of the columns is [index number, 'Date','Lat','Long','Type','Value','Unit']"""

    #defines a general set consisting of all of the column names of the current dataFrame
    generalSet=set(argsDict['dirtyFrame'].columns.values)
    #Creates a set that is the name of the column that contains the data of interest
    valueSet=generalSet.intersection(argsDict['dataPossible'])
    #Creates a set that contains, by process of elimination, the latitudes
    latSet=generalSet.intersection(argsDict['latPossible'])
    #Creates a set that contains the name of the old Longitude column
    lonSet=generalSet.intersection(argsDict['longPossible'])
    #creates a set that contains the name of the old unit columns
    unitSet=generalSet.intersection(argsDict['unitPossible'])
    #Creates a set that contains the name of the date column
    dateSet=generalSet.intersection(argsDict['datePossible'])
    '''From here down, the process is repeated for each column, so all of these if statements should look similar'''
    #Checks to make sure there is actually a date column
    if dateSet is not None:
        #creates a temporary variable
        newDate=dateSet
        #populates the date column of the output frame
        argsDict['outputFrame']['Date']=argsDict['dirtyFrame'][str(newDate)[2:-2]]
    if valueSet is not None:
        #Temporary variable
        newColumn=valueSet
        #populates the value column of the output frame
        argsDict['outputFrame']['Value']=argsDict['dirtyFrame'][str(newColumn)[2:-2]]
    if latSet is not None:
        #Temporary variable
        newLatitude=latSet
        #populates the latitude column of the output frame
        argsDict['outputFrame']['Lat']=argsDict['dirtyFrame'][str(newLatitude)[2:-2]]
    if lonSet is not None:
        #Temporary variable
        newLongitude=lonSet
        #populates the longitude column of the output frame
        argsDict['outputFrame']['Long']=argsDict['dirtyFrame'][str(newLongitude)[2:-2]]
    if argsDict['dirtyFrame']['Type'] is not None:
        #populates the type column of the output frame
        argsDict['outputFrame']['Type']=argsDict['dirtyFrame']['Type']
    if unitSet is not None:
        #Temporary variable
        newUnit=unitSet
        #populates the Units column of the output frame
        argsDict['outputFrame']['Unit']=argsDict['dirtyFrame'][str(newUnit)[2:-2]]
    return argsDict['outputFrame']


'''This part of the script will be re-implemented in swift, from here down'''

#Sets and loads file paths from a director specified here
path =r'C:\Rdcep Github\EPADataFiles'
allFiles = glob.glob(path + "/*.csv")

#Creates an empty list that will eventually be concatenated into a large dataframe, and then a CSV
list=[]

'''These are all the possible names for columns'''


datePossible=['Date','DATE_LOCAL','DATE','Date_Local', 'Date Local']
dataColumnsPossible=['Daily Mean Pb Concentration','Daily Max 8-Hour Ozone Concentration','Daily Max 8-hour CO Concentration','Daily Mean PM2.5 Concentration','Result','Values', 'Daily Max 1-hour NO2 Concentration', '1st Max Value', 'Daily Max 1-hour SO2 Concentration', 'Daily Mean PM10 Concentration']
newColumns=['Date','Lat','Long','Type','Value','Unit']
latPossible=['SITE_LATITUDE','Latitude']
longPossible=['SITE_LONGITUDE','Longitude']
unitPossible=['UNIT','Units','Unit','UNITS']

'''For this block of code, I am casting the lists into sets, in order to be able to do the set.intersection() function to check which one is needed per file'''

newColumnsSet=set(newColumns)
dataColumnsPossible=set(dataColumnsPossible)
latPossible=set(latPossible)
longPossible=set(longPossible)
unitPossible=set(unitPossible)
datePossible=set(datePossible)


#Here, I define the arguments Dictionary.  Each of the keys are required for the functions above, except dirtyFrame, which load() creates from the file path, and outputFrame, which load() creates
argsDict={'file':None,'dirtyFrame':None,'outputFrame':None,'dataPossible':dataColumnsPossible,'latPossible':latPossible,'longPossible':longPossible,'unitPossible':unitPossible,'datePossible':datePossible}

'''This is the loop that goes through every file in the same directory as before, and loads and cleans every one inside it'''
for file in allFiles:
    #creates empty dataFrame in new, clean format
    dfNew=pd.DataFrame(columns=newColumns)
    #adds new dataframe to dictionary
    argsDict['outputFrame']=dfNew
    #sets the path of the file to be whatever file is currently on
    argsDict['file']=file
    #appends he cleaned file to the empty list from before
    list.append(loadClean(argsDict=argsDict))

#this is the path where the clean CSV will be stored
path2='C:\Rdcep Github\Ben Git Stuff\FinalCSV.csv'
#in one line, this concatenates the clean dataFrames to one dataFrame and then writes to a CSV
pd.concat(list).to_csv(path2)
