# Binary Search Tree

class Tree:
    def __init__(self, key, value, left=None, right=None):
        self.key = key
        self.value = value
        self.left = left
        self.right = right

def bst_search(tree, key):
    if tree is not None:
        if key == tree.key:
            return tree
        if key < tree.key:
            return bst_search(tree.left, key)
        return bst_search(tree.right, key)
    return None

def is_bst(tree, lower, upper):
    if tree is None:
        return True
    if not (lower <= tree.key and tree.key < upper):
        return False
    return is_bst(tree.left, lower, tree.key) and is_bst(tree.right, tree.key, upper)
