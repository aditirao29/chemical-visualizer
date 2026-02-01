import requests
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("API_TOKEN")
API_BASE = os.getenv("API_BASE")

HEADERS = {
    "Authorization": f"Token {TOKEN}"
}

def upload_csv(file_path):
    with open(file_path, "rb") as f:
        files = {"file": f}
        response = requests.post(
            API_BASE + "upload/",
            headers=HEADERS,
            files=files,
            timeout=10
        )

    if response.status_code == 401:
        raise Exception("401 Unauthorized - check token")

    response.raise_for_status()
    return response.json()

def fetch_history():
    response = requests.get(
        API_BASE + "history/",
        headers=HEADERS
    )
    response.raise_for_status()
    return response.json()


def fetch_dataset_by_id(dataset_id):
    response = requests.get(
        API_BASE + f"history/{dataset_id}/",
        headers=HEADERS
    )
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    print(fetch_history())
