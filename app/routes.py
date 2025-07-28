from flask import Blueprint, request, jsonify
from app.services.openai_service import generate_image, generate_product_text
from app.services.printful_service import upload_image, create_mockup

api = Blueprint('api', __name__)

@api.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    prompt = data.get("prompt", "").strip()

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        image_url = generate_image(prompt)
        file_id = upload_image(image_url)
        mockup_url = create_mockup(file_id)
        title, description = generate_product_text(prompt)

        return jsonify({
            "image_url": image_url,
            "printful_mockup_url": mockup_url,
            "product_title": title,
            "product_description": description
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route("/webhook/printful", methods=["POST"])
def handle_webhook():
    data = request.get_json()
    event_type = data.get("type")
    payload = data.get("data")

    print(f"[Webhook] Event received: {event_type}")
    print(payload)

    # You can add logic here to process fulfillment, shipping updates, etc.
    return jsonify({"status": "received"}), 200
