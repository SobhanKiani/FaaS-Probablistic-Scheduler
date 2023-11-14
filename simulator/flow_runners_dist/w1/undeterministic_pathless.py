from dag.dag import DAG
import time
from utils.utils import generate_random_sample
import threading
from termcolor import cprint
from statistics import mean
import os
import random
import copy

# COLD START FR


def cold_start_fr(dag_main: DAG, dist_funcs, error=0.2, iters=100):
    durations = []
    rams = []
    dag = copy.copy(dag_main)

    for iter in range(iters):
        # experiment_path = [2, 0, 1, 2, 0]
        # experiment_path = [2, 0, 1, 1]
        # experiment_path = [1]
        total_ram_usage = 0
        total_cs_time = 0
        total_cs_count = 0
        total_sim_time = 0
        init_times = dist_funcs['cold_start']
        runtimes = dist_funcs['ex_time']
        ram_usages = dist_funcs['ram']

        i = 0
        # start_time = time.time()

        init_time = generate_random_sample(init_times[i])
        run_time = generate_random_sample(runtimes[i])
        ram_usage = generate_random_sample(ram_usages[i])

        total_ram_usage += ram_usage
        cprint(f'Running node: {i}', 'green')
        cprint(f"TIMES: {init_time} {run_time}", 'yellow')
        # time.sleep(init_time)
        # time.sleep(run_time)
        cprint(f"Node {i} finished running", 'green')
        print("")
        total_cs_time += init_time
        total_cs_count += 1
        
        total_sim_time += init_time
        total_sim_time += run_time


        while True:
            edges = list(dag.dag_wfh.G.out_edges(i, data=True))
            if len(edges) == 0:
                break

            edge_weights = [edge[2]['weight'] for edge in edges]

            # # It Uses range(len(edge_weights)) to get the indexes instead of the weights themselves
            chosen_index = random.choices(
                range(len(edge_weights)), weights=edge_weights, k=1)[0]

            
            chosen = edges[chosen_index]
            _, child, _ = chosen
            # dag.dag_wfh.update_graph_by_request(from_node=i, to_node=child)
            print("CHOSEN INDEX", chosen_index, child)

            init_time = generate_random_sample(init_times[child])
            run_time = generate_random_sample(runtimes[child])
            ram_usage = generate_random_sample(ram_usages[child])

            total_ram_usage += ram_usage
            cprint(f'Running node: {child}', 'green')
            cprint(f"TIMES {init_time} {run_time}", 'yellow')
            # time.sleep(init_time)
            # time.sleep(run_time)
            cprint(f"Node {child} finished running", 'green')
            print("")
            
            total_cs_time += init_time
            total_cs_count += 1
            
            total_sim_time += init_time
            total_sim_time += run_time

            i = child
            print('New Parent: ', i)

        # end_time = time.time()
        # d = end_time - start_time
        d = total_sim_time
        durations.append(d)
        rams.append(total_ram_usage)

        print("")
        cprint(f"------- TEST {iter} FINISHED -------", 'blue')
        print("")
        # with open(f'{os.getcwd()}/results/w1/u-cs-pathless.txt', 'a') as f:
        #     # d = durations[i]
        #     r = total_ram_usage / (1024 * 1024)
        #     f.write(f"{d},{r},{total_cs_time},{total_cs_count}\n")

    print("Durations", durations)
    print("RAM Usage: ", rams)
    print("Mean Duration: ", mean(durations))
    # with open(f'{os.getcwd()}/results/w1/w1-undeterministic-cs-pathless.txt', 'a') as f:
    #     for i in range(durations.__len__()):
    #         d = durations[i]
    #         r = rams[i] / (1024 * 1024)
    #         f.write(f"{d},{r}\n")


# MOST PROBABLE FR

def update_init_times(dag: DAG, init_times, ex_times, ram_usages, mutex, ram_using_nodes, total_ram_usage, semaphore):
    
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
        # cprint(node_idx, 'red')
        ex = mean(ex_times[node_idx])
        cs = mean(init_times[node_idx])

        children = levels[node_idx]
        cprint(children.__len__(), "red")
        # cprint(f"Thread: node - {node_idx}", 'red')
        if children.__len__() > 0:
            c_idx, c_info, c_prob = children[0]
            # sleep_time = ex + cs - 0.5 if ex + cs - 0.5 > 0 else 0
            sleep_time = ex + cs - 1 if ex + cs - 1 > 0 else 0
            # time.sleep(sleep_time)
            # time.sleep(ex + cs)
            # time.sleep(cs)

            # semaphore.acquire()
            init_times[c_idx] = [0]
            # semaphore.release()

            current_node_idx = c_idx
        else:
            break

    for node_idx, _, _ in cold_start_candidates:
        if not node_idx in ram_using_nodes:
            ram_using_nodes.append(node_idx)
            ram = generate_random_sample(ram_usages[node_idx])
            cprint(f"RAM: {node_idx}: {ram}", 'red')
            with mutex:
                total_ram_usage[0] += ram
            cprint(f"TOTAL RAM USAGE: {total_ram_usage[0]}", 'green')


def most_probable_fr(dag_main: DAG, dist_funcs, error=0.2, iters=5):
    dag = copy.copy(dag_main)
    durations = []
    rams = []

    for iter in range(iters):
        experiment_path = [2, 0, 1, 2, 0]
        # experiment_path = [2, 0, 1, 1]
        # experiment_path = [1]

        # Finding cold start candidates
        init_times = dist_funcs['cold_start']
        runtimes = dist_funcs['ex_time']
        ram_usages = dist_funcs['ram']

        ram_using_nodes = []
        # it's defined as an array so it can be passed as reference to the thread
        total_ram_usage = [0]
        total_cs_time = 0
        total_cs_count = 0
        total_sim_time = 0

        mutex = threading.Lock()
        semaphore = threading.Semaphore(1)

        cold_start_thread = threading.Thread(target=update_init_times,
                                             args=(dag, init_times, runtimes, ram_usages, mutex, ram_using_nodes, total_ram_usage, semaphore))
        cold_start_thread.start()

        i = 0
        start_time = time.time()

        init_time = generate_random_sample(init_times[i])
        run_time = generate_random_sample(runtimes[i])

        cprint(f'Running node: {i}', 'yellow')
        cprint(f"TIMES: {init_time} {run_time}", 'yellow')
        # time.sleep(init_time)
        # time.sleep(run_time)
        cprint(f"Node {i} finished running", 'yellow')
        print("")
        total_sim_time += init_time
        total_sim_time += run_time

        if i not in ram_using_nodes:
            ram_using_nodes.append(i)
            ram = generate_random_sample(ram_usages[i])
            with mutex:
                total_ram_usage[0] += ram
            total_cs_time += init_time
            total_cs_count += 1
            cprint(f"RAM: {i}: {ram}", 'cyan')
            cprint(f"TOTAL RAM USAGE: {total_ram_usage[0]}", 'green')

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
            # dag.dag_wfh.update_graph_by_request(from_node=i, to_node=child)

            init_time = generate_random_sample(init_times[child])
            run_time = generate_random_sample(runtimes[child])

            cprint(f'Running node: {child}', 'yellow')
            cprint(f"TIMES: {init_time} {run_time}", 'yellow')
            # time.sleep(init_time)
            # time.sleep(run_time)
            cprint(f"Node {child} finished running", 'yellow')
            
            total_sim_time += init_time
            total_sim_time += run_time

            if child not in ram_using_nodes:
                ram_using_nodes.append(child)
                ram = generate_random_sample(ram_usages[child])
                with mutex:
                    total_ram_usage[0] += ram
                total_cs_time += init_time
                total_cs_count += 1
                cprint(f"RAM: {child}: {ram}", 'cyan')
                cprint(f"TOTAL RAM USAGE: {total_ram_usage[0]}", 'green')

            print("")
            i = child

        # end_time = time.time()
        # d = end_time - start_time
        d = total_sim_time
        durations.append(d)
        rams.append(total_ram_usage[0])
        print("")
        cprint(f"------- TEST {iter} FINISHED -------", 'blue')
        print("")
        # with open(f'{os.getcwd()}/results/w1/u-probable-pathless.txt', 'a') as f:
        #         # d = durations[iter]
        #         r = total_ram_usage[0] / (1024 * 1024)
        #         f.write(f"{d},{r},{total_cs_time},{total_cs_count}\n")
                
    print("Durations: ", durations)
    print("Durations Mean: ", mean(durations))
    print("RAM Usage List: ", rams)



def update_init_time_optimal(dag: DAG, init_times, ex_times, ram_usages, ram_using_nodes, total_ram_usage, mutex, semaphore):
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

    for node_idx, _, _ in cold_start_candidates:
        if not node_idx in ram_using_nodes:
            ram_using_nodes.append(node_idx)
            ram = generate_random_sample(ram_usages[node_idx])
            cprint(f"RAM: {node_idx}: {ram}", 'red')
            with mutex:
                total_ram_usage[0] += ram
            cprint(f"TOTAL RAM USAGE: {total_ram_usage[0]}", 'green')


def planner(node_idx, levels, ex_times, init_times):
    ex = mean(ex_times[node_idx])
    cs = mean(init_times[node_idx])

    # cprint(f"Thread: node - {node_idx}", 'red')

    children = levels[node_idx]

    if children.__len__() > 0:
        # sleep_time = ex + cs - 0.5 if ex + cs - 0.5 > 0 else 0
        sleep_time = ex + cs - 0.5 if ex + cs - 0.5 > 0 else 0

        # time.sleep(sleep_time)

        for c_idx, c_info, c_prob in children:
            init_times[c_idx] = [0]

            p_thread = threading.Thread(target=planner, args=(
                c_idx, levels, ex_times, init_times))
            p_thread.start()


def optimal(dag_main: DAG, dist_funcs, error=0.2, iters=5):
    dag = copy.copy(dag_main)
    durations = []
    rams = []

    for iter in range(iters):

        init_times = dist_funcs['cold_start']
        runtimes = dist_funcs['ex_time']
        ram_usages = dist_funcs['ram']

        ram_using_nodes = []
        total_ram_usage = [0]
        total_cs_time = 0
        total_cs_count = 0
        total_sim_time = 0

        # Finding cold start candidates
        mutex = threading.Lock()
        semaphore = threading.Semaphore(1)
        cold_start_thread = threading.Thread(target=update_init_time_optimal,
                                             args=(dag, init_times, runtimes, ram_usages, ram_using_nodes, total_ram_usage, mutex, semaphore))
        cold_start_thread.start()

        i = 0
        # start_time = time.time()

        init_time = generate_random_sample(init_times[i])
        run_time = generate_random_sample(runtimes[i])

        cprint(f'Running node: {i}', 'green')
        cprint(f"TIMES: {init_time} {run_time}", 'yellow')
        # time.sleep(init_time)
        # time.sleep(run_time)
        cprint(f"Node {i} finished running", 'green')
        total_sim_time += init_time
        total_sim_time += run_time

        if i not in ram_using_nodes:
            ram_using_nodes.append(i)
            ram = generate_random_sample(ram_usages[i])
            with mutex:
                total_ram_usage[0] += ram
            total_cs_time += init_time
            total_cs_count += 1
            cprint(f"RAM: {i}: {ram}", 'cyan')
            cprint(f"TOTAL RAM USAGE: {total_ram_usage[0]}", 'green')
        print("")

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
            # dag.dag_wfh.update_graph_by_request(from_node=i, to_node=child)

            init_time = generate_random_sample(init_times[child])
            run_time = generate_random_sample(runtimes[child])
            cprint(f'Running node: {child}', 'green')
            cprint(f"TIMES {init_time} {run_time}", 'yellow')
            # time.sleep(init_time)
            # time.sleep(run_time)
            cprint(f"Node {child} finished running", 'green')
            
            total_sim_time += init_time
            total_sim_time += run_time

            if child not in ram_using_nodes:
                ram_using_nodes.append(child)
                ram = generate_random_sample(ram_usages[child])
                with mutex:
                    total_ram_usage[0] += ram
                total_cs_time += init_time
                total_cs_count += 1
                cprint(f"RAM: {child}: {ram}", 'cyan')
                cprint(f"TOTAL RAM USAGE: {total_ram_usage[0]}", 'green')
            print("")

            i = child
        # end_time = time.time()
        # d = end_time - start_time
        d = total_sim_time
        durations.append(d)
        rams.append(total_ram_usage[0])
        print("")
        cprint(f"------- TEST {iter} FINISHED -------", 'blue')
        print("")
        # with open(f'{os.getcwd()}/results/w1/u-optimal-parameters-pathless.txt', 'a') as f:
        #     # d = durations[iter]
        #     r = total_ram_usage[0] / (1024 * 1024)
        #     f.write(f"{d},{r},{total_cs_time},{total_cs_count}\n")  
              
    print("Durations: ", durations)
    print("Durations Mean: ", mean(durations))
    print("Total RAM: ", rams)
    
    
    # with open(f'{os.getcwd()}/results/w1/w1-undeterministic-optimal-parameters-pathless.txt', 'a') as f:
    # with open(f'{os.getcwd()}/results/w1/w1-undeterministic-optimal-pathless.txt', 'a') as f:
    #     for i in range(durations.__len__()):
    #         d = durations[i]
    #         r = rams[i] / (1024 * 1024)
    #         f.write(f"{d},{r}\n")    
