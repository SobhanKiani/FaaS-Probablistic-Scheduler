import time
import docker 

cli = docker.from_env()

st = time.time()

container = cli.containers.run("f1:latest", detach=True)

while True:
    container.reload()
    if container.status == 'running':
        break
    time.sleep(0.01)

et = time.time()

duration = et - st
print("DURATION: ", duration)

container.stop()
container.remove()

