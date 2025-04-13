import os
from pathlib import Path
from fastapi import File, UploadFile
import requests
import time
import uuid

from fastapi import  HTTPException
from fastapi.responses import StreamingResponse

def bind_general_router(app):
    
    @app.get("/api/health")
    async def health_endpoint():
        """
        ヘルスチェック
        """
        return {"status": "ok"}
    
    @app.get("/api/infos")
    async def infos_endpoint():
        """
        hubのエンドポイント一覧に関する情報を取得
        """
        return app.openapi()
    
    @app.get("/api/nodes/")
    async def nodes_endpoint():
        """
        hubのnode一覧とそのエンドポイントに関する情報を取得
        """
        try:
            datas = []
            for node in app.nodes:
                datas.append({
                    "container_id": node.container_id,
                    "node_id": node.node_id,
                    "node_name": node.node_name,
                    "endpoint": node.endpoint
                })
            return datas
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting nodes: {str(e)}")
        
    @app.get("/api/nodes/item/{node_id}")
    async def nodes_one_endpoint(node_id: str):
        """
        対象nodeに含まれるapp tool一覧に関する情報を取得
        """
        try:
            # find node where name is node_name
            target_node = [n for n in app.nodes if n.node_id == node_id]
            if len(target_node) == 0:
                raise Exception(f"Node {node_id} not found")
            else:
                node = target_node[0]
                port = node.port
                host = node.host
                res = requests.get(f'http://{node.node_name}:{port}/api/apps')
                if res.status_code != 200:
                    raise Exception(f"{res.json()}")
                
                return {
                    "node_id": node.node_id,
                    "node_name": node.node_name,
                    "node_endpoint": node.endpoint,
                    "container_id": node.container_id,  
                    "apps":res.json()
                }
        except Exception as e:
            return HTTPException(status_code=500, detail=f"Error getting nodes: {str(e)}")

    @app.post("/api/uploads/")
    async def upload_file(file: UploadFile = File(...)):
        """
        ファイルアップロード
        """
        # Define the upload directory
        upload_directory = app.volume_dir
        # os.makedirs(upload_directory, exist_ok=True)

        # Define the file path
        file_extension = Path(file.filename).suffix
        fname = "{}_{}".format(str(time.time()).split(".")[0], str(uuid.uuid4()))
        save_path = os.path.join(upload_directory, fname + file_extension)

        # Save the file
        with open(save_path, "wb") as buffer:
            buffer.write(await file.read())

        return {"path": save_path, 
                "content_type": file.content_type}

    # @app.get("/api/uploads/clean")
    # def upload_image_clean_endpoint():
    #     """
    #     アップロードされたファイルを削除
    #     """
    #     pths = glob.glob(f'{app.volume_dir}/*')
    #     for pth in pths:
    #         os.remove(pth)
    #     return {
    #         'cleaned_num': len(pths),
    #     }
    
