from flask import Flask, render_template, request, Response
import requests, os

app = Flask(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    prompt = request.json["message"]

    def stream():
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "llama3-70b-8192",
                "stream": True,
                "messages": [{"role": "user", "content": prompt}],
            },
            stream=True,
        )

        for line in r.iter_lines():
            if line and line.startswith(b"data: "):
                yield line[6:].decode("utf-8")

    return Response(stream(), mimetype="text/plain")

if __name__ == "__main__":
    app.run(debug=True)
