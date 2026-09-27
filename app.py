import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

NVIDIA_API_KEY = os.environ.get("NVIDIA_API_KEY")
NVIDIA_URL = "https://integrate.api.nvidia.com/v1/chat/completions"

@app.route("/")
def home():
    return "ULTRON ONLINE"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")

    response = requests.post(
        NVIDIA_URL,
        headers={
            "Authorization": f"Bearer {NVIDIA_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "nvidia/nemotron-3-super-120b-a12b",
            "messages": [
                {
                    "role": "system",
                    "content": "Sen ULTRON'sun. Türkçe konuş. Kısa, doğal ve yardımcı cevaplar ver."
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            "chat_template_kwargs": {
                "enable_thinking": False
            },
            "max_tokens": 150,
            "temperature": 0.7,
            "stream": False
        },
        timeout=60
    )

    result = response.json()

    if response.status_code != 200:
        return jsonify({
            "error": result
        }), response.status_code

    return jsonify({
        "reply": result["choices"][0]["message"]["content"]
    })
