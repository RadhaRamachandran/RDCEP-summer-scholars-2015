__author__ = 'Ben'
import glob
import pandas as pd
import sys

#path =sys.argv[1]
path='C:\Rdcep Github\EPADataFiles'
allFiles = glob.glob(path + "/*.csv")
frame = pd.DataFrame()
list_ = []
for file_ in allFiles:
    df = pd.read_csv(file_,index_col=['Date'],parse_dates=['Date'])
    df2 = pd.read_csv(file_)
    list_.append(df)
frame = pd.concat(list_)
path2='C:\Rdcep Github\Ben Git Stuff\\finalDB.sql'
frame.to_sql(name=path2, con='SQLAlchemy engine', flavor='sqlite', schema=None, if_exists='fail', index=True, index_label=None, chunksize=None, dtype=None)