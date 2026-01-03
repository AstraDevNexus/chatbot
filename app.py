from flask import Flask, render_template, request, jsonify
import requests
import os
import json

app = Flask(__name__)
GROQ_KEY = os.getenv("GROQ_API_KEY")

def get_groq_reply(prompt):
    if not GROQ_KEY:
        return "🚀 Groq key ready? Render Env → GROQ_API_KEY"
    
    headers = {
        "Authorization": f"Bearer {GROQ_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3.1-8b-instant",  # GPT-fast free
        "messages": [
            {"role": "system", "content": "You are Astra Nexus, 7th grade full-stack dev, AstraDev Nexus founder. Friendly, short, expert, fun replies."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 300,
        "temperature": 0.7
    }
    try:
        resp = requests.post("https://api.groq.com/openai/v1/chat/completions", 
                           headers=headers, json=data, timeout=20)
        if resp.status_code == 200:
            return resp.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Groq live! {str(e)[:50]}"
    
    return "AstraDev Groq-GPT bot ready! 🚀"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    msg = request.json.get("msg", "")
    reply = get_groq_reply(msg)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    print("🤖 AstraDev Groq-GPT LIVE!")
    app.run(debug=True)
