from dag.dag import DAG
import copy
from queue import Queue
from threading import Thread
from utils.utils import generate_random_sample
from statistics import mean
import random
from termcolor import cprint
from .utils import Job, store_in_file


def time_handler(jobs: Queue, total_durations: list, total_rams: list, total_cs_counts: list, total_cs_durations: list, ):
    flow_ram_value = []  # The time and amount of ram allocation to each node
    flow_ram_usage = 0  # Total Usage Of RAM
    flow_cs_time = 0
    flow_cs_count = 0
    flow_sim_time = 0

    while True:
        item: Job = jobs.get()
        if item.topic == 'Finish':
            print("Flow Finished")
            print("")
            break
        else:
            if item.topic == 'CS':
                if item.value > 0:
                    flow_cs_time += item.value
                    flow_cs_count += 1
                    flow_sim_time += item.value

            elif item.topic == 'EX':
                flow_sim_time += item.value

            elif item.topic == 'RAM_START':
                curr_rds = [rd for rd in flow_ram_value if rd['node']
                            == item.value['node']]

                if curr_rds.__len__() == 0:
                    print("Adding ram for node: ",
                          item.value['node'], ",", item.value['amount'])
                    ram_data = {
                        "node": item.value['node'],
                        'amount': item.value['amount'],
                        'allocation_start_time': flow_sim_time
                    }
                    flow_ram_value.append(ram_data)
                    flow_ram_usage += item.value['amount']

            elif item.topic == 'RAM_START_BY_TIME':
                print("Adding ram for node: ",
                      item.value['node'], ",", item.value['amount'], "Time: ", item.value['time'])

                curr_rds = [rd for rd in flow_ram_value if rd['node']
                            == item.value['node']]
                if curr_rds.__len__() == 0:
                    ram_data = {
                        'node': item.value['node'],
                        'amount': item.value['amount'],
                        'allocation_start_time': item.value['time']
                    }
                    flow_ram_value.append(ram_data)
                    flow_ram_usage += item.value['amount']

                else:
                    curr_rd = curr_rds[0]
                    if curr_rd['allocation_start_time'] > item.value['time']:
                        # Remove the last ram data of the node
                        keeping_rds = [rd for rd in flow_ram_value if rd['node']
                                       != item.value['node']]
                        # Add the new one
                        keeping_rds.append({
                            'node': item.value['node'],
                            'amount': item.value['amount'],
                            'allocation_start_time': item.value['time']
                        })

            elif item.topic == 'RAM_END':
                ram_start_data = [
                    ram_data for ram_data in flow_ram_value if ram_data['node'] == item.value['node']][0]

                if ram_start_data and ram_start_data['allocation_start_time'] < flow_sim_time:
                    # ram_usage = (
                    #     flow_sim_time - ram_start_data['allocation_start_time']) * ram_start_data['amount']
                    ram_usage = ram_start_data['amount']
                    # flow_ram_usage += ram_usage

    cprint(f"FLOW RAM VALUE: {flow_ram_value}", 'red')
    total_durations.append(flow_sim_time)
    total_rams.append(flow_ram_usage)
    total_cs_counts.append(flow_cs_count)
    total_cs_durations.append(flow_cs_time)

    jobs.put(Job(topic="FLOW ENDED", value=None))

    # print(total_durations)
    # print(total_rams)
    # print(total_cs_durations)
    # print(total_cs_counts)


def allocate_function(node: int, ex: float, cs: float, ram: float, jobs: Queue):
    jobs.put(Job(topic='RAM_START', value={'node': node, 'amount': ram}))
    cprint(f'RAM Allocated For Node {node}: {ram}', 'yellow')

    jobs.put(Job(topic='CS', value=cs))
    cprint(f'CS For Node {node}: {cs}', 'blue')

    jobs.put(Job(topic='EX', value=ex))
    cprint(f'EX For Node {node}: {ex}', 'cyan')

    jobs.put(Job(topic='RAM_END', value={'node': node}))
    cprint(f'RAM Regained For Node {node}', 'green')
    print("")


def random_runner(dag_main: DAG, dist_funcs, warming_approach=None, iters=100, store_file_path=None):

    total_durations = []
    total_rams = []
    total_cs_counts = []
    total_cs_durations = []

    dag = copy.copy(dag_main)

    for iter in range(iters):
        jobs = Queue()
        time_handler_thread = Thread(target=time_handler, args=(
            jobs, total_durations, total_rams, total_cs_counts, total_cs_durations))
        time_handler_thread.start()

        cs_times = dist_funcs['cold_start'].copy()
        ex_times = dist_funcs['ex_time'].copy()
        ram_usage = dist_funcs['ram'].copy()

        if warming_approach != None:
            cs_candidates_thread = Thread(target=warming_approach, args=(
                dag, jobs, ex_times, cs_times, ram_usage))
            cs_candidates_thread.start()
            cs_candidates_thread.join()

        i = 0

        # warming the first function of the DAG
        cs = generate_random_sample(cs_times[i])
        ex = generate_random_sample(ex_times[i])
        ram = generate_random_sample(ram_usage[i])

        # Execution
        allocate_function(i, ex, cs, ram, jobs)

        # Running other nodes
        while True:
            # Getting the list of edges for the current node
            edges = list(dag.dag_wfh.G.out_edges(i, data=True))
            if len(edges) == 0:
                break
            # getting the weight for each edge
            edge_weights = [edge[2]['weight'] for edge in edges]

            # Randomly choose an edge based on the weights
            chosen_index = random.choices(
                range(len(edge_weights)), weights=edge_weights, k=1)[0]

            # Get the chose child
            chosen = edges[chosen_index]
            _, child, _ = chosen

            # Run the child
            cs = generate_random_sample(cs_times[child])
            ex = generate_random_sample(ex_times[child])
            ram = generate_random_sample(ram_usage[child])

            allocate_function(child, ex, cs, ram, jobs)

            # Set the child to be the parent for the next iteration
            i = child

        # End the flow by putting a finish message in the queue
        jobs.put(Job(topic='Finish', value=None))

        # wait for the time_handler to process all of the jobs
        time_handler_thread.join()

    # Print the mean value for the data
    print('Mean of Durations: ', mean(total_durations))
    print('Mean of CS Durations', mean(total_cs_durations))
    print("Mean of CS Counts", mean(total_cs_counts))
    print("Mean of RAM Usages", mean(total_rams))

    if store_file_path != None:
        store_in_file(store_file_path, (total_durations, total_rams,
                      total_cs_durations, total_cs_counts))


def path_runner(dag_main: DAG, dist_funcs, path: list, warming_approach=None, iters=100, store_file_path=None):

    total_durations = []
    total_rams = []
    total_cs_counts = []
    total_cs_durations = []

    dag = copy.copy(dag_main)

    for iter in range(iters):
        path_c = copy.copy(path)
        jobs = Queue()
        time_handler_thread = Thread(target=time_handler, args=(
            jobs, total_durations, total_rams, total_cs_counts, total_cs_durations))
        time_handler_thread.start()

        cs_times = dist_funcs['cold_start'].copy()
        ex_times = dist_funcs['ex_time'].copy()
        ram_usage = dist_funcs['ram'].copy()

        if warming_approach != None:
            cs_candidates_thread = Thread(target=warming_approach, args=(
                dag, jobs, ex_times, cs_times, ram_usage))
            cs_candidates_thread.start()
            cs_candidates_thread.join()

        i = 0

        # warming the first function of the DAG
        cs = generate_random_sample(cs_times[i])
        ex = generate_random_sample(ex_times[i])
        ram = generate_random_sample(ram_usage[i])
        # cs = mean(cs_times[i])
        # ex = mean(ex_times[i])
        # ram = mean(ram_usage[i])

        # Execution
        allocate_function(i, ex, cs, ram, jobs)

        # Running other nodes
        while True:
            # Getting the list of edges for the current node
            edges = list(dag.dag_wfh.G.out_edges(i, data=True))
            if len(edges) == 0:
                break

            # Randomly choose an edge based on the weights
            chosen_index = path_c.pop(0)

            # Get the chose child
            chosen = edges[chosen_index]
            _, child, _ = chosen

            # Run the child
            cs = generate_random_sample(cs_times[child])
            ex = generate_random_sample(ex_times[child])
            ram = generate_random_sample(ram_usage[child])
            # cs = mean(cs_times[child])
            # ex = mean(ex_times[child])
            # ram = mean(ram_usage[child])

            allocate_function(child, ex, cs, ram, jobs)

            # Set the child to be the parent for the next iteration
            i = child

        # End the flow by putting a finish message in the queue
        jobs.put(Job(topic='Finish', value=None))

        # wait for the time_handler to process all of the jobs
        time_handler_thread.join()

    # Print the mean value for the data
    print('Mean of Durations: ', mean(total_durations))
    print('Mean of CS Durations', mean(total_cs_durations))
    print("Mean of CS Counts", mean(total_cs_counts))
    print("Mean of RAM Usages", mean(total_rams))

    if store_file_path != None:
        store_in_file(store_file_path, (total_durations, total_rams,
                      total_cs_durations, total_cs_counts))


# This is a wrapper for that specifies paths in the flow runners
def path_runner_wrapper(path):
    def runner(dag_main: DAG, dist_funcs, warming_approach=None, iters=100, store_file_path=None):
        path_runner(dag_main=dag_main, dist_funcs=dist_funcs,
                    warming_approach=warming_approach, iters=iters, path=path, store_file_path=store_file_path)

    return runner

# W1 Path: [2, 0, 1, 2, 0]
# W2 Path [0, 1, 0, 1, 4]
