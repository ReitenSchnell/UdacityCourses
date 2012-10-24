# Decision problems are often just as hard as as actually returning an answer.
# Show how a k-clique can be found using a solution to the k-clique decision 
# problem.  Write a Python function that takes a graph G and a number k 
# as input, and returns a list of k nodes from G that are all connected 
# which takes a graph G and a number k and answers whether G contains a k-clique.
# We will also provide the standard routines for adding and removing edges from a graph.

# Returns a list of all the subsets of a list of size k
from unittest import TestCase

def k_subsets(lst, k):
    if len(lst) < k:
        return []
    if len(lst) == k:
        return [lst]
    if k == 1:
        return [[i] for i in lst]
    return k_subsets(lst[1:],k) + map(lambda x: x + [lst[0]], k_subsets(lst[1:], k-1))

# Checks if the given list of nodes forms a clique in the given graph.
def is_clique(G, nodes):
    for pair in k_subsets(nodes, 2):
        if pair[1] not in G[pair[0]]:
            return False
    return True

# Determines if there is clique of size k or greater in the given graph.
def k_clique_decision(G, k):
    nodes = G.keys()
    for i in range(k, len(nodes) + 1):
        for subset in k_subsets(nodes, i):
            if is_clique(G, subset):
                return True
    return False

def make_link(G, node1, node2):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = 1
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = 1
    return G

def break_link(G, node1, node2):
    if node1 not in G:
        print "error: breaking link in a non-existent node"
        return
    if node2 not in G:
        print "error: breaking link in a non-existent node"
        return
    if node2 not in G[node1]:
        print "error: breaking non-existent link"
        return
    if node1 not in G[node2]:
        print "error: breaking non-existent link"
        return
    del G[node1][node2]
    del G[node2][node1]
    return G

def k_clique(G, k):
    if not k_clique_decision(G, k):
        return False
    for node1 in G:
        for node2 in G:
            if node1 < node2 and node2 in G[node1]:
                G = break_link(G, node1, node2)
                clique = k_clique(G, k)
                if not clique:
                    G = make_link(G, node1, node2)
    return sorted([k for k in G.keys() if (len(G[k]) and k>1) or (k == 1)])

class CliqueTests(TestCase):
    def test_k_clique_decision_Should_be_true(self):
        n1, n2, n3, n4, n5 = '1', '2', '3', '4', '5'
        H = {}
        make_link(H, n1, n2)
        make_link(H, n1, n3)
        make_link(H, n2, n3)
        make_link(H, n2, n4)
        make_link(H, n3, n5)
        result = k_clique_decision(H, 3)
        self.assertEquals(result, True)

    def test_k_clique_decision_Should_be_false(self):
        n1, n2, n3, n4, n5 = '1', '2', '3', '4', '5'
        H = {}
        make_link(H, n1, n2)
        make_link(H, n1, n3)
        make_link(H, n2, n5)
        make_link(H, n2, n4)
        make_link(H, n3, n5)
        result = k_clique_decision(H, 3)
        self.assertEquals(result, False)

    def test_k_clique_should_return_clique_nodes(self):
        n1, n2, n3, n4, n5 = '1', '2', '3', '4', '5'
        H = {}
        make_link(H, n1, n2)
        make_link(H, n1, n3)
        make_link(H, n2, n3)
        make_link(H, n2, n4)
        make_link(H, n3, n5)
        result = k_clique(H, 3)
        self.assertEquals(result, [n1, n2, n3])

    def test_single_node_should_return_the_node(self):
        G = {1:{}}
        result = k_clique(G, 1)
        self.assertEqual(result, [1])