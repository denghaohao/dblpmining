from lib.conn import query

dbname = 'default'
year_threshold = 8
authors = {}


def obtain_papers(names, distinct=True):
    whereclause = ''
    for name in names:
        whereclause += " author like '%%%s%%' and" % name
    return query(
        # %% is an escape character for %
        dbname,
        'select %s year from dblp where %s 1' % ('distinct' if distinct else '', whereclause)
    )


def set_db(name):
    global dbname
    dbname = name
    # obtain author information from the database
    raw_authors = query(dbname, 'select * from authors')
    global authors
    authors = {}
    for rec in raw_authors:
        authors[rec[0]] = rec[1:]


def cooperate_relation(itemset):
    raw_edges = filter(lambda item: len(item[0]) == 2, itemset)
    for edge in raw_edges:
        # evaluation for each edge (frequent item)
        copapers = obtain_papers([edge[0][0], edge[0][1]], distinct=False)
        edge[1] = (float(len(copapers)) / authors[edge[0][0]][1]) * \
                  (float(len(copapers)) / authors[edge[0][1]][1]) * len(copapers)

    return raw_edges


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
            if authors[author1][1] + 5 <= authors[author2][1]:
                raw_relation.append((author1, author2, edge[1]))
        elif authors[author2][0] - authors[author1][0] >= year_threshold:
            if authors[author2][1] + 5<= authors[author1][1]:
                raw_relation.append((author2, author1, edge[1]))

    # now we're going to check when the student is supervised by his supervisor
    relation = []
    for rel in raw_relation:
        copapers = obtain_papers([rel[0], rel[1]])
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


def group_cooperate_relation(itemset):
    itemset = filter(lambda item: len(item[0]) >= 3 and item[1] >= 4, itemset)
    flag = True
    while flag:
        flag = False
        for i in range(len(itemset)):
            for j in range(i + 1, len(itemset)):
                if len(set(itemset[i][0]) & set(itemset[j][0])) >= 2:
                    itemset[i][0] = list(set(itemset[i][0]) | set(itemset[j][0]))
                    itemset[i][1] += itemset[j][1]
                    del itemset[j]
                    flag = True
                    break

    return itemset