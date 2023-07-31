from dag.dag import DAG
from analysors.dag_analysis import DAGAnalysis
import random
import time
from utils.utils import generate_random_sample
import threading
from termcolor import cprint
from statistics import mean

# COLD START FR


def cold_start_fr(dag: DAG, dag_analysis: DAGAnalysis, error=0.2, iters=100):
    durations = []

    for iter in range(iters):
        experiment_path = [2, 0, 1, 2, 0]
        # experiment_path = [2, 0, 1, 1]
        # experiment_path = [1]
        
        init_times = dag_analysis.get_all_initializations()
        runtimes = dag_analysis.get_all_run_times()

        i = 0
        start_time = time.time()

        init_time = generate_random_sample(init_times[i])
        run_time = generate_random_sample(runtimes[i])
        cprint(f'Running node: {i}', 'green')
        cprint(f"TIMES: {init_time} {run_time}", 'yellow')
        time.sleep(init_time)
        time.sleep(run_time)
        cprint(f"Node {i} finished running", 'green')
        print("")

        while True:
            edges = list(dag.dag_wfh.G.out_edges(i, data=True))
            if len(edges) == 0:
                break

            # edge_weights = [edge[2]['weight'] for edge in edges]

            # # It Uses range(len(edge_weights)) to get the indexes instead of the weights themselves
            # chosen_index = random.choices(
            #     range(len(edge_weights)), weights=edge_weights, k=1)[0]

            chosen_index = experiment_path.pop(0)
            chosen = edges[chosen_index]
            _, child, _ = chosen
            dag.dag_wfh.update_graph_by_request(from_node=i, to_node=child)
            print("CHOSE INDEX", chosen_index, child)

            init_time = generate_random_sample(init_times[child])
            run_time = generate_random_sample(runtimes[child])

            cprint(f'Running node: {child}', 'green')
            cprint(f"TIMES {init_time} {run_time}", 'yellow')
            time.sleep(init_time)
            time.sleep(run_time)
            cprint(f"Node {child} finished running", 'green')
            print("")

            i = child
            print('New Parent: ', i)

        end_time = time.time()
        d = end_time - start_time
        durations.append(d)
    print(durations)


# MOST PROBABLE FR


def update_init_times(dag: DAG, init_times, ex_times, semaphore,):
    cprint("Thread Started", 'red')
    cold_start_candidates = dag.get_cold_start_candidates(parent_idx=0)

    # This should be changed by each dag
    cs_dict = {0: (0, (), {'weight': 1000})}
    for node in cold_start_candidates:
        cs_dict[node[0]] = node

    levels = {0: [cold_start_candidates[0]]}
    for node in cold_start_candidates:
        node_idx, info, prob = node
        p, c, _ = info
        if p in levels:
            levels[p].append(node)
        else:
            levels[p] = [node]

        if c not in levels:
            levels[c] = []

    current_node_idx = 0

    while True:
        node_idx, info, prbo = cs_dict[current_node_idx]
        cprint(node_idx, 'red')
        ex = mean(ex_times[node_idx])
        cs = mean(init_times[node_idx])

        children = levels[node_idx]

        cprint(f"Thread: node - {node_idx}", 'red')
        if children.__len__() > 0:
            c_idx, c_info, c_prob = children[0]

            # sleep_time = ex + cs - 0.5 if ex + cs - 0.5 > 0 else 0
            sleep_time = ex + cs - 1 if ex + cs - 1 > 0 else 0
            time.sleep(sleep_time)
            # time.sleep(ex + cs)
            # time.sleep(cs)

            # semaphore.acquire()
            init_times[c_idx] = [0]
            # semaphore.release()

            current_node_idx = c_idx
        else:
            break


def most_probable_fr(dag: DAG, dag_analysis: DAGAnalysis, error=0.2, iters=5):
    durations = []

    for iter in range(iters):
        experiment_path = [2, 0, 1, 2, 0]
        # experiment_path = [2, 0, 1, 1]
        # experiment_path = [1]

        # Finding cold start candidates
        init_times = dag_analysis.get_all_initializations()
        runtimes = dag_analysis.get_all_run_times()

        semaphore = threading.Semaphore(1)
        cold_start_thread = threading.Thread(target=update_init_times,
                                             args=(dag, init_times, runtimes, semaphore))
        cold_start_thread.start()

        i = 0
        start_time = time.time()

        init_time = generate_random_sample(init_times[i])
        run_time = generate_random_sample(runtimes[i])

        cprint(f'Running node: {i}', 'yellow')
        cprint(f"TIMES: {init_time} {run_time}", 'yellow')
        time.sleep(init_time)
        time.sleep(run_time)
        cprint(f"Node {i} finished running", 'yellow')
        print("")

        while True:
            print('Parent: ', i)

            edges = list(dag.dag_wfh.G.out_edges(i, data=True))
            if len(edges) == 0:
                break

            # edge_weights = [edge[2]['weight'] for edge in edges]

            # # It Uses range(len(edge_weights)) to get the indexes instead of the weights themselves
            # chosen_index = random.choices(
            #     range(len(edge_weights)), weights=edge_weights, k=1)[0]

            chosen_index = experiment_path.pop(0)

            chosen = edges[chosen_index]
            _, child, _ = chosen
            dag.dag_wfh.update_graph_by_request(from_node=i, to_node=child)

            init_time = generate_random_sample(init_times[child]) / 10000
            run_time = generate_random_sample(runtimes[child])

            cprint(f'Running node: {child}', 'yellow')
            cprint(f"TIMES: {init_time} {run_time}", 'yellow')
            time.sleep(init_time)
            time.sleep(run_time)
            cprint(f"Node {child} finished running", 'yellow')
            print("")

            i = child
        end_time = time.time()
        d = end_time - start_time
        durations.append(d)
        print(f"ITER {iter} FINISHED")
        print("")
    print("Durations: ", durations)
    print("Durations Mean: ", mean(durations))


def update_init_time_optimal(dag: DAG, init_times, ex_times, semaphore):
    cprint("Thread Started", 'red')
    cold_start_candidates = dag.get_cold_start_candidates(
        parent_idx=0, alpha=100)
    
    print("CS Candidates", cold_start_candidates)

    # print(cold_start_candidates)
    for node_idx, info, prob in cold_start_candidates:
        # Acquire the semaphore before updating the shared mean_init_time
        semaphore.acquire()
        init_times[node_idx] = 0
        # Release the semaphore after the update is done
        semaphore.release()

    cs_dict = {0: (0, (), {'weight': 100})}
    for node in cold_start_candidates:
        cs_dict[node[0]] = node

    levels = {0: [cold_start_candidates[0]]}
    for node in cold_start_candidates:
        node_idx, info, prob = node
        p, c, _ = info
        if p in levels:
            levels[p].append(node)
        else:
            levels[p] = [node]

        if c not in levels:
            levels[c] = []

    current_node_idx = 0

    planner(current_node_idx, levels, ex_times, init_times)


def planner(node_idx, levels, ex_times, init_times):
    ex = mean(ex_times[node_idx])
    cs = mean(init_times[node_idx])
    
    cprint(f"Thread: node - {node_idx}", 'red')

    children = levels[node_idx]

    if children.__len__() > 0:
        # sleep_time = ex + cs - 0.5 if ex + cs - 0.5 > 0 else 0
        sleep_time = ex + cs - 1 if ex + cs - 1 > 0 else 0

        time.sleep(sleep_time)

        for c_idx, c_info, c_prob in children:
            init_times[c_idx] = [0]

            p_thread = threading.Thread(target=planner, args=(
                c_idx, levels, ex_times, init_times))
            p_thread.start()


def optimal(dag: DAG, dag_analysis: DAGAnalysis, error=0.2, iters=5):

    durations = []

    for iter in range(iters):
        experiment_path = [2, 0, 1, 2, 0]
        # experiment_path = [2, 0, 1, 1]
        # experiment_path = [1]
        

        init_times = dag_analysis.get_all_initializations()
        runtimes = dag_analysis.get_all_run_times()

        # Finding cold start candidates
        semaphore = threading.Semaphore(1)
        cold_start_thread = threading.Thread(target=update_init_time_optimal,
                                             args=(dag, init_times, runtimes, semaphore))
        cold_start_thread.start()

        i = 0
        start_time = time.time()

        init_time = generate_random_sample(init_times[i])
        run_time = generate_random_sample(runtimes[i])

        cprint(f'Running node: {i}', 'green')
        cprint(f"TIMES: {init_time} {run_time}", 'yellow')
        time.sleep(init_time)
        time.sleep(run_time)
        cprint(f"Node {i} finished running", 'green')
        print("")

        while True:
            print('Parent: ', i)

            edges = list(dag.dag_wfh.G.out_edges(i, data=True))
            if len(edges) == 0:
                break

            # edge_weights = [edge[2]['weight'] for edge in edges]

            # # It Uses range(len(edge_weights)) to get the indexes instead of the weights themselves
            # chosen_index = random.choices(
            #     range(len(edge_weights)), weights=edge_weights, k=1)[0]

            chosen_index = experiment_path.pop(0)
            chosen = edges[chosen_index]
            _, child, _ = chosen
            dag.dag_wfh.update_graph_by_request(from_node=i, to_node=child)

            init_time = generate_random_sample(init_times[child]) / 10000
            run_time = generate_random_sample(runtimes[child])
            cprint(f'Running node: {child}', 'green')
            cprint(f"TIMES {init_time} {run_time}", 'yellow')
            time.sleep(init_time)
            time.sleep(run_time)
            cprint(f"Node {child} finished running", 'green')
            print("")

            i = child
        end_time = time.time()
        d = end_time - start_time
        durations.append(d)
        print(f"ITER {iter} FINISHED")
    print("Durations: ", durations)
    print("Durations Mean: ", mean(durations))
