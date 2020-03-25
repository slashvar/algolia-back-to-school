# Graph representation

from collections import deque
from json import load
import heapq

class Graph:
    def __init__(self, order, directed=False):
        self.vertices = [ [] for i in range(order) ]
        self.directed = directed
        self.costs = {}

    def add_edge(self, src, dst, cost=None):
        self.vertices[src].append(dst)
        self.vertices[src].sort()
        if not self.directed:
            self.vertices[dst].append(src)
            self.vertices[dst].sort()
        if cost is not None:
            self.costs[(src, dst)] = cost
            if not self.directed:
                self.costs[(dst, src)] = cost


    def display(self):
        for v in range(len(self.vertices)):
            print(v, ':', self.vertices[v])

    def successors(self, v):
        return self.vertices[v]

    def order(self):
        return len(self.vertices)

    def is_directed(self):
        return self.directed

    def cost(self, edge):
        if edge in self.costs:
            return self.costs[edge]
        return None


def graph_from_json(jdata):
    graph = Graph(jdata["order"], directed=jdata["directed"])
    for edge in jdata["edges"]:
        cost = edge["cost"] if "cost" in edge else None
        graph.add_edge(edge["src"], edge["dst"], cost=cost)
    return graph


def dfs_rec(g, v, parent):
    # Iterate on successors
    for s in g.successors(v):
        # if the current successor hasn't been visited
        if parent[s] is None:
            # mark the successor
            parent[s] = v
            # Recursion
            dfs_rec(g, s, parent)


def dfs(g, src=0, full=False):
    parent = [None] * g.order()
    parent[src] = src
    dfs_rec(g, src, parent)
    # If the graph is not connected, restart on unmarked vertices
    if full:
        for v in range(g.order()):
            if parent[v] is None:
                parent[v] = v
                dfs_rec(g, v, parent)
    return parent

class SpanningForest:
    def __init__(self):
        self.spanning = []
        self.backward = []
        self.forward = []
        self.cross = []

    def add_edge(self, src, dst):
        self.spanning.append((src, dst))

    def add_backward(self, src, dst):
        self.backward.append((src, dst))

    def add_forward(self, src, dst):
        self.forward.append((src, dst))

    def add_cross(self, src, dst):
        self.cross.append((src, dst))

    def print_dot(self, extra=False):
        print('digraph G {')
        for (u, v) in self.spanning:
            print(' ', u, '->', v)
        if extra:
            for (u, v) in self.backward:
                print(' ', u, '->', v, '[color="red" constraint=false]')
            for (u, v) in self.forward:
                print(' ', u, '->', v, '[color="blue" constraint=false]')
            for (u, v) in self.cross:
                print(' ', u, '->', v, '[color="orange" constraint=false]')
        print('}')

def directed_dfs_extra_edges(g, v, parents, preorder, postorder, count, forest):
    preorder[v] = count[0]
    count[0] += 1
    for s in g.successors(v):
        if parents[s] is None:
            forest.add_edge(v, s)
            parents[s] = v
            directed_dfs_extra_edges(g, s, parents, preorder, postorder, count, forest)
        else:
            if postorder[s] is None:
                forest.add_backward(v, s)
            else:
                if preorder[s] < preorder[v]:
                    forest.add_cross(v, s)
                else:
                    forest.add_forward(v, s)
    postorder[v] = count[0]
    count[0] += 1


def directed_dfs(g, src=0):
    forest = SpanningForest()
    parents = [None] * g.order()
    preorder = [None] * g.order()
    postorder = [None] * g.order()
    count = [0]
    parents[src] = src
    directed_dfs_extra_edges(g, src, parents, preorder, postorder, count, forest)
    for v in range(g.order()):
        if parents[v] is None:
            directed_dfs_extra_edges(g, v, parents, preorder, postorder, count, forest)
    return parents, forest


def print_as_dot(g):
    arrow = '->' if g.is_directed() else '--'
    pre = 'di' if g.is_directed() else ''
    print(pre, 'graph G {', sep='')
    for v in range(g.order()):
        for s in g.successors(v):
            if g.is_directed() or s >= v:
                label=''
                if g.cost((v, s)) is not None:
                    label='[label={}]'.format(g.cost((v, s)))
                print(' ', v, arrow, s, label)
    print('}')


def bfs_single_source(g, src, parents, distances, forest=None):
    q = deque()
    q.append(src)
    distances[src] = 0
    parents[src] = src
    while (len(q) > 0):
        v = q.popleft()
        for s in g.successors(v):
            if parents[s] is None:
                if forest != None:
                    forest.add_edge(v, s)
                parents[s] = v
                distances[s] = distances[v] + 1
                q.append(s)


def bfs(g, src=0, full=False, forest=None):
    parents = [None] * g.order()
    distances = [None] * g.order()
    bfs_single_source(g, src, parents, distances, forest=forest)
    if full:
        for v in range(g.order()):
            if parents[v] is None:
                bfs_single_source(g, v, parents, distances, forest=forest)
    return parents, distances


def rebuild_path_to(parents, dst):
    path = deque([dst])
    cur = dst
    while parents[cur] != cur:
        path.appendleft(parents[cur])
        cur = parents[cur]
    return path


def find(components, u):
    q = deque()
    while components[u] != u:
        q.append(u)
        u = components[u]
    for v in q:
        components[v] = u
    return u


def find(components, u):
    while components[u] != u:
        u = components[u]
    return u


def unify(components, u, v):
    pu = find(components, u)
    pv = find(components, v)
    if pu != pv:
        components[pv] = pu


def union_find(order, edges):
    components = [ i for i in range(order) ]
    for (u, v) in edges:
        unify(components, u, v)
    return components


class OpenSet:
    def __init__(self, order):
        self._present = [None] * order
        self._queue = []

    def update(self, vertex, dist):
        if self._present[vertex] is not None:
            entry = self._present[vertex]
            entry[-1] = False
            self._present[vertex] = None
        entry = [dist, vertex, True]
        self._present[vertex] = entry
        heapq.heappush(self._queue, entry)

    def take_min(self):
        while self._queue:
            dist, vertex, active = heapq.heappop(self._queue)
            if active:
                self._present[vertex] = None
                return vertex
        return None

    def is_empty(self):
        while self._queue:
            if self._queue[0][-1]:
                return False
            heapq.heappop(self._queue)
        return True


if __name__ == '__main__':
    g = Graph(11, directed=True)
    edges = [ (1, 2), (1, 3), (2, 4), (4, 2), (4, 5), (4, 6), (3, 7), (5, 8), (6, 8), (7, 8), (7, 6), (6, 1), (1, 8), (9, 10), (9, 11), (10, 1) ]
    for (u, v) in edges:
        g.add_edge(u-1, v-1)
    _, forest = directed_dfs(g, src=0)
    # print_as_dot(g)
    # forest.print_dot()
    # forest.print_dot(extra=True)
    # forestBFS = SpanningForest()
    # shortest, distances = bfs(g, src=8, full=False, forest=forestBFS)
    # forestBFS.print_dot()
    # print(shortest)
    # print(distances)
    # print(rebuild_path_to(shortest, 5))
    forestBFS2 = SpanningForest()
    bfs(g, src=0, full=True, forest=forestBFS2)
    # forestBFS2.print_dot()
    with open("graph_for_path.json") as file:
        g2 = graph_from_json(load(file))
        print_as_dot(g2)
