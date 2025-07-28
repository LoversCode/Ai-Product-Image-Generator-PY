import os
import time
import requests
from app.utils.retry import retry
from app.config.constants import (
    PRINTFUL_UPLOAD_URL,
    PRINTFUL_MOCKUP_TASK_URL,
    PRINTFUL_MOCKUP_STATUS_URL
)

PRINTFUL_API_KEY = os.getenv("PRINTFUL_API_KEY")
HEADERS = {"Authorization": f"Bearer {PRINTFUL_API_KEY}"}

def upload_image(image_url):
    def call_upload():
        res = requests.post(
            PRINTFUL_UPLOAD_URL,
            headers=HEADERS,
            json={"url": image_url}
        )
        res.raise_for_status()
        data = res.json()
        if "result" not in data or "id" not in data["result"]:
            raise ValueError("Invalid response from Printful on image upload.")
        return data["result"]["id"]

    return retry(call_upload)

def create_mockup(file_id):
    def call_create_mockup_task():
        payload = {
            "variant_ids": [4012],  # Gildan hoodie - Black
            "files": [{"placement": "front", "id": file_id}],
            "options": {"mockup_format": "jpg"}
        }

        res = requests.post(
            PRINTFUL_MOCKUP_TASK_URL,
            headers=HEADERS,
            json=payload
        )
        res.raise_for_status()
        task_data = res.json()
        if "result" not in task_data or "task_key" not in task_data["result"]:
            raise ValueError("Invalid response from Printful on mockup task creation.")
        return task_data["result"]["task_key"]

    task_key = retry(call_create_mockup_task)

    for _ in range(10):
        time.sleep(3)
        try:
            check = requests.get(
                f"{PRINTFUL_MOCKUP_STATUS_URL}?task_key={task_key}",
                headers=HEADERS
            )
            check.raise_for_status()
            task_status = check.json()["result"]
            if task_status["status"] == "completed":
                return task_status["mockups"][0]["mockup_url"]
        except Exception:
            continue

    raise TimeoutError("Mockup generation failed or timed out.")
