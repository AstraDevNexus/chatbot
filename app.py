import os, requests, uuid
from flask import Flask, render_template, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
from datetime import datetime
import pytz

app = Flask(__name__)

# Firebase
cred = credentials.Certificate("firebase/serviceAccountKey.json")
initialize_app(cred)
db = firestore.client()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENWEATHER_KEY = os.getenv("OPENWEATHER_API_KEY")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

# ---------- AI CHAT ----------
@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    messages = data["messages"]

    r = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama3-70b-8192",
            "messages": messages
        }
    ).json()

    return {"reply": r["choices"][0]["message"]["content"]}

# ---------- WEATHER ----------
@app.route("/api/weather")
def weather():
    city = request.args.get("city")
    r = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_KEY}&units=metric"
    ).json()

    tz = pytz.timezone("Asia/Kolkata")
    time = datetime.now(tz).strftime("%I:%M %p")

    return {
        "temp": r["main"]["temp"],
        "desc": r["weather"][0]["description"],
        "time": time
    }

# ---------- FIRESTORE ----------
@app.route("/api/chats/<uid>")
def chats(uid):
    res = []
    for c in db.collection("users").document(uid).collection("chats").stream():
        res.append({"id": c.id, **c.to_dict()})
    return jsonify(res)

@app.route("/api/chat/new", methods=["POST"])
def new_chat():
    d = request.json
    cid = str(uuid.uuid4())
    db.collection("users").document(d["uid"]).collection("chats").document(cid).set({
        "title": "New Chat",
        "messages": []
    })
    return {"id": cid}

@app.route("/api/chat/save", methods=["POST"])
def save_chat():
    d = request.json
    db.collection("users").document(d["uid"])\
      .collection("chats").document(d["chatId"])\
      .update({"messages": d["messages"]})
    return {"ok": True}

@app.route("/api/chat/rename", methods=["POST"])
def rename_chat():
    d = request.json
    db.collection("users").document(d["uid"])\
      .collection("chats").document(d["chatId"])\
      .update({"title": d["title"]})
    return {"ok": True}

@app.route("/api/chat/delete", methods=["POST"])
def delete_chat():
    d = request.json
    db.collection("users").document(d["uid"])\
      .collection("chats").document(d["chatId"])\
      .delete()
    return {"ok": True}
