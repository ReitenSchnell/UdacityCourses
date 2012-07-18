def create_rooted_spanning_tree(G, root):
    S = {}
    open_list = [root]
    nodes = [root]
    S[root] = {}
    while len(open_list):
        current = open_list.pop(0)
        for node in G[current]:
            if node not in S.keys():
                S[node] = {}
            if current not in S[node]:
                label = 'red' if node in nodes and current in nodes else 'green'
                S[node][current] = label
                S[current][node] = label
                open_list.append(node)
                nodes.append(node)
    return S

def test_create_rooted_spanning_tree():
    G = {'a': {'c': 1, 'b': 1},
         'b': {'a': 1, 'd': 1},
         'c': {'a': 1, 'd': 1},
         'd': {'c': 1, 'b': 1, 'e': 1},
         'e': {'d': 1, 'g': 1, 'f': 1},
         'f': {'e': 1, 'g': 1},
         'g': {'e': 1, 'f': 1}
         }
    S = create_rooted_spanning_tree(G, "a")
    assert S == {'a': {'c': 'green', 'b': 'green'},
                 'b': {'a': 'green', 'd': 'red'},
                 'c': {'a': 'green', 'd': 'green'},
                 'd': {'c': 'green', 'b': 'red', 'e': 'green'},
                 'e': {'d': 'green', 'g': 'green', 'f': 'green'},
                 'f': {'e': 'green', 'g': 'red'},
                 'g': {'e': 'green', 'f': 'red'}
                 }

def post_order(S, root):
    result = {}
    result[root] = get_post_order(S, root, None, 0, result)
    return result

def get_post_order(G, node, parent, current, po):
    children = get_children(G, node, parent)
    for child in children:
        current = get_post_order(G, child, node, current, po)
    current += 1
    po[node] = current
    return current

def get_children(G, node, parent):
    lst = []
    for child in G[node]:
        if child is not parent and G[node][child] != 'red':
            lst.append(child)
    return sorted(lst)

def test_post_order():
    S = {'a': {'c': 'green', 'b': 'green'},
         'b': {'a': 'green', 'd': 'red'},
         'c': {'a': 'green', 'd': 'green'},
         'd': {'c': 'green', 'b': 'red', 'e': 'green'},
         'e': {'d': 'green', 'g': 'green', 'f': 'green'},
         'f': {'e': 'green', 'g': 'red'},
         'g': {'e': 'green', 'f': 'red'}
         }
    po = post_order(S, 'a')
    assert po == {'a':7, 'b':1, 'c':6, 'd':5, 'e':4, 'f':2, 'g':3}

def number_of_descendants(S, root):
    result = {}
    result[root] = get_desc_number(S, root, None, result)
    return result

def get_desc_number(G, node, parent, po):
    children = get_children(G, node, parent)
    result = 1
    for child in children:
        result += get_desc_number(G, child, node, po)
    po[node] = result
    return result

def test_number_of_descendants():
    S =  {'a': {'c': 'green', 'b': 'green'},
          'b': {'a': 'green', 'd': 'red'},
          'c': {'a': 'green', 'd': 'green'},
          'd': {'c': 'green', 'b': 'red', 'e': 'green'},
          'e': {'d': 'green', 'g': 'green', 'f': 'green'},
          'f': {'e': 'green', 'g': 'red'},
          'g': {'e': 'green', 'f': 'red'}
          }
    nd = number_of_descendants(S, 'a')
    assert nd == {'a':7, 'b':1, 'c':5, 'd':4, 'e':3, 'f':1, 'g':1}

def lowest_post_order(S, root, po):
    result = {}
    result[root] = get_low_number(S, root, None, po, result)
    return result

def get_low_number(G, node, parent, po, lo):
    children = get_children(G, node, parent)
    red_children = [c for c in G[node] if G[node][c] == 'red']
    result = []
    if red_children:
        result.append(po[red_children[0]])
    result.append(po[node])
    for child in children:
        result.append(get_low_number(G, child, node, po, lo))
    val = min(result)
    lo[node] = val
    return val

def get_high_number(G, node, parent, po, lo):
    children = get_children(G, node, parent)
    red_children = [c for c in G[node] if G[node][c] == 'red']
    result = []
    if red_children:
        result.append(po[red_children[0]])
    result.append(po[node])
    for child in children:
        result.append(get_high_number(G, child, node, po, lo))
    val = max(result)
    lo[node] = val
    return val

def test_lowest_post_order():
    S = {'a': {'c': 'green', 'b': 'green'},
         'b': {'a': 'green', 'd': 'red'},
         'c': {'a': 'green', 'd': 'green'},
         'd': {'c': 'green', 'b': 'red', 'e': 'green'},
         'e': {'d': 'green', 'g': 'green', 'f': 'green'},
         'f': {'e': 'green', 'g': 'red'},
         'g': {'e': 'green', 'f': 'red'}
         }
    po = post_order(S, 'a')
    l = lowest_post_order(S, 'a', po)
    print l
    assert l == {'a':1, 'b':1, 'c':1, 'd':1, 'e':2, 'f':2, 'g':2}


def highest_post_order(S, root, po):
    result = {}
    result[root] = get_high_number(S, root, None, po, result)
    return result

def test_highest_post_order():
    S = {'a': {'c': 'green', 'b': 'green'},
         'b': {'a': 'green', 'd': 'red'},
         'c': {'a': 'green', 'd': 'green'},
         'd': {'c': 'green', 'b': 'red', 'e': 'green'},
         'e': {'d': 'green', 'g': 'green', 'f': 'green'},
         'f': {'e': 'green', 'g': 'red'},
         'g': {'e': 'green', 'f': 'red'}
         }
    po = post_order(S, 'a')
    h = highest_post_order(S, 'a', po)
    assert h == {'a':7, 'b':5, 'c':6, 'd':5, 'e':4, 'f':3, 'g':3}

def bridge_edges(G, root):
    S = create_rooted_spanning_tree(G, root)
    po = post_order(S, root)
    print po
    nd = number_of_descendants(S, root)
    print nd
    lo = lowest_post_order(S, root, po)
    print lo
    ho = highest_post_order(S, root, po)
    print ho
    nodes = [node for node in po if ho[node] <= po[node] and lo[node] > po[node] - nd[node] and node is not root]
    print nodes

def test_bridge_edges():
    G = {'a': {'c': 1, 'b': 1},
         'b': {'a': 1, 'd': 1},
         'c': {'a': 1, 'd': 1},
         'd': {'c': 1, 'b': 1, 'e': 1},
         'e': {'d': 1, 'g': 1, 'f': 1},
         'f': {'e': 1, 'g': 1},
         'g': {'e': 1, 'f': 1}
         }
    bridges = bridge_edges(G, 'a')
    assert bridges == [('d', 'e')]

test_create_rooted_spanning_tree()
test_post_order()
test_number_of_descendants()
test_lowest_post_order()
test_highest_post_order()
test_bridge_edges()
