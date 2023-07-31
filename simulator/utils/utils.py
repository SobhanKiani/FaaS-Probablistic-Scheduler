import requests
import time
import numpy as np
from scipy.stats import norm
from termcolor import cprint
from statistics import mean, stdev

adj_matrix = [
    [-1, 100, -1, -1, -1, -1, -1, -1],
    [-1, -1, 40, 60, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, 32, 8],
    [-1, -1, -1, -1, 18, 42, -1, -1],
    [-1, -1, -1, -1, -1, -1, 6, 12],
    [-1, -1, -1, -1, -1, -1, 7, 35],
    [-1, -1, -1, -1, -1, -1, -1, 45],
    [-1, -1, -1, -1, -1, -1, -1, -1]
]
image_vector = ['f1:latest', 'f1:latest', 'f1:latest',
                'f1:latest', 'f1:latest', 'f1:latest', 'f1:latest', 'f1:latest',]

small_adj_matrix = [
    [-1, 100, -1, -1],
    [-1, -1, 100, -1],
    [-1, -1, -1, 100],
    [-1, -1, -1, -1],
]
small_image_vector = ['f1:latest', 'f1:latest', 'f1:latest',
                      'f1:latest',]
flask_image_vector = ['flask_test:latest', 'flask_test:latest',
                      'flask_test:latest', 'flask_test:latest']
mono_flask_image_vector = ['flask_test:mono', 'flask_test:mono',
                           'flask_test:mono', 'flask_test:mono']


def send_get_request(url):
    max_retries = 50
    retry_count = 0
    while retry_count < max_retries:
        print(f"Trying To Request The App: ", retry_count)
        try:
            res = requests.get(url)
            if res.status_code == 200:
                return res
        except requests.exceptions.ConnectionError:
            pass
        except requests.exceptions.InvalidSchema:
            pass

        time.sleep(1)
        retry_count += 1
    raise Exception(f"Failed to connect to {url}")


def generate_random_sample(data):
    if set(data) == {0}:
        return 0.0
    
    # cprint( data, 'cyan')
    # Calculate mean and standard deviation of past start times
    # mean = np.mean(data)
    # std_dev = np.std(data)

    mean_data = mean(data)
    std_dev_data = stdev(data)
    # print("G", mean_data, std_dev_data)
    
    generated_num = np.random.normal(mean_data, std_dev_data)

    # Create normal distribution object with calculated mean and standard deviation
    # norm_dist = norm(loc=mean_data, scale=std_dev_data)

    # # # Generate a new random start time for a container
    # generated_num = norm_dist.rvs()
    
    
    return generated_num


# equal_adj_matrix = [
#     [-1, 100, -1, -1, -1, -1, -1, -1],
#     [-1, -1, 49, 51, -1, -1, -1, -1],
#     [-1, -1, -1, -1, -1, -1, 25, 24],
#     [-1, -1, -1, -1, 25, 26, -1, -1],
#     [-1, -1, -1, -1, -1, -1, 12, 13],
#     [-1, -1, -1, -1, -1, -1, 12, 14],
#     [-1, -1, -1, -1, -1, -1, -1, 49],
#     [-1, -1, -1, -1, -1, -1, -1, -1]
# ]
equal_adj_matrix = [
    [-1, 100, -1, -1, -1, -1, -1, -1],
    [-1, -1, 49, 51, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, 24, 25],
    [-1, -1, -1, -1, 25, 26, -1, -1],
    [-1, -1, -1, -1, -1, -1, 12, 13],
    [-1, -1, -1, -1, -1, -1, 12, 14],
    [-1, -1, -1, -1, -1, -1, -1, 48],
    [-1, -1, -1, -1, -1, -1, -1, -1]
]
equal_image_vector = ['f1:latest', 'f1:latest', 'f1:latest',
                      'f1:latest', 'f1:latest', 'f1:latest', 'f1:latest', 'f1:latest',]



