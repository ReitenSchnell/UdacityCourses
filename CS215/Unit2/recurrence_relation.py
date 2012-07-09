import math
import random
import pylab

class Node(object):
    def __init__(self):
        self.links = []

class RecursiveGraph(list):
    def add_nodes(self, nodes):
        for node in nodes:
            self.append(node)

    def add_link(self, e):
        v, w = e
        v.links.append(w)

    def links_count(self):
        return sum([len(node.links) for node in self])

    def get_random_node(self):
        random_index = random.randint(0, len(self) - 1)
        return self[random_index]

def make_graph(n):
    if n == 1:
        inner_graph = RecursiveGraph()
        inner_graph.add_nodes([Node()])
        return inner_graph
    g1 = make_graph(n/2)
    g2 = make_graph(n/2)
    g = RecursiveGraph()
    g.add_nodes(g1)
    g.add_nodes(g2)
    for i in range(int(math.log(n, 2))):
        i1 = g1.get_random_node()
        i2 = g2.get_random_node()
        g.add_link((i1, i2))
    return g

x_list = []
y_list = []
for i in range(1,20):
    n = 2**i
    g = make_graph(n)
    m = g.links_count()
    print 'n=%s T(n)=%s'%(n, m)
    x_list.append(n)
    y_list.append(m)
pylab.plot(x_list, y_list)
pylab.savefig('fig2.png')