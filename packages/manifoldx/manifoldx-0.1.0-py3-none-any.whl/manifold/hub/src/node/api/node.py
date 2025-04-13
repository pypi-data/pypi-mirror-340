import os
from fastapi import HTTPException
import requests

MANIFOLD_URL = os.getenv("MANIFOLD_URL")
        

def api_get_node_item(node_id):
    
    try:
        if not MANIFOLD_URL:
            raise ValueError("Environment variable MANIFOLD_URL is not set.")
        
        # Construct the API URL
        url = f"{MANIFOLD_URL}/api/nodes/item/{node_id}"
        
        # Perform the GET request
        response = requests.get(url)
        
        # Check for HTTP errors
        if response.status_code != 200:
            return HTTPException(status_code=response.status_code, detail=f"Error fetching node item: {response.text}")
        
        # Parse and return the JSON response
        data = response.json()
        return data
    
    except Exception as error:
        print("Error fetching node items:", error)
        return HTTPException(status_code=500, detail=f"Error fetching node items: {str(error)}")

def api_get_node_pickups():
    
    try:
        if not MANIFOLD_URL:
            raise ValueError("Environment variable MANIFOLD_URL is not set.")
        
        # Construct the API URL
        url = f"{MANIFOLD_URL}/api/nodes/pickups"
        
        # Perform the GET request
        response = requests.get(url)
        
        # Check for HTTP errors
        if response.status_code != 200:
            return HTTPException(status_code=response.status_code, detail=f"Error fetching node pickups: {response.text}")
            
        # Parse and return the JSON response
        data = response.json()
        return data
    
    except Exception as error:
        print("Error fetching node pickups:", error)
        return HTTPException(status_code=500, detail=f"Error fetching node pickups: {str(error)}")