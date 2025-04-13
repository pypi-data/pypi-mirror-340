import asyncio
import os
import docker
import requests
import time

from manifold.hub.modules.node import Node


async def node_cleanup(app, node_name: str, stop_only: bool = False):
            """
            Cleans up processes related to the node identified by its name using Docker SDK.
            """
            client = docker.from_env()  # Initialize Docker client

            try:
                # Stop and remove the Docker container
                app.logger.info(f"Attempting to stop and remove Docker container for node_name: {node_name}")
                try:
                    container = client.containers.get(node_name)  # Get the container by name
                    if stop_only:
                        container.stop()  # Stop the container
                    else:
                        container.stop() # Stop the container
                        container.remove()  # Remove the container
                    app.logger.info(f"Docker container for node_name: {node_name} successfully stopped and removed.")
                except docker.errors.NotFound:
                    app.logger.warning(f"No Docker container found with name: {node_name}")

                # Clean up temporary files
                temp_file_path = f"/tmp/{node_name}.log"
                app.logger.info(f"Removing temporary file: {temp_file_path}")
                try:
                    import os
                    if os.path.exists(temp_file_path):
                        os.remove(temp_file_path)
                        app.logger.info(f"Temporary file for node_name: {node_name} removed.")
                    else:
                        app.logger.warning(f"Temporary file {temp_file_path} does not exist.")
                except Exception as e:
                    app.logger.error(f"Error removing temporary file for node_name {node_name}: {str(e)}")

                # Add additional cleanup tasks if necessary
                app.logger.info(f"Cleanup process completed for node_name: {node_name}")

            except Exception as e:
                app.logger.error(f"Error during cleanup for node_name {node_name}: {str(e)}")
            finally:
                # Close the Docker client
                client.close()