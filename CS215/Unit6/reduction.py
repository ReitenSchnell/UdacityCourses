# In the lecture, we described how a solution to k_clique_decision(G, k)
# can be used to solve independent_set_decision(H,s).  
# Write a Python function that carries out this transformation.  

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

# This function should use the k_clique_decision function
# to solve the independent set decision problem
def independent_set_decision(H, s):
    for node1 in H:
        for node2 in H:
            if node1 > node2:
                if node2 in H[node1]:
                    break_link(H, node1, node2)
                else:
                    make_link(H, node1, node2)
    return k_clique_decision(H, s)

class ReductionTests(TestCase):
    def test_reduction_should_be_true_for_4(self):
        n1, n2, n3, n4, n5, n6, n7, n8 = '1', '2', '3', '4', '5', '6', '7', '8'
        H = {}
        make_link(H, n1, n6)
        make_link(H, n1, n7)
        make_link(H, n1, n8)
        make_link(H, n2, n5)
        make_link(H, n2, n7)
        make_link(H, n2, n8)
        make_link(H, n3, n5)
        make_link(H, n3, n6)
        make_link(H, n3, n7)
        make_link(H, n3, n8)
        make_link(H, n4, n7)
        make_link(H, n4, n5)
        make_link(H, n5, n7)
        make_link(H, n5, n8)
        result = independent_set_decision(H, 4)
        self.assertEquals(result, True)

    def test_reduction_should_be_false_for_4(self):
        n1, n2, n3, n4, n5, n6, n7, n8 = '1', '2', '3', '4', '5', '6', '7', '8'
        H = {}
        make_link(H, n1, n6)
        make_link(H, n1, n7)
        make_link(H, n1, n8)
        make_link(H, n2, n5)
        make_link(H, n2, n7)
        make_link(H, n2, n8)
        make_link(H, n3, n5)
        make_link(H, n3, n6)
        make_link(H, n3, n7)
        make_link(H, n3, n8)
        make_link(H, n4, n7)
        make_link(H, n4, n5)
        make_link(H, n5, n7)
        make_link(H, n5, n8)
        make_link(H, n1, n2)
        result = independent_set_decision(H, 4)
        self.assertEquals(result, False)



