#
# Write a function, `bipartite` that
# takes as input a graph, `G` and tries
# to divide G into two sets where
# there are no edges between elements of the
# the same set - only between elements in
# different sets.
# If two sets exists, return one of them
# or `None` otherwise
# Assume G is connected
#

def bipartite(G):
    r, g, b = 'r', 'g', 'b'
    checked_nodes = []
    first_node = G.keys()[0]
    colored_nodes = {first_node:r}
    frontier = [first_node]
    while len(frontier):
        current = frontier.pop(0)
        next_color = g if colored_nodes[current] == r else r
        for n in G[current]:
            if n not in checked_nodes:
                frontier.append(n)
                if n not in colored_nodes:
                    colored_nodes[n] = next_color
                else:
                    if colored_nodes[n] != next_color:
                        colored_nodes[n] = b
        checked_nodes.append(current)
    blue_nodes = [c for c in colored_nodes if colored_nodes[c] == b]
    return None if len(blue_nodes) else set([c for c in colored_nodes if colored_nodes[c] == r])

########
#
# Test

def make_link(G, node1, node2, weight=1):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = weight
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = weight
    return G


def test():
    edges = [(1, 2), (2, 3), (1, 4), (2, 5),
             (3, 8), (5, 6)]
    G = {}
    for n1, n2 in edges:
        make_link(G, n1, n2)
    g1 = bipartite(G)
    assert (g1 == set([1, 3, 5]) or
            g1 == set([2, 4, 6, 8]))
    edges = [(1, 2), (1, 3), (2, 3)]
    G = {}
    for n1, n2 in edges:
        make_link(G, n1, n2)
    g1 = bipartite(G)
    assert g1 == None

test()
