from unittest import TestCase
from operator import itemgetter
file_name = "actors"

def load_file(filename):
    f = open(filename)
    lines =  f.readlines()
    f.close()
    return lines

def make_link(G, node1, node2):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = 1
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = 1
    return G

def build_bipartite(lines):
    g = {}
    actors = []
    for line in lines:
        a, f, y = line.split('\t')
        make_link(g, a, f+y)
        if a not in actors:
            actors.append(a)
    return g, actors

def get_avg_centrality(node, graph):
    centrality = {node:0}
    frontier = [node]
    while len(frontier):
        current = frontier.pop(0)
        for n in graph[current]:
            if n not in centrality:
                frontier.append(n)
                centrality[n] = centrality[current] + 1
    return sum(centrality.values())*1.0/len(centrality)

class CentralityTests(TestCase):
    def make_graph(self):
        nodes = ['a1', 'a2', 'a3', 'a4', 'a5']
        graph = {}
        make_link(graph, nodes[0], nodes[1])
        make_link(graph, nodes[0], nodes[2])
        make_link(graph, nodes[1], nodes[3])
        make_link(graph, nodes[2], nodes[4])
        return graph

    def test_get_avg_centrality(self):
        graph = self.make_graph()
        centrality = get_avg_centrality('a1', graph)
        self.assertAlmostEqual(1.2, centrality)

def count_top_20():
    print 'load lines'
    lines = load_file(file_name)
    print 'make bipartite'
    graph, actors = build_bipartite(lines)
    centrality = {}
    count = len(actors)
    for i in range(count):
        actor = actors[i]
        print 'calculating centrality for %s (%s of %s)'%(actor, i, count)
        centrality[actor] = get_avg_centrality(actor, graph)
    print 'getting top 20'
    top20 = sorted(centrality.items(), key = itemgetter(1))[0:20]
    print top20

count_top_20()



