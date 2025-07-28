import os
import time
import openai
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
PRINTFUL_API_KEY = os.getenv("PRINTFUL_API_KEY")

app = Flask(__name__)

# === Helper Functions ===

def retry_request(func, retries=3, delay=2, backoff=2):
    for attempt in range(retries):
        try:
            return func()
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(delay)
                delay *= backoff
            else:
                raise e

def generate_image(prompt):
    def call_openai():
        response = openai.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            n=1
        )
        return response.data[0].url

    return retry_request(call_openai)

def upload_to_printful(image_url):
    def call_printful_upload():
        response = requests.post(
            "https://api.printful.com/files",
            headers={"Authorization": f"Bearer {PRINTFUL_API_KEY}"},
            json={"url": image_url}
        )
        response.raise_for_status()
        return response.json()["result"]["id"]

    return retry_request(call_printful_upload)

def create_mockup(file_id):
    def start_mockup_task():
        payload = {
            "variant_ids": [4012],  # Gildan 18500 Unisex Hoodie - Black
            "files": [{"placement": "front", "id": file_id}],
            "options": {"mockup_format": "jpg"}
        }
        response = requests.post(
            "https://api.printful.com/mockup-generator/create-task/71",
            headers={"Authorization": f"Bearer {PRINTFUL_API_KEY}"},
            json=payload
        )
        response.raise_for_status()
        return response.json()["result"]["task_key"]

    task_key = retry_request(start_mockup_task)

    for _ in range(10):
        time.sleep(3)
        try:
            check = requests.get(
                f"https://api.printful.com/mockup-generator/task?task_key={task_key}",
                headers={"Authorization": f"Bearer {PRINTFUL_API_KEY}"}
            )
            check.raise_for_status()
            result = check.json()["result"]
            if result["status"] == "completed":
                return result["mockups"][0]["mockup_url"]
        except Exception as e:
            continue

    raise Exception("Mockup generation failed or timed out.")

def generate_product_text(prompt):
    def call_openai_chat():
        system_prompt = "You are a branding expert writing fun, catchy hoodie titles and descriptions."
        user_prompt = f"Create a product title and a 2-sentence product description for a hoodie design with the prompt: '{prompt}'"

        res = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        return res.choices[0].message.content.strip()

    text = retry_request(call_openai_chat)
    lines = text.split("\n")
    title = lines[0].strip()
    description = " ".join([line.strip() for line in lines[1:]])
    return title, description

# === Run App ===

if __name__ == "__main__":
    app.run(debug=True)
