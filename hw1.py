from lib.conn import query
from lib.fptree import *

dataset = query('default', 'select author from dblp')

# we only consider the authors
dataset = map(lambda item: item[0].split(','), list(dataset))

tree = fptree(dataset, 50)
