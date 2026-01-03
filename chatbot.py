import re
import random

class AstraDevBot:
    def get_reply(self, user_input):
        q = user_input.lower()
        
        # Math solver
        math_match = re.search(r'(\d+\s*[\+\-\*/x]\s*\d+)', q)
        if math_match:
            expr = math_match.group(1).replace('x','*')
            try:
                return f"🤖 Math: {expr} = {eval(expr.replace(' ',''))}"
            except: pass

        # Keywords → Smart
        if any(word in q for word in ['python','flask','code','pip']):
            return random.choice([
                "Python: `flask --app app run` → Deploy Render with gunicorn!",
                "Code tip: VS Code + GitHub + requirements.txt = pro workflow."
            ])
        if 'web' in q or 'html' in q or 'css' in q:
            return "Web: Responsive = media queries + flex/grid. Netlify/Render free!"
        if 'ai' in q or 'gemini' in q or 'gpt' in q:
            return "AI: This bot rules-based (quota-proof). Next Ollama local models!"
        if any(word in q for word in ['anime','demon','slayer']):
            return "Demon Slayer 🔥 Tanjiro = persistent coder. Nezuko = cute UI!"
        if 'project' in q or 'portfolio' in q:
            return "Projects: Purple gamer portfolio, TicTacToe multiplayer, this bot—all Render!"
        if 'deploy' in q or 'render' in q:
            return "Deploy: Git push → Render auto. Procfile: web: gunicorn app:app"
        if 'help' in q:
            return "Try: math/code/web/anime/projects/deploy. AstraDev unlimited bot!"

        # GPT-like general
        return random.choice([
            f"Astra reply: '{user_input[:30]}...' → Great Q! Share more for code/math.",
            f"🤖 Thinking: {user_input[:20]}... Daily practice = pro dev 🚀",
            "Astra Nexus tip: HTML/CSS → JS → Python → AI. Your turn!"
        ])

bot = AstraDevBot()
print("🤖 AstraDev SMART Bot LIVE!")
