AstraDev Nexus – Flask AI Chatbot
==================================

Project Overview
----------------
AstraDev Nexus is a Flask-based AI chatbot web application.
It supports:

• AI responses using Groq API (LLaMA 3.1 model)
• Weather lookup for any city
• Time and date (IST default)
• Basic math calculations
• Portfolio information fallback
• Rule-based fallback when API key is missing

----------------------------------------

Features
--------

1. AI Chat (Groq API)
   - Uses Groq's OpenAI-compatible endpoint
   - Model default: llama-3.1-8b-instant
   - Structured ChatGPT-style replies

2. Weather Support
   - Uses wttr.in API
   - Example:
     weather in London
     weather Pune

3. Time & Date
   - Default timezone: Asia/Kolkata (IST)
   - Example:
     time
     time in New York
     date
     today

4. Quick Math
   - Supports basic expressions:
     5+3
     10*4
     20/5

5. Fallback System
   - If GROQ_API_KEY is missing, rules-based responses are used.

----------------------------------------

Project Structure
-----------------

app.py
templates/
    index.html
static/ (optional for CSS/JS)

----------------------------------------

Installation
------------

1. Clone the project
2. Create virtual environment

   python -m venv venv
   venv\Scripts\activate   (Windows)
   source venv/bin/activate (Mac/Linux)

3. Install dependencies

   pip install flask requests

4. Set environment variables (IMPORTANT)

   Windows:
   set GROQ_API_KEY=your_key_here

   Mac/Linux:
   export GROQ_API_KEY=your_key_here

Optional:
   set GROQ_MODEL=llama-3.1-8b-instant
   set DEFAULT_TZ=Asia/Kolkata
   set DEFAULT_LOCATION=Pune

5. Run the app

   python app.py

App runs on:
   http://127.0.0.1:5000/

----------------------------------------

Environment Variables
---------------------

GROQ_API_KEY      → Required for AI responses
GROQ_MODEL        → Default: llama-3.1-8b-instant
DEFAULT_TZ        → Default: Asia/Kolkata
DEFAULT_LOCATION  → Default: Pune

----------------------------------------

API Endpoints
-------------

GET /
    Loads index.html

POST /chat
    Request:
        {
            "msg": "Hello"
        }

    Response:
        {
            "reply": "AI response here"
        }

----------------------------------------

Technologies Used
-----------------

• Python 3.10+
• Flask
• Requests
• Groq API
• wttr.in weather API
• ZoneInfo (Python timezone module)

----------------------------------------

Deployment Ideas
----------------

• Render
• Railway
• Vercel (via serverless)
• DigitalOcean
• AWS EC2

----------------------------------------

Security Notes
--------------

• Never expose your GROQ_API_KEY publicly
• Use environment variables in production
• Disable debug=True in production

Change:
    app.run(debug=True)

To:
    app.run()

----------------------------------------

Author
------

AstraDev Nexus
AI + Web Developer Portfolio Project

----------------------------------------

Future Improvements
-------------------

• Add real timezone API for accurate city time
• Add database chat history
• Add user authentication
• Add UI chat bubbles
• Add streaming AI responses
• Add Docker support

----------------------------------------

End of File
----------------------------------------