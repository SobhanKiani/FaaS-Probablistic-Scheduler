import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean


class DAGGraphHandler:
    def __init__(self, adj_matrix, dist_funcs=None) -> None:
        self.adj_matrix = adj_matrix
        self.G = self.get_graph_from_matrix(adj_matrix)
        self.dist_funcs = dist_funcs

    def get_graph_from_matrix(self, adj_matrix):
        G = nx.DiGraph()
        G.add_nodes_from(list(range(0, len(adj_matrix)-1)))
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

    # def get_most_probable_children(self, parent_idx=0, l=-1, alpha=0, beta=0, gamma=0, results=None):
    #     if results is None:
    #         results = []
    #     parent_edges = list(self.G.out_edges(parent_idx, data=True))
    #     children = list(self.G.successors(parent_idx))

    #     if len(children) == 0 or l == 0:
    #         return results
    #     else:
    #         total_weight = self.get_the_complete_incoming_weight(parent_idx)
    #         child_probs = []
    #         for i, edge in enumerate(parent_edges):
    #             weight = edge[2]['weight']
    #             prob = weight / total_weight * 100
    #             child_probs.append((children[i], edge, prob))
    #         child_probs.sort(key=lambda x: x[2], reverse=True)

    #         # is_parallel = len(child_probs) > 1 and all([child_probs[0][2] == child[2]
    #         #                                             for child in child_probs])
    #         is_parallel = False

    #         if not is_parallel:
    #             current_level_results = []
    #             final_max_prob_child, final_max_prob = child_probs[0][0], child_probs[0][2]
    #             max_prob_child, max_prob, max_prob_idx = child_probs[0][0], child_probs[0][2], 0
    #             # print("Child Probs", child_probs)
    #             for i in range(1, len(child_probs)):

    #                 if self.dist_funcs != None:
    #                     cs_mean = mean(
    #                         self.dist_funcs['cold_start'][max_prob_child])
    #                     ex_mean = mean(
    #                         self.dist_funcs['ex_time'][max_prob_child])
    #                     cs_power = cs_mean / ex_mean

    #                     if max_prob >= beta and cs_power >= gamma and max_prob_child not in [r[0] for r in results]:
    #                         results.append(
    #                             (max_prob_child, child_probs[i-1][1], max_prob))
    #                         current_level_results.append(
    #                             (max_prob_child, child_probs[i-1][1], max_prob))
    #                 else:
    #                     if max_prob >= beta and max_prob_child not in [r[0] for r in results]:
    #                         results.append(
    #                             (max_prob_child, child_probs[i-1][1], max_prob))
    #                         current_level_results.append(
    #                             (max_prob_child, child_probs[i-1][1], max_prob))

    #                 curr_prob_child, curr_prob = child_probs[i][0], child_probs[i][2]

    #                 if max_prob - curr_prob >= alpha:
    #                     break
    #                 if curr_prob < beta:
    #                     continue

    #                 if self.dist_funcs != None:
    #                     cs_mean = mean(
    #                         self.dist_funcs['cold_start'][curr_prob_child])
    #                     ex_mean = mean(
    #                         self.dist_funcs['ex_time'][curr_prob_child])

    #                     if cs_mean / ex_mean < gamma:
    #                         continue

    #                 # if max_prob_child not in [r[0] for r in results]:
    #                 #     results.append((max_prob_child, child_probs[i-1][1], max_prob))
    #                 max_prob_child, max_prob, max_prob_idx = curr_prob_child, curr_prob, i

    #             if self.dist_funcs != None:
    #                 cs_mean = mean(
    #                     self.dist_funcs['cold_start'][max_prob_child])
    #                 ex_mean = mean(
    #                     self.dist_funcs['ex_time'][max_prob_child])
    #                 cs_power = cs_mean / ex_mean

    #                 if max_prob >= beta and cs_power >= gamma and max_prob_child not in [r[0] for r in results]:
    #                     results.append(
    #                         (max_prob_child, child_probs[max_prob_idx][1], max_prob))
    #                     current_level_results.append(
    #                         (max_prob_child, child_probs[i-1][1], max_prob))

    #             else:
    #                 if max_prob >= beta and max_prob_child not in [r[0] for r in results]:
    #                     results.append(
    #                         (max_prob_child, child_probs[max_prob_idx][1], max_prob))
    #                     current_level_results.append(
    #                         (max_prob_child, child_probs[i-1][1], max_prob))

    #             if l != -1 and l <= 1:
    #                 return results
    #             elif l == -1:
    #                 # Latest
    #                 # return self.get_most_probable_children(parent_idx=final_max_prob_child, l=l, alpha=alpha,beta=beta, results=results)

    #                 for child, prob, prob_idx in current_level_results:
    #                     self.get_most_probable_children(
    #                         parent_idx=child, l=l, alpha=alpha, beta=beta, gamma=gamma, results=results)
    #                 return results

    #             else:
    #                 # Latest
    #                 # return self.get_most_probable_children(parent_idx=final_max_prob_child, l=l-1, alpha=alpha, beta=beta, results=results)

    #                 for child, prob, prob_idx in current_level_results:
    #                     self.get_most_probable_children(
    #                         parent_idx=child, l=l-1, alpha=alpha, beta=beta, gamma=gamma, results=results)
    #                 return results

    #                 # else:
    #                 # return results

    #         # else:
    #         #     for child in child_probs:
    #         #         if child[2] > beta:
    #         #             results.append(child)

    #         #     for child in child_probs:
    #         #         results += self.get_most_probable_children(
    #         #              parent_idx=child[0], l=l-1, alpha=alpha, beta=beta, results=results)

    #         #     final_results = []
    #         #     ids = []
    #         #     for node in results:
    #         #         if node[0] not in ids:
    #         #             final_results.append(node)
    #         #             ids.append(node[0])
    #         #     return final_results

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
        matrix[from_node][to_node] += 1
        self.adj_matrix = matrix
        self.G = self.get_graph_from_matrix(self.adj_matrix)
        return self.adj_matrix, self.G

    # Only gets the most probable nodes (Cold Start Candidates)
    def handle_cold_start_request(self, parent_idx: int = 0,  alpha: int = 0, beta: int = 0, gamma: int = 0, l: int = -1):
        if alpha < 0 or alpha > 100:
            raise "alpha should be in range of 0 to 100"

        if beta < 0 or beta > 100:
            raise "beta should be in range of 0 to 100"

        if l < -1:
            raise "l is a positive integer or -1"

        if parent_idx <= -1:
            raise "Parent index should be a valid index"

        if gamma < 0:
            raise "Gamma should be at least 0"

        cold_start_candidates = self.get_most_probable_children(
            parent_idx=parent_idx, l=l, alpha=alpha, gamma=gamma, beta=beta)

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

    # def xanadu_most_probable(self, parent_index=0, l=-1, results=None, probs=None):
    #     if results is None:
    #         results = []
    #         probs = {0: 1}

    #     edges_of_parent = list(self.G.out_edges(parent_index, data=True))
    #     children = list(self.G.successors(parent_index))

    #     if len(children) == 0 or l == 0:
    #         return results

    #     child_probs = []
    #     for i, edge in enumerate(edges_of_parent):
    #         child_idx = edge[1]
    #         # Get the parents for the current child
    #         incoming_edges = self.G.in_edges(child_idx, data=True)
    #         node_l = 0

    #         # iterate over the parents
    #         for source, _, info in incoming_edges:
    #             # Get the total incoming weights for the parent
    #             parent_total_incoming_weight = self.get_the_complete_incoming_weight(
    #                 source)

    #             # Find the probability of transition from the parent to the current child
    #             prob = info['weight'] / parent_total_incoming_weight
    #             # add it to the probability for the child
    #             node_l += prob

    #         total_prob = node_l * probs[parent_index]
    #         child_probs.append((children[i], edge, total_prob))

    #     child_probs = sorted(child_probs, key=lambda x: x[2], reverse=True)

    #     most_probable_child = child_probs[0]
    #     child, edge, prob = most_probable_child
    #     results.append(most_probable_child)
    #     probs[child] = prob

    #     if l == -1:
    #         results = self.xanadu_most_probable(
    #             parent_index=child, l=l, results=results, probs=probs)
    #         return results

    #     elif l >= 1:
    #         results = self.xanadu_most_probable(
    #             parent_index=child, l=l-1, results=results, probs=probs)
    #         return results

    def get_most_probable_children(self, parent_idx=0, l=-1, alpha=0, beta=0, gamma=0):
        # Initialize list for candidates
        nodes = [(0, (), 100)]
        # Initialize the queue for iterating on the nodes
        q = [((0, (), 100), 0)]
        # this variable checks for duplicated nodes
        seen_nodes = set({0})

        # check if the queue is not empty
        while q.__len__() > 0:
            # get the first index of the queue
            # u = (index, the edge from a parent to u, probability)
            u, curr_l = q.pop(0)

            # get the out edges and the children for u
            parent_out_edges = self.G.out_edges(u[0], data=True)
            children = list(self.G.successors(u[0]))

            # continue if u is an end node and doensn't have any children
            if parent_out_edges.__len__() == 0 or (l != -1 and curr_l > l):
                continue

            # get the total incoming weight to the current node
            total_weight = self.get_the_complete_incoming_weight(
                parent_idx)
            # initialize the list to store the children and their probs
            child_probs = []

            # get the probability for each child
            for i, edge in enumerate(parent_out_edges):
                weight = edge[2]['weight']
                prob = weight / total_weight * 100
                child_probs.append((children[i], edge, prob))
                # sort the children on their probabilty
            child_probs.sort(key=lambda x: x[2], reverse=True)
            most_probable_child = child_probs[0]

            # adding the most_probable node, if it hasn't been seen before
            if child_probs[0][0] not in seen_nodes:
                nodes.append(most_probable_child)
                q.append((most_probable_child, l+1))
                seen_nodes.add(most_probable_child[0])

            for i in range(1, child_probs.__len__()):
                # Find the difference between the
                # Probabilities of a node to it's immediate larger sibling
                # This is for alpha
                # the format of curr_child = (index, the edge from a parent to u, probability)
                curr_child = child_probs[i]
                diff = child_probs[i-1][2] - curr_child[2]

                # for gamma
                c_index = curr_child[0]
                cs = mean(self.dist_funcs['cold_start'][c_index])
                ex = mean(self.dist_funcs['ex_time'][c_index])

                if diff <= alpha and curr_child[2] >= beta and cs/ex > gamma and curr_child[0] not in seen_nodes:
                    nodes.append((curr_child))
                    q.append((curr_child, l+1))
                    seen_nodes.add(curr_child[0])
                else:
                    break

        return nodes

    def xanadu_most_probable(self, parent_index=0, l=-1):
        probs = {0: 1}
        nodes = [(0, (), 100)]
        q = [((0, (), 100), 0)]

        while q.__len__() > 0:
            u, curr_l = q.pop(0)
            edges_of_parents = self.G.out_edges(u[0], data=True)
            children = list(self.G.successors(u[0]))

            if children.__len__() == 0 or (l != -1 and curr_l > l):
                continue

            child_probs = []
            for i, edge in enumerate(edges_of_parents):
                child_idx = edge[1]
                incoming_edges = self.G.in_edges(child_idx, data=True)
                node_l = 0

                for source, _, info in incoming_edges:
                    # Get the total incoming weights for the parent
                    parent_total_incoming_weight = self.get_the_complete_incoming_weight(
                        source)

                    # Find the probability of transition from the parent to the current child
                    prob = info['weight'] / parent_total_incoming_weight
                    # add it to the probability for the child
                    node_l += prob

                total_prob = node_l * probs[parent_index]
                child_probs.append((children[i], edge, total_prob))
            child_probs = sorted(child_probs, key=lambda x: x[2], reverse=True)

            most_probable_child = child_probs[0]
            child, edge, prob = most_probable_child

            nodes.append(most_probable_child)
            q.append((most_probable_child, l+1))

            probs[child] = prob

        return nodes
