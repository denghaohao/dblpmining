'''
this file is used to simplify the query process from the database
'''

import os
import sqlite3

''' where to store the data? '''
currpath = os.path.abspath(__file__)

''' locate the parent folder '''
dbpath = os.path.dirname(os.path.dirname(currpath)) + "/dataset/"


def query(dbname, sql):
    # initialize the sqlite connection
    dbaddr = dbpath + dbname + '.sqlite'
    dbconn = sqlite3.connect(dbaddr)
    cursor = dbconn.cursor()

    # locating the data records
    cursor.execute(sql)
    data = cursor.fetchall()

    # close the connection
    cursor.close()
    dbconn.close()

    return data
