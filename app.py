from flask import Flask, render_template, request, jsonify
import os
import requests

app = Flask(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.1-8b-instant"


@app.route("/")
def login():
    return render_template("login.html")


@app.route("/chat")
def chat():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json()
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"reply": "Please type something."})

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "Reply like ChatGPT. Use bullet points and code blocks when helpful."},
            {"role": "user", "content": message}
        ],
        "temperature": 0.7,
        "max_tokens": 400
    }

    r = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=20
    )

    reply = r.json()["choices"][0]["message"]["content"]
    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(debug=True)
