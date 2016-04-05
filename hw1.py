from lib.conn import query
from lib.fptree import *

dataset = query('default', 'select author from dblp')

# we only consider the authors
dataset = map(lambda item: item[0].split(','), list(dataset))

# print len(filter(lambda rec: 'Jiawei Han' in rec and 'Jialu Liu' in rec, dataset))

minsup = 6

tree = fptree(dataset, minsup)
print tree.growth()
