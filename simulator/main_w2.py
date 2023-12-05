import sys
from termcolor import cprint

parent_module = sys.modules['.'.join(__name__.split('.')[:-1]) or '__main__']
if __name__ == '__main__' or parent_module.__name__ == '__main__':
    # from flow.flow import Flow
    from flow.flow_dist_func import FlowDistFunc
    # from flow_runners_dist.w1.deterministic import most_probable_fr, optimal, cold_start_fr
    # from flow_runners_dist.w1.undeterministic import most_probable_fr, optimal, cold_start_fr
    # from flow_runners_dist.w1.undeterministic_pathless import most_probable_fr, optimal, cold_start_fr
    from flow_runners_dist.w1.test_runner import random_runner, path_runner_wrapper
    from flow_runners_dist.w1.warming_approaches import mlp, optimal_approach, warming_all_approach
    from utils.random_matrices import random_DAG_2 as random_DAG, random_dag_2_images as dag_images, w2_dist_funcs as w_dist_funcs


if __name__ == '__main__':
    # f = Flow(equal_adj_matrix, equal_imageff_vector)
    f = FlowDistFunc(random_DAG, dag_images, w_dist_funcs)

    # Random Test
    # ---------------------------------------------------------------------
    # print("RANDOM TEST STARTED")

    # iters = 500
    # print("--------------------------------------------------------------------")
    # cprint("COLD START TEST", 'white', 'on_magenta')
    # f_cold_start = FlowDistFunc(random_DAG, dag_images, w_dist_funcs)
    # f_cold_start.set_flow_runner(random_runner, warming_approach=None)
    # f_cold_start.start_flow_runner(
    #     iters=iters, store_file_path='./new-results/w2/random/cold-start.txt')
    # cprint(
    #     f"COLD START TEST FINISHED FOR {iters} ITERS", 'white', 'on_magenta')
    # print("----------------")

    # cprint("MLP TEST", 'white', 'on_magenta')
    # f_mlp = FlowDistFunc(random_DAG, dag_images, w_dist_funcs)
    # f_mlp.set_flow_runner(random_runner, warming_approach=mlp)
    # f_mlp.start_flow_runner(
    #     iters=iters, store_file_path='./new-results/w2/random/mlp.txt')
    # cprint(f"MLP TEST FINISHED FOR {iters} ITERS", 'white', 'on_magenta')
    # print("----------------")

    # cprint("WARMING ALL TEST", 'white', 'on_magenta')
    # f_all = FlowDistFunc(random_DAG, dag_images, w_dist_funcs)
    # f_all.set_flow_runner(random_runner, warming_approach=warming_all_approach)
    # f_all.start_flow_runner(
    #     iters=iters, store_file_path='./new-results/w2/random/warming-all.txt')
    # cprint(
    #     f"WARMING ALL TEST FINISHED FOR {iters} ITERS", 'white', 'on_magenta')
    # print("----------------")

    # cprint("OPTIMAL TEST", 'white', 'on_magenta')
    # f_optimal = FlowDistFunc(random_DAG, dag_images, w_dist_funcs)
    # f_optimal.set_flow_runner(random_runner, warming_approach=optimal_approach)
    # f_optimal.start_flow_runner(
    #     iters=iters, store_file_path='./new-results/w2/random/optimal.txt')
    # cprint(f"OPTIMAL TEST FINISHED FOR {iters} ITERS", 'white', 'on_magenta')
    # print("----------------")
    # # ---------------------------------------------------------------------

    ####### Path Test ##########
    ############################
    ############################
    ############################
    # ---------------------------------------------------------------------
    print("PATH TEST STARTED")
    iters = 500
    path = [0, 1, 0, 1, 4]

    print("PATH TEST")
    print("--------------------------------------------------------------------")
    cprint("COLD START TEST", 'white', 'on_magenta')
    f_cold_start = FlowDistFunc(random_DAG, dag_images, w_dist_funcs)
    f_cold_start.set_flow_runner(
        path_runner_wrapper(path=path), warming_approach=None)
    f_cold_start.start_flow_runner(
        iters=iters, store_file_path='./new-results/w2/path/cold-start.txt')
    cprint(
        f"COLD START TEST FINISHED FOR {iters} ITERS", 'white', 'on_magenta')
    # print("----------------")
    print("")

    cprint("MLP TEST", 'white', 'on_magenta')
    f_mlp = FlowDistFunc(random_DAG, dag_images, w_dist_funcs)
    f_mlp.set_flow_runner(path_runner_wrapper(path=path), warming_approach=mlp)
    f_mlp.start_flow_runner(
        iters=iters, store_file_path='./new-results/w2/path/mlp.txt')
    cprint(f"MLP TEST FINISHED FOR {iters} ITERS", 'white', 'on_magenta')
    print("----------------")
    print("")

    cprint("WARMING ALL TEST", 'white', 'on_magenta')
    f_all = FlowDistFunc(random_DAG, dag_images, w_dist_funcs)
    f_all.set_flow_runner(path_runner_wrapper(path=path),
                          warming_approach=warming_all_approach)
    f_all.start_flow_runner(
        iters=iters, store_file_path='./new-results/w2/path/warming-all.txt')
    cprint(
        f"WARMING ALL TEST FINISHED FOR {iters} ITERS", 'white', 'on_magenta')
    print("----------------")
    print("")

    cprint("OPTIMAL TEST", 'white', 'on_magenta')
    f_optimal = FlowDistFunc(random_DAG, dag_images, w_dist_funcs)
    f_optimal.set_flow_runner(
        path_runner_wrapper(path=path), warming_approach=optimal_approach)
    f_optimal.start_flow_runner(
        iters=iters, store_file_path='./new-results/w2/path/optimal.txt')
    cprint(f"OPTIMAL TEST FINISHED FOR {iters} ITERS", 'white', 'on_magenta')
    print("----------------")
    # ---------------------------------------------------------------------
