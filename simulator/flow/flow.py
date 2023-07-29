from dag.dag import DAG
from analysors.dag_analysis import DAGAnalysis
from analysors.container_analysis_refined import ContainerAnalysis
from types import FunctionType
import time


class Flow:
    def __init__(self, adj_matrix, image_vector, dag_id=None, Analysis=ContainerAnalysis) -> None:
        self.adj_matrix = adj_matrix
        self.image_vector = image_vector
        self.dag = DAG(self.adj_matrix, self.image_vector, dag_id)
        self.dag_analysis = DAGAnalysis(self.dag, Analysis=Analysis)

    def analyze_dag(self, iter=100):
        # try:
        # self.dag_analysis.analyze_run_times(iter, 3, 'w1')
        # self.dag_analysis.analyze_init(iter)
        self.dag_analysis.analyse_both_times(iter, 3, 'w1')
        self.mean_init_time = self.dag_analysis.get_init_time_mean()
        self.mean_run_time = self.dag_analysis.get_run_time_mean()
        # except:
        #     return "Error"

    def set_flow_runner(self, flow_runner: FunctionType):
        self.flow_runner = flow_runner

    def start_flow_runner(self, iters=None):
        start_time = time.time()
        self.flow_runner(self.dag, self.dag_analysis, iters=iters)
        end_time = time.time()
        self.last_duration = end_time - start_time
        print("Duration Of The Flow: ", self.last_duration)

    def plot_init_histogram(self, image_name, node_idx):
        ca = ContainerAnalysis(image_name, node_idx)
        ca.plot_init_time_hist()

    def plot_runtime_histogram(self, image_name, node_idx):
        ca = ContainerAnalysis(image_name, node_idx)
        ca.plot_runtime_hist()
