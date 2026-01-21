from flask import Flask, render_template, request, jsonify
import requests, os

app = Flask(__name__)

AI_API_KEY = os.environ.get("GROQ_API_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    if not AI_API_KEY:
        return jsonify({"reply": "Server AI key not configured."})

    user_msg = request.json.get("message", "")

    res = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {AI_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.1-8b-instant",
            "messages": [{"role": "user", "content": user_msg}]
        }
    )

    return jsonify({
        "reply": res.json()["choices"][0]["message"]["content"]
    })
