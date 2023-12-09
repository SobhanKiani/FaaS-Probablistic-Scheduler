import random
from dag.dag import DAG
import os
from queue import Queue
from typing import Optional, List, Tuple
from enum import Enum
from termcolor import cprint, COLORS, HIGHLIGHTS

show_print = True
curr_show_print = True


def custom_print(text: str, color: COLORS = 'white', on_color: HIGHLIGHTS = '', show: bool = True):
    if show:
        if on_color != '':
            cprint(text, color, on_color)
        else:
            cprint(text, color)


class JobTopics(Enum):
    RAM_START = 'RAM_START'
    RAM_RESTART = 'RAM_RESTART'
    EXECUTION = 'EXECUTION'
    FINISH = "FINISH"


class Job:
    def __init__(self, topic: str, value) -> None:
        self.topic = topic
        self.value = value


def store_in_file(file_path, data):
    duration, ram, cs_duration, cs_count, cost = data
    zipped_data = zip(duration, ram, cs_duration, cs_count, cost)

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, 'w') as f:
        for d, r, cs_d, cs_c, c in zipped_data:
            f.write(f"{d},{r},{cs_d},{cs_c},{c}\n")


class WorkflowData:
    def __init__(self) -> None:
        self.ram_value: List[RamData] = []
        self.ram_usage = 0.0  # Total Megabytes of RAM
        self.compute_cost = 0.0  # GB-S To Calculate The Cost
        self.cs_time = 0.0
        self.cs_count = 0.0
        self.sim_time = 0.0
        self.cost = 0.0

    def find_ram_value(self, node: int):
        found = [ram_data for ram_data in self.ram_value if ram_data.node == node]
        if found.__len__() == 0:
            return None
        elif found.__len__() > 1:
            raise "Two Allocations For One Function"
        else:
            return found[0]

    def find_ram_data_similar_level(self, node, level):
        found = [ram_data for ram_data in self.ram_value if (
            level == ram_data.level and node != ram_data.node)]
        # print("Finding Similar Levels", node, level, [{'node':rd.node, 'level':rd.level} for rd in self.ram_value])
        # print("Found Similar Levels", found)
        return found


class RamData:
    def __init__(self, node: int, amount: float, alloc_time: float, level: int) -> WorkflowData:
        self.node = node
        self.alloc_time = alloc_time
        self.amount = amount
        self.level = level
        self.compute_cost = None
        self.end_time = None
        self.up_duration = None
        self.cost = None

    def calculate_price(self, ):
        # Compute cost = Duration (Up Time) * Ram Amount
        compute_cost_in_MB = self.compute_cost
        compute_cost_in_GB = compute_cost_in_MB * 1/1000
        # return compute_cost_in_GB * 0.0000133334
        return compute_cost_in_GB * 1


def ex_handler(w: WorkflowData, ex: float) -> WorkflowData:
    w.sim_time += ex
    return w


def cs_handler(w: WorkflowData, cs: float) -> WorkflowData:
    w.sim_time += cs
    if cs > 0:
        w.cs_count += 1
    return w


def ram_end_handler():
    pass


def ram_start_handler(w: WorkflowData, node: int, amount: float, level: int, alloc_time: Optional[float] = None):
    if not w:
        w = WorkflowData()

    if alloc_time == None:
        alloc_time = w.sim_time

    found = w.find_ram_value(node)

    if found == None:
        ram_data = RamData(node, amount, alloc_time, level)
        w.ram_value.append(ram_data)
        custom_print(text=f"Ram Allocation For Node {node}, Amount {amount}, Alloc Time {alloc_time}, Level {level}",
                     color='cyan', show=show_print)

    return w


def ram_restart_handler(w: WorkflowData, node: int, amount: float, alloc_time: Optional[float], level: int) -> Tuple[List[RamData], RamData]:
    ram_values_list = [rm for rm in w.ram_value if rm.node != node]

    if alloc_time == None:
        alloc_time = w.sim_time

    new_ram_data = RamData(
        node=node, alloc_time=alloc_time, amount=amount, level=level)
    ram_values_list.append(new_ram_data)

    return ram_values_list, new_ram_data


def execution_handler(w: WorkflowData, node: int, cs: float, ex: float):
    if not w:
        w = WorkflowData()

    last_sim_time = w.sim_time
    # w.sim_time += cs + ex
    # if cs > 0:
    #     w.cs_time += cs
    #     w.cs_count += 1

    ram_data: RamData = w.find_ram_value(node)
    last_alloc_time = ram_data.alloc_time

    print("CS Before Changing:", cs)
    if ram_data != None:
        if ram_data.alloc_time - last_sim_time > 0:
            print("h1")
            w.ram_value, ram_data = ram_restart_handler(
                w, node=node, amount=ram_data.amount, alloc_time=None, level=ram_data.level)
        elif ram_data.alloc_time - last_sim_time == 0:
            # do nothing if they were equal
            print('h4')
            pass
        else:
            if last_sim_time - ram_data.alloc_time > cs:
                print("h2")
                cs = 0
            else:
                print("h3")
                cs = last_sim_time - ram_data.alloc_time

        custom_print(
            f'Ram Data For Node: {node} , Amount: {ram_data.amount}, Alloc Time: {ram_data.alloc_time}, Last Alloc Time {last_alloc_time},  Level {ram_data.level}', show=show_print)

        w.sim_time += cs + ex
        if cs > 0:
            w.cs_time += cs
            w.cs_count += 1

        up_duration = w.sim_time - ram_data.alloc_time
        ram_data.up_duration = up_duration

        last_computation_cost = w.compute_cost
        compute_cost = up_duration * ram_data.amount
        ram_data.compute_cost = compute_cost
        w.compute_cost += compute_cost

        ram_data.cost = ram_data.calculate_price()
        w.cost += ram_data.cost

        last_ram_usage = w.ram_usage
        w.ram_usage += ram_data.amount

        sim_level_ram_data = w.find_ram_data_similar_level(
            node, ram_data.level)

        simi_level_nodes = [{'node': rd.node, 'level': rd.level}
                            for rd in sim_level_ram_data]
        custom_print(
            f"Level {ram_data.level}: Similart Level Ram Data {simi_level_nodes}", show=show_print)

        for sibling in sim_level_ram_data:
            if last_sim_time - sibling.alloc_time > 0:
                sibling_up_duration = last_sim_time - sibling.alloc_time
            else:
                sibling_up_duration = 0

            sibling_up_duration = (w.sim_time - sibling.alloc_time)
            sibling.up_duration = sibling_up_duration

            sibling_compute_cost = sibling_up_duration * ram_data.amount
            sibling.compute_cost = sibling_compute_cost
            w.compute_cost += sibling_compute_cost

            sibling.cost = sibling.calculate_price()
            w.cost += sibling.cost

            w.ram_usage += sibling.amount

        custom_print(
            f"Node {node}: SIM TIME BEFORE ENDING {last_sim_time}, Last Ram Usage {last_ram_usage}, Last Compute Cost {last_computation_cost}", color='green', show=curr_show_print)
        custom_print(
            f"Exection For Node {node}, CS {cs}, EX {ex}, Total Duration {cs + ex}, ", 'white', 'on_cyan', show_print)
        custom_print(
            f"RAM For Node {node}, Leve {ram_data.level} , Amount {ram_data.amount}, Alloc Time {ram_data.alloc_time}, END TIME {w.sim_time}, Up Duration {up_duration}, Computation Cost {ram_data.compute_cost}", 'white', 'on_cyan', show_print)
        custom_print(
            f"Node {node}: SIM TIME AFTER ENDING {w.sim_time}, New Ram Usage {w.ram_usage}, New Compute Cost {w.compute_cost}", color='green', show=curr_show_print)
        custom_print("", show=show_print)
        return w
    else:
        raise "No Ram Data Found For The Function"


def finish_handler():
    custom_print("FLOW FINIHSED", 'white', 'on_green', show_print)
    custom_print("", show=show_print)


def time_handler(jobs: Queue, total_durations: list, total_rams: list, total_cs_counts: list, total_cs_duration: list, total_compute_costs: list, total_cost: list):
    custom_print(f"Entered The Job Queue", color='white',
                 on_color='on_yellow', show=show_print)
    workflow_data = WorkflowData()

    while True:
        item: Job = jobs.get()

        if item.topic == JobTopics.FINISH:
            finish_handler()
            break

        elif item.topic == JobTopics.RAM_START:
            workflow_data = ram_start_handler(
                w=workflow_data, node=item.value['node'], amount=item.value['amount'], level=item.value['level'], alloc_time=item.value['alloc_time'])

        elif item.topic == JobTopics.EXECUTION:
            workflow_data = execution_handler(
                w=workflow_data, node=item.value['node'], cs=item.value['cs'], ex=item.value['ex'])

    custom_print(f"Exited The Job Queue", color='white',
                 on_color='on_yellow', show=show_print)

    ram_data = [{'node': ram_data.node, 'level': ram_data.level, 'amount': ram_data.amount}
                for ram_data in workflow_data.ram_value]

    custom_print(f"List Of Ram Data: {ram_data}",
                 color='red',  show=curr_show_print)
    custom_print("", color='red',  show=curr_show_print)

    custom_print("-------------------", show=show_print)
    custom_print("", show=show_print)

    total_durations.append(workflow_data.sim_time)
    total_cs_duration.append(workflow_data.cs_time)
    total_cs_counts.append(workflow_data.cs_count)
    total_rams.append(workflow_data.ram_usage)
    total_compute_costs.append(workflow_data.compute_cost)
    total_cost.append(workflow_data.cost)


def path_generator(dag_main: DAG):
    path = []
    dag = dag_main
    i = 0

    # Running other nodes
    while True:
        # Getting the list of edges for the current node
        edges = list(dag.dag_wfh.G.out_edges(i, data=True))
        if len(edges) == 0:
            break

        edge_weights = [edge[2]['weight'] for edge in edges]

        # Randomly choose an edge based on the weights
        chosen_index = random.choices(
            range(len(edge_weights)), weights=edge_weights, k=1)[0]
        path.append(chosen_index)
        # Get the chose child
        chosen = edges[chosen_index]
        _, child, _ = chosen

        # Set the child to be the parent for the next iteration
        i = child
