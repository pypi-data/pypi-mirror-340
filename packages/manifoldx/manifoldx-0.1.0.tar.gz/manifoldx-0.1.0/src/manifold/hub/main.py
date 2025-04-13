import docker
import logging

from fastapi import FastAPI
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .src.node.node_launch import node_launch
from .routers.node_router import bind_node_router
from .routers.general_router import bind_general_router
from .modules.node import Node

class Manifold():
    
    def __init__(self, title='Manifold', version='0.0.0', volume_dir="/volumes"):
        self.volume_dir = volume_dir
        
        self.app = FastAPI(title=title, version=version)
        self.app.nodes = [] 

        self.app.volume_dir = volume_dir
        self.app.mount(volume_dir, StaticFiles(directory=volume_dir), name=volume_dir.replace("/", ""))

        # docker client
        self.app.docker_client = docker.from_env()

        # append general endpoint
        bind_general_router(self.app)
        # append node managing endpoint
        bind_node_router(self.app)
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.app.logger = logging.getLogger("manifoldHub")
        self.app.logger.setLevel(logging.INFO)

        # Register shutdown event
        @self.app.on_event("shutdown")
        async def shutdown_event():
            self.shutdown()
    
    def __del__(self):
        self.app.logger.info("Running Shutdown Process .. ")
        self.shutdown()
        self.app.logger.info("Shutdown Complete")
        
    async def api(self, app_name, docker_image_name):
        await node_launch(self.app, app_name, docker_image_name)
        
    def stop_api(self, app_name):
        """
        Stop the running node
        """
        client = self.app.docker_client
        for node in self.nodes:
            if node.app_name == app_name:
                container = client.containers.get(node.container_id)
                container.stop()
                # remove the container
                container.remove()
                self.nodes.remove(node)
    
    def shutdown(self):
        """
        Shutdown all running nodes
        """
        client = docker.from_env()

        for node in self.app.nodes:
            container = client.containers.get(node.container_id)
            container.stop()
            container.remove()
            self.nodes.remove(node)