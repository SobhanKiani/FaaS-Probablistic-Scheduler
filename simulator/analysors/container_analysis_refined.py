import time
import docker
import redis
import statistics
from utils.utils import send_get_request
from utils.container_utils import wait_for_container, wait_for_container_mem
import numpy as np
import matplotlib.pyplot as plt


class ContainerAnalysis:
    def __init__(self, image_name: str, node_idx) -> None:
        self.image_name = image_name
        self.image_base_name = image_name.split(':')[0]
        self. image_version = image_name.split(':')[1]

        self.docker_client = docker.from_env()
        self.node_idx = node_idx
        self.base_key = f'{self.node_idx}:{self.image_name}'

        self.redis_client = redis.Redis(
            # host='localhost', port=32769, username='default', password='redispw')
            host='localhost', port=6380, username='default', password='redispw')

    def login(self, email: str, username: str, password: str):
        self.set_login_config(username, email, password)
        self.docker_client.login(
            email=email, username=username, password=password)

    def set_login_config(self, username: str, email: str, password: str):
        self.username = username
        self.email = email
        self.password = password

    def pull_image(self):
        image = self.docker_client.images.pull(
            f'{self.image_name}')

        self.image = image

    def store(self, key: str, value: str):
        self.redis_client.rpush(key, value)

    def store_list(self, key: str, value: list):
        self.redis_client.rpush(key, *value)

    def get_initialization_time(self):
        start_time = time.time()
        container = self.docker_client.containers.run(
            self.image_name, detach=True)

        while True:
            container.reload()
            if container.status == 'running':
                break
            time.sleep(1)

        end_time = time.time()

        container.stop()
        container.remove()

        starting_duration = end_time - start_time
        return starting_duration


    def get_all_init_times_list(self):
        init_times = self.redis_client.lrange(f"{self.base_key}_{self.node_idx}:init", 0, -1)
        init_times_decoded = [float(it.decode()) for it in init_times]
        
        return init_times_decoded

    def get_running_time(self, volume):
        container = self.docker_client.containers.run(
            self.image_name,
            detach=True,
            volumes=[volume],
        )
        id = container.id
        wait_for_container(container)
        

    def store_running_times(self):
        running_times_key = f'{self.base_key}_{self.node_idx}:duration'

        with open(f"{self.running_time_file_addr}durations.txt", 'r') as f:
            durations = f.read().split('\n')[:-1]
            self.store_list(running_times_key, durations)

    def get_all_running_times_list(self):
        running_times = self.redis_client.lrange(f"{self.base_key}_{self.node_idx}:duration", 0, -1)
        running_times_decoded = [float(d.decode()) for d in running_times]
        return running_times_decoded
    
    def get_all_ram_usage(self):
        ram_usage_list = self.redis_client.lrange(f"{self.base_key}_{self.node_idx}:memory", 0, -1)
        ram_usage_list_decoded = [int(ru.decode()) for ru in ram_usage_list]    
        return ram_usage_list_decoded
    
    def caluclate_information(self, iters, host_add, container_add, sleep_time=3):
        # Deleting times stored in the past
        self.redis_client.delete(f"{self.base_key}_{self.node_idx}:duration")
        self.redis_client.delete(f"{self.base_key}_{self.node_idx}:init")
        self.redis_client.delete(f"{self.base_key}_{self.node_idx}:memory")

        self.running_time_file_addr = host_add

        for i in range(iters):
            print(f"Iteration Number: {i+1}")
            
            start_time = time.time()
            # Creating Container
            # container = self.docker_client.containers.run(
            #     self.image_name, detach=True)
            container = self.docker_client.containers.run(
            self.image_name,
            detach=True,
            volumes=[f'{self.running_time_file_addr}/:{container_add}'],
        )

            # Calculating CS time
            while True:
                container.reload()
                if container.status == 'running':
                    break
                time.sleep(1)

            end_time = time.time()
            
            stats = container.stats(stream=False)
            memory_usage = stats['memory_stats']['usage']


            # Calculating Mem and EX time
            wait_for_container(container)

            cs_time = end_time - start_time 
            self.store(f"{self.base_key}_{self.node_idx}:init", cs_time)
            self.store(f"{self.base_key}_{self.node_idx}:memory", memory_usage)        

        # print("Storing all of the running times from the file")
        # time.sleep(sleep_time)
        # self.store_running_times()
        # print("Finished")
        
        
    # def caluclate_both_times(self, iters, host_add, container_add, sleep_time=3):
    #     # Deleting times stored in the past
    #     self.redis_client.delete(f"{self.base_key}_{self.node_idx}:duration")
    #     self.redis_client.delete(f"{self.base_key}_{self.node_idx}:init")

    #     self.running_time_file_addr = host_add

    #     for i in range(iters):
    #         print(f"Iteration Number: {i+1}")

    #         # Calculating CS time
    #         init_time = self.get_initialization_time()
    #         self.store(f"{self.base_key}_{self.node_idx}:init", init_time)

    #         # Calculating EX Time
    #         self.get_running_time(f'{self.running_time_file_addr}/:{container_add}')

    #     print("Storing all of the running times from the file")
    #     time.sleep(sleep_time)
    #     self.store_running_times()
    #     print("Finished")
    
    # def calculate_mem_usage(self, iters=100):
    #     for i in range(iters):
    #         container = self.docker_client.containers.run(
    #             self.image_name, detach=True)
    #         while True:
    #             container.reload()
    #             if container.status == 'running':
    #                 break
    #             time.sleep(1)
    #         # status, mem_usage= wait_for_container_mem(container)    
            
    #         # time.sleep(3)
    #         status = container.stats(stream=False)
    #         print(status['memory_stats'])
    #         container.stop()
    #         container.remove()
    #         # print("Mem Usage", mem_usage)
    #         # return status, mem_usage

    def get_mean_init_time(self,):
        init_times = self.get_all_init_times_list()
        avg = statistics.mean(init_times)
        return avg

    def get_mean_run_time(self,):
        init_times = self.get_all_running_times_list()
        avg = statistics.mean(init_times)
        return avg
    
    def get_mean_ram_usage(self,):
        ram_usage_list = self.get_all_ram_usage()
        avg = statistics.mean(ram_usage_list)
        return avg
    
    def plot_init_time_hist(self):
        init_times = self.get_all_init_times_list()
        print(max(init_times), len(init_times))
        init_times = np.array(init_times)
        
        plt.hist(init_times, bins=5, density=True, alpha=0.5, color='blue')
        plt.xlabel('CS')
        plt.ylabel('Frequency')
        plt.title('CS Histogram')
        plt.show()

    def plot_runtime_hist(self):
        running_times = self.get_all_running_times_list()
        print(max(running_times), len(running_times))
        running_times = np.array(running_times)

        plt.hist(running_times, bins=5, density=True, alpha=0.5, color='blue')
        plt.xlabel('EX')
        plt.ylabel('Frequency')
        plt.title('EX Histogram')
        plt.show()
        
    def plot_ram_usage_hist(self):
        ru_list = self.get_all_ram_usage()
        # print(max(ru_list), len(ru_list))
        print(ru_list, len(ru_list))
        ru_list = np.array(ru_list)

        plt.hist(ru_list, bins=5, density=True, alpha=0.5, color='blue')
        plt.xlabel('EX')
        plt.ylabel('Frequency')
        plt.title('EX Histogram')
        plt.show()


