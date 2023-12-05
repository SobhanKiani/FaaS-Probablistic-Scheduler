from dag.dag import DAG
from analysors.dag_analysis import DAGAnalysis
import time
from utils.random_matrices import random_DAG_2, random_dag_2_cs, random_dag_2_ex, random_dag_2_ram
import threading
# from colorama import Fore
from termcolor import cprint
import os
from statistics import mean

# COLD START FR
def cold_start_fr(dag: DAG, dag_analysis: DAGAnalysis, error=0.2, iters=100):
    durations = []
    rams = []

    for iter in range(iters):
        experiment_path = [0, 1, 0, 1, 4]

        init_times = random_dag_2_cs.copy()
        runtimes = random_dag_2_ex.copy()
        rams_usages = random_dag_2_ram.copy()

        total_ram_usage = 0
        total_cs_time = 0
        total_cs_count = 0
        total_sim_time = 0

        i = 0
        # start_time = time.time()

        init_time = init_times[i]
        run_time = runtimes[i]

        print(f'Running node: {i}')
        print("TIMES", init_time, run_time)
        # time.sleep(init_time)
        # time.sleep(run_time)
        total_sim_time += init_time
        total_sim_time += run_time
        print(f"Node {i} finished running")
        total_ram_usage += rams_usages[i]
        total_cs_time += init_time
        total_cs_count += 1
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

            chosen = edges[chosen_index]
            _, child, _ = chosen
            dag.dag_wfh.update_graph_by_request(from_node=i, to_node=child)
            print("CHOSE INDEX", chosen_index, child)

            init_time = init_times[child]
            run_time = runtimes[child]

            print(f'Running node: {child}')
            print("TIMES", init_time, run_time)
            # time.sleep(init_time)
            # time.sleep(run_time)
            total_sim_time += init_time
            total_sim_time += run_time
            print(f"Node {child} finished running")
            print("")
            total_ram_usage += rams_usages[child]
            total_cs_time += init_time
            total_cs_count += 1
            
            i = child
            print('New Parent: ', i)

        # end_time = time.time()
        # d = end_time - start_time
        d =  total_sim_time
        durations.append(d)
        rams.append(total_ram_usage)
        print("")
        cprint(f"------- TEST {iter} FINISHED -------", 'yellow')
        print("")
        # with open(f'{os.getcwd()}/results/w2/d-cs.txt', 'a') as f:
        #     r = total_ram_usage
        #     f.write(f"{d},{r},{total_cs_time},{total_cs_count}\n")

    print("FINAL DURATIONS", durations)
    print("FINAL RAMS", rams)
    print("Mean of Durations: ", mean(durations))
    # with open(f'{os.getcwd()}/results/w2/d-cs.txt', 'a') as f:
    #     for i in range(durations.__len__()):
    #         d = durations[i]
    #         r = rams[i]
    #         f.write(f"{d},{r}\n")


# MOST PROBABLE FR
def update_init_times(dag: DAG, init_times, ex_times, ram_usages, semaphore, mutex, total_ram_usage, ram_using_nodes):
    cprint("Thread Started", 'red')
    cold_start_candidates = dag.get_cold_start_candidates(parent_idx=0)

    # for node_idx, info, prob in cold_start_candidates:
    #     # Acquire the semaphore before updating the shared mean_init_time
    #     semaphore.acquire()
    #     init_times[node_idx] = 0
    #     # Release the semaphore after the update is done
    #     semaphore.release()

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
        node_idx, info, prob = cs_dict[current_node_idx]
        cprint(node_idx, 'red')
        ex = ex_times[node_idx]
        cs = init_times[node_idx]

        children = levels[node_idx]

        cprint(f"Thread: node - {node_idx}", 'red')
        if children.__len__() > 0:
            c_idx, c_info, c_prob = children[0]

            sleep_time = ex + cs - 0.5 if ex + cs - 0.5 > 0 else 0
            # time.sleep(sleep_time)
            # time.sleep(ex + cs)
            # time.sleep(cs)

            # semaphore.acquire()
            init_times[c_idx] = 0
            # semaphore.release()

            current_node_idx = c_idx
        else:
            break

    for node_idx, _, _ in cold_start_candidates:
        if node_idx not in ram_using_nodes:
            mutex.acquire()
            ram_using_nodes.append(node_idx)
            total_ram_usage[0] += random_dag_2_ram[node_idx]
            mutex.release()
            cprint(f"Total Ram Usage: {total_ram_usage[0]}", 'cyan')


def most_probable_fr(dag: DAG, dag_analysis: DAGAnalysis, error=0.2, iters=5):

    rams = []
    durations = []

    for iter in range(iters):
        experiment_path = [0, 1, 0, 1, 4]

        # Finding cold start candidates
        init_times = random_dag_2_cs.copy()
        runtimes = random_dag_2_ex.copy()
        ram_usages = random_dag_2_ram.copy()

        total_ram_usage = [0]
        ram_using_nodes = []
        total_cs_time = 0
        total_cs_count = 0
        total_sim_time = 0

        semaphore = threading.Semaphore(1)
        mutex = threading.Lock()
        cold_start_thread = threading.Thread(target=update_init_times,
                                             args=(dag, init_times, runtimes, ram_usages, semaphore, mutex, total_ram_usage, ram_using_nodes))
        cold_start_thread.start()
        # cold_start_thread.join()

        i = 0
        # start_time = time.time()

        init_time = init_times[i]
        run_time = runtimes[i]
        cprint(f'Running node: {i}', 'yellow')
        cprint(f"TIMES: {init_time} {run_time}", 'yellow')
        # time.sleep(init_time)
        # time.sleep(run_time)
        total_sim_time += init_time
        total_sim_time += run_time
        cprint(f"Node {i} finished running", 'yellow')

        if i not in ram_using_nodes:
            mutex.acquire()
            ram_using_nodes.append(i)
            total_ram_usage[0] += ram_usages[i]
            mutex.release()
            total_cs_time += init_time
            total_cs_count += 1
            cprint(f"Total Ram Usage: {total_ram_usage[0]}", 'cyan')
        print("")

        while True:
            cprint(f'Parent: {i}', 'magenta')

            edges = list(dag.dag_wfh.G.out_edges(i, data=True))
            if len(edges) == 0:
                break

            # edge_weights = [edge[2]['weight'] for edge in edges]

            # # It Uses range(len(edge_weights)) to get the indexes instead of the weights themselves
            # chosen_index = random.choices(
            #     range(len(edge_weights)), weights=edge_weights, k=1)[0]

            chosen_index = experiment_path.pop(0)
            cprint(f"CHOSEN INDEX {chosen_index}", 'green')
            chosen = edges[chosen_index]
            _, child, _ = chosen

            dag.dag_wfh.update_graph_by_request(from_node=i, to_node=child)

            init_time = init_times[child]
            run_time = runtimes[child]
            cprint(f'Running node: {child}', 'green')
            cprint(f"TIMES: {init_time} {run_time}", 'yellow')
            # time.sleep(init_time)
            # time.sleep(run_time)
            total_sim_time += init_time
            total_sim_time += run_time
            cprint(f"Node {child} finished running", 'green')
            if child not in ram_using_nodes:
                mutex.acquire()
                ram_using_nodes.append(child)
                total_ram_usage[0] += ram_usages[child]
                mutex.release()
                total_cs_time += init_time
                total_cs_count += 1
                cprint(f"Total Ram Usage: {total_ram_usage[0]}", 'cyan')

            i = child
            print("")

        # end_time = time.time()
        # d = end_time - start_time
        d = total_sim_time
        durations.append(d)
        rams.append(total_ram_usage[0])

        print("")
        cprint(f"------- TEST {iter} FINISHED -------", 'yellow')
        print("")
        # with open(f'{os.getcwd()}/results/w2/d-probable.txt', 'a') as f:
        #     r = total_ram_usage[0]
        #     f.write(f"{d},{r},{total_cs_time},{total_cs_count}\n")
    print("FINAL DURATIONS", durations)
    print("FINAL RAMS", rams)
    print("Mean of Durations: ", mean(durations))


    # with open(f'{os.getcwd()}/results/w2/d-probable.txt', 'a') as f:
    #     for i in range(durations.__len__()):
    #         d = durations[i]
    #         r = rams[i]
    #         f.write(f"{d},{r}\n")


def update_init_time_optimal(dag: DAG, init_times, ex_times, ram_usages, semaphore, mutex, ram_using_nodes, total_ram_usage):
    cprint("Thread Started", 'red')
    cold_start_candidates = dag.get_cold_start_candidates(
        # parent_idx=0, alpha=100)
        parent_idx=0, alpha=50, beta=20)

    # print(cold_start_candidates)
    for node_idx, info, prob in cold_start_candidates:
        # Acquire the semaphore before updating the shared mean_init_time
        semaphore.acquire()
        init_times[node_idx] = 0
        # Release the semaphore after the update is done
        semaphore.release()

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

    planner(current_node_idx, levels, ex_times, init_times)

    for node_idx, _, _ in cold_start_candidates:
        if node_idx not in ram_using_nodes:
            mutex.acquire()
            ram_using_nodes.append(node_idx)
            total_ram_usage[0] += ram_usages[node_idx]
            mutex.release()
            cprint(f"Total Ram Usage: {total_ram_usage[0]}", 'cyan')


def planner(node_idx, levels, ex_times, init_times):
    ex = ex_times[node_idx]
    cs = init_times[node_idx]

    children = levels[node_idx]

    if children.__len__() > 0:
        sleep_time = ex + cs - 0.5 if ex + cs - 0.5 > 0 else 0
        # time.sleep(sleep_time)

        for c_idx, c_info, c_prob in children:
            init_times[c_idx] = 0

            p_thread = threading.Thread(target=planner, args=(
                c_idx, levels, ex_times, init_times))
            p_thread.start()


def optimal(dag: DAG, dag_analysis: DAGAnalysis, error=0.2, iters=5):
    durations = []
    rams = []
    # experiment_path = [2, 0, 1, 2, 0]
    # experiment_path = [2, 0, 1, 1]

    for iter in range(iters):
        experiment_path = [0, 1, 0, 1, 4]

        init_times = random_dag_2_cs
        runtimes = random_dag_2_ex
        ram_usages = random_dag_2_ram

        ram_using_nodes = []
        total_ram_usage = [0]
        total_cs_time = 0
        total_cs_count = 0
        total_sim_time = 0

        # Finding cold start candidates
        semaphore = threading.Semaphore(1)
        mutex = threading.Lock()
        cold_start_thread = threading.Thread(target=update_init_time_optimal,
                                             args=(dag, init_times, runtimes, ram_usages, semaphore, mutex, ram_using_nodes, total_ram_usage))
        cold_start_thread.start()

        i = 0
        # start_time = time.time()

        init_time = init_times[i]
        run_time = runtimes[i]
        cprint(f'Running node: {i}', 'green')
        cprint(f"TIMES: {init_time} {run_time}", 'yellow')
        # time.sleep(init_time)
        # time.sleep(run_time)
        total_sim_time += init_time
        total_sim_time += run_time
        cprint(f"Node {i} finished running", 'green')
        if i not in ram_using_nodes:
            mutex.acquire()
            ram_using_nodes.append(i)
            total_ram_usage[0] += ram_usages[i]
            mutex.release()
            total_cs_time += init_time
            total_cs_count += 1
            cprint(f"Total Ram Usage: {total_ram_usage[0]}", 'cyan')

        print("")

        while True:
            cprint(f'Parent: {i}', 'magenta')

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

            init_time = init_times[child]
            run_time = runtimes[child]
            cprint(f'Running node: {child}', 'green')
            cprint(f"TIMES {init_time} {run_time}", 'yellow')
            # time.sleep(init_time)
            # time.sleep(run_time)
            total_sim_time += init_time
            total_sim_time += run_time
            cprint(f"Node {child} finished running", 'green')
            if i not in ram_using_nodes:
                mutex.acquire()
                ram_using_nodes.append(i)
                total_ram_usage[0] += ram_usages[i]
                mutex.release()
                total_cs_time += init_time
                total_cs_count += 1
                cprint(f"Total Ram Usage: {total_ram_usage[0]}", 'cyan')

            print("")

            i = child
        # end_time = time.time()
        # d = end_time - start_time
        d = total_sim_time
        durations.append(d)
        rams.append(total_ram_usage[0])

        print("")
        cprint(f"------- TEST {iter} FINISHED -------", 'yellow')
        print("")
        # with open(f'{os.getcwd()}/results/w2/d-optimal-parameters.txt', 'a') as f:
        #     r = total_ram_usage[0]
        #     f.write(f"{d},{r},{total_cs_time},{total_cs_count}\n")

    print("FINAL DURATIONS: ", durations)
    print("FINAL RAMS: ", rams)
    print("Mean of Durations: ", mean(durations))


    # with open(f'{os.getcwd()}/results/w2/d-optimal.txt', 'a') as f:
    #     for i in range(durations.__len__()):
    #         d = durations[i]
    #         r = rams[i]
    #         f.write(f"{d},{r}\n")
