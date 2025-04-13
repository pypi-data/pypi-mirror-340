

class Node:
    
    def __init__(self, container_id, node_id, node_name, docker_image_name, port, host="0.0.0.0", token=None):
        self.container_id = container_id
        self.node_id = node_id
        self.node_name = node_name
        self.docker_image_name = docker_image_name
        self.port = port
        self.host = host
        self.token = token
        self.endpoint = f"http://{host}:{port}"
        
    def __str__(self):
        return f"{self.node_id}, {self.node_name}, {self.port}, {self.container_id}"
    