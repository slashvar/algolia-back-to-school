# Tree implementation

class Tree:
    def __init__(self, key, left=None, right=None):
        self.key = key
        self.left = left
        self.right = right
        self.bal = 0

def to_dot_rec(tree, label_):
    if tree:
        label = label_[0]
        label_[0] += 1
        print('\t', label, ' [label= "{} ({})"];'.format(tree.key, tree.bal), sep='')
        if tree.left:
            print('\t', label, ' -> ', label_[0], ';', sep='')
            to_dot_rec(tree.left, label_)
        if tree.right:
            print('\t', label, ' -> ', label_[0], ';', sep='')
            to_dot_rec(tree.right, label_)

def to_dot(tree, name='tree'):
    print("digraph", name, "{")
    label = [0]
    to_dot_rec(tree, label)
    print('}')

def _lr(tree):
    new_root = tree.right
    tree.right = new_root.left
    new_root.left = tree
    return new_root


def left_rotation(tree):
    new_root = _lr(tree)
    new_root.left.bal = -1 - new_root.bal
    new_root.bal = - new_root.left.bal
    return new_root

def _rr(tree):
    new_root = tree.left
    tree.left = new_root.right
    new_root.right = tree
    return new_root

def right_rotation(tree):
    new_root = _rr(tree)
    new_root.right.bal = 1 - new_root.bal
    new_root.bal = - new_root.right.bal
    return new_root

def right_left_rotation(tree):
    tree.right = _rr(tree.right)
    new_root = _lr(tree)
    new_root.left.bal = (new_root.bal * (new_root.bal - 1)) // 2
    new_root.right.bal = - (new_root.bal * (new_root.bal + 1)) // 2
    new_root.bal = 0
    return new_root

def left_right_rotation(tree):
    tree.left = _lr(tree.left)
    new_root = _rr(tree)
    new_root.left.bal = (new_root.bal * (new_root.bal - 1)) // 2
    new_root.right.bal = - (new_root.bal * (new_root.bal + 1)) // 2
    new_root.bal = 0
    return new_root

def insert(tree, key):
    if tree is None: return True, Tree(key)
    if key == tree.key: return False, tree
    change = False
    if key < tree.key:
        change, tree.left = insert(tree.left, key)
        tree.bal += change
    else:
        change, tree.right = insert(tree.right, key)
        tree.bal -= change
    if not change: return False, tree
    if tree.bal == 2:
        if tree.left.bal == -1:
            tree = left_right_rotation(tree)
        else:
            tree = right_rotation(tree)
    elif tree.bal == -2:
        if tree.right.bal == 1:
            tree = right_left_rotation(tree)
        else:
            tree = left_rotation(tree)
    return tree.bal != 0, tree

tree = None

for i in range(1, 10):
    _, tree = insert(tree, i)

to_dot(tree)
