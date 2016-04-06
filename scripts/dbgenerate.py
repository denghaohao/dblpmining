"""
this script is used to obtain xml data from dblp.org and save it to
a local database
"""

import json
import os
import sqlite3
import sys
import urllib

''' we obtain no more than MAXITEM papers in a single query '''
MAXITEM = 10000

conferences = [
    'sdm', 'icdm', 'ecml-pkdd', 'pakdd', 'wsdm',
    'dmkd', 'kdd', 'cvpr', 'icml', 'nips', 'colt', 'sigir',
]

journals = [
    "sigkdd_explorations_sigkdd_",    # SIGKDD explorations
    "tkdd", 
    "ieee_trans_knowl_data_eng_tkde_" # TKDE
    ]

venues = conferences + journals
apiaddr = 'http://dblp.org/search/api/?q='
# apiaddr = 'http://dblp.uni-trier.de/search/publ/api?q='

''' where to store the data? '''
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
    dbcursor.execute('DROP TABLE dblp')
except:
    ''' no existing table is dropped '''

dbcursor.execute('''
CREATE TABLE dblp (
    title varchar(255),
    author varchar(255),
    venue varchar(255),
    type varchar(255),
    year int(20)
)
''')

''' how many items we've found '''
amount = 0

for venue in venues:
    sourcetype = 'conference' if venue in conferences else 'journal'
    url = apiaddr + 'ce:type:%s:* ce:venue:%s:*&h=%d&c=4&f=0&format=json' \
        % (sourcetype, venue, MAXITEM)
    print 'Searching for papers in %s <%s> ...' % (sourcetype, venue),
    sys.stdout.flush()
    query = None
    while True:
        try:
            query = urllib.urlopen(url).read()
            break
        except:
            ''' retry when network failed '''
    jsonresult = json.loads(query)
    hits = jsonresult["result"]["hits"]
    print hits["@total"], "items found."
    amount += int(hits["@total"])

    if int(hits["@total"]) == 0:
        print 'FAILED at <%s> plz check if you\'re using the correct venue name -_-' % venue
        continue

    # appending paper items to the database
    for hit in hits["hit"]:
        title = hit['info']['title']['text']
        year = hit['info']['year']
        try:
            # some items may include no information about authors
            author = ''
            for name in hit['info']['authors']['author']:
                author += name + ","
        except:
            # if an item contains no authors, we would ignore it
            continue
        dbcursor.execute('''
            INSERT INTO dblp (title, author, venue, year, type) VALUES
            ('%s', '%s', '%s', %s, '%s')
            ''' % (title, author, venue, year, sourcetype)
        )

dbconn.commit()
dbconn.close()
print 'data grabbing finished with %d items.' % amount
