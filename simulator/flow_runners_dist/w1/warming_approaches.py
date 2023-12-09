from dag.dag import DAG
from termcolor import cprint
from queue import Queue
from statistics import mean
from .utils import Job, JobTopics, custom_print, show_print


def mlp(dag: DAG, jobs: Queue, ex_times, cs_times, ram_usages):
    warming_sim_time = 0

    cs_candidates = dag.get_xanadu_cold_start_candidates(parent_idx=0, l=-1)
    if len(cs_candidates) == 0:
        return []

    cs_indexes = [u[0] for u in cs_candidates]

    custom_print("", show=show_print)
    custom_print(
        f'MLP-Cold Start Candidates: {cs_indexes} ', 'red', show=show_print)
    custom_print("", show=show_print)

    # Without Planning
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
        curr_level = 0

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
                # node_idx, edge_info, transition_prob
                c_idx, _, _ = children[0]
                # cs_times[c_idx] = [0]
                ram = mean(ram_usages[c_idx])
                # warming_sim_time +=  ex - 3.5
                warming_sim_time += cs + ex - 3.5
                jobs.put(Job(topic=JobTopics.RAM_START, value={
                        #  'node': c_idx, 'amount': ram, 'alloc_time': warming_sim_time, 'level': curr_level+1}))
                         'node': c_idx, 'amount': ram, 'alloc_time': 0, 'level': curr_level+1}))

                curr_node_i = c_idx
                curr_level += 1
            else:
                break


def optimal(dag: DAG, jobs: Queue, ex_times, cs_times, ram_usages, alpha=100, beta=0, l=-1):
    warming_queue = Queue()

    cs_candidates = dag.get_cold_start_candidates(
        parent_idx=0, l=l, alpha=alpha, beta=beta)

    cs_indexes = [u[0] for u in cs_candidates]

    custom_print("", show=show_print)
    custom_print(
        f"OPTIMAL CS Candidates: {cs_indexes}", 'red', show=show_print)
    custom_print("", show=show_print)

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

    # (node, cs+ex of the parent, level)
    warming_queue.put((cs_dict[0], 0, 0))

    while not warming_queue.empty():
        node, parent_time, level = warming_queue.get()
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
                # cs_times[c_idx] = [0]
                ram = mean(ram_usages[c_idx])
                jobs.put(Job(topic=JobTopics.RAM_START, value={
                    # 'node': c_idx, 'amount': ram, 'alloc_time': parent_wst - 3.5, 'level': level + 1
                    'node': c_idx, 'amount': ram, 'alloc_time': 0, 'level': level + 1
                }))

                # adding to queue to get checked next
                warming_queue.put((child, parent_wst, level+1))


# These are the wrapper functions
# That let us to give parameters to algorithm
# Without changing the runner
def optimal_approach(dag, jobs, ex_times, cs_times, ram_usages):
    optimal(dag, jobs, ex_times, cs_times,
            ram_usages, alpha=50, beta=20, l=-1)


def warming_all_approach(dag, jobs, ex_times, cs_times, ram_usages):
    optimal(dag, jobs, ex_times, cs_times,
            ram_usages, alpha=100, beta=0, l=-1)
