import asyncio
import os
import docker
import requests
import time
from manifold.hub.src.node.utils.port_lookup import port_lookup
from manifold.hub.modules.node import Node


async def node_launch(app, node_id, node_name, docker_image_name, gpu_required, websocket=None):
    """
    Launch a new container with the given name and image.
    """
    docker_client = app.docker_client
    logger = app.logger
    mouted_nodes = app.nodes

    port = port_lookup(mouted_nodes)
    
    # > Check Launched Container ================ 
    # check if the container is already running
    # if so, stop the container
    # ======================================
    try:
        container = docker_client.containers.get(node_name)
        if container.status == 'running':
            # stop the container
            container.stop()
            container.remove()
            await send_message(f"Container '{node_name}' is already running. Stopping the container...", websocket, logger)
        else:
            container.remove()
            await send_message(f"Container '{node_name}' is already running. Removing the container...", websocket, logger)
    except docker.errors.NotFound:
        # Container doesn't exist, which is fine
        await send_message(f"Container '{node_name}' is not existing.", websocket, logger)
        pass
    except docker.errors.APIError as e:
        raise Exception(f"Error checking container status: {e.explanation}")


    # > Pull the Docker image ================
    # if not available in local, pull from Docker Hub
    # ======================================
    try:
        image = docker_client.images.get(docker_image_name)
        await send_message(f"Image '{docker_image_name}' found locally.", websocket, logger)
    except docker.errors.ImageNotFound:
        await send_message(f"Image '{docker_image_name}' not found locally. Pulling from Hub...", websocket, logger)
        await send_message(f"This process may take a few minutes...", websocket, logger)
        # image = docker_client.images.pull(docker_image_name)
        for log_line in docker_client.api.pull(docker_image_name, stream=True, decode=True):
            if 'status' in log_line:
                status_message = log_line.get('status', '')
                progress_message = log_line.get('progress', '')
                full_message = f"{status_message} {progress_message}".strip()
                if full_message:  # Only send non-empty messages
                    await send_message(full_message, websocket, logger, code=104)
        await send_message(f"Image '{docker_image_name}' successfully pulled.", websocket, logger)
    except docker.errors.APIError as e:
        raise Exception(f"Error pulling image: {e.explanation}")
    
    
    # Define the command to run inside the container
    command = (f"uvicorn main:manifoldNode.app --reload --host 0.0.0.0 --port {port}")

    # > Run the container ================
    # =================================
    try:
        # mkdir for this node
        HOST_PWD = os.getenv("HOST_PWD")
        node_volume_path = f"{HOST_PWD}/volumes/nodes/{node_id}/"
        os.makedirs(node_volume_path, exist_ok=True)
        if gpu_required:
            container = container_for_gpu(docker_client, docker_image_name, node_name, command, port, node_volume_path)
        else:
            container = container_for_cpu(docker_client, docker_image_name, node_name, command, port, node_volume_path)
        
        launcedNode = Node(container.id, node_id, node_name, docker_image_name, port, host="0.0.0.0")

        await send_message(f"Container '{node_name}' is successfully running...", websocket, logger)
    except docker.errors.APIError as e:
        raise Exception(f"Error running container: {e.explanation}")
    
    # > Container Health Check ================
    # =================================
    start_time = time.time()
    while True:
        await asyncio.sleep(7)
        
        try:
            app.logger.info(f"Checking health of container '{node_name}'... http://{node_name}:{port}/api/health ")   
            response = requests.get(f"http://{node_name}:{port}/api/health")
            app.logger.info(f"Health check response: {response.status_code}")

            # if health: resturn is { "status": "ok" }
            if response.status_code == 200:
                await send_message(f"Container '{node_name}' is healthy.", websocket, logger)

                # check if node_id is not exist or not
                duplicated_idxs = [i for i, n in enumerate(app.nodes) if n.node_id == node_id]
                if len(duplicated_idxs) > 0:
                    # remove the duplicated node
                    for idx in duplicated_idxs:
                        app.nodes.pop(idx)    
                app.nodes.append(launcedNode)
                
                break

        except Exception as e:
            app.logger.error(f"Error checking health of container '{node_name}': {e}")
            await send_message(f"Container '{node_name}' is not healthy. Retrying...", websocket, logger)
            
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time > 300:
            raise Exception(f"Container health check timed out after 180 seconds.")
    
    # > teardown other node ================ 
    # memory leak prevention
    # meomory offload for eeach of the nodes
    # ======================================
    try:
        for node in mouted_nodes:
            # hit POST: /api/teardown for each of node
            # response will be { "status": "ok" } on success
            response = requests.post(f"http://{node.node_name}:{node.port}/api/teardown")
            if response.status_code != 200:
                raise Exception(f"Error tearing down container '{node.node_name}': {response.json()}")
    except Exception as e:
        raise Exception(f"Error teardown other nodes: {e}")

    return launcedNode.__dict__

async def send_message(message, websocket=None, logger=None, code=102):
    """
    Send a message to the websocket and/or log it.
    """
    if websocket is not None:
        await websocket.send_json({
            "status_code": code,
            "message": message
        })
        await asyncio.sleep(0.5)

    if logger is not None:
        logger.info(message)


def container_for_gpu(docker_client, docker_image_name, node_name, command, port, node_volume_path, network="manifold-network"):
    try:
        container = docker_client.containers.run(
            image=docker_image_name,
            name=node_name,
            command=command,
            detach=True,
            ports={f'{port}/tcp': port},
            volumes={
                os.path.abspath(node_volume_path): {'bind': '/volumes', 'mode': 'rw'},
            },
            tty=True,
            stdin_open=True,
            network=network,
            restart_policy={"Name": "always"},
            environment={
                "NVIDIA_VISIBLE_DEVICES": "all",  # Expose all NVIDIA devices
                "NVIDIA_DRIVER_CAPABILITIES": "all",  # Grant all driver capabilities
            },
            runtime="nvidia",
        )
    except Exception as e:
        print(f"Error creating container: {e}")
        return None
    return container


def container_for_cpu(docker_client, docker_image_name, node_name, command, port, node_volume_path, network="manifold-network"):
    try:
        container = docker_client.containers.run(
                image=docker_image_name,
                name=node_name,
                command=command,
                detach=True,
                ports={f'{port}/tcp': port},
                volumes={
                    os.path.abspath(node_volume_path): {'bind': '/volumes', 'mode': 'rw'},
                },
                tty=True,
                stdin_open=True,
                network=network,
                restart_policy={"Name": "always"},
            )
    except Exception as e:
        print(f"Error creating container: {e}")
        return None
    return container