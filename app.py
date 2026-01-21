from flask import Flask, render_template, request, jsonify, session, redirect
from flask_cors import CORS
import uuid

app = Flask(__name__)
app.secret_key = "astra-secret-key"
CORS(app, supports_credentials=True)

# In-memory storage (later replace with Firestore)
USERS = {}
CHATS = {}

@app.route("/")
def home():
    if not session.get("user"):
        return redirect("/login")
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.json.get("email")
        session["user"] = email
        USERS[email] = True
        return jsonify({"success": True})
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/new-chat", methods=["POST"])
def new_chat():
    chat_id = str(uuid.uuid4())
    CHATS[chat_id] = {
        "title": "New Chat",
        "messages": []
    }
    return jsonify({"id": chat_id})

@app.route("/history")
def history():
    return jsonify([
        {"id": cid, "title": c["title"]}
        for cid, c in CHATS.items()
    ])

@app.route("/rename", methods=["POST"])
def rename():
    cid = request.json["id"]
    title = request.json["title"]
    CHATS[cid]["title"] = title
    return jsonify(success=True)

@app.route("/delete", methods=["POST"])
def delete():
    cid = request.json["id"]
    CHATS.pop(cid, None)
    return jsonify(success=True)

@app.route("/chat", methods=["POST"])
def chat():
    cid = request.json["id"]
    msg = request.json["message"]

    CHATS[cid]["messages"].append({"role": "user", "text": msg})

    reply = f"✨ AstraDev AI: {msg[::-1]}"  # demo response
    CHATS[cid]["messages"].append({"role": "bot", "text": reply})

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
