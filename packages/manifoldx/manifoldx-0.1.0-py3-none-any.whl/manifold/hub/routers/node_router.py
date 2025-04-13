import json
import os
from fastapi import HTTPException, WebSocket, WebSocketDisconnect
import docker
import glob
import time
from fastapi.responses import StreamingResponse

# from manifold.hub.src.node.node_launch import node_launch
# from manifold.hub.src.node.api.fetch_node_info import fetch_node_info
from ..src.node.node_launch import node_launch
from ..src.node.node_cleanup import node_cleanup
from ..src.node.api.node import *
     

def bind_node_router(app):
    
    @app.get("/api/mfldx/nodes/pickups")
    async def get_node_historys():
        node_pickups = api_get_node_pickups()
        return node_pickups
    
    @app.get("/api/mfldx/nodes/item/{node_id}")
    async def get_node_item(node_id: str):
        node_item = api_get_node_item(node_id)
        return node_item
    
    @app.get("/api/nodes/hists")
    async def get_node_local_historys():
        history_pths = glob.glob(app.volume_dir + "/.config/nodes/historys/*.json")
        historys = []
        for pth in history_pths:
            with open(pth, "r") as f:
                historys.append(json.load(f))
        return historys

    @app.get("/api/nodes/stream-logs/{node_name}")
    async def node_log_stream_endpoint(node_name: str):
        """
        Stream logs from a Node Container.
        :param node_name: Name of the container
        """
        # Find the node in app.nodes to verify it exists
        node = None
        for n in app.nodes:
            if n.node_name == node_name:
                node = n
                break
                
        if node is None:
            raise HTTPException(status_code=404, detail=f"Node '{node_name}' not found")
            
        try:
            # Get the container by name
            container = app.docker_client.containers.get(node_name)
        except docker.errors.NotFound:
            raise HTTPException(status_code=404, detail=f"Container '{node_name}' not found")
        except docker.errors.APIError as e:
            raise HTTPException(status_code=500, detail=f"Docker API error: {str(e)}")
        
        def log_stream():
            try:
                # Stream logs from the container with timestamps
                log_buffer = ""
                for log in container.logs(stream=True, timestamps=True, tail=100):
                    log_buffer += log.decode("utf-8")
                    while "\n" in log_buffer:
                        line, log_buffer = log_buffer.split("\n", 1)
                        yield f"{line}\n"
            except docker.errors.APIError as e:
                yield f"Docker API error while streaming logs: {str(e)}\n"
            except Exception as e:
                yield f"Error streaming logs: {str(e)}\n"
        
        return StreamingResponse(
            log_stream(),
            media_type="text/plain",
            headers={"X-Node-Name": node_name}
        )
    
    @app.websocket("/ws/node/launch/{node_id}")
    async def websocket_launch_node_endpoint(websocket: WebSocket, node_id:str):
        # ------------------------------
        # get node info via api
        # ------------------------------
        try:
            node_info = api_get_node_item(node_id)
            node_name = node_info["data"]["name"]
            image_name = node_info["data"]["docker_url"]
            gpu_required = node_info["data"]["gpuRequired"]

            # store nodeinfo in .config
            savepth = f"{NODE_HISTORY_DIR}{node_id}.json"
            with open(savepth, "w") as f:
                json.dump(node_info["data"], f)

        except Exception as e:
            app.logger.error(f"Error fetching node info: {str(e)}") 
            await websocket.accept()
            await websocket.send_json({
                "status_code": 500,
                "message": f"Error: {str(e)}"
            })
            return

        # ------------------------------
        # establish websocket connection
        # ------------------------------
        await websocket.accept()
        try:
            node = await node_launch(app, node_id, node_name, image_name, gpu_required, websocket=websocket)
            # when completed
            await websocket.send_json({"status_code": 200, "message":"success", "node": node})
        except WebSocketDisconnect:
            app.logger.info(f"WebSocket disconnected for node_id: {node_id}")
            # Cleanup resources or processes related to the node
            await node_cleanup(app, node_name)
        except Exception as e:
            app.logger.error(f"Error launching node: {str(e)}") 
            try:
                await websocket.send_json({
                    "status_code": 500,
                    "message": f"Error: {str(e)}"
                })
            except RuntimeError:
                app.logger.warning("Failed to send error message: WebSocket already closed.")
        finally:
            # Cleanup and ensure no processes are left running
            # await cleanup_node_process(node_id)
            # Attempt to close WebSocket gracefully
            try:
                await websocket.close()
            except RuntimeError:
                app.logger.warning("WebSocket already closed, skipping close operation.")

    
    @app.websocket("/ws/node/cleanup/{node_id}")
    async def websocket_cleanup_node_endpoint(websocket: WebSocket, node_id:str):
        mounted_nodes = app.nodes

        # ------------------------------
        # find node with the node_id
        # ------------------------------
        try:
            target_nodes = [n for n in app.nodes if n.node_id == node_id]

            if len(target_nodes) == 0:
                raise Exception(f"Node {node_id} not found")
            
            target_node = target_nodes[0]
            
        except Exception as e:
            app.logger.error(f"Error On fetching node info: {str(e)}") 
            await websocket.accept()
            await websocket.send_json({
                "status_code": 500,
                "message": f"Error: {str(e)}"
            })
            return

        # ------------------------------
        # establish websocket connection
        # ------------------------------
        await websocket.accept()
        try:
            time.sleep(1)
            await websocket.send_json({"status_code": 104, "message":"target node found"})
            time.sleep(1)
            await websocket.send_json({"status_code": 104, "message":"starting cleanup"})
            time.sleep(1)
            await node_cleanup(app, target_node.node_name, stop_only=True)
            # remove from app.nodes
            app.nodes = [n for n in app.nodes if n.node_id != node_id]
            await websocket.send_json({"status_code": 200, "message":"success"})
        except WebSocketDisconnect:
            app.logger.info(f"WebSocket disconnected for node_id: {node_id}")
            # Cleanup resources or processes related to the node
        except Exception as e:
            app.logger.error(f"Error On CleanUp Node: {str(e)}") 
            try:
                await websocket.send_json({
                    "status_code": 500,
                    "message": f"Error: {str(e)}"
                })
            except RuntimeError:
                app.logger.warning("Failed to send error message: WebSocket already closed.")
        finally:
            # Cleanup and ensure no processes are left running
            # await cleanup_node_process(node_id)
            # Attempt to close WebSocket gracefully
            try:
                await websocket.close()
            except RuntimeError:
                app.logger.warning("WebSocket already closed, skipping close operation.")