
import time
import uuid
import os
import torch
from pathlib import Path
from fastapi import File, HTTPException, UploadFile

def json_decode_by_link(jsonobj, linkpths):
    d = jsonobj
    for linkpth in linkpths.split("/"):
        d = d[linkpth]
    return d

def bind_general_node_endpoint(app):
    
    @app.get("/api/health")
    async def health_endpoint():
        return {"status": "ok"}
    
    @app.get("/api/version")
    async def health_endpoint():
        version_pth = os.path.join("version.txt")
        with open(version_pth, "r") as f:
            version = f.read()
        return {"version": version}
    
    @app.get("/api/device")
    async def health_endpoint():
        device_num = torch.cuda.device_count() if torch.cuda.is_available() else 0
        device_list = [torch.cuda.get_device_name(i) for i in range(device_num)]
        return {"num": device_num, "devices": device_list}
    
    @app.get("/api/infos")
    async def infos_endpoint():
        return app.openapi()
    
    @app.get("/api/apps", operation_id="get_apps")
    async def apps_endpoint():
        endpoints = app.endpoints
        app_list = [{"app_name": ep.name, "description": ep.description, "url": ep.url} for k, ep in endpoints.items()]
        
        return app_list
    
    @app.get("/api/apps/{app_name}", operation_id="get_apps_detail")
    async def apps_detail_endpoint(app_name: str):
        endpoints = app.endpoints

        if app_name not in endpoints:
            raise HTTPException(status_code=400, detail="no app found")
        
        endpoint = endpoints[app_name]
        app_infos = {"app_name": endpoint.name, 
                    "description": endpoint.description, 
                    "url": endpoint.url}
        return app_infos
    
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
    
    @app.post("/api/teardown")
    async def teardown_endpoint():
        try:
            for endpoint_name in app.endpoints:
                endpoint = app.endpoints[endpoint_name]
                if endpoint is not None:
                    endpoint.teardown_handler()
            torch.cuda.empty_cache()
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        return {"status": "ok"}