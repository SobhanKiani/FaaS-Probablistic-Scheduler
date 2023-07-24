
from analysors.dag_analysis import DAGAnalysis
from dag.dag import DAG
from utils.container_utils import run_container, get_container_ports, get_or_run_container, stop_and_remove_container, wait_for_container, wait_for_container_boot
import random
from utils.utils import send_get_request
import threading


def flask_most_probable_fr_container(dag: DAG, dag_analysis: DAGAnalysis, error=0.2):

    cold_start_candidates = dag.get_cold_start_candidates(0)
    ports = []

    # Creating Container For The First Node
    first_image = dag.image_vector[0]
    run_container(first_image, local_port=9000, container_port=5000)
    ports.append((9000, 5000))

    # Creating container for cold start candidates
    for node_idx, info, prob in cold_start_candidates:
        print('NODE IDX ', node_idx)
        image = dag.image_vector[node_idx]
        port = 9000 + node_idx
        run_container(image, local_port=port, container_port=5000)
        ports.append((port, 5000))

    i = 0
    while True:
        print('Parent: ', i)

        edges = list(dag.dag_wfh.G.out_edges(i, data=True))
        if len(edges) == 0:
            break

        edge_weights = [edge[2]['weight'] for edge in edges]

        # It Uses range(len(edge_weights)) to get the indexes instead of the weights themselves
        chosen_index = random.choices(
            range(len(edge_weights)), weights=edge_weights, k=1)[0]

        chosen = edges[chosen_index]
        _, child, _ = chosen

        local_port, container_port = ports[chosen_index]
        container = get_or_run_container(
            dag.image_vector[chosen_index], local_port=local_port, container_port=5000)

        print(f'Running node: {child}')
        res = send_get_request(f'http://127.0.0.1:{local_port}/test')
        thread = threading.Thread(
            target=stop_and_remove_container, args=(container,))
        thread.start()

        print(f"Node {child} finished running")

        i = child


def flask_cold_start_fr_container(dag: DAG, dag_analysis: DAGAnalysis, error=0.2):
    # mean_init_time = dag_analysis.get_init_time_mean()
    # mean_runtime = dag_analysis.get_run_time_mean()

    i = 0
    while True:
        print("PARENT NODE: ", i)
        edges = list(dag.dag_wfh.G.out_edges(i, data=True))
        if len(edges) == 0:
            break

        edge_weights = [edge[2]['weight'] for edge in edges]

        # It Uses range(len(edge_weights)) to get the indexes instead of the weights themselves
        chosen_index = random.choices(
            range(len(edge_weights)), weights=edge_weights, k=1)[0]

        chosen = edges[chosen_index]
        _, child, _ = chosen

        print(f'Running node: {child}')

        port = 9000 + i
        container = run_container(
            dag.image_vector[i], local_port=port, container_port=5000)

        wait_for_container_boot(container)

        res = send_get_request(f'http://127.0.0.1:{port}/test')
        thread = threading.Thread(
            target=stop_and_remove_container, args=(container,))
        thread.start()

        print(f"Node {child} finished running")

        i = child
        print('New Parent: ', i)
