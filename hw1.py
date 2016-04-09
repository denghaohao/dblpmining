from lib.fptree import *
from lib.analysis import *
import sys

# debug, this should be removed when this project is released
# if __name__ == "__main__":
#     if len(sys.argv) < 2:
#         sys.argv.append('3')

# to make sure which database we're using
if len(sys.argv) <= 1:
    print 'sorry but to run this program, you need to specify a phase which can be:'
    print '- 1: cooperative relationship'
    print '- 2: supervising relationship'
    print '- 3: multiple cooperative relationship'
    print 'you can also specify a certain database by the second parament, e.g.'
    print '`python hw1.py 1 default`'
else:
    set_db('default' if len(sys.argv) <= 2 else sys.argv[2])
    dataset = query(dbname, 'select author, year from dblp')
    # we only consider the authors in the database
    dataset = map(lambda item: item[0].split(','), list(dataset))
    minsup = 3

    # constructing fp-tree
    tree = fptree(dataset, minsup)
    # generating frequent item set
    terms = tree.growth()

    result = []
    if sys.argv[1] == '1':
        result = sorted(cooperate_relation(terms), key=lambda edge: edge[1], reverse=True)
    elif sys.argv[1] == '2':
        result = teacher_student_analyse(terms)
    elif sys.argv[1] == '3':
        result = group_cooperate_relation(terms)

    if isinstance(result, dict):
        for key in result:
            print '[%s]' % key
            for line in result[key]:
                print '  ', line

        for key in result:
            print '%s &' % key,
            for line in result[key]:
                print line[0],
                if result[key].index(line) < len(result[key]) - 1:
                    print ',',
            print ' & \\\\'
    elif isinstance(result, list):
        for line in result:
            print line

    print 'program finished with %d patterns found' % len(result)