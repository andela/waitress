import json
import os

import requests
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

URI = "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart"
CONTENT_TYPE = "application/json; charset=UTF-8"


def upload_to_drive(filepath, filename):
    token = os.getenv("GDRIVE_TOKEN", "")
    headers = {"Authorization": f"Bearer {token}"}

    parameter = {"name": filename, "parents": ["### folder ID ###"]}
    files = {
        "data": ("metadata", json.dumps(parameter), CONTENT_TYPE),
        "file": open(filepath, "rb"),
    }
    response = requests.post(URI, headers=headers, files=files)
    return response.json()
