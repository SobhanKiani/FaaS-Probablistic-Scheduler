import redis
import uuid
import json
from dag.dag_graph_handler import DAGGraphHandler


class DAG:
    def __init__(self, adj_matrix: list = None, image_vector: list = None, dag_id: str = None) -> None:
        # Gets A DAG As Input
        if adj_matrix and image_vector:
            self.adj_matrix = adj_matrix
            self.image_vector = image_vector
            self.redis_client = redis.Redis(
                host='localhost', port=32768, username='default', password='redispw')
            self.dag_wfh: DAGGraphHandler = self.to_graph_handler()

        # Gets DAG ID As Input
        if dag_id:
            self.dag_id = dag_id

        if not dag_id and not adj_matrix:
            raise "You Should Provde DAG Id Or The Adjacency Matrix Of The DAG"

    # Stores The Adj Matrix And Images From DB
    def store_in_db(self):
        self.dag_id = uuid()
        self.adj_matrix_str = json.dumps(self.adj_matrix)
        self.image_vector_str = json.dumps(self.image_vector)

        self.redis_client.set(self.dag_id, self.adj_matrix_str)
        self.redis_client.set(
            f'{self.dag_id}:image_vector', self.image_vector_str)

    # Fetch The Adj Matrix And Images From DB
    def fetch_dag_from_db(self):
        if not self.dag_id:
            raise "DAG id is not defined"

        self.adj_matrix_str = self.redis_client.get(self.dag_id)
        self.adj_matrix = json.loads(self.adj_matrix_str)

        self.image_vector_str = self.redis_client.get(self.dag_id)
        self.image_vector = self.redis_client.get(
            f'{self.dag_id}:image_vector')

        self.to_graph_handler(self.adj_matrix)
        return self.adj_matrix, self.image_vector

    # Updates the DAG in DB
    def update_in_db(self):
        if not self.dag_id:
            raise "DAG id is not defined"
        self.redis_client.set(self.dag_id, self.adj_matrix_str)

    # Remove The DAG from DB
    def remove_from_db(self):
        if not self.dag_id:
            raise "DAG id is not defined"

        self.redis_client.delete(self.dag_id)
        self.redis_client.delete(f'{self.dag_id}:image_vector')

    # Creates a DAGGraphHanlder From The DAG
    def to_graph_handler(self):
        self.dag_wfh = DAGGraphHandler(self.adj_matrix)
        return self.dag_wfh

    # Gets a transition and updates the matrix
    def update_by_transition(self, from_node: int, to_node: int):
        if not self.dag_wfh:
            raise "No Workflow handler for the matrix is defined"

        updated_matrix, _ = self.dag_wfh.update_graph_by_request(
            from_node, to_node)

        self.adj_matrix = updated_matrix
        self.adj_matrix_str = json.loads(self.adj_matrix)

        self.update_in_db()
        return self.adj_matrix

    # Gets a new matrix and updates the latest matrix
    def update_by_new_matrix(self, updated_adj_matrix):
        self.adj_matrix = updated_adj_matrix
        self.adj_matrix_str = json.dumps(updated_adj_matrix)
        self.update_in_db()
        self.dag_wfh = self.to_graph_handler()
        return self.adj_matrix

    # Only gets cold start candidates
    def get_cold_start_candidates(self, parent_idx: int,  alpha: int = 0, beta: int = 0, l: int = -1):
        candidates = self.dag_wfh.handle_cold_start_request(
            parent_idx=parent_idx, alpha=alpha, beta=beta, l=l)
        return candidates

    # Update the matrix and get the cold start candidates
    def handle_request_and_cold_start(self, from_node: int, to_node: int, alpha: int, beta: int, l: int):
        self.update_by_transition(from_node=from_node, to_node=to_node)
        cold_start_candidates = self.get_cold_start_candidates(
            parent_idx=to_node, alpha=alpha, beta=beta, l=l)

        return cold_start_candidates

    # Updates the matrix and gets the cold start candidates using
    # hanle_update_matrix_and_get_cold_start_cnandidates method of DAGGraphHandler
    # This method updates the matrix and return the cold start candidates in a single method
    # def handle_request_and_cold_start_simultaneously(self, from_node: int, to_node: int, alpha: int, beta: int, l: int):
    #     updated_adj_matrix, _, cold_start_candidates = self.dag_wfh.hanle_update_matrix_and_get_cold_start_cnandidates(
    #         from_node=from_node, to_node=to_node, alpha=alpha, beta=beta, l=l)

    #     self.update_by_new_matrix(updated_adj_matrix)
    #     return updated_adj_matrix, cold_start_candidates
