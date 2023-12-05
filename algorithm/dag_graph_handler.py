import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


class DAGGraphHandler:
    def __init__(self, adj_matrix) -> None:
        self.adj_matrix = adj_matrix
        self.G = self.get_graph_from_matrix(adj_matrix)

    def get_graph_from_matrix(self, adj_matrix):
        G = nx.DiGraph()
        for i in range(len(adj_matrix)):
            for j in range(len(adj_matrix)):
                if adj_matrix[i][j] >= 0:
                    G.add_edge(i, j, weight=adj_matrix[i][j])
        return G

    def show_graph_with_weights(self):
        pos = nx.spring_layout(self.G)
        nx.draw(self.G, pos, with_labels=True)

        # Create a dictionary of edge labels
        edge_labels = {(u, v): d["weight"]
                       for u, v, d in self.G.edges(data=True)}

        # Draw the edge labels
        nx.draw_networkx_edge_labels(
            self.G, pos, edge_labels=edge_labels, font_color="red")

        plt.show()

    def get_number_of_requests_came_in_node(self, node_idx):

        if node_idx == 0:
            # The number of incoming and outgoing requests for the first node is equal
            edges = list(self.G.out_edges(node_idx, data=True))
        else:
            edges = list(self.G.in_edges(node_idx, data=True))

        number_of_requests = 0
        for _, _, edge_data in edges:
            number_of_requests += edge_data['weight']

        return number_of_requests

    # The other implementation for the last code
    def get_the_complete_incoming_weight(self, node_idx):
        if node_idx != 0:
            return sum(edge[2]['weight'] for edge in self.G.in_edges(node_idx, data=True))
        else:
            return sum(edge[2]['weight'] for edge in self.G.out_edges(node_idx, data=True))

    def get_most_probable_children(self, parent_idx, l=-1, alpha=0, beta=0, results=None):
        if results is None:
            results = []
        parent_edges = list(self.G.out_edges(parent_idx, data=True))
        children = list(self.G.successors(parent_idx))

        if len(children) == 0 or l == 0:
            return results
        else:
            total_weight = self.get_the_complete_incoming_weight(parent_idx)
            child_probs = []
            for i, edge in enumerate(parent_edges):
                weight = edge[2]['weight']
                prob = weight / total_weight * 100
                child_probs.append((children[i], edge, prob))
            child_probs.sort(key=lambda x: x[2], reverse=True)

            is_parallel = len(child_probs) > 1 and all([child_probs[0][2] == child[2]
                                                        for child in child_probs])

            if not is_parallel:
                final_max_prob_child, final_max_prob = child_probs[0][0], child_probs[0][2]
                max_prob_child, max_prob, max_prob_idx = child_probs[0][0], child_probs[0][2], 0
                for i in range(1, len(child_probs)):
                    if max_prob >= beta and max_prob_child not in [r[0] for r in results]:
                        results.append(
                            (max_prob_child, child_probs[i-1][1], max_prob))

                    curr_prob_child, curr_prob = child_probs[i][0], child_probs[i][2]
                    if max_prob - curr_prob >= alpha:
                        break
                    if curr_prob < beta:
                        continue
                    # if max_prob_child not in [r[0] for r in results]:
                    #     results.append((max_prob_child, child_probs[i-1][1], max_prob))
                    max_prob_child, max_prob, max_prob_idx = curr_prob_child, curr_prob, i

                if max_prob >= beta and max_prob_child not in [r[0] for r in results]:
                    results.append(
                        (max_prob_child, child_probs[max_prob_idx][1], max_prob))

                if l != -1 and l <= 1:
                    return results
                elif l == -1:
                    # if final_max_prob >= beta or final_max_prob_child in [r[0] for r in results]:
                    #     return get_most_probable_children(G, final_max_prob_child, l, alpha, beta, results)
                    # else:
                    return self.get_most_probable_children(self.G, final_max_prob_child, l, alpha, beta, results)
                else:
                    # if max_prob >= beta or max_prob_child in [r[0] for r in results]:
                    return self.get_most_probable_children(self.G, final_max_prob_child, l-1, alpha, beta, results)
                    # else:
                    # return results

            else:
                for child in child_probs:
                    if child[2] > beta:
                        results.append(child)

                for child in child_probs:
                    results += self.get_most_probable_children(
                        self.G, child[0], l-1, alpha, beta, results)

                final_results = []
                ids = []
                for node in results:
                    if node[0] not in ids:
                        final_results.append(node)
                        ids.append(node[0])
                return final_results

    def get_resource_fraction(self, probable_children):
        # Group the results by parent index
        groups = {}
        for result in probable_children:
            parent_idx = result[1][0]
            if parent_idx not in groups:
                groups[parent_idx] = []
            groups[parent_idx].append(result)

        # Calculate resource fractions for each group
        resource_fractions = []
        for parent_idx, group_results in groups.items():
            total_prob = sum(result[2] for result in group_results)
            for result in group_results:
                child_idx = result[0]
                child_prob = result[2]
                if len(group_results) == 1:
                    resource_fraction = 1.0
                else:
                    resource_fraction = child_prob / total_prob
                result[1][2]['resource_fraction'] = resource_fraction
                resource_fractions.append(result)

        return resource_fractions

    def update_graph_by_request(self, from_node: int, to_node: int):
        matrix = self.adj_matrix
        matrix[from_node, to_node] += 1
        self.adj_matrix = matrix
        self.G = self.get_graph_from_matrix(self.adj_matrix)
        return self.adj_matrix, self.G

    # Only gets the most probable nodes (Cold Start Candidates)
    def handle_cold_start_request(self, parent_idx: int,  alpha: int, beta: int, l: int):
        if alpha < 0 or alpha > 100:
            raise "alpha should be in range of 0 to 100"

        if beta < 0 or beta > 100:
            raise "beta should be in range of 0 to 100"

        if l < -1:
            raise "l is a positive integer or -1"

        if parent_idx <= -1:
            raise "Parent index should be a valid index"

        cold_start_candidates = self.get_most_probable_children(
            parent_idx=parent_idx, l=l, alpha=alpha, beta=beta)

        return cold_start_candidates

    # Update the matrix and gets the most probable graphs
    # def hanle_update_matrix_and_get_cold_start_cnandidates(self, from_node: int, to_node: int, alpha: int, beta: int, l: int):
    #     adj_matrix, G = self.update_graph_by_request(
    #         from_node=from_node, to_node=to_node)

    #     if alpha < 0 or alpha > 100:
    #         raise "alpha should be in range of 0 to 100"

    #     if beta < 0 or beta > 100:
    #         raise "beta should be in range of 0 to 100"

    #     if l < -1:
    #         raise "l is a positive integer or -1"

    #     cold_start_candidates = self.get_most_probable_children(
    #         to_node, l, alpha, beta)

    #     return adj_matrix, G, cold_start_candidates
