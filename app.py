from flask import Flask, render_template, request, jsonify
import os
import re
import requests
from datetime import datetime
from zoneinfo import ZoneInfo
from urllib.parse import quote_plus

app = Flask(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant").strip()

DEFAULT_TZ = os.getenv("DEFAULT_TZ", "Asia/Kolkata")  # IST
DEFAULT_LOCATION = os.getenv("DEFAULT_LOCATION", "Pune")  # change if you want

# ---- Helpers ----
def _compact_blank_lines(text: str) -> str:
    text = text.replace("\r\n", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

def _extract_location(text: str, keyword: str) -> str | None:
    """
    Matches:
      weather in London
      weather London
      time in New York
      time New York
      date in Tokyo
    """
    t = text.strip()

    # "keyword in <location>"
    m = re.search(rf"\b{keyword}\b\s+in\s+(.+)$", t, flags=re.I)
    if m:
        return m.group(1).strip(" ?.!")

    # "keyword <location>"
    m = re.search(rf"\b{keyword}\b\s+(.+)$", t, flags=re.I)
    if m:
        loc = m.group(1).strip(" ?.!")

        # avoid catching "time is it" / "weather today"
        if loc.lower() in ["today", "now", "is it", "right now", "currently"]:
            return None
        return loc

    return None

def _wttr(location: str) -> str:
    # wttr supports custom one-line format strings [web:159]
    loc = quote_plus(location)
    url = f"https://wttr.in/{loc}?format=%l:+%c+%t+%w"
    r = requests.get(url, timeout=8)
    if r.status_code == 200 and r.text.strip():
        return r.text.strip()
    return f"{location}: weather unavailable"

def _get_time_text(location: str | None) -> str:
    # If user asks "time in <location>", show IST time + mention timezone.
    # Without geocoding API keys, use IST as baseline but still respond clearly.
    tz = ZoneInfo(DEFAULT_TZ)
    now = datetime.now(tz)
    if location:
        return f"Time (IST) now: {now.strftime('%H:%M')} • Note: exact local timezone conversion for “{location}” needs a timezone API."
    return f"Time (IST) now: {now.strftime('%H:%M')}"

def _get_date_text(location: str | None) -> str:
    tz = ZoneInfo(DEFAULT_TZ)
    now = datetime.now(tz)
    if location:
        return f"Date (IST) today: {now.strftime('%A, %d %B %Y')} • Note: exact local date for “{location}” needs a timezone API."
    return f"Date (IST) today: {now.strftime('%A, %d %B %Y')}"

def groq_chat(user_text: str) -> str | None:
    if not GROQ_API_KEY:
        return None

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": GROQ_MODEL,  # e.g., llama-3.1-8b-instant [web:165]
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are AstraDev Nexus Bot. Reply like ChatGPT: clear, structured, short paragraphs, "
                    "use bullet points when helpful. If asked about portfolio, explain AstraDev Nexus projects briefly."
                ),
            },
            {"role": "user", "content": user_text},
        ],
        "temperature": 0.7,
        "max_tokens": 350,
    }

    try:
        resp = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=20,
        )
        if resp.status_code == 200:
            text = resp.json()["choices"][0]["message"]["content"]
            return _compact_blank_lines(text)
        # If key/model wrong you’ll see it in reply for debugging
        return f"Groq error {resp.status_code}: {_compact_blank_lines(resp.text)[:220]}"
    except Exception as e:
        return f"Groq request failed: {str(e)[:120]}"

def rules_fallback(user_text: str) -> str:
    q = user_text.lower().strip()

    # math quick
    m = re.search(r"(\d+\s*[\+\-\*/]\s*\d+)", q)
    if m:
        expr = m.group(1).replace(" ", "")
        try:
            return f"{expr} = {eval(expr)}"
        except:
            pass

    if any(w in q for w in ["hi", "hello", "hey", "namaste"]):
        return "Namaste! Ask anything—portfolio, code, math, weather, time."
    if "portfolio" in q or "projects" in q:
        return "AstraDev Nexus portfolio: web projects, AI chatbot demo, and deploys on Render/Netlify."
    return "Ask me anything—try: “weather in Pune”, “time”, “explain Flask routes”, or “explain my portfolio”."

# ---- Routes ----
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    msg = (data.get("message") or data.get("msg") or "").strip()  # <-- FIX

    if not msg:
        return jsonify({"reply": "Type a message."})

    # ... keep the rest same ...


    # Weather handling (any location)
    if re.search(r"\bweather\b", msg, flags=re.I):
        loc = _extract_location(msg, "weather") or DEFAULT_LOCATION
        return jsonify({"reply": _wttr(loc)})

    # Time/date handling (any location keyword)
    if re.search(r"\btime\b", msg, flags=re.I):
        loc = _extract_location(msg, "time")
        return jsonify({"reply": _get_time_text(loc)})

    if re.search(r"\bdate\b|\btoday\b", msg, flags=re.I):
        loc = _extract_location(msg, "date")
        return jsonify({"reply": _get_date_text(loc)})

    # GPT-like first
    gpt = groq_chat(msg)
    if gpt:
        return jsonify({"reply": gpt})

    # fallback if no key
    return jsonify({"reply": rules_fallback(msg)})

if __name__ == "__main__":
    app.run(debug=True)
