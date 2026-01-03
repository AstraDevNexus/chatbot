import google.generativeai as genai
import re
import random
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))  # Set env var on Render
model = genai.GenerativeModel("gemini-1.5-flash")  # Fast, cheap

class SmartPortfolioBot:
    def __init__(self):
        self.system_prompt = """
        You are Astra Nexus, 7th-grade student-entrepreneur from Narnaund, Haryana, India.
        Company: AstraDev Nexus. Skills: HTML/CSS/JS, Python/Flask, Flutter/Dart, SQL, Firebase, AI APIs (Gemini, ElevenLabs).
        Interests: Web dev, AI chatbots, anime (Demon Slayer), video animation.
        Projects: Responsive portfolios (purple/cyan gamer theme), AI assistants, file transfer apps, admin dashboards.
        Answer helpfully, shortly, in friendly tone. Mention portfolio if relevant.
        """
        self.rule_responses = {
            r'\b(hi|hello|hey|namaste)\b': ["Namaste! AstraDev Nexus bot here. Ask anything!", "Hello! Ready for any question 🚀"],
            r'\b(bye|exit|thanks)\b': ["Dhanyavaad! Check my portfolio. Bye!", "Thanks! Keep building."],
        }

    def get_reply(self, user_input):
        # Check rules first
        user_lower = user_input.lower()
        for pattern, replies in self.rule_responses.items():
            if re.search(pattern, user_lower):
                return random.choice(replies)

        try:
            # AI for all else
            chat = model.start_chat(history=[])
            response = chat.send_message(f"{self.system_prompt}\nUser: {user_input}")
            return response.text.strip()
        except:
            return "Oops! AI offline. Try 'hi' or general questions. Portfolio tip: Integrate APIs like this!"

    def stream_chat(self):
        print("🤖 Astra Bot: Ask ANY question! 'bye' to exit.")
        while True:
            msg = input("You: ")
            if "bye" in msg.lower(): break
            print("🤖 Bot:", self.get_reply(msg))
