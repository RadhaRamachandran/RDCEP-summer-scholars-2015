__author__ = 'Ben'
import glob
import pandas as pd
<<<<<<< HEAD
from sqlalchemy import create_engine
=======
import sys
>>>>>>> 46f7e5fc2e731fd4bb502d53dee3f0418a5aef25

#path =sys.argv[1]
path='C:\Rdcep Github\EPADataFiles'
allFiles = glob.glob(path + "/*.csv")
frame = pd.DataFrame()
list_ = []
for file_ in allFiles:
<<<<<<< HEAD
    df = pd.read_csv(file_)
    df2 = pd.read_csv(file_)
    list_.append(df)
frame = pd.concat(list_)

low_memory= False


engine = create_engine('mysql://root:1234@localhost:111')
path2='C:\Rdcep Github\Ben Git Stuff\\finalDB.sql'
frame.to_sql(name='name' , con=engine, flavor='sqlite', schema=None, if_exists='fail', index=True, index_label=None, chunksize=None, dtype=None)
=======
    df = pd.read_csv(file_,index_col=['Date'],parse_dates=['Date'])
    df2 = pd.read_csv(file_)
    list_.append(df)
frame = pd.concat(list_)
path2='C:\Rdcep Github\Ben Git Stuff\\finalDB.sql'
frame.to_sql(name=path2, con='SQLAlchemy engine', flavor='sqlite', schema=None, if_exists='fail', index=True, index_label=None, chunksize=None, dtype=None)
>>>>>>> 46f7e5fc2e731fd4bb502d53dee3f0418a5aef25
