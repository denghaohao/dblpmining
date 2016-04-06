from lib.conn import query

dbname = 'default'
year_threshold = 8

# obtain author information from the database
raw_authors = query(dbname, 'select * from authors')
authors = {}
for rec in raw_authors:
    authors[rec[0]] = rec[1:]


def set_db(name):
    global dbname
    dbname = name


def teacher_student_analyse(itemset):
    raw_edges = filter(lambda item: len(item[0]) == 2, itemset)
    # relation should be a set of pairs where the first on is student
    # and the second one is the corresponding teacher
    raw_relation = []
    for edge in raw_edges:
        author1 = edge[0][0]
        author2 = edge[0][1]
        # if an author published his first paper much earlier than another one,
        # and the former has a larger number of publications, we will take this
        # as a teacher-student relation
        if authors[author1][0] - authors[author2][0] >= year_threshold:
            if authors[author1][1] <= authors[author2][1]:
                raw_relation.append((author1, author2, edge[1]))
        elif authors[author2][0] - authors[author1][0] >= year_threshold:
            if authors[author2][1] <= authors[author1][1]:
                raw_relation.append((author2, author1, edge[1]))

    # now we're going to check when the student is supervised by his supervisor
    relation = []
    for rel in raw_relation:
        copapers = query(
            dbname,
            'select distinct year from dblp where \
                author like "%%%s%%%s%%" or \
                author like "%%%s%%%s%%" order by year' %
            (rel[0], rel[1], rel[1], rel[0])
        )
        relation.append((rel[0], rel[1], copapers[0][0], copapers[-1][0]))

    group_relation = {}
    supervisors = set(map(lambda item: item[1], relation))
    for supervisor in supervisors:
        curr = []
        # find the students that work for him/her
        for rel in relation:
            if rel[1] == supervisor:
                curr.append((rel[0], rel[2], rel[3]))

        # note: usually a supervisor have more than one students
        if len(curr) > 1:
            group_relation[supervisor] = curr

    return group_relation


def cooperate_relation(itemset):
    itemset = filter(lambda item: len(item[0]) >= 2, itemset)

    nodes = []
    for item in itemset:
        nodes += item[0]

    nodes = list(set(nodes))
    edges = [[0] * len(nodes)] * len(nodes)

    # construct the graph
    for rel in itemset:
        print rel
        break
    pass