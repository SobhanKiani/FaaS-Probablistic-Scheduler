from dag.dag import DAG
from termcolor import cprint
from queue import Queue
from statistics import mean
from .utils import Job


def mlp(dag: DAG, jobs: Queue, ex_times, cs_times, ram_usages):
    warming_sim_time = 0

    cs_candidates = dag.get_xanadu_cold_start_candidates(parent_idx=0, l=-1)
    if len(cs_candidates) == 0:
        return []

    cs_indexes = [u[0] for u in cs_candidates]

    print("")
    cprint(f'MLP-Cold Start Candidates: {cs_indexes} ', 'red')
    print("")

    # Without Planning
    # for node_idx, info, prob in cs_candidates:
    #     if node_idx != 0:
    #         ram = mean(ram_usages[node_idx])
    #         cs_times[node_idx] = [0]
    #         jobs.put(Job(topic='RAM_START_BY_TIME', value={
    #             'node': node_idx, 'amount': ram, 'time': 0}))

    cs_dict = {0: (0, (), {'weight': 1000})}
    cs_dict = {}
    for node in cs_candidates:
        cs_dict[node[0]] = node

    # levels = {0: [cs_candidates[0]]}
    levels = {}
    for node in cs_candidates:
        node_idx, info, prob = node

        if node_idx == 0:
            levels[0] = []
        else:
            p, c, _ = info
            # if parent is in levels
            if p in levels:
                # add node to children of the parent
                levels[p].append(node)
            else:
                # create a list for the parent
                levels[p] = [node]
            # create a list for the child
            if c not in levels:
                levels[c] = []

        curr_node_i = 0
        while True:
            node_idx, info, prob = cs_dict[curr_node_i]

            ex = mean(ex_times[node_idx])
            cs = mean(cs_times[node_idx])

            # other way to get the cs time
            # if node_idx == 0:
            #     cs = mean(cs_times[node_idx])
            # else:
            #     cs = 0

            children = levels[node_idx]

            if children.__len__() > 0:
                c_idx, c_info, c_prob = children[0]
                cs_times[c_idx] = [0]
                ram = mean(ram_usages[c_idx])
                warming_sim_time += cs + ex
                jobs.put(Job(topic='RAM_START_BY_TIME', value={
                         'node': c_idx, 'amount': ram, 'time': warming_sim_time}))

                curr_node_i = c_idx
            else:
                break


def optimal(dag: DAG, jobs: Queue, ex_times, cs_times, ram_usages, alpha=100, beta=0, l=-1):
    warming_queue = Queue()
    warming_sim_time = 0

    cs_candidates = dag.get_cold_start_candidates(
        parent_idx=0, l=l, alpha=alpha, beta=beta)

    cs_indexes = [u[0] for u in cs_candidates]

    print("")
    cprint(f"OPTIMAL CS Candidates: {cs_indexes}", 'red')
    print("")

    if len(cs_candidates) == 0:
        return []

    # without planning
    # for node_idx, info, prob in cs_candidates:
    #     if node_idx != 0:
    #         ram = mean(ram_usages[node_idx])
    #         cs_times[node_idx] = [0]
    #         jobs.put(Job(topic='RAM_START', value={
    #             'node': node_idx, 'amount': ram, 'time': 0}))

    cs_dict = {0: (0, (), {'weight': 1000})}
    cs_dict = {}
    for node in cs_candidates:
        cs_dict[node[0]] = node

    # levels = {0: [cs_candidates[0]]}
    levels = {}
    for node in cs_candidates:
        node_idx, info, prob = node

        if node_idx == 0:
            levels[0] = []
        else:
            p, c, info = info

            if p in levels:
                levels[p].append(node)
            else:
                levels[p] = [node]
            if c not in levels:
                levels[c] = []

    # (node, cs+ex of the parent)
    warming_queue.put((cs_dict[0], 0))

    while not warming_queue.empty():
        node, parent_time = warming_queue.get()
        node_idx, info, prob = node
        # print('Parent Node For Warming', node_idx)

        # These are for the parent
        ex = mean(ex_times[node_idx])
        cs = mean(cs_times[node_idx])

        # This shows in what time the children should get warmed
        parent_wst = parent_time
        parent_wst += cs + ex

        children = levels[node_idx]
        if children.__len__() > 0:
            for child in children:
                c_idx, c_info, c_prob = child
                cs_times[c_idx] = [0]
                ram = mean(ram_usages[c_idx])
                jobs.put(Job(topic='RAM_START_BY_TIME', value={
                    'node': c_idx, 'amount': ram, 'time': parent_wst
                }))

                # adding to queue to get checked next
                warming_queue.put((child, parent_wst))


# These are the wrapper functions
# That let us to give parameters to algorithm
# Without changing the runner
def optimal_approach(dag, jobs, ex_times, cs_times, ram_usages):
    optimal(dag, jobs, ex_times, cs_times,
            ram_usages, alpha=50, beta=20, l=-1)


def warming_all_approach(dag, jobs, ex_times, cs_times, ram_usages):
    optimal(dag, jobs, ex_times, cs_times,
            ram_usages, alpha=100, beta=0, l=-1)
