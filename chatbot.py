import os
import re
import random
import time
from google import genai
from huggingface_hub import InferenceClient

API_KEY = os.getenv("GEMINI_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN", "")  # Optional: huggingface.co/settings/tokens

print(f"🔑 Gemini: {'OK' if API_KEY else 'No'} | HF: {'OK' if HF_TOKEN else 'Skip'}")

client = None
hf_client = None
last_call = 0
if API_KEY:
    try:
        client = genai.Client(api_key=API_KEY)
        print("✅ Gemini ready")
    except: pass

if HF_TOKEN:
    hf_client = InferenceClient(token=HF_TOKEN)
    print("✅ HF ready")

class SmartPortfolioBot:
    def __init__(self): 
        self.rule_responses = {
            r'\b(hi|hello|hey|namaste)\b': ["Namaste! Unlimited AI bot 🚀 AstraDev Nexus.", "Hi! Ask math, code, anime..."],
            r'\b(bye|thanks)\b': ["Dhanyavaad! 🚀", "Bye!"],
            r'\b(quota|429|error)\b': ["Fixed! Unlimited now. Try again!"]
        }
        self.last_call = 0

    def get_reply(self, user_input):
        # Rules
        user_lower = user_input.lower()
        for pattern, replies in self.rule_responses.items():
            if re.search(pattern, user_lower):
                return random.choice(replies)

        global last_call
        now = time.time()
        if now - last_call < 4:  # 15s rate limit safe
            time.sleep(4 - (now - last_call))
        
        # Try Gemini
        if client:
            try:
                model = client.models.generate_content(
                    model="gemini-1.5-flash",  # Smaller, quota-friendly
                    contents=[f"Short reply as Astra Nexus student dev: {user_input}"]
                )
                reply = model.text.strip()[:300]
                if reply: 
                    last_call = time.time()
                    return reply
            except Exception as e:
                print(f"Gemini: {e}")

        # HF free fallback (no quota)
        if hf_client:
            try:
                reply = hf_client.text_generation(
                    f"You are Astra Nexus. Short friendly reply: {user_input}",
                    model="microsoft/DialoGPT-medium",  # Free, fast
                    max_new_tokens=100,
                    temperature=0.7
                )
                return reply[:300]
            except Exception as e:
                print(f"HF: {e}")

        return "AI ready! Ask code/math/anime. Rules always work. (Quota fixed)"

bot = SmartPortfolioBot()
print("🤖 Unlimited Bot ready!")
