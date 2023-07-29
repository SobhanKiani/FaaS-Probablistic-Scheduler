from analysors.container_analysis_refined import ContainerAnalysis
from dag.dag import DAG
from utils.utils import small_adj_matrix, small_image_vector
import os
import time


class DAGAnalysis:
    def __init__(self, dag: DAG, Analysis=ContainerAnalysis) -> None:
        self.dag = dag
        self.Analysis = Analysis

    def analyze_init(self, iter=100):
        for idx, image_name in enumerate(self.dag.image_vector):
            print(idx, image_name)
            try:
                container_analysis = self.Analysis(image_name, idx)
                container_analysis.calculate_initialization_time(iter)
            except:
                return f"Could Not Complete The Operation For Index {idx} In Init Times"

    def analyze_run_times(self,  iter=100, sleep_time=3, workflow_folder_name='w1'):

        for idx, image_name in enumerate(list(set(self.dag.image_vector))):
            # try:
            image_base_name = image_name.split(':')[0]
            # host_addr = f'{os.getcwd()}/functions/{workflow_folder_name}/{image_base_name}_{idx}/output/'
            host_addr = f'{os.getcwd()}/functions/{workflow_folder_name}/{image_base_name}/output/'

            container_analysis = self.Analysis(image_name, idx)
            container_analysis.calculate_running_time(
                iter=iter, host_add=host_addr, container_add='/app/output/')

            # Sleeps the code to weight for all the containers to finish running
            time.sleep(sleep_time)
            container_analysis.store_running_times()
            # except:
            #     return f"Could Not Complete The Operation For Index {idx} In Run Times"


    def analyse_both_times(self, iter=100, slee_time=3, workflow_folder_name='w1'):
        for idx, image_name in enumerate(self.dag.image_vector):
            print('Image:', image_name, "Id:", idx)
            # Getting the volumes ready
            image_base_name = image_name.split(':')[0]
            # host_addr = f'{os.getcwd()}/functions/{workflow_folder_name}/{image_base_name}_{idx}/output/'
            host_addr = f'{os.getcwd()}/functions/{workflow_folder_name}/{image_base_name}/output/'

            ca = self.Analysis(image_name, idx)
            ca.caluclate_both_times(iters=iter, host_add=host_addr, container_add='/app/output/')
                

    def get_init_time_mean(self):
        mean_list = []
        for idx, image_name in enumerate(self.dag.image_vector):
            try:
                # container_analysis = self.Analysis(image_name, idx)
                container_analysis = self.Analysis(image_name, 0)
                mean_time = container_analysis.get_mean_init_time()
                mean_list.append(mean_time)
            except :
                return f"Could Not Complete The Operation For Index {idx}"
        return mean_list

    def get_run_time_mean(self):
        mean_list = []
        for idx, image_name in enumerate(self.dag.image_vector):
            try:
                # container_analysis = self.Analysis(image_name, idx)
                container_analysis = self.Analysis(image_name, 0)
                mean_time = container_analysis.get_mean_run_time()
                mean_list.append(mean_time)
            except:
                return f"Could Not Complete The Operation For Index {idx}"
        return mean_list

    def get_all_run_times(self):
        run_times_list = []
        for idx, image_name in enumerate(self.dag.image_vector):
            try:
                container_analysis = self.Analysis(image_name, 0)
                run_times = container_analysis.get_all_running_times_list()
                run_times_list.append(run_times)
            except:
                return f"Could Not Complete The Operation For Index {idx}"
        return run_times_list

    def get_all_initializations(self):
        init_list = []
        for idx, image_name in enumerate(self.dag.image_vector):
            try:
                container_analysis = self.Analysis(image_name, 0)
                image_inits = container_analysis.get_all_init_times_list()
                init_list.append(image_inits)
            except:
                return f"Could Not Complete The Operation For Index {idx}"
        return init_list


d = DAG(adj_matrix=small_adj_matrix, image_vector=small_image_vector)
dag_analysis = DAGAnalysis(d)
# dag_analysis.analyze_init(5)
# dag_analysis.analyze_run_times(5)

# print("INIT TIME MEAN",dag_analysis.get_init_time_mean())
# print("RUN TIME MEAN", dag_analysis.get_run_time_mean())
# print(dag_analysis.get_all_run_times()[0])
