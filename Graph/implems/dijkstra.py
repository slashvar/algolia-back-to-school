from graph import Graph, OpenSet, graph_from_json
from math import inf
from json import load


def dijkstra(g, src):
    parents = [None] * g.order()
    dist = [inf] * g.order()
    queue = OpenSet(g.order())

    parents[src] = src
    dist[src] = 0
    queue.update(src, 0)

    while not queue.is_empty():
        v = queue.take_min()
        for s in g.successors(v):
            if dist[s] >= dist[v] + g.cost((v,s)):
                dist[s] = dist[v] + g.cost((v,s))
                parents[s] = v
                queue.update(s, dist[s])

    return parents, dist


if __name__ == '__main__':
    with open('graph_for_path.json') as file:
        g = graph_from_json(load(file))
        parents, dist = dijkstra(g, 0)
        for p in parents:
            print(p, end=' ')
        print()
        for d in dist:
            print(d, end=' ')
        print()
