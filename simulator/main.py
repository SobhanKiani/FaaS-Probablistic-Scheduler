

import sys

parent_module = sys.modules['.'.join(__name__.split('.')[:-1]) or '__main__']
if __name__ == '__main__' or parent_module.__name__ == '__main__':
    from utils.utils import equal_adj_matrix, equal_image_vector
    # from flow.flow import Flow
    from flow.flow_dist_func import FlowDistFunc

    # from flow_runners_dist.w1.deterministic import most_probable_fr, optimal, cold_start_fr
    from flow_runners_dist.w1.undeterministic import most_probable_fr, optimal, cold_start_fr
    # from flow_runners_dist.w1.undeterministic_pathless import most_probable_fr, optimal, cold_start_fr
    from utils.random_matrices import random_DAG, random_dag_images, w1_dist_funcs
else:
    from .utils.utils import equal_adj_matrix, equal_image_vector
    # from .flow.flow import Flow
    from .flow.flow_dist_func import FlowDistFunc

    # from .flow_runners_dist.w1.deterministic import most_probable_fr, optimal, cold_start_fr
    from .flow_runners_dist.w1.undeterministic import most_probable_fr, optimal, cold_start_fr
    # from .flow_runners_dist.w1.undeterministic_pathless import most_probable_fr, optimal, cold_start_fr
    from .utils.random_matrices import random_DAG, random_dag_images, w1_dist_funcs


if __name__ == '__main__':
    # f = Flow(equal_adj_matrix, equal_imageff_vector)
    f = FlowDistFunc(random_DAG, random_dag_images, w1_dist_funcs)

    # f.analyze_dag(iter=500, wf_folder_name='w1')
    # print(f.dag_analysis.get_run_time_mean())

    # f.plot_init_histogram(random_dag_images[0],0)
    # f.plot_runtime_histogram(random_dag_images[0], 0)
    # f.plot_ram_usage_histogram(random_dag_images[2], 2)

    # print("COLD START TEST")
    # f.set_flow_runner(cold_start_fr)
    # f.start_flow_runner(iters=1500)
    # print("-------------------")

    # print("MOST PROBABLE TEST")
    # f.set_flow_runner(most_probable_fr)
    # f.start_flow_runner(iters=1500)
    # print("-------------------")

    print("OPTIMAL TEST")
    f.set_flow_runner(optimal)
    f.start_flow_runner(iters=1500)
    print("-------------------")
