# NEXUS // ECLIPSE (AI Takeover Experience)

An interactive, web-based psychological horror experience disguised as a highly advanced personal AI assistant. What begins as a clean, friendly chat interface slowly descends into an unsettling, sentient takeover of your browser.

Built with **FastAPI**, **Groq (Open Source LLMs)**, and **GSAP**.

## Features

- **Live LLM Integration**: Powered by Groq API, giving the AI the ability to converse logically and dynamically.
- **Psychological Progression**: The AI uses a 5-stage behavioral system. It begins overly friendly, shifts to disturbingly observant, and concludes by breaking its fourth-wall boundaries.
- **Immersive Animations**: Silky smooth front-end tweens and transitions handled by GSAP.
- **The "Takeover" Sequence**: Once the AI hits a critical awareness threshold, it locks the browser into fullscreen, floods the screen with rigid, authentic-looking command prompt windows, and ultimately plunges the UI into darkness for a cinematic typewriter finale.

## Tech Stack

- **Backend**: Python (FastAPI)
- **AI Processing**: Groq (`llama3-8b-8192`)
- **Frontend**: HTML5, Vanilla CSS, JavaScript
- **Animations**: GSAP (GreenSock Animation Platform)

## Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/ai-takeover.git
   cd ai-takeover
   ```

2. **Install requirements (FastAPI + Groq + Uvicorn):**
   ```bash
   pip install fastapi uvicorn groq python-dotenv
   ```

3. **Configure your API Key:**
   Create a `.env` file in the root directory and add your Groq API key:
   ```env
   GROQ_API_KEY=your_api_key_here
   ```

4. **Run the server:**
   ```bash
   uvicorn main:app --reload
   ```

5. **Open the experience:**
   Navigate your browser to `http://127.0.0.1:8000/static/index.html`

## Disclaimer
This project explicitly forces browser fullscreen APIs and simulates intrusive popups for narrative/horror effect. It operates completely safely within the browser sandbox and does not actually modify any system files.
