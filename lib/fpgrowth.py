""" the fp-growth algorithm should be written in this file
"""
import fptree as fpt


def cpb(treenode):
    assert(isinstance(treenode, fpt.Node))
    result = []
    sup = treenode.sup
    # the root node has a none name field
    while treenode is not None and treenode.name is not None:
        result.append(treenode.name)
        treenode = treenode.parent

    return list(reversed(result)), sup


def fpgrowth(tree, a, minsup):
    # the input argument tree has to be in form of fptree
    # and the subfix should be a list (initialized as [])
    assert (
        isinstance(tree, fpt.fptree) and isinstance(a, list)
    )
    for key in tree.headertable:
        # construct a conditional fp-tree
        cpbs = []
        for node in tree.headertable[key]:
             cpbs.append(cpb(node))

        # remove the items with low frequency
        cpbs = filter(lambda item: item[1] > minsup, cpbs)
        if len(cpbs) == 0:
            # we will not apply any further operations on an empty list
            continue

        # expand the cpbs to a dataset which is accepted by the fptree algorithm
        dset = []
        for rec in cpbs:
            dset += [rec[0]] * rec[1]

        # construct the new conditional fp-tree
        newfpt = fpt.fptree(dset, minsup)
        break
