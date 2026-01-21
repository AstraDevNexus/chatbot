from flask import Flask, render_template, request, jsonify, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash
import requests, os, sqlite3

app = Flask(__name__)
app.secret_key = "astra-secret-key"

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = "llama-3.1-8b-instant"

# ---------------- DATABASE ----------------
def db():
    return sqlite3.connect("users.db")

def init_db():
    c = db().cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        email TEXT UNIQUE,
        password TEXT
    )
    """)
    db().commit()

init_db()

# ---------------- AUTH ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        pwd = request.form["password"]

        c = db().cursor()
        c.execute("SELECT * FROM users WHERE email=?", (email,))
        user = c.fetchone()

        if user and check_password_hash(user[2], pwd):
            session["user"] = email
            return redirect("/chat")

        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


@app.route("/register", methods=["POST"])
def register():
    email = request.form["email"]
    pwd = generate_password_hash(request.form["password"])

    try:
        db().execute("INSERT INTO users(email,password) VALUES(?,?)", (email, pwd))
        db().commit()
        return redirect("/")
    except:
        return render_template("login.html", error="User already exists")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ---------------- CHAT ----------------
@app.route("/chat")
def chat():
    if "user" not in session:
        return redirect("/")
    return render_template("index.html", user=session["user"])


@app.route("/api/chat", methods=["POST"])
def api_chat():
    if "user" not in session:
        return jsonify({"reply": "Unauthorized"})

    msg = request.json.get("message", "")

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are AstraDev Nexus, a professional AI assistant. Use markdown."},
            {"role": "user", "content": msg}
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            json=payload,
            headers=headers,
            timeout=20
        )
        reply = r.json()["choices"][0]["message"]["content"]
        return jsonify({"reply": reply})
    except:
        return jsonify({"reply": "AI service unavailable."})


if __name__ == "__main__":
    app.run(debug=True)
