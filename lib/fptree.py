""" in this file, we describe the data type of fp-tree nodes and present
an algorithm to build a fp-tree from existing datasets """
import fpgrowth
import Queue

def supfilter(dataset, minsup):
    """
    supfilter : scan the items and drop the infrequent elements
    :param dataset: dataset could be in two available types: list(data) and list((data, support))
    :param minsup:
    :return:
    """
    rec = {}
    for item in dataset:
        for elem in item:
            # counting the number of existance for all elements
            if elem not in rec:
                rec[elem] = 0
            rec[elem] += 1

    # filter: find the infrequent keywords
    if '' in rec:
        del rec['']
    inf = filter(lambda i: i[1] >= minsup, rec.items())
    inf = map(lambda i: i[0], inf)

    # remove the infrequent elements from the dataset
    dataset = map(
        lambda i: filter(lambda ele: ele in inf, i),
        dataset
    )
    # remove the empty items
    dataset = filter(lambda i: len(i) > 0, dataset)

    # sort by the support of items
    dataset = map(
        lambda i: sorted(
            i,
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
        data items can be any strings
        NOTE: once a fptree is created, it should never be modified
        (at least in this scenario)
        """

        # minimum support
        self.minsup = minsup
        items = supfilter(dataset, minsup)

        """ the root node of a fp-tree """
        self.root = Node()
        """ header table """
        self.headertable = {}
        for item in items:
            self.root.appenditem(item, self.headertable)

        # check if the tree contains only a single prefix
        # todo

    def growth(self):
        """
        important!! this function is not thread-safe, so never try to execute it
        parallelly
        :return:
        """
        # initialize the queue
        fpgrowth.patterns = Queue.Queue()
        fpgrowth.fpgrowth(self, [], self.minsup)
        fpgrowth.wait()

        result = []
        while not fpgrowth.patterns.empty():
            patt = fpgrowth.patterns.get()
            if len(patt) > 1:
                result.append(patt)

        return result
