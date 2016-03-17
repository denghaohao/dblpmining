'''
this script is used to obtain xml data from dblp.org and save it to
a local database
'''

import urllib
import sys
import os
import sqlite3
import json

''' we obtain no more than MAXITEM papers in a single query '''
MAXITEM = 1000

sourcetype = 'conference'
venues = ['facs', 'fm']
apiaddr = 'http://dblp.org/search/api/?q='

''' where to store the data? '''
dbaddr = os.path.dirname(os.path.dirname(__file__))
dbaddr = (dbaddr + '/') if dbaddr != '' else './'
dbaddr += 'dataset/'

''' which file ? '''
if len(sys.argv) > 1:
    dbaddr += sys.argv[1] + '.sqlite'
else:
    dbaddr += 'default.sqlite'

''' start database connection '''
dbconn = sqlite3.connect(dbaddr)
dbcursor = dbconn.cursor()
print 'data will be stored in', dbaddr

''' initialization of database '''
try:
    dbcursor.execute('DROP TABLE dblp')
except:
    ''' no existing table is dropped '''

dbcursor.execute('''
CREATE TABLE dblp (
    title varchar(255),
    authors varchar(255),
    venue varchar(255),
    year int(20)
)
''')

for venue in venues:
    url = apiaddr + 'ce:type:%s:* ce:venue:%s:*&h=%d&c=4&f=0&format=json' \
        % (sourcetype, venue, MAXITEM)
    print 'Searching for papers in %s <%s> ...' % (sourcetype, venue),
    sys.stdout.flush()
    query = urllib.urlopen(url).read()
    jsonresult = json.loads(query)
    hits = jsonresult["result"]["hits"]
    print hits["@total"], "items found."

    # appending paper items to the database
    for hit in hits["hit"]:
        title = hit['info']['title']['text']
        year = hit['info']['year']
        dbcursor.execute('''
            INSERT INTO dblp (title, venue, year) VALUES
            ('%s', '%s', %s)
            ''' % (title, venue, year)
        )

dbconn.commit()
dbconn.close()
print 'data grabbing finished.'
