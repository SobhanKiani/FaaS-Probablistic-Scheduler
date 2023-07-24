from dag.dag import DAG
from analysors.dag_analysis import DAGAnalysis
import random
import time
from utils.utils import send_get_request, generate_random_sample
from utils.container_utils import get_container_ports, get_or_run_container, run_container, stop_and_remove_container, wait_for_container, wait_for_container_boot
import threading


# experiment_path = [1, 3, 5, 6, 7]

# COLD START FR
def cold_start_fr(dag: DAG, dag_analysis: DAGAnalysis, error=0.2):
    # experiment_path = [0, 1, 1, 0, 0]
    experiment_path = [0, 0, 0, 0]
    # experiment_path = [0, 1, 1, 1]

    init_times = dag_analysis.get_all_initializations()
    runtimes = dag_analysis.get_all_run_times()

    i = 0
    while True:
        edges = list(dag.dag_wfh.G.out_edges(i, data=True))
        if len(edges) == 0:
            break

        edge_weights = [edge[2]['weight'] for edge in edges]

        # It Uses range(len(edge_weights)) to get the indexes instead of the weights themselves
        # chosen_index = random.choices(
        #     range(len(edge_weights)), weights=edge_weights, k=1)[0]

        chosen_index = experiment_path.pop(0)

        chosen = edges[chosen_index]
        _, child, _ = chosen
        print("CHOSE INDEX", chosen_index, child)

        init_time = generate_random_sample(init_times[child]) / 10000
        run_time = generate_random_sample(runtimes[child])

        print(f'Running node: {child}')
        print("TIMES", init_time, run_time)
        time.sleep(init_time)
        time.sleep(run_time)
        print(f"Node {child} finished running")
        print("")

        i = child
        print('New Parent: ', i)


# MOST PROBABLE FR


def update_init_times(dag, init_times, semaphore):

    cold_start_candidates = dag.get_cold_start_candidates(0)
    for node_idx, info, prob in cold_start_candidates:
        # Acquire the semaphore before updating the shared mean_init_time
        semaphore.acquire()
        init_times[node_idx] = [0]
        # Release the semaphore after the update is done
        semaphore.release()


def most_probable_fr(dag: DAG, dag_analysis: DAGAnalysis, error=0.2):
    # experiment_path = [0, 1, 0, 0, 0]
    experiment_path = [0, 0, 0, 0]
    # experiment_path = [0, 1, 1, 1]

    init_times = dag_analysis.get_all_initializations()
    runtimes = dag_analysis.get_all_run_times()

    # Finding cold start candidates
    semaphore = threading.Semaphore(1)
    cold_start_thread = threading.Thread(target=update_init_times,
                                         args=(dag, init_times, semaphore))
    cold_start_thread.start()
    cold_start_thread.join()
    # cold_start_candidates = dag.get_cold_start_candidates(0)
    # for node_idx, info, prob in cold_start_candidates:
    #     mean_init_time[node_idx] = 0

    i = 0
    while True:
        print('Parent: ', i)

        edges = list(dag.dag_wfh.G.out_edges(i, data=True))
        if len(edges) == 0:
            break

        edge_weights = [edge[2]['weight'] for edge in edges]

        # It Uses range(len(edge_weights)) to get the indexes instead of the weights themselves
        # chosen_index = random.choices(
        #     range(len(edge_weights)), weights=edge_weights, k=1)[0]
        chosen_index = experiment_path.pop(0)

        chosen = edges[chosen_index]
        _, child, _ = chosen

        init_time = generate_random_sample(init_times[child]) / 10000
        run_time = generate_random_sample(runtimes[child])
        print("TIMES", init_time, run_time)
        print(f'Running node: {child}')
        time.sleep(init_time)
        time.sleep(run_time)
        print(f"Node {child} finished running")
        print("")

        i = child


def update_init_time_optimal(dag, init_times, semaphore):

    cold_start_candidates = dag.get_cold_start_candidates(0, alpha=100)
    # print(cold_start_candidates)
    for node_idx, info, prob in cold_start_candidates:
        # Acquire the semaphore before updating the shared mean_init_time
        semaphore.acquire()
        init_times[node_idx] = [0]
        # Release the semaphore after the update is done
        semaphore.release()
    print(init_times[1])



def optimal(dag: DAG, dag_analysis: DAGAnalysis, error=0.2):
    # experiment_path = [0, 1, 0, 0, 0]
    experiment_path = [0, 0, 0, 0]
    # experiment_path = [0, 1, 1, 1]

    init_times = dag_analysis.get_all_initializations()
    runtimes = dag_analysis.get_all_run_times()


    # Finding cold start candidates
    semaphore = threading.Semaphore(1)
    cold_start_thread = threading.Thread(target=update_init_time_optimal,
                                         args=(dag, init_times, semaphore))
    cold_start_thread.start()
    cold_start_thread.join()
    # cold_start_candidates = dag.get_cold_start_candidates(0)
    # for node_idx, info, prob in cold_start_candidates:
    #     mean_init_time[node_idx] = 0

    i = 0
    while True:
        print('Parent: ', i)

        edges = list(dag.dag_wfh.G.out_edges(i, data=True))
        if len(edges) == 0:
            break

        edge_weights = [edge[2]['weight'] for edge in edges]

        # It Uses range(len(edge_weights)) to get the indexes instead of the weights themselves
        # chosen_index = random.choices(
        #     range(len(edge_weights)), weights=edge_weights, k=1)[0]
        chosen_index = experiment_path.pop(0)

        chosen = edges[chosen_index]
        _, child, _ = chosen

        init_time = generate_random_sample(init_times[child]) / 10000
        run_time = generate_random_sample(runtimes[child])
        print("TIMES", init_time, run_time)
        print(f'Running node: {child}')
        time.sleep(init_time)
        time.sleep(run_time)
        print(f"Node {child} finished running")
        print("")

        i = child
