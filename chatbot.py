import os
from google import genai  # New SDK
import re
import random

API_KEY = os.getenv("GEMINI_API_KEY")
print(f"🔑 API Key: {'Loaded' if API_KEY else 'MISSING'}")

client = None
if API_KEY:
    try:
        client = genai.Client(api_key=API_KEY)
        print("✅ New Gemini client ready")
    except Exception as e:
        print(f"❌ Client error: {e}")

class SmartPortfolioBot:
    def __init__(self):
        self.rule_responses = {
            r'\b(hi|hello|hey|namaste)\b': ["Namaste! AstraDev Nexus AI bot 🚀 Ask anything!", "Hello! Gemini-powered & ready."],
            r'\b(bye|thanks)\b': ["Dhanyavaad! Visit portfolio.", "Bye! 🚀"],
            r'\b(api|gemini)\b': ["New google-genai SDK live! Smart replies now work."]
        }

    def get_reply(self, user_input):
        user_lower = user_input.lower()
        for pattern, replies in self.rule_responses.items():
            if re.search(pattern, user_lower):
                return random.choice(replies)

        if client:
            try:
                model = client.models.generate_content(
                    model="gemini-2.0-flash-exp",  # New stable model
                    contents=[f"Short friendly reply as Astra Nexus (7th grader, AstraDev Nexus): {user_input}"]
                )
                return model.text.strip()[:400]
            except Exception as e:
                print(f"❌ Gen error: {e}")
                return f"Trying... {str(e)[:80]} Rules always work!"
        return "🚧 Set GEMINI_API_KEY (ai.google.dev/app/apikey). Rules OK!"

bot = SmartPortfolioBot()
print("🤖 AstraDev Bot upgraded!")
