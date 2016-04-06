from lib.conn import query
from lib.fptree import *
from lib.analysis import *

dbname = 'default'

dataset = query(dbname, 'select author, year from dblp')

# we only consider the authors in the database
dataset = map(lambda item: item[0].split(','), list(dataset))


minsup = 3

# constructing fp-tree
tree = fptree(dataset, minsup)
# generating frequent item set
terms = tree.growth()

# print teacher_student_analyse(terms)
print cooperate_relation(terms)
