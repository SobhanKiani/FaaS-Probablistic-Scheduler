import docker 

def run_container(image, command=None, **kwargs):
    client = docker.from_env()
    local_port = kwargs.get('local_port')
    container_port = kwargs.get('container_port')

    if local_port and container_port:
        ports_arg = {f'{container_port}/tcp': local_port}
    else:
        ports_arg = None

    container = client.containers.run(
        image, command, detach=True, ports=ports_arg)
    return container


def get_or_run_container(image, command=None, **kwargs):
    client = docker.from_env()
    container = None
    for c in client.containers.list(all=True):
        if c.image.tags[0] == image and c.status in ['running', 'exited']:
            container = c
            break
    if container is None:
        container = run_container(image, command, **kwargs)
    elif container.status == 'exited':
        container.start()
    return container


# get_or_run_container('flask_test:latest', local_port=5000, container_port=5000)

def wait_for_container(container):
    # Wait for the container to finish executing
    exit_code = container.wait()['StatusCode']
    if exit_code != 0:
        # Handle container errors here
        return 400
    container.remove()
    return 200


def wait_for_container_boot(container):
    # Wait for the container to boot up
    print('Waiting For Container To BOOT')
    while True:
        container.reload()
        if container.status == 'running':
            break
    print('Booted')
    # Get container IP address
    container_ip = container.attrs['NetworkSettings']['IPAddress']

    # Test container connectivity by pinging it
    client = docker.from_env()
    ping_container = client.containers.run(
        'alpine', f'ping -c1 {container_ip}', remove=True)
    # Wait for the container to finish executing
    # container.remove()


def stop_and_remove_container(container):
    client = docker.from_env()
    try:
        container_data = client.containers.get(container.id)
        container.stop()
        container.remove()
    except docker.errors.NotFound:
        pass


def get_container_ports(container):
    client = docker.from_env()
    # Get the container ID
    container_id = container.id

    # Inspect the container to get its network settings
    inspect_data = client.api.inspect_container(container_id)

    # Get the container's port mappings
    port_mappings = inspect_data['NetworkSettings']['Ports']
    # print("PORT MAPPINGS", port_mappings)

    # Print the container's port mappings
    for port in port_mappings:
        print('Container port:', port)
        for mapping in port_mappings[port]:
            print('Host IP:', mapping['HostIp'])
            print('Host port:', mapping['HostPort'])
