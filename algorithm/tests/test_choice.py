import pytest
import networkx as nx
from handlers import get_most_probable_children, get_graph, get_number_of_requests_came_in_node, get_the_complete_incoming_weight


@pytest.fixture
def graph():
    adj_matrix = [
        [-1, 100, -1, -1, -1, -1, -1, -1],
        [-1, -1, 40, 60, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, 32, 8],
        [-1, -1, -1, -1, 18, 42, -1, -1],
        [-1, -1, -1, -1, -1, -1, 6, 12],
        [-1, -1, -1, -1, -1, -1, 7, 35],
        [-1, -1, -1, -1, -1, -1, -1, 45],
        [-1, -1, -1, -1, -1, -1, -1, -1]
    ]
    G = get_graph(adj_matrix)
    return G


class TestChoice():

    def test_level_0(self, graph: nx.Graph):
        result = get_most_probable_children(
            graph, parent_idx=1, l=0, alpha=0, beta=0)
        assert result == []

        result = get_most_probable_children(
            graph, parent_idx=3, l=0, alpha=0, beta=0)
        assert result == []

    def test_level_1(self, graph: nx.Graph):
        result = get_most_probable_children(
            graph, parent_idx=1, l=1, alpha=0, beta=0)

        assert len(result) == 1

        child = result[0]

        # checking the child index
        assert child[0] == 3
        # checking the child prob
        assert child[2] == 60

    def test_level_2(self, graph: nx.Graph):
        result = get_most_probable_children(
            graph, parent_idx=1, l=2, alpha=0, beta=0)

        assert len(result) == 2

        assert result[0][0] == 3

        # checking the second level child
        assert result[1][0] == 5
        assert result[1][2] == 70

    def test_level_all(self, graph: nx.Graph):
        result = get_most_probable_children(
            graph, parent_idx=0, l=-1, alpha=0, beta=0)
        print(result)
        assert len(result) == 4

    def test_level_1_alpha(self, graph: nx.Graph):
        result = get_most_probable_children(
            graph, parent_idx=1, l=1, alpha=50, beta=0)

        assert len(result) == 2

        assert result[0][0] == 3
        assert result[1][0] == 2

    def test_level_2_alpha_low(self, graph: nx.Graph):
        result = get_most_probable_children(
            graph, parent_idx=1, l=2, alpha=30, beta=0)

        print(result)
        assert len(result) == 3

        assert result[0][0] == 3
        assert result[1][0] == 2
        assert result[2][0] == 5

    def test_level_2_alpha_high(self, graph: nx.Graph):
        result = get_most_probable_children(
            graph, parent_idx=1, l=2, alpha=50, beta=0)

        print(result)
        assert len(result) == 4

        assert result[0][0] == 3
        assert result[1][0] == 2
        assert result[2][0] == 5
        assert result[3][0] == 4

    def test_beta_level_1(self, graph: nx.Graph):
        result = get_most_probable_children(
            graph, parent_idx=1, l=1, alpha=0, beta=100)

        assert len(result) == 0

    def test_beta_high_level_1_alpha(self, graph: nx.Graph):
        result = get_most_probable_children(
            graph, parent_idx=1, l=1, alpha=50, beta=70)

        assert len(result) == 0

    def test_beta_mid_level_1_alpha(self, graph: nx.Graph):
        result = get_most_probable_children(
            graph, parent_idx=1, l=1, alpha=50, beta=50)

        assert len(result) == 1
        assert result[0][0] == 3

    def test_beta_low_level_1_alpha(self, graph: nx.Graph):
        result = get_most_probable_children(
            graph, parent_idx=1, l=1, alpha=50, beta=30)

        assert len(result) == 2
        assert result[0][0] == 3
        assert result[1][0] == 2

    def test_beta_low_level_1_alpha_low(self, graph: nx.Graph):
        result = get_most_probable_children(
            graph, parent_idx=1, l=1, alpha=10, beta=30)

        assert len(result) == 1
        assert result[0][0] == 3

    def test_beta_mid_level_1_alpha(self, graph: nx.Graph):
        result = get_most_probable_children(
            graph, parent_idx=1, l=2, alpha=80, beta=10)

        assert len(result) == 4

        children = [child[0] for child in result]
        assert 3 in children
        assert 2 in children
        assert 4 in children
        assert 5 in children
