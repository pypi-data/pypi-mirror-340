import docker
from typing import List

from manifold.hub.modules.node import Node

def port_lookup(mouted_nodes: List[Node]):

    # find empty port in range 7000 - 8000 by checking docker containers
    docker_client = docker.from_env()
    containers = docker_client.containers.list()

    used_ports = []
    for container in containers:
        # コンテナの名前を取得
        name = container.name
        
        # コンテナでマッピングされているポート情報を取得
        ports = container.ports  # 例: {'80/tcp': [{'HostIp': '0.0.0.0', 'HostPort': '8080'}], '443/tcp': None}

        print(f"Container Name: {name}")
        if ports:
            for port, mappings in ports.items():
                print(f"  Container Port: {port}")
                if mappings:
                    for mapping in mappings:
                        host_ip = mapping['HostIp']
                        host_port = mapping['HostPort']
                        used_ports.append(int(host_port))
                        print(f"    Host IP: {host_ip}, Host Port: {host_port}")
                else:
                    print("    No host mapping (exposed, but not published)")
        else:
            print("  No ports exposed.")
    
    # Find the first available port in the range 7000-8000
    print("Used Ports: ", used_ports)
    for port in range(7001, 8000):
        if port not in used_ports:
            return port

    # If no port is available, raise an exception
    raise RuntimeError("No available ports found in range 7000-8000")
