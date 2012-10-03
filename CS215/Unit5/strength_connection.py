from _heapq import heappush, heappop
from copy import copy, deepcopy
import heapq
from time import time
from unittest import TestCase

filename = 'marvel'

charactersForSearch = ['SPIDER-MAN/PETER PAR', 'GREEN GOBLIN/NORMAN ', 'WOLVERINE/LOGAN ','PROFESSOR X/CHARLES ', 'CAPTAIN AMERICA']

def get_characters_from_file(filename):
    f = open(filename)
    lines =  f.readlines()
    f.close()
    marvelG = {}
    characters = []
    old_char = ''
    for line in lines:
        char, book = line.replace('\n', '').replace('"', '').split('\t')
        make_link(marvelG, char, book, 1)
        if char != old_char:
            characters.append(char)
        old_char = char
    return marvelG, characters

def make_weighted_link(G, node1, node2):
    if node1 not in G:
        G[node1] = {}
    if node2 not in G[node1]:
        (G[node1])[node2] = 1
    else:
        (G[node1])[node2] += 1
    if node2 not in G:
        G[node2] = {}
    if node1 not in G[node2]:
        (G[node2])[node1] = 1
    else:
        (G[node2])[node1] += 1
    return G

def make_link(G, node1, node2, weight):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = weight
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = weight
    return G

def make_char_graph(bookG, characters):
    charsG = {}
    for char1 in characters:
        for book in bookG[char1]:
            for char2 in bookG[book]:
                if char1 > char2:
                    make_weighted_link(charsG, char1, char2)
    return charsG

def transform_graph_to_weighted(g):
    G = deepcopy(g)
    for char1 in G:
        for char2 in G[char1]:
            G[char1][char2] = 1.0/G[char1][char2]
    return G

def transform_graph_to_unweighted(g):
    G = deepcopy(g)
    for char1 in G:
        for char2 in G[char1]:
            G[char1][char2] = 1.0
    return G

def find_shortest_path(G, v):
    dist_so_far = {v: [0,[v]]}
    final_dist = {}
    heap=[]
    heappush(heap,(0,v))
    while len(final_dist) < len(G) and len(heap) :
        value,w = heappop(heap)
        if w not in final_dist:
            final_dist[w] = dist_so_far[w]
            del dist_so_far[w]
            for x in G[w]:
                if x not in final_dist:
                    path_len = G[w][x]
                    if x not in dist_so_far:
                        dist_so_far[x] = []
                        dist_so_far[x].append(final_dist[w][0] + path_len)
                        dist_so_far[x].append(final_dist[w][1] + [x])
                        heappush(heap,(final_dist[w][0] + path_len, x))
                    elif final_dist[w][0] + path_len < dist_so_far[x][0]:
                        dist_so_far[x][0] = final_dist[w][0] + path_len
                        dist_so_far[x][1] = final_dist[w][1] + [x]
                        heappush(heap,(final_dist[w][0] + path_len, x))
    return final_dist

def main():
    time1 =  time()
    bookG, chars = get_characters_from_file(filename)
    charsG = make_char_graph(bookG, chars)
    weighted = transform_graph_to_weighted(charsG)
    unweighted = transform_graph_to_unweighted(charsG)
    result = 0
    for char in charactersForSearch:
        dist_weighted = find_shortest_path(weighted, char)
        dist_unweighted = find_shortest_path(unweighted, char)
        current_sum = 0
        for ch in dist_unweighted:
            if len(dist_unweighted[ch][1]) != len(dist_weighted[ch][1]):
                current_sum+= 1
        result += current_sum
        print 'Count for '+char+' is '+str(current_sum)
    print result
    time2 = time()
    print time2 - time1

class TestCases(TestCase):
    def test_should_add_link_to_empty_graph_for_first_node(self):
        G = {}
        a, b = 'a', 'b'
        make_link(G, a, b, 1)
        self.assertEqual({b:1}, G[a])
        self.assertEqual({a:1}, G[b])

    def test_should_add_link_from_existed_node_to_new_node(self):
        a, b, c = 'a', 'b', 'c'
        G = {a:{b:1}, b:{a:1}}
        make_link(G, a, c, 1)
        self.assertEqual({b:1, c:1}, G[a])
        self.assertEqual({a:1}, G[c])

    def test_should_add_weighted_link_to_empty_graph_for_first_node(self):
        G = {}
        a, b = 'a', 'b'
        make_weighted_link(G, a, b)
        self.assertEqual({b:1}, G[a])
        self.assertEqual({a:1}, G[b])

    def test_should_add_weighted_link_from_existed_node_to_new_node(self):
        a, b, c = 'a', 'b', 'c'
        G = {a:{b:1}, b:{a:1}}
        make_weighted_link(G, a, c)
        self.assertEqual({b:1, c:1}, G[a])
        self.assertEqual({a:1}, G[c])

    def test_should_add_weighted_link_from_existed_node_to_existed_node_and_increase_weights(self):
        a, b, c = 'a', 'b', 'c'
        G = {a:{b:2}, b:{a:2}}
        make_weighted_link(G, a, b)
        self.assertEqual({b:3}, G[a])
        self.assertEqual({a:3}, G[b])

    def test_should_get_characters_list_from_file(self):
        g, characters = get_characters_from_file('testfile.txt')
        self.assertEqual(['Char1', 'Char2'], characters)

    def test_should_get_graph_from_file(self):
        g, characters = get_characters_from_file('testfile.txt')
        self.assertEqual({'Char1': {'Book1':1, 'Book2':1}, 'Char2':{'Book1':1, 'Book2':1}, 'Book1':{'Char1':1, 'Char2':1}, 'Book2':{'Char1':1, 'Char2':1}}, g)

    def test_should_make_char_graph_from_characters_and_marvel_graph(self):
        graph = {'Char1': {'Book1':1, 'Book2':1}, 'Char2':{'Book1':1, 'Book2':1}, 'Book1':{'Char1':1, 'Char2':1}, 'Book2':{'Char1':1, 'Char2':1}}
        chars = ['Char1', 'Char2']
        charsG = make_char_graph(graph, chars)
        self.assertEqual({'Char1':{'Char2' : 2}, 'Char2':{'Char1' : 2}}, charsG)

    def test_heap_add(self):
        h = []
        heapq.heappush(h, 4)
        heapq.heappush(h, 2)
        heapq.heappush(h, 5)
        heapq.heappush(h, 9)
        heapq.heappush(h, 1)
        self.assertEqual([1, 2, 5, 9, 4], h)

    def test_heap_remove(self):
        h = []
        heapq.heappush(h, 4)
        heapq.heappush(h, 2)
        heapq.heappush(h, 5)
        heapq.heappush(h, 9)
        heapq.heappush(h, 1)
        p = heapq.heappop(h)
        self.assertEqual(1, p)
        self.assertEqual([2,4,5,9], h)


    def test_find_shortest_path(self):
        (a,b,c) = ('A', 'B', 'C')
        triples = ((a,b,1), (a,c,3), (b,c,1))
        G = {}
        for (i,j,k) in triples:
            make_link(G, i, j, k)

        dist = find_shortest_path(G, a)

        self.assertEqual(dist[b][0], 1)
        self.assertEqual(dist[b][1], [a,b])
        self.assertEqual(dist[c][0], 2)
        self.assertEqual(dist[c][1], [a,b,c])

    def test_transform_graph_to_weighted(self):
        (a,b,c) = ('A', 'B', 'C')
        triples = ((a,b,1), (a,c,3), (b,c,1))
        G = {}
        for (i,j,k) in triples:
            make_link(G, i, j, k)

        t = transform_graph_to_weighted(G)
        self.assertEqual(1, t[a][b])
        self.assertEqual(1, t[b][a])
        self.assertEqual(1, t[b][c])
        self.assertEqual(1, t[c][b])
        self.assertEqual(1/3, t[a][c])
        self.assertEqual(1/3, t[c][a])

    def test_transform_graph_to_weighted(self):
        (a,b,c) = ('A', 'B', 'C')
        triples = ((a,b,2), (a,c,3), (b,c,4))
        G = {}
        for (i,j,k) in triples:
            make_link(G, i, j, k)

        t = transform_graph_to_unweighted(G)
        self.assertEqual(1, t[a][b])
        self.assertEqual(1, t[b][a])
        self.assertEqual(1, t[b][c])
        self.assertEqual(1, t[c][b])
        self.assertEqual(1, t[a][c])
        self.assertEqual(1, t[c][a])
