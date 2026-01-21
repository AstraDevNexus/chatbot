from flask import Flask, render_template, request, Response
import requests, os, time

app = Flask(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

SYSTEM_PROMPT = """
You are ChatGPT.
Rules:
- Answer clearly and accurately
- Use bullet points when useful
- Do NOT include code unless asked
- Do NOT mention limitations or cutoffs
- Be concise and factual
"""

def groq_reply(msg):
    res = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama3-70b-8192",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": msg}
            ],
            "temperature": 0.4
        }
    )
    return res.json()["choices"][0]["message"]["content"]

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/chat")
def chat():
    return render_template("index.html")

@app.route("/stream", methods=["POST"])
def stream():
    msg = request.json["message"]

    def generate():
        reply = groq_reply(msg)
        for word in reply.split(" "):
            yield f"data:{word} "
            time.sleep(0.025)

    return Response(generate(), mimetype="text/event-stream")
