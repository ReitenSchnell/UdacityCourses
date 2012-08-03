from unittest import TestCase
import itertools

file_name = "C:/actors"

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

def make_graph(lines):
    graph = {}
    for line in lines:
        a, f, y = line.split('\t')
        make_link(graph, f, a)
    return graph


p = load_file(file_name)
s = make_graph(p)
a =2

class CentralityTests(TestCase):
    def test_graph(self):
        lines = ['McClure, Marc (I) Freaky Friday 2003', 'McClure, Marc (I) Superman 1978', 'Cooper, Marc (I) Freaky Friday 2003', 'Frei, Marc (I) Superman 1978']