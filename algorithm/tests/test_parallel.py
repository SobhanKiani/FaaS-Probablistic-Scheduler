import pytest
import networkx as nx
from handlers import get_most_probable_children, get_graph


@pytest.fixture
def parallel_graph():
    adj_matrix = [
        [-1, 120, 80, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, 120, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, 30, 50, -1, -1],
        [-1, -1, -1, -1, 120, 120, 120, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, 80, 40, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, 70, -1, -1, 50, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 20, 100],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    ]
    G = get_graph(adj_matrix)
    return G


class TestParallel():

    def test_get_parallels(self, parallel_graph):
        result = get_most_probable_children(
            parallel_graph, parent_idx=3, l=2, alpha=10, beta=0)
        
        parallel_nodes = [4,5,6]
        result_nodes = []
        for node in result:
            result_nodes.append(node[0])
        
        
        assert len(result) == 6
        for node in parallel_nodes:
            assert node in result_nodes

    def test_get_parallels_beta(self, parallel_graph):
        result = get_most_probable_children(
            parallel_graph, parent_idx=3, l=2, alpha=10, beta=50)
        
        parallel_nodes = [4,5,6]
        result_nodes = []
        for node in result:
            result_nodes.append(node[0])
        
        
        assert len(result) == 6

        for node in parallel_nodes:
            assert node in result_nodes
