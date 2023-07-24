

import sys

parent_module = sys.modules['.'.join(__name__.split('.')[:-1]) or '__main__']
if __name__ == '__main__' or parent_module.__name__ == '__main__':
    from utils.utils import equal_adj_matrix, equal_image_vector
    from flow.flow import Flow
    from flow_runners.fr_full_test import cold_start_fr, most_probable_fr, optimal
else:
    from .utils.utils import equal_adj_matrix, equal_image_vector
    from .flow.flow import Flow
    from .flow_runners.fr_full_test import cold_start_fr, most_probable_fr, optimal


if __name__ == '__main__':
    f = Flow(equal_adj_matrix, equal_image_vector)
    # f.analyze_dag(iter=500)
    # print(f.dag_analysis.get_run_time_mean())

    print("COLD START TEST")
    f.set_flow_runner(cold_start_fr)
    f.start_flow_runner()
    print("-------------------")

    # print("MOST PROBABLE TEST")
    # f.set_flow_runner(most_probable_fr)
    # f.start_flow_runner()
    # print("-------------------")

    # print("OPTIMAL TEST")
    # f.set_flow_runner(optimal)
    # f.start_flow_runner()
    # print("-------------------")
