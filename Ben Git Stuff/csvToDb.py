import argparse
import csv
import getpass
import MySQLdb
import os
import re

###############################################################################
def dbInit(username, password, hostname, database, bDbEnable = True):
    if bDbEnable:
        #  use parameters from the default file
        # con = MySQLdb.connect(read_default_file="~/.my.cnf")
        con = MySQLdb.connect(user=username, passwd=password, host=hostname, db = database,
                    charset='utf8', use_unicode=True)  # essential for proper handling of unicode characters
        
        # create a Cursor object to execute queries
        cur = con.cursor()
        # print con.get_character_set_info()
    else:
        con = None
        cur = None
    return (con, cur)
###############################################################################
def dbExit(con, cur):
    cur.close()
    con.commit()
    con.close()
    
###############################################################################
def dbCmd(cmd, bForceExecute=False, bOutput=False, bPrint=True):
    bPrintOnly = False  # set to true to print, but not execute, commands
    output = ''
    
    if bPrint:
        print ('"%s"' % cmd)
        
    if cur is not None:
        if (bPrintOnly != True) or bForceExecute:
            cur.execute(cmd)
            if bOutput:
                output = cur.fetchall()
                if bPrint:
                    print(output)
    return output
###############################################################################
def dbCmdFast(cmd):
    cur.execute(cmd)

###############################################################################
# convert the csv filename to a valid table name,
# Also convert csv file's column names uniformly to camel-hump style
###############################################################################
def FixName(s):
    # remove the ".csv" at the end (or '.CSV', and any trailing whitespace before end of string)
    s = re.sub('\.[cC][sS][vV]\s*$', ' ', s)
    
    # break up underscore-separated words and illegal characters to spaces
    s = re.sub('[_\.\?]', ' ', s)
    
    # insert a space between a lower-case followed by an upper-case (mixed case implies word break)
    s = re.sub('([a-z])([A-Z])', '\g<1> \g<2>', s)    
    
    # split by white space
    l = s.split()
    
    #capitalize the 1st letter of each word - as in a Title
    l = [ss.title() for ss in l]
    
    # join all the pieces
    s = ''.join(l)
    
    # first word/letter is lower case
    s = s[0].lower() + s[1:]
    
    return s
    

    
###############################################################################
if __name__ == "__main__":
    # Get arguments from the command-line
    argParser = argparse.ArgumentParser()
    argParser.add_argument('inCsvFilename')
    argParser.add_argument('db')
    argParser.add_argument('outTable')

    argParser.add_argument("-delim", default = ',', help = "delimiter",
                                    action = "store")
    argParser.add_argument("-i", help="create an 'id' field, AUTO_INCREMENT",
                                    action="store_true")
    argParser.add_argument("-u", "--username", default="root", help="username for database",
                                    action="store")
    argParser.add_argument("-host", "--host", default=None, help="host IP for database",
                                    action="store")
    argParser.add_argument("-p", help="prompt for password for database",
                                    action="store_true")
    argParser.add_argument("-numValuesPerInsert", default = 300, help="# of values in each SQL insert command",
                                    action="store")
    argParser.add_argument("--password", default=None, help="password for database specified on command line",
                                    action="store")
    argParser.add_argument("-table_literal", help="table name will be cleaned unless this flag is set",
                                    action="store_true")
    argParser.add_argument("-v", "--verbose", help="verbose - prints more debug info",
                                    action="store_true")
    argsParsed = argParser.parse_args()
    print('argsParsed = ', argsParsed)
    if False:   # test the name fixing - small camel hump
        for a in ['the first one', "SECOND_NAME_BILL", 'x', 'has.period oh no', "JOE_blow9393_", 'two separate', 'all88lower', 'catSkills', 'filename.csv.and.csv', 'fileAnd space.csv ']:
            print(a, FixName(a))
    
    if argsParsed.p:
        argsParsed.password = getpass.getpass('Enter password for database: ')
    
    outTable = argsParsed.outTable
    if not argsParsed.table_literal:
        outTable = FixName(outTable)
        
    # open database cursor
    dbCon, cur = dbInit(argsParsed.username, argsParsed.password, hostname = argsParsed.host, database = argsParsed.db)

    # open the CSV file - read the 1st line to get the headings, which will be column names
    csv.register_dialect('myDialect', delimiter = argsParsed.delim, quotechar='"', doublequote = True)

    with open(argsParsed.inCsvFilename, 'rb') as fIn:
        csvReader = csv.reader(fIn, dialect = 'myDialect')
        # read headings
        headings = csvReader.next()
        headings = [FixName(h) for h in headings]
        nCol = len(headings)
        print(nCol, ' headings:', headings)
        # translate each line
        lengths = [0 for _ in headings]
    # scan the data to form the CREATE TABLE types
        try:
            for iRow, row in enumerate(csvReader):
                lengths = [max(lengths[i], len(row[i])) for i in xrange(nCol)]
                #for iCol, col in enumerate(row):
                #    pass
                    #print iCol, col
                    #print '.....', MySQLdb.escape_string(col)
        except:
            print( 'iRow = ', iRow)
        print ('lengths:', lengths)
    # CREATE TABLE
    dbCmd('DROP TABLE IF EXISTS ' + outTable)
    cmdList = ['CREATE TABLE ' + outTable + ' (']
    if argsParsed.i:
        cmdList.append('id INT NOT NULL AUTO_INCREMENT, ')
    for iHeading, heading in enumerate(headings):
        cmdList.append(headings[iHeading])
        if lengths[iHeading] > 60:
            cmdList.append(' TEXT ')
        else:
            cmdList.append(' VARCHAR(%d)' % (lengths[iHeading] + 1))
        cmdList.append(', ')
    del cmdList[-1] # remove the last comma
    if argsParsed.i:
        cmdList.append(", PRIMARY KEY (id)")

    cmdList.append(') ENGINE = MYISAM, CHARACTER SET utf8 COLLATE utf8_unicode_ci;')
    cmd = ''.join(cmdList)
    dbCmd(cmd)
    
    # LOCK TABLE
    dbCmd('LOCK TABLES ' + outTable + ' WRITE')
    
    # send the data through a series of INSERTs
    nLinesPerCommand = int(argsParsed.numValuesPerInsert)
    headingCommas = ','.join(headings)
    with open(argsParsed.inCsvFilename, 'rU') as fIn:
        csvReader = csv.reader(fIn, dialect = 'myDialect')
        csvReader.next()      # skip the header line
        iLineTotal = 0
        iLine = 0
        while True:   #for limit in xrange(3):         # read chunks of lines until file is exhausted
            iLineTotal += iLine
            print('iLineTotal: ', iLineTotal)
            str0 = 'INSERT INTO ' + outTable + '(' + headingCommas + ') VALUES ('
            iLine = 0
            try:
                for iLine, line in enumerate(csvReader):
                    nColCur = len(line)
                    if nColCur == nCol:
                        lineText =  ','.join(['"' + MySQLdb.escape_string(value.strip().decode('utf8', 'replace').encode('utf8', 'replace')) + '"' for value in line])
                    elif  nColCur < nCol:
                        print('line #{} has {} columns (should have {})!!!!!:'.format(iLine, nColCur, nCol), line)
                        lineText =  ','.join(['"' + MySQLdb.escape_string(value.strip().decode('utf8', 'replace').encode('utf8', 'replace')) + '"' for value in line])
                        lineText += (', NULL' * (nCol - nColCur))   # append NULL for each missing value
                    else: #if nColCur > nCol:
                        print( 'line #{} has {} columns (should have {})!!!!!:'.format(iLine, nColCur, nCol), line)
                        lineText =  ','.join(['"' + MySQLdb.escape_string(value.strip().decode('utf8', 'replace').encode('utf8', 'replace')) + '"' for value in line[:nCol]])
                        
                    if iLine == 0:
                        cmdList = [str0, lineText]  
                    else:
                        cmdList.append('), (' + lineText)
                        if iLine >= nLinesPerCommand:
                            break
            except:
                print('EXCEPT: iLine = ', iLine)
            if iLine > 0:
                cmdList.append(');')
                dbCmdFast(''.join(cmdList))         #dbCmdFast
                #dbCmd(''.join(cmdList), bPrint = True)         #dbCmdFast
            else:
                break       # file is exhausted

    # UNLOCK TABLE
    dbCmd('UNLOCK TABLES')
    
    # flush the db channel and close
    dbExit(dbCon, cur)
    
    
    
    

