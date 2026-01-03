from flask import Flask, render_template, request, jsonify, stream_with_context
from chatbot import SmartPortfolioBot
import json

app = Flask(__name__)
bot = SmartPortfolioBot()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json["msg"]
    reply = bot.get_reply(user_msg)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
