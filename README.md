# 🧠 AI Product Mockup Generator

A Flask-based API that generates product mockups for hoodies, t-shirts, and mugs using OpenAI (DALL·E + GPT) and the Printful API. Automatically create unique artwork, catchy product titles and descriptions, and realistic product mockups — perfect for launching your merch store or creative prototype.

---

## 🧩 Overview

This project allows you to input a creative prompt and a product type (hoodie, t-shirt, or mug), and it returns:

- 🖼️ AI-generated artwork  
- 📝 Product copy (title + description)  
- 🛍️ Realistic mockups via Printful  

Built using Flask, OpenAI APIs, and the Printful Mockup Generator.

---

## 🚀 Features

- 🎨 Artwork generation using OpenAI DALL·E 3  
- 🤖 Title and description generation using GPT-4 or GPT-3.5  
- 🖨️ Integration with Printful for uploading designs and retrieving mockups  
- 🔁 Single API endpoint for full product generation  
- 👕 Supports hoodie, t-shirt, and mug (easily extendable)  
- 🧼 Clean, modular Python codebase  

---

## 🛠️ Tech Stack

- Python 3.9+  
- Flask  
- OpenAI API (DALL·E 3 + GPT-4/GPT-3.5)  
- Printful API  
- `requests`  
- `python-dotenv`  

---

## 📦 Repository Setup

### 1. Clone the Repository

```bash

1. Clone the repo and `cd` into the folder.

    git clone https://github.com/LoversCode/Ai-Product-Image-Generator-PY.git
    cd Ai-Product-Image-Generator-PY



2. Create a virtual environment:
    ```
    python -m venv venv
    source venv/bin/activate  # or venv\Scripts\activate on Windows
    ```

3. Install dependencies:
    ```
    pip install -r requirements.txt
    ```

4. Create a `.env` file using `.env.example` and add your keys.
    ```
    OPENAI_API_KEY=your_openai_key_here  
    PRINTFUL_API_KEY=your_printful_api_key_here
    ```

    These are required for communicating with OpenAI and Printful.

5. Run the app:
    ```
    python run.py
    ```
    Once started, the server will be available at:  
    `http://localhost:5000`

### API Endpoint

**POST** `/generate`  
This endpoint generates the product image, uploads it to Printful, gets the mockup, and returns the product title and description.

#### Request Payload

```json
{
  "prompt": "cyberpunk lion",
  "product_type": "hoodie"
}
```

- `prompt`: Creative idea for the design  
- `product_type`: `"hoodie"`, `"tshirt"`, or `"mug"`

#### Example Responses

**Hoodie**

```json
{
  "image_url": "https://example.com/generated-image.jpg",
  "printful_mockup_url": "https://example.com/mockup.jpg",
  "product_title": "Neon Mane Majesty",
  "product_description": "This hoodie features a cyberpunk lion roaring through neon streets. A bold pick for fans of futuristic fashion and wild energy."
}
```

**T-Shirt**

```json
{
  "image_url": "https://example.com/generated-image.jpg",
  "printful_mockup_url": "https://example.com/mockup.jpg",
  "product_title": "Pixel Mountainscape",
  "product_description": "Bring nostalgia to life with a pixel-style mountain sunrise. Soft, stylish, and totally retro."
}
```

**Mug**

```json
{
  "image_url": "https://example.com/generated-image.jpg",
  "printful_mockup_url": "https://example.com/mockup.jpg",
  "product_title": "Sloth Mode Activated",
  "product_description": "Start your mornings slow with a chill sloth sipping coffee. A mug that speaks to your cozy side."
}
```