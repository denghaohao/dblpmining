"""
this script is used to prepare the database, especially calculating some
static information
"""

import os
import sqlite3
import sys

''' where is the database? '''
currpath = os.path.abspath(__file__)

''' locate the parent folder '''
dbaddr = os.path.dirname(os.path.dirname(currpath))
dbaddr = (dbaddr + '/') if dbaddr != '' else './'
dbaddr += 'dataset/'

''' which file ? '''
if len(sys.argv) > 1:
    dbaddr += sys.argv[1] + '.sqlite'
else:
    dbaddr += 'default.sqlite'

''' start database connection '''
dbconn = None
try:
    dbconn = sqlite3.connect(dbaddr)
except:
    # failed to open the database
    print 'failed to connect database', dbaddr
    exit(1)

dbcursor = dbconn.cursor()
print 'data will be stored in', dbaddr

''' initialization of database '''
try:
    dbcursor.execute('DROP TABLE authors')
except:
    ''' no existing table is dropped '''

dbcursor.execute('''
CREATE TABLE authors (
    name varchar(255),
    first_paper int(20),
    amount_paper int(20)
)
''')

''' how many items we've found '''
dbcursor.execute('select distinct author, year from dblp order by year')
records = dbcursor.fetchall()

info = {}

for rec in records:
    authors = rec[0].split(',')
    if '' in authors:
        authors.remove('')
    for author in authors:
        if author not in info:
            info[author] = {
                'start': rec[1],
                'amount': 1
            }
        else:
            info[author]['amount'] += 1


for name in info:
    dbcursor.execute(
        'INSERT INTO authors (name, first_paper, amount_paper) VALUES ("%s", %d, %d)' %
        (name, info[name]['start'], info[name]['amount'])
    )


dbconn.commit()
dbconn.close()
print 'static information generation finished.'
