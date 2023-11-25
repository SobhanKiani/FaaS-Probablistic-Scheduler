from dag.dag import DAG
from types import FunctionType
import time
import numpy as np
import matplotlib.pyplot as plt


class FlowDistFunc:
    def __init__(self, adj_matrix, image_vector, dist_funcs, dag_id=None) -> None:
        self.adj_matrix = adj_matrix
        self.image_vector = image_vector
        self.dag = DAG(adj_matrix, image_vector, dag_id, dist_funcs)
        self.dist_funcs = dist_funcs

    def set_flow_runner(self, flow_runner: FunctionType):
        self.flow_runner = flow_runner

    def start_flow_runner(self, iters=None):
        self.flow_runner(self.dag, self.dist_funcs, iters=iters)


    def plot_init_histogram(self, node_idx):
        dist_function = self.dist_funcs['cold_start'][node_idx]
        plt.hist(dist_function, bins=5, density=True, alpha=0.5, color='blue')
        plt.xlabel('CS')
        plt.ylabel('Frequency')
        plt.title('CS Histogram')
        plt.show()

    def plot_execution_histogram(self, node_idx):
        dist_function = self.dist_funcs['ex_time'][node_idx]
        plt.hist(dist_function, bins=5, density=True, alpha=0.5, color='blue')
        plt.xlabel('EX')
        plt.ylabel('Frequency')
        plt.title('EX Histogram')
        plt.show()

    def plot_ram_usage_histogram(self, node_idx):
        dist_function = self.dist_funcs['ram'][node_idx]
        plt.hist(dist_function, bins=5, density=True, alpha=0.5, color='blue')
        plt.xlabel('RAM')
        plt.ylabel('Frequency')
        plt.title('RAM Histogram')
        plt.show()
