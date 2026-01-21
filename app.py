import os, json, requests
from flask import Flask, render_template, request, jsonify
import firebase_admin
from firebase_admin import credentials

app = Flask(__name__)

# Firebase init (safe via env)
cred = credentials.Certificate(json.loads(os.environ["FIREBASE_SERVICE_ACCOUNT"]))
firebase_admin.initialize_app(cred)

GROQ_API_KEY = os.environ["GROQ_API_KEY"]

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/chat")
def chat():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat_api():
    prompt = request.json.get("message")

    r = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama3-8b-8192",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.6
        }
    )

    data = r.json()
    return jsonify({"reply": data["choices"][0]["message"]["content"]})
