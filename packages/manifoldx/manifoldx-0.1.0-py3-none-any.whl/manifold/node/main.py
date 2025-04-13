import gradio as gr

import logging
from typing import Dict, Type
from fastapi import FastAPI, HTTPException
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_mcp import FastApiMCP

import torch

from .modules.endpoint import ManifoldEndpoint
from .routers.general_node_router import bind_general_node_endpoint

class ManifoldNode():
    
    def __init__(self, title='Manifold', version='0.0.0', volume_dir="/volumes", port=8000, mcp=True, endpoint_map={}):
        # ====================
        # fastapi app
        # ====================
        self.app = FastAPI(title=title, version=version)
        self.app.endpoints = {}

        if volume_dir is not None:
            self.app.volume_dir = volume_dir
            self.app.mount(volume_dir, StaticFiles(directory=volume_dir), name=volume_dir.replace("/", ""))

        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.app.logger = logging.getLogger("manifoldNode")
        self.app.logger.setLevel(logging.INFO)

        # append general endpoint
        bind_general_node_endpoint(self.app)

        # bind endpoint
        self.bind_endpoint(endpoint_map)

        # Mount the MCP server directly to your FastAPI app 
        if mcp:
            self.mcp = FastApiMCP(
                self.app,
                name=f"{title} MCP",
                description="Manifold Node MCP",
                base_url=f"http://localhost:{port}",
                describe_all_responses=True, 
                describe_full_response_schema=True
            )
            self.mcp.mount()
            self.app.logger.info(f"MCP server is running on http://localhost:{port}/mcp")

    
    def add_static_dir(self, name: str, target_dir: str):
        self.app.mount(target_dir, StaticFiles(directory=target_dir), name=name)
    
    def bind_endpoint(self, endpoint_map: Dict[str, Type[ManifoldEndpoint]]):
        for endpoint_name in endpoint_map:
            self.app.logger.info(f"Adding endpoint {endpoint_name}")

            # check if endpoint types is MANIFOLD_ENDPOINT class
            endpoint_class = endpoint_map[endpoint_name]
            if issubclass(endpoint_class, ManifoldEndpoint):
                try:
                    device = "cuda" if torch.cuda.is_available() else "cpu" 
                    endpoint_instance = endpoint_class()
                    endpoint_instance.device = device
                    self._add_endpoint(endpoint_instance)
                except Exception as e:
                    self.app.logger.info(f"Failed to instantiate endpoint '{endpoint_name}' with error: {e}")
            else:
                self.app.logger.info(f"Endpoint {endpoint_name} is not a valid ManifoldEndpoint class")
        
    def _add_endpoint(self, endpoint: ManifoldEndpoint): 
        endpoint_url = endpoint.url 
        endpoint_name = endpoint.name
        endpoint_description = endpoint.description

        # mount one gradio endpoint app
        app_interface = endpoint.create_app()
        self.app = gr.mount_gradio_app(self.app, app_interface, path=endpoint_url)

        # register
        self.app.endpoints[endpoint_name] = endpoint       
        
    def _teardown_all(self, excepts_endpoint_names=[]):
        for endpoint_name in self.app.endpoints:
            if endpoint_name in excepts_endpoint_names:
                continue
            
            endpoint = self.app.endpoints[endpoint_name]
            if endpoint is not None:
                endpoint.teardown_handler()
        