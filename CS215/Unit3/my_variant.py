def create_rooted_spanning_tree(G, root):
    green_graph = {}
    red_graph = {}
    open_list = [root]
    checked = []
    while len(open_list):
        current = open_list.pop(0)
        green_graph[current] = []
        for node in G[current]:
            if node not in checked:
                if len([child for child in green_graph.values() if node in child]) > 0:
                    if current not in red_graph:
                        red_graph[current] = []
                    red_graph[current].append(node)
                    if node not in red_graph:
                        red_graph[node] = []
                    red_graph[node].append(current)
                else:
                    green_graph[current].append(node)
                if node not in open_list:
                    open_list.append(node)
        checked.append(current)
    return green_graph, red_graph

def post_order(S, root):
    result = {}
    result[root] = get_post_order(S, root, 0, result)
    return result

def get_post_order(G, node, current, dict):
    children = G[node]
    for child in sorted(children):
        current = get_post_order(G, child, current, dict)
    current += 1
    dict[node] = current
    return current

def number_of_descendants(S, root):
    result = {}
    result[root] = get_desc_number(S, root, result)
    return result

def get_desc_number(G, node, dict):
    children = G[node]
    result = 1
    for child in children:
        result += get_desc_number(G, child, dict)
    dict[node] = result
    return result

def get_low_number(G, R, node, po, lo):
    children = G[node]
    result = []
    if node in R:
        red_children = R[node]
        result.append(po[red_children[0]])
    result.append(po[node])
    for child in children:
        result.append(get_low_number(G, R, child, po, lo))
    val = min(result)
    lo[node] = val
    return val

def get_high_number(G, R, node, po, ho):
    children = G[node]
    result = []
    if node in R:
        red_children = R[node]
        result.append(po[red_children[0]])
    result.append(po[node])
    for child in children:
        result.append(get_high_number(G, R, child, po, ho))
    val = max(result)
    ho[node] = val
    return val

def bridge_edges(G, root):
    S, R = create_rooted_spanning_tree(G, root)
    po = {}
    po[root] = get_post_order(S, root, 0, po)
    nd = {}
    nd[root] = get_desc_number(S, root, nd)
    ho = {}
    ho[root] = get_high_number(S, R, root, po, ho)
    lo = {}
    lo[root] = get_low_number(S, R, root, po, lo)
    nodes = [node for node in po if ho[node] <= po[node] and lo[node] > po[node] - nd[node] and node is not root]
    edges = []
    for node in nodes:
        upper = [c for c in G[node] if c not in S[node]]
        edges.append((upper[0], node))
    return edges



def test_create_rooted_spanning_tree():
    S = {'a': {'c': 1, 'b': 1},
         'b': {'a': 1, 'd': 1},
         'c': {'a': 1, 'd': 1},
         'd': {'c': 1, 'b': 1, 'e': 1},
         'e': {'d': 1, 'g': 1, 'f': 1},
         'f': {'e': 1, 'g': 1},
         'g': {'e': 1, 'f': 1}
    }
    S={'a': {'c': 1, 'b': 1}, 'c': {'a': 1, 'b': 1, 'd': 1}, 'b': {'a': 1, 'c': 1}, 'e': {'d': 1, 'f': 1}, 'd': {'c': 1, 'e': 1, 'g': 1, 'f': 1}, 'g': {'i': 1, 'h': 1, 'd': 1}, 'f': {'e': 1, 'd': 1}, 'i': {'h': 1, 'g': 1}, 'h': {'i': 1, 'g': 1}}

    bridges = bridge_edges(S, 'a')
    print bridges
    #assert bridges == [('d', 'e')]

test_create_rooted_spanning_tree()


