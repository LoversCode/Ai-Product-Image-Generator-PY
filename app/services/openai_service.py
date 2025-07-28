import os
import openai
from app.utils.retry import retry

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_image(prompt):
    def call_openai_image():
        response = openai.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            n=1
        )
        if not response or not response.data:
            raise ValueError("No image data returned from OpenAI.")
        return response.data[0].url

    return retry(call_openai_image)

def generate_product_text(prompt):
    def call_openai_chat():
        system_prompt = "You are a branding expert creating product titles and descriptions for hoodies."
        user_prompt = f"Create a hoodie title and 2-sentence description for: '{prompt}'"

        chat = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )

        if not chat or not chat.choices:
            raise ValueError("No chat response returned from OpenAI.")

        response = chat.choices[0].message.content.strip()
        lines = response.split("\n")
        title = lines[0].strip()
        description = " ".join(line.strip() for line in lines[1:])
        return title, description

    return retry(call_openai_chat)
