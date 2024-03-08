import websocket
import uuid
import os
from PIL import Image
import io
from flask import request

from utils.get_comfyui_images import get_comfyui_images

def execute_workflow(workflow, seed):
    server_address = os.getenv("COMFYUI_SERVER_ADDRESS")
    client_id = str(uuid.uuid4())

    # Connect to the ComfyUI websocket
    ws = websocket.WebSocket()
    ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))

    # Execute ComfyUI workflow and get the generated images
    images = get_comfyui_images(ws, workflow, client_id)

    # Save the images to the output folder
    app_url = request.url_root
    final_images = []
    for node_id in images:
        for image_data in images[node_id]:
            image = Image.open(io.BytesIO(image_data))
            image.save(f"./output/{node_id}-{seed}.png")
            final_images.append(f"{app_url}output/{node_id}-{seed}.png")
    
    ws.close()

    return {
        "message": "Workflow executed successfully",
        "seed": seed,
        "images": final_images
    }

