#
# In lecture, we took the bipartite Marvel graph,
# where edges went between characters and the comics
# books they appeared in, and created a weighted graph
# with edges between characters where the weight was the
# number of comic books in which they both appeared.
#
# In this assignment, determine the weights between
# comic book characters by giving the probability
# that a randomly chosen comic book containing one of
# the characters will also contain the other
#

def create_weighted_graph(bipartiteG, characters):
    G = {}
    for char1 in characters:
        for book in bipartiteG[char1]:
            for char2 in bipartiteG[book]:
                if char1 > char2:
                    set1 = set(bipartiteG[char1])
                    set2 = set(bipartiteG[char2])
                    weight = 1.0*len(set1&set2)/len(set1|set2)
                    make_link(G, char1, char2, weight)
    return G

def make_link(G, node1, node2, weight):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = weight
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = weight
    return G


######
#
# Test

def test():
    bipartiteG = {'charA':{'comicB':1, 'comicC':1},
                  'charB':{'comicB':1, 'comicD':1},
                  'charC':{'comicD':1},
                  'comicB':{'charA':1, 'charB':1},
                  'comicC':{'charA':1},
                  'comicD': {'charC':1, 'charB':1}}
    G = create_weighted_graph(bipartiteG, ['charA', 'charB', 'charC'])
    # three comics contain charA or charB
    # charA and charB are together in one of them
    print G
    assert G['charA']['charB'] == 1.0 / 3
    assert G['charA'].get('charA') == None
    assert G['charA'].get('charC') == None

test()