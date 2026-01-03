import re
import random
import json

class AstraDevBot:
    def __init__(self):
        self.knowledge = {
            "greeting": ["Namaste! AstraDev Nexus AI bot 🚀", "Hello! Ask about code, math, anime..."],
            "python": ["Python great for Flask bots like this! Use pip install flask gunicorn.", "Tips: Virtual env (`python -m venv env`), requirements.txt, git deploy Render."],
            "math": [
                lambda q: self.solve_math(q) if re.search(r'(\d+[+\-*/]\d+)', q) else "Solve step-by-step: e.g. '2+3*4'",
                "Algebra: Isolate variable. Calculus: Limits → derivatives."
            ],
            "web": ["Flask + HTML/CSS/JS + Render = portfolio gold! Responsive: media queries, flex/grid."],
            "ai": ["Built with Gemini (quota fixed soon). Next: Ollama local models, no limits!"],
            "anime": ["Demon Slayer epic! Tanjiro's Water Breathing = smooth code flow 💧"],
            "projects": ["Portfolio: Purple/cyan gamer site. This bot! Tic-tac-toe multiplayer Render."],
            "deploy": ["GitHub → Render: requirements.txt + Procfile (web: gunicorn app:app)"],
            "default": ["Cool Q! Astra Nexus (7th grade) tip: Practice HTML/CSS → JS → Python → AI 🚀"]
        }

    def solve_math(self, query):
        try:
            expr = re.search(r'(\d+(?:\s*[\+\-\*/]\s*\d+)+)', query.replace(' ', '')).group(1)
            return f"🤖 {expr} = {eval(expr)}"
        except: return "Math parser: Use '2+3' format."

    def get_reply(self, user_input):
        q = user_input.lower()
        
        # Smart keyword match
        for topic, responses in self.knowledge.items():
            if topic in q or any(word in q for word in topic.split()):
                if callable(responses[0]):
                    return responses[0](user_input)
                return random.choice(responses) if isinstance(responses, list) else responses

        return random.choice(self.knowledge["default"])

bot = AstraDevBot()
print("🤖 AstraDev Bot: Unlimited rules ready! No quota/model issues.")
