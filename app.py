from flask import Flask, render_template, redirect, request, session, jsonify

app = Flask(__name__)
app.secret_key = "CHANGE_THIS_SECRET_KEY"

# ---------------------------
# ROUTE: LOGIN PAGE
# ---------------------------
@app.route("/login")
def login():
    return render_template("login.html")


# ---------------------------
# ROUTE: MAIN CHAT UI
# ---------------------------
@app.route("/")
def index():
    """
    Protected route.
    Frontend Firebase auth will redirect if not logged in.
    """
    return render_template("index.html")


# ---------------------------
# ROUTE: LOGOUT
# ---------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# ---------------------------
# ROUTE: AI CHAT (API)
# ---------------------------
@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"reply": "Empty message"}), 400

    # 🔥 TEMP AI RESPONSE (replace with OpenAI later)
    ai_reply = f"You said: {user_message}"

    return jsonify({
        "reply": ai_reply
    })


# ---------------------------
# ROUTE: HEALTH CHECK
# ---------------------------
@app.route("/ping")
def ping():
    return "OK", 200


# ---------------------------
# RUN SERVER
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)
