from lib.conn import query

print query('default', 'select author, year from dblp where author like "%Jiawei Han%"')