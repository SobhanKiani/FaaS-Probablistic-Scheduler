

import sys

parent_module = sys.modules['.'.join(__name__.split('.')[:-1]) or '__main__']
if __name__ == '__main__' or parent_module.__name__ == '__main__':
    from utils.utils import equal_adj_matrix, equal_image_vector
    from flow.flow import Flow
    # from flow_runners.fr_full_test import cold_start_fr, most_probable_fr, optimal
    # from flow_runners.w1.deterministic import most_probable_fr, optimal, cold_start_fr
    # from flow_runners.w1.undeterministic import most_probable_fr, optimal, cold_start_fr
    from flow_runners.w1.undeterministic_pathless import most_probable_fr, optimal, cold_start_fr
    from utils.random_matrices import random_DAG, random_dag_images
else:
    from .utils.utils import equal_adj_matrix, equal_image_vector
    from .flow.flow import Flow
    # from .flow_runners.fr_full_test import cold_start_fr, most_probable_fr, optimal
    # from .flow_runners.w1.deterministic import most_probable_fr, optimal, cold_start_fr
    # from .flow_runners.w1.undeterministic import most_probable_fr, optimal, cold_start_fr
    from .flow_runners.w1.undeterministic_pathless import most_probable_fr, optimal, cold_start_fr
    from .utils.random_matrices import random_DAG, random_dag_images


if __name__ == '__main__':
    # f = Flow(equal_adj_matrix, equal_imageff_vector)
    f = Flow(random_DAG, random_dag_images)

    # f.analyze_dag(iter=500, wf_folder_name='w1')
    # print(f.dag_analysis.get_run_time_mean())
    
    # f.plot_init_histogram(random_dag_images[0],0)
    # f.plot_runtime_histogram(random_dag_images[0], 0)
    # f.plot_ram_usage_histogram(random_dag_images[2], 2)

    print("COLD START TEST")
    f.set_flow_runner(cold_start_fr)
    f.start_flow_runner(iters=10)
    print("-------------------")

    print("MOST PROBABLE TEST")
    f.set_flow_runner(most_probable_fr)
    f.start_flow_runner(iters=10)
    print("-------------------")

    print("OPTIMAL TEST")
    f.set_flow_runner(optimal)
    f.start_flow_runner(iters=10)
    print("-------------------")
