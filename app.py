import os
import json
import uuid
import requests
from datetime import datetime
import pytz

from flask import Flask, render_template, request, jsonify
from firebase_admin import credentials, firestore, initialize_app

app = Flask(__name__)

# --------------------------------------------------
# FIREBASE INITIALIZATION (ENV VAR BASED)
# --------------------------------------------------
firebase_json = os.getenv("FIREBASE_SERVICE_ACCOUNT")

if not firebase_json:
    raise RuntimeError("FIREBASE_SERVICE_ACCOUNT env variable not set")

cred = credentials.Certificate(json.loads(firebase_json))
initialize_app(cred)
db = firestore.client()

# --------------------------------------------------
# API KEYS
# --------------------------------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# --------------------------------------------------
# ROUTES
# --------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

# --------------------------------------------------
# AI CHAT
# --------------------------------------------------
@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    messages = data.get("messages", [])

    r = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama3-70b-8192",
            "messages": messages
        },
        timeout=60
    )

    r.raise_for_status()
    reply = r.json()["choices"][0]["message"]["content"]

    return jsonify({"reply": reply})

# --------------------------------------------------
# WEATHER + TIME
# --------------------------------------------------
@app.route("/api/weather")
def weather():
    city = request.args.get("city", "Delhi")

    r = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather",
        params={
            "q": city,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric"
        },
        timeout=20
    )

    r.raise_for_status()
    data = r.json()

    tz = pytz.timezone("Asia/Kolkata")
    local_time = datetime.now(tz).strftime("%I:%M %p")

    return jsonify({
        "city": city,
        "temp": data["main"]["temp"],
        "desc": data["weather"][0]["description"].title(),
        "time": local_time
    })

# --------------------------------------------------
# FIRESTORE CHAT HISTORY
# --------------------------------------------------
@app.route("/api/chats/<uid>")
def get_chats(uid):
    chats = []
    for doc in db.collection("users").document(uid).collection("chats").stream():
        chats.append({"id": doc.id, **doc.to_dict()})
    return jsonify(chats)

@app.route("/api/chat/new", methods=["POST"])
def new_chat():
    d = request.json
    uid = d["uid"]
    chat_id = str(uuid.uuid4())

    db.collection("users").document(uid)\
      .collection("chats").document(chat_id)\
      .set({
          "title": "New Chat",
          "messages": [],
          "createdAt": firestore.SERVER_TIMESTAMP
      })

    return jsonify({"chatId": chat_id})

@app.route("/api/chat/save", methods=["POST"])
def save_chat():
    d = request.json
    db.collection("users").document(d["uid"])\
      .collection("chats").document(d["chatId"])\
      .update({
          "messages": d["messages"],
          "updatedAt": firestore.SERVER_TIMESTAMP
      })
    return jsonify({"ok": True})

@app.route("/api/chat/rename", methods=["POST"])
def rename_chat():
    d = request.json
    db.collection("users").document(d["uid"])\
      .collection("chats").document(d["chatId"])\
      .update({"title": d["title"]})
    return jsonify({"ok": True})

@app.route("/api/chat/delete", methods=["POST"])
def delete_chat():
    d = request.json
    db.collection("users").document(d["uid"])\
      .collection("chats").document(d["chatId"])\
      .delete()
    return jsonify({"ok": True})

# --------------------------------------------------
# MAIN
# --------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
