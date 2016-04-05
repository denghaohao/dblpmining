from lib.conn import query
from lib.fpgrowth import *
from lib.fptree import *

dataset = query('default', 'select author from dblp')

# we only consider the authors
dataset = map(lambda item: item[0].split(','), list(dataset))

minsup = 20

tree = fptree(dataset, minsup)
patterns = fpgrowth(tree, [], minsup)
