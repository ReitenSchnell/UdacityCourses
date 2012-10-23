from heapq import heappush, heappop
import obscure_test

filename = 'imdb'
weights_filename = 'imdb_weights'

def get_characters_from_file(filename):
    f = open(filename)
    lines =  f.readlines()
    f.close()
    marvelG = {}
    characters = []
    old_char = ''
    for line in lines:
        arr = line.replace('\n', '').split('\t')
        char, book = arr[0], arr[1]+' '+arr[2]
        make_link(marvelG, char, book, 1)
        if char != old_char:
            characters.append(char)
        old_char = char
    return marvelG, characters

def get_weights(filename):
    f = open(filename)
    lines =  f.readlines()
    f.close()
    weights = {}
    for line in lines:
        arr = line.replace('\n', '').split('\t')
        book, weight = arr[0]+' '+arr[1], arr[2]
        weights[book] = float(weight)
    return weights

def make_link(G, node1, node2, weight):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = weight
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = weight
    return G

def make_char_graph(bookG, characters, weights):
    charsG = {}
    for char1 in characters:
        for book in bookG[char1]:
            for char2 in bookG[book]:
                if char1 > char2:
                    make_weighted_link(charsG, char1, char2, weights[book])
    return charsG

def make_weighted_link(G, node1, node2, weight):
    if node1 not in G:
        G[node1] = {}
    if node2 not in G[node1]:
        (G[node1])[node2] = weight
    else:
        (G[node1])[node2] = max(((G[node1])[node2], weight))
    if node2 not in G:
        G[node2] = {}
    if node1 not in G[node2]:
        (G[node2])[node1] = weight
    else:
        (G[node2])[node1] = max(((G[node1])[node2], weight))
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
                    weight = G[w][x]
                    if x not in dist_so_far:
                        dist_so_far[x] = []
                        dist_so_far[x].append(max(final_dist[w][0], weight))
                        dist_so_far[x].append(final_dist[w][1] + [x])
                        heappush(heap,(dist_so_far[x][0], x))
                    elif max(final_dist[w][0], weight) < dist_so_far[x][0]:
                        dist_so_far[x][0] = max(final_dist[w][0], weight)
                        dist_so_far[x][1] = final_dist[w][1] + [x]
                        heappush(heap,(dist_so_far[x][0], x))
    return final_dist

def main():
    G, characters = get_characters_from_file(filename)
    weights = get_weights(weights_filename)
    G = make_char_graph(G, characters, weights)
    for t in obscure_test.test:
        start, finish = t
        dist = find_shortest_path(G, start)
        print dist[finish][0] == obscure_test.test[t]
    for t in sorted(obscure_test.answer):
        start, finish = t
        dist = find_shortest_path(G, start)
        print dist[finish]

main()
