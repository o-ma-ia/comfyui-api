import os
from flask import abort
import requests
import datetime
from urllib.parse import urlparse


def download_file(url: str, dest_folder: str):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # create folder if it does not exist

    # Get the current date and time
    now = datetime.datetime.now()
    # Format it as a string
    date_str = now.strftime('%Y-%m-%d_%H-%M-%S')

    # Parse the URL and get the path
    path = urlparse(url).path
    # Extract the real filename from the path
    real_filename = os.path.splitext(os.path.basename(path))[0]
    # Extract the file extension from the path
    extension = os.path.splitext(path)[1]

    # Combine the real filename, date, and extension
    filename = f"{real_filename}_{date_str}{extension}"

    file_path = os.path.join(dest_folder, filename)

    r = requests.get(url, stream=True)
    if r.ok:
        print("saving to", os.path.abspath(file_path))
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
        
        return file_path
    else:  # HTTP status code 4XX/5XX
        print("Download failed: status code {}\n{}".format(r.status_code, r.text))
        abort(500, description="Can't dowloand file from the given URL")