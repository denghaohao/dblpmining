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
    dataset = map(
        lambda item: sorted(
            item,
            # we use support of elements as sorting keys
            key=lambda ele: rec[ele],
            reverse=True
        ),
        dataset
    )
    return dataset


class Node:
    def __init__(self, name=None, parent=None, headertable=None):
        self.name = name
        self.sup = 0
        self.children = {}
        self.parent = parent
        if headertable is not None:
            # the node will be appended to the header table if such
            # such a table is provided
            if name not in headertable:
                headertable[name] = []
            headertable[name].append(self)

    def appenditem(self, item, headertable):
        self.sup += 1
        if len(item) == 0:
            return
        if item[0] not in self.children:
            self.children[item[0]] = Node(item[0], self, headertable)
        self.children[item[0]].appenditem(item[1:], headertable)


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

        """ the root node of a fp-tree """
        self.root = Node()
        """ header table """
        self.headertable = {}
        for item in items:
            self.root.appenditem(item, self.headertable)
