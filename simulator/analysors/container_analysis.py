import time
import datetime
import docker
import redis
import statistics
from utils.utils import send_get_request
from utils.container_utils import wait_for_container


class ContainerAnalysis:
    def __init__(self, image_name: str, node_idx) -> None:
        self.image_name = image_name
        self.image_base_name = image_name.split(':')[0]
        self. image_version = image_name.split(':')[1]

        self.docker_client = docker.from_env()
        self.node_idx = node_idx
        self.base_key = f'{self.node_idx}:{self.image_name}'

        self.redis_client = redis.Redis(
            host='localhost', port=32768, username='default', password='redispw')

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

    def calculate_initialization_time(self, iter: int):
        print(
            f'Calculating inititalization times for {self.image_name} at index {self.node_idx} in {iter} iterations')
        self.redis_client.delete(f"{self.base_key}:init")
        for i in range(iter):
            print(f"Iteration Number: {i}")
            init_time = self.get_initialization_time()

            # self.store(f"{self.base_key}:init", init_time)
            self.store(f"{self.base_key}_{self.node_idx}:init", init_time)
        print("Initializations stored")
        print("")

    def get_all_init_times_list(self):
        # init_times = self.redis_client.lrange(
        #     f"{self.base_key}_{self.node_idx}:init", 0, -1)
        init_times = self.redis_client.lrange(
            f"{self.base_key}_0:init", 0, -1)
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
        # exited_container = self.docker_client.containers.get(id)
        # container.remove(exited_container)
        

    def calculate_running_time(self, iter, host_add, container_add):
        # self.running_time_file_addr = f"{host_add}{self.image_base_name}_durations"
        self.running_time_file_addr = host_add

        self.redis_client.delete(f"{self.base_key}:duration")

        print("Calculating Running times started For: ",
              f'{self.image_name}_{self.node_idx}')
        for i in range(iter):
            print(f"Iteration Number: {i}")
            self.get_running_time(
                f'{self.running_time_file_addr}/:{container_add}')
        print("Finished")
        print("")

    def store_running_times(self):
        running_times_key = f'{self.base_key}_{self.node_idx}:duration'

        with open(f"{self.running_time_file_addr}durations.txt", 'r') as f:
            durations = f.read().split('\n')[:-1]
            self.store_list(running_times_key, durations)

    def get_all_running_times_list(self):
        # running_times = self.redis_client.lrange(
        #     f"{self.base_key}_{self.node_idx}:duration", 0, -1)
        running_times = self.redis_client.lrange(
            f"{self.base_key}_0:duration", 0, -1)
        running_times_decoded = [float(d.decode()) for d in running_times]
        return running_times_decoded

    def get_mean_init_time(self,):
        init_times = self.get_all_init_times_list()
        avg = statistics.mean(init_times)
        return avg

    def get_mean_run_time(self,):
        init_times = self.get_all_running_times_list()
        avg = statistics.mean(init_times)
        return avg


# a = ContainerAnalysis(image_name='mongo:latest', node_idx=1)
# a = ContainerAnalysis(image_name='f1:latest', node_idx=2)
# a.set_login_config('sobhankiani04@gmail.com', 'skn1942', 'gameisthebest2014')

# a.calculate_initialization_time(iter=3)
# print(a.get_all_init_times_list())

# a.get_running_time(volume=f'{os.getcwd()}/functions/f1/output/:/app/output/')
# a.calculate_running_time(
    # 3, f'{os.getcwd()}/functions/f1/output/', '/app/output/')

# time.sleep(3)
# a.stor_running_times()
# l = a.get_all_running_times_list()
# print(l)
# https://registry-1.docker.io/v2/
# docker.from_env().containers.run()
