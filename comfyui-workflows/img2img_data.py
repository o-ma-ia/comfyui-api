from flask import abort
from utils.download_file import download_file
from utils.upload_file import upload_file

def get_data(data, seed):

    # Check if the required parameters are present
    if "positive" not in data:
        abort(500, description="The parameter 'positive' is required for this workflow")

    if "negative" not in data:
        abort(500, description="The parameter 'negative' is required for this workflow")
    
    if "image" not in data:
        abort(500, description="The parameter 'image' is required for this workflow")

    # Download the image
    file = download_file(data["image"], "./temp")
    # upload and set the image name for our LoadImage node
    with open(file, "rb") as f:
        comfyui_path_image = upload_file(f,"",True)

    return {
        "SEED": seed,
        "POSITIVE": data["positive"],
        "NEGATIVE": data["negative"],
        "IMAGE": comfyui_path_image,
    }