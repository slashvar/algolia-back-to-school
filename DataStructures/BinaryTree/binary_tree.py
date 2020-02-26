class Tree:
    def __init__(self, key, left=None, right=None):
        self.key = key
        self.left = left
        self.right = right

def size(tree):
    if tree is None:
        return 0
    return 1 + size(tree.left) + size(tree.right)

def height(tree):
    if tree is None:
        return -1
    return 1 + max(height(tree.left), height(tree.right))

def preorder_print(tree):
    if tree != None:
        print(tree.key, end=' ')
        preorder_print(tree.left)
        preorder_print(tree.right)

def postorder_print(tree):
    if tree != None:
        postorder_print(tree.left)
        postorder_print(tree.right)
        print(tree.key, end=' ')

def inorder_print(tree):
    if tree != None:
        inorder_print(tree.left)
        print(tree.key, end=' ')
        inorder_print(tree.right)

def dfs(tree, key):
    if tree is None:
        return False
    if tree.key == key:
        return True
    return dfs(tree.left, key) or dfs(tree.right, key)

from collections import deque

def bfs_print(tree):
    if tree is None: return
    queue = deque()
    queue.append(tree)
    while len(queue) > 0:
        current = queue.popleft()
        print(current.key, end=' ')
        if current.left != None:
            queue.append(current.left)
        if current.right != None:
            queue.append(current.right)
    print()

def bfs_print_level(tree):
    if tree is None: return
    queue = deque([tree, None])
    while len(queue) > 0:
        current = queue.popleft()
        if current is None:
            print()
            if len(queue) > 0:
                queue.append(None)
            continue
        print(current.key, end=' ')
        if current.left != None:
            queue.append(current.left)
        if current.right != None:
            queue.append(current.right)
    print()

tree = Tree(0, Tree(1, Tree(3), Tree(4)), Tree(2, Tree(5), Tree(6)))

print('size:', size(tree))
print('height:', height(tree))
print("preorder:", end=' ')
preorder_print(tree)
print()
print("postorder:", end=' ')
postorder_print(tree)
print()
print("inorder:", end=' ')
inorder_print(tree)
print()
bfs_print(tree)
bfs_print_level(tree)
