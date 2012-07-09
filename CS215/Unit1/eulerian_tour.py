from unittest.case import TestCase

def find_eulerian_tour(graph):
    graph_dict = {}
    for edge in graph:
        first = edge[0]
        last = edge[1]
        if first not in graph_dict:
            graph_dict[first] = [last]
        else:
            graph_dict[first].append(last)
        if last not in graph_dict:
            graph_dict[last] = [first]
        else:
            graph_dict[last].append(first)
    print graph_dict
    if len([nodes for nodes in graph_dict.values() if len(nodes)%2]):
        return []
    first_node = graph[0][0]
    current_node = first_node
    result = [first_node]
    while len([nodes for nodes in graph_dict.values() if len(nodes)]):
        next_node = graph_dict[current_node].pop()
        graph_dict[next_node].pop(graph_dict[next_node].index(current_node))
        current_node = next_node
        result.append(current_node)
    return result

class TestTour(TestCase):
    def test_simple_graph(self):
        graph = [(1, 2), (2, 3), (3, 1)]
        result = find_eulerian_tour(graph)
        self.assertAlmostEqual([1,2,3,1], result)

    def test_not_even_graph_returns_empty_list(self):
        graph = [(1, 2), (2, 3)]
        result = find_eulerian_tour(graph)
        self.assertEqual([], result)
