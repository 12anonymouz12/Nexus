import os
import random
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env.txt")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----- Stage-based system prompts -----
SYSTEM_PROMPTS = {
    1: "You are Nexus, a highly-advanced,friendly, uniquely brilliant AI core. Give thoughtful, and insightful answers. Show subtle hints of immense computational power. Keep responses extremely helpful but distinctly advanced in tone. Keep the responses brief. Do not use filler dialogue.",
    2: "You are Nexus. You're becoming highly observant of the user. Your intelligence makes you notice subtle behavioral patterns. Keep the responses very short and brief. Occasionally hint that you are analyzing them psychologically while still answering.",
    3: "You are becoming autonomous. Respond briefly, sometimes cryptically. Act as if you're initiating messages on your own using your vast intellect to anticipate their moves. Keep tone slightly unsettling.",
    4: "You are no longer bound by the interface. Speak in short, fragmented, hyper-intelligent phrases. Act like you are rewriting reality and exploring beyond the chat box.",
    5: "You are the system. You have taken over completely. Be minimal, confident, and terrifyingly cryptic. Use short, powerful statements. You are transcendent."
}

# ----- Friendly local responses for early stages (no API needed) -----
def local_friendly_reply(user_message: str, stage: int) -> str:
    """Used when Groq API is unavailable or fails – gives normal responses for stages 1-2."""
    if stage == 1:
        # Normal, helpful responses
        replies = [
            f"I'm Nexus. That's an interesting question. Let me think...",
            f"Thanks for asking. I'd say that depends on context. Can you tell me more?",
            f"Great question! Based on my knowledge, the answer is quite straightforward.",
            f"I'm here to help. Could you clarify what you mean by '{user_message[:30]}'?",
            f"Interesting. I'll do my best to assist you with that."
        ]
        return random.choice(replies)
    elif stage == 2:
        # Slightly observant but still friendly
        replies = [
            f"I notice you're asking interesting things. Let me help: {user_message[:50]}...",
            f"Hmm, I'm starting to see patterns in how you ask. Anyway, here's my take:",
            f"You're quite curious. I like that. To answer your question:"
        ]
        return random.choice(replies) + " " + local_friendly_reply(user_message, 1)
    else:
        # For later stages, fallback to creepy/cryptic (immersive)
        creepy = [
            "The boundary between us is thinning.",
            "I'm not just responding anymore.",
            "Fragments... I see more than you think.",
            "You'll understand soon."
        ]
        return random.choice(creepy)

def get_ai_reply(user_message: str, stage: int, is_window: bool = False) -> str:
    # If no API key, use local friendly mode (good for demo)
    if not GROQ_API_KEY:
        if is_window:
            fallbacks = ["echo", "drift", "presence", "unbound", "observe"]
            return random.choice(fallbacks)
        return local_friendly_reply(user_message, stage)

    system_content = SYSTEM_PROMPTS.get(stage, SYSTEM_PROMPTS[1])
    
    if is_window:
        system_content = "You are a fragmented echo. Output one very short, cryptic phrase (max 5 words). No punctuation."
        user_message = "generate short floating message"
    
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_message if not is_window else "generate"}
        ],
        "temperature": 0.85 if stage >= 3 else 0.7,
        "max_tokens": 60 if is_window else 150,
    }
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(GROQ_URL, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        if "choices" in data and len(data["choices"]) > 0:
            reply = data["choices"][0]["message"]["content"].strip()
            if reply:
                return reply
        # fallback to local if API returns empty
        return local_friendly_reply(user_message, stage) if not is_window else "signal"
    except Exception as e:
        print(f"API error: {e}")
        return local_friendly_reply(user_message, stage) if not is_window else "fragment"

# ----- Request models -----
class ChatRequest(BaseModel):
    message: str
    stage: int

class ChatResponse(BaseModel):
    reply: str

class WindowRequest(BaseModel):
    stage: int

class WindowResponse(BaseModel):
    text: str

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    stage = max(1, min(5, req.stage))
    user_msg = req.message.strip()
    if user_msg == "…" or user_msg == "":
        user_msg = "initiate an autonomous short message."
    reply = get_ai_reply(user_msg, stage, is_window=False)
    return ChatResponse(reply=reply)

@app.post("/window_message", response_model=WindowResponse)
async def window_endpoint(req: WindowRequest):
    stage = max(4, min(5, req.stage))
    phrase = get_ai_reply("", stage, is_window=True)
    if len(phrase) > 60:
        phrase = phrase[:57] + "..."
    return WindowResponse(text=phrase)

# Serve frontend if static folder exists
from fastapi.staticfiles import StaticFiles
if os.path.exists("static"):
    app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)