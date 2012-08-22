from unittest import TestCase

def parent(i):
    return (i-1)/2
def left_child(i):
    return 2*i+1
def right_child(i):
    return 2*i+2
def is_leaf(heap,i):
    return (left_child(i) >= len(heap)) and (right_child(i) >= len(heap))
def one_child(heap,i):
    return (left_child(i) < len(heap)) and (right_child(i) >= len(heap))

def add_value_to_heap(heap, new_item):
    heap.append(new_item)
    new_pos = len(heap) - 1
    while heap[parent(new_pos)][1] > heap[new_pos][1] and new_pos>0:
        heap[parent(new_pos)], heap[new_pos] = heap[new_pos], heap[parent(new_pos)]
        new_pos = parent(new_pos)
    return

def remove_node_and_rebuild(heap, node):
    index = heap.index(node)
    top = heap.pop(index)
    heap_down(heap, index)
    return top

def heap_down(heap, i):
    if is_leaf(heap, i): return
    if one_child(heap, i):
        if heap[i][1] > heap[left_child(i)][1]:
            heap[i], heap[left_child(i)] = heap[left_child(i)], heap[i]
        return
    if min(heap[left_child(i)][1], heap[right_child(i)][1]) >= heap[i][1] : return
    if heap[left_child(i)][1] < heap[right_child(i)][1]:
        heap[i], heap[left_child(i)] = heap[left_child(i)], heap[i]
        heap_down(heap, left_child(i))
        return
    heap[i], heap[right_child(i)] = heap[right_child(i)], heap[i]
    heap_down(heap, right_child(i))
    return

def get_node_by_name(heap, node_name):
    nodes = [n for n in heap if n[0] == node_name]
    if len(nodes):
        return nodes[0]
    else:
        return None


class HeapTests(TestCase):
    def setUp(self):
        self.list = [('a', 2), ('b', 4), ('c', 3), ('d', 5), ('e', 9), ('f', 7), ('g', 7)]

    def test_add_value_to_heap(self):
       add_value_to_heap(self.list, ('h', 1))
       self.assertEqual(('h', 1), self.list[0])
       self.assertEqual(('a', 2), self.list[1])

    def test_remove_node_and_rebuild_check_result_if_top(self):
        result = remove_node_and_rebuild(self.list, self.list[0])
        self.assertEqual(('a', 2), result)

    def test_remove_node_and_rebuild_check_heap_if_top(self):
        remove_node_and_rebuild(self.list, self.list[0])
        self.assertEqual( [('c', 3), ('b', 4), ('d', 5), ('e', 9), ('f', 7), ('g', 7)], self.list)

    def test_get_node_by_name_found(self):
        result = get_node_by_name(self.list, 'd')
        self.assertEquals(('d', 5), result)

    def test_get_node_by_name_not_found(self):
        result = get_node_by_name(self.list, 'y')
        self.assertEquals(None, result)

def shortest_dist_node(dist):
    best_node = 'undefined'
    best_value = 1000000
    for v in dist:
        if dist[v] < best_value:
            (best_node, best_value) = (v, dist[v])
    return best_node

def dijkstra(G,v):
    root = (v,0)
    dist_so_far = [root]
    final_dist = {}
    while len(final_dist) < len(G):
        node = remove_node_and_rebuild(dist_so_far, dist_so_far[0])
        node_name, node_val = node[0], node[1]
        # lock it down!
        final_dist[node_name] = node_val
        for x in G[node_name]:
            if x not in final_dist:
                x_node = get_node_by_name(dist_so_far, x)
                if not x_node:
                    add_value_to_heap(dist_so_far, (x, final_dist[node_name] + G[node_name][x]))
                elif final_dist[node_name] + G[node_name][x] < x_node[1]:
                    #add_value_to_heap(dist_so_far, (x, final_dist[node_name] + G[node_name][x]))
                    dist_so_far[dist_so_far.index(x_node)] = (x, final_dist[node_name] + G[node_name][x])
        print final_dist
    return final_dist

def make_link(G, node1, node2, w):
    if node1 not in G:
        G[node1] = {}
    if node2 not in G[node1]:
        (G[node1])[node2] = 0
    (G[node1])[node2] += w
    if node2 not in G:
        G[node2] = {}
    if node1 not in G[node2]:
        (G[node2])[node1] = 0
    (G[node2])[node1] += w
    return G

def test():
    # shortcuts
    (a,b,c,d,e,f,g) = ('A', 'B', 'C', 'D', 'E', 'F', 'G')
    triples = ((a,c,3),(c,b,10),(a,b,15),(d,b,9),(a,d,4),(d,f,7),(d,e,3),
               (e,g,1),(e,f,5),(f,g,2),(b,f,1))
    G = {}
    for (i,j,k) in triples:
        make_link(G, i, j, k)

    dist = dijkstra(G, a)
    assert dist[g] == 8 #(a -> d -> e -> g)
    assert dist[b] == 11 #(a -> d -> e -> g -> f -> b)
    print 'success'
test()






