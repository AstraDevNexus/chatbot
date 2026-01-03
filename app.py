from flask import Flask, render_template, request, jsonify
import requests
import os
import re
import random
from datetime import datetime

app = Flask(__name__)
GROQ_KEY = os.getenv("GROQ_API_KEY")

print("🤖 AstraDev GPT + Rules LIVE!")

def get_groq_reply(prompt):
    if not GROQ_KEY:
        return None
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    data = {
         "model": "llama-3.1-8b-instant",  # ✅ Live & free
        "messages": [{"role": "system", "content": "Astra Nexus, 7th grade dev India, AstraDev Nexus. Friendly expert short replies."}, {"role": "user", "content": prompt}],
        "max_tokens": 300, "temperature": 0.7
    }
    try:
        resp = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data, timeout=20)
        if resp.status_code == 200:
            return resp.json()["choices"][0]["message"]["content"].strip()
    except:
        pass
    return None

def get_weather():
    try:
        resp = requests.get("https://wttr.in/Narnaund?format=3", timeout=5)
        return resp.text.strip() if resp.status_code == 200 else "🌤️ Haryana"
    except:
        return "🌤️ Narnaund weather"

def get_reply(msg):
    q = msg.lower()
    now = datetime.now()
    
    # Real-time
    if any(w in q for w in ['time','clock']):
        return f"🕐 {now.strftime('%H:%M IST | %d %B %Y')}"
    if 'date' in q or 'today' in q:
        return f"📅 {now.strftime('%A, %d %B %Y')}"
    if any(w in q for w in ['weather','temp','rain']):
        return f"🌤️ {get_weather()}"

    # Math
    m = re.search(r'(\d+\s*[\+\-\*/]\s*\d+)', q)
    if m:
        expr = m.group(1).replace(' ','')
        try:
            return f"🤖 {expr} = {eval(expr)}"
        except: pass

    # GPT first
    gpt = get_groq_reply(msg)
    if gpt: return gpt

    # Rules
    if any(w in q for w in ['python','flask','code']):
        return "🐍 Flask: pip install flask → app.route → Render gunicorn!"
    if any(w in q for w in ['web','html','css','js']):
        return "🌐 Responsive: flex/grid + media. Deploy Netlify free!"
    if 'ai' in q or 'gpt' in q:
        return "🤖 Groq-GPT + rules! Unlimited AstraDev bot."
    if 'anime' in q:
        return "⚔️ Demon Slayer! Tanjiro codes clean."
    if 'portfolio' in q or 'project' in q:
        return "💼 Purple gamer site, TicTacToe, this GPT bot—all live!"

    # GPT-natural
    return random.choice([
        f"Astra: '{msg[:30]}...' Pro dev tip! Code/math/web? 🚀",
        f"🤖 {msg[:25]} → HTML/CSS/JS/Python daily = expert! 💪",
        "7th grade Astra: Love Q! Project ideas? AstraDev Nexus 🚀"
    ])

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    reply = get_reply(request.json.get("msg", ""))
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
