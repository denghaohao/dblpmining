""" the fp-growth algorithm should be written in this file
"""
import fptree as fpt


def fpgrowth(tree, a):
    # the input argument tree has to be in form of fptree
    # and the subfix should be a list (initialized as [])
    assert (
        isinstance(tree, fpt.fptree) and isinstance(a, list)
    )
    for key in tree.headertable:
        # construct a conditional fp-tree
        print key
