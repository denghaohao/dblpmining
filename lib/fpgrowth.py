""" the fp-growth algorithm should be written in this file
"""
from threading import Thread

import fptree as fpt
import Queue

patterns = Queue.Queue()
threads = Queue.Queue()


def push_pattern(patt):
    patterns.put(patt)


def cpb(treenode):
    assert(isinstance(treenode, fpt.Node))
    result = []
    sup = treenode.sup
    # the root node has a none name field
    while treenode is not None and treenode.name is not None:
        result.append(treenode.name)
        treenode = treenode.parent

    # remove the last element (name of current treenode)
    return list(reversed(result))[:-1], sup


def fpgrowth(tree, a, minsup):
    # the input argument tree has to be in form of fptree
    # and the subfix should be a list (initialized as [])
    assert (
        isinstance(tree, fpt.fptree) and isinstance(a, list)
    )

    for key in tree.headertable:
        # construct a conditional fp-tree
        cpbs = []
        sup = 0
        for node in tree.headertable[key]:
            cpbs.append(cpb(node))
            sup += node.sup

        push_pattern([[key] + a, sup])

        # remove the items with low frequency
        cpbs = filter(lambda item: item[1] >= minsup, cpbs)

        # expand the cpbs to a dataset which is accepted by the fptree algorithm
        # note that in each iteration, we decrease the length of samples
        # e.g. a,b,c -> a,b -> a
        dset = []
        for rec in cpbs:
            if len(rec[0]) > 1:
                dset += [rec[0]] * rec[1]

        if len(dset) != 0:
            # construct the new conditional fp-tree
            newfpt = fpt.fptree(dset, minsup)
            thr = Thread(
                target=fpgrowth,
                args=(newfpt, [key] + a, minsup)
            )
            threads.put(thr)
            thr.start()


def wait():
    while not threads.empty():
        thr = threads.get()
        thr.join()
