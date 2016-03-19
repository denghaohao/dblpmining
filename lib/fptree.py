""" in this file, we describe the data type of fp-tree nodes and present
an algorithm to build a fp-tree from existing datasets """


def supfilter(dataset, minsup):
    """ supfilter : scan the items and drop the infrequent elements
    """
    rec = {}
    for item in dataset:
        for elem in item:
            # counting the number of existance for all elements
            if elem not in rec:
                rec[elem] = 0
            rec[elem] += 1

    # filter: find the infrequent keywords
    del rec['']
    inf = filter(lambda item: item[1] >= minsup, rec.items())
    inf = map(lambda item: item[0], inf)

    # remove the infrequent elements from the dataset
    dataset = map(
        lambda item: filter(lambda ele: ele in inf, item),
        dataset
    )
    # remove the empty items
    dataset = filter(lambda item: len(item) > 0, dataset)

    # sort by the support of items
    def termcmp(a, b):
        if rec[a] < rec[b]:
            return 1
        elif rec[a] > rec[b]:
            return -1
        else:
            return 0

    dataset = map(lambda item: sorted(item, cmp=termcmp), dataset)

    return dataset


class node:
    def __init__(self, name=None):
        self.name = name
        self.sup = 0
        self.children = {}

    def appenditem(self, item):
        self.sup += 1
        if len(item) == 0:
            return
        if item[0] not in self.children:
            self.children[item[0]] = node(item[0])
        self.children[item[0]].appenditem(item[1:])


class fptree:
    def __init__(self, dataset, minsup):
        """ dataset should be a list of data items, in form of
        [
            ['apple', 'milk', 'wtf'],
            ['banana'],
            ....
        ]
        data items can be any strings """

        # minimum support
        self.minsup = minsup
        items = supfilter(dataset, minsup)

        # create fp-tree
        root = node()
        for item in items:
            root.appenditem(item)
