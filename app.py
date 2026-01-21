from flask import Flask, render_template, request, jsonify
import os
import requests
from groq import Groq

app = Flask(__name__)

# Groq Client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# ---------- ROUTES ----------

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/chat")
def chat():
    return render_template("index.html")

# ---------- CHAT API ----------
@app.route("/api/chat", methods=["POST"])
def chat_api():
    user_message = request.json.get("message", "")

    completion = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are Astra Nexus AI. "
                    "Reply accurately, in clear bullet points when helpful, "
                    "use markdown, code blocks, and structured formatting. "
                    "Never say you lack real-time data unless explicitly required."
                )
            },
            {"role": "user", "content": user_message}
        ],
        temperature=0.4,
        max_tokens=1024
    )

    reply = completion.choices[0].message.content

    return jsonify({"reply": reply})

# ---------- WEATHER API ----------
@app.route("/api/weather")
def weather():
    city = request.args.get("city")
    api_key = os.environ.get("OPENWEATHER_API_KEY")

    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&units=metric&appid={api_key}"
    )

    res = requests.get(url).json()
    return jsonify(res)

# ---------- RUN ----------
if __name__ == "__main__":
    app.run(debug=True)
