import os
import requests
from flask import Flask, request, Response, jsonify

app = Flask(__name__)

NVIDIA_API_KEY = os.environ.get("NVIDIA_API_KEY")
NVIDIA_URL = "https://integrate.api.nvidia.com/v1/chat/completions"


def ask_ultron(message):
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
                    "content": (
                        "Sen ULTRON'sun. "
                        "Türkçe konuş. "
                        "Kısa, doğal ve yardımcı cevaplar ver."
                    )
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

    if response.status_code != 200:
        return "Üzgünüm, şu anda NVIDIA servisine bağlanamıyorum."

    data = response.json()
    return data["choices"][0]["message"]["content"]


@app.route("/")
def home():
    return "ULTRON ONLINE"


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "message gerekli"}), 400

    reply = ask_ultron(message)

    return jsonify({
        "reply": reply
    })


# Telefon sağlayıcısının çağrıyı yönlendireceği endpoint
@app.route("/voice", methods=["POST", "GET"])
def voice():
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say language="tr-TR">
        Merhaba. Ben ULTRON. Şu anda sesli sistemim hazırlanıyor.
    </Say>
</Response>
"""
    return Response(xml, mimetype="text/xml")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
