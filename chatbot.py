import streamlit as st
from google import genai
from google.genai import types
from datetime import datetime
import pytz
import requests
import random

# --- VEDA 3.1 ULTRA: SANSKRITI-VEDA CONFIGURATION ---
st.set_page_config(page_title="VEDA 3.1 ULTRA", page_icon="🔱", layout="wide", initial_sidebar_state="expanded")

# SOVEREIGN UI: Orange Glow, Shadow Pulse, and Live Clock
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    button[kind="header"] { color: #ff8c00 !important; }

    .centered-title { 
        text-align: center; color: #ff8c00; text-shadow: 2px 2px #000000; 
        font-family: 'Courier New', Courier, monospace; margin-top: -30px;
        font-weight: bold; letter-spacing: 2px;
    }

    /* SHADOW-PULSE ANIMATION: DARK TO REAL */
    @keyframes shadowPulse {
        0% { opacity: 0.2; text-shadow: 0 0 5px #000; }
        50% { opacity: 1; text-shadow: 0 0 20px #ff8c00; }
        100% { opacity: 0.2; text-shadow: 0 0 5px #000; }
    }
    .thinking-text {
        text-align: center; color: #ff8c00; font-family: 'Courier New', Courier, monospace;
        font-size: 1.2rem; animation: shadowPulse 2s infinite ease-in-out; margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 1. SIDEBAR: THE TRISHUL STATION
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #ff8c00; margin-top: -20px;'>🔱</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>VEDA 3.1 ULTRA</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # LIVE TIME INJECTOR (IST)
    st.markdown("⌚ **Live Time (IST):**")
    st.components.v1.html("""
        <div id="clock" style="color: white; font-family: 'Courier New', monospace; font-weight: bold; font-size: 16px;"></div>
        <script>
        function updateClock() {
            var now = new Date();
            var options = { timeZone: 'Asia/Kolkata', hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' };
            document.getElementById('clock').innerHTML = now.toLocaleTimeString('en-GB', options);
        }
        setInterval(updateClock, 1000);
        updateClock();
        </script>
    """, height=35)
    
    st.markdown("---")
    # THE FOUR SOVEREIGN PILLARS
    mode = st.radio("SELECT FREQUENCY:", ["MEDHA (CHAT)", "SRIJAN (IMAGE)", "SANGEET (MUSIC)", "DRISHYAM (VIDEO)"])
    st.markdown("---")
    st.info("ARCHITECT: DUMPALA KARTHIK")

# 2. FAILOVER SEARCH LOGIC
def fallback_intelligence(prompt):
    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            results = [r['body'] for r in ddgs.text(prompt, max_results=3)]
            context = "\n".join(results)
        url = f"https://text.pollinations.ai/Prompt:{prompt} Context:{context}?model=openai&system=You+are+VEDA+3.1+ULTRA+created+by+DUMPALA+KARTHIK"
        return requests.get(url).text
    except: return None

# --- MODE: MEDHA (INTELLIGENCE) ---
if mode == "MEDHA (CHAT)":
    st.markdown("<h1 class='centered-title'>MEDHA: INTELLIGENCE HUB</h1>", unsafe_allow_html=True)
    if prompt := st.chat_input("Command Medha..."):
        with st.chat_message("assistant"):
            pulse = st.empty()
            pulse.markdown("<div class='thinking-text'>🔱 THINKING WITH VEDA...</div>", unsafe_allow_html=True)
            try:
                client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
                res = client.models.generate_content(model='gemini-3.1-pro-preview', contents=prompt, 
                                                   config=types.GenerateContentConfig(system_instruction="You are VEDA 3.1 ULTRA by DUMPALA KARTHIK."))
                response = res.text
            except:
                response = fallback_intelligence(prompt)
            pulse.empty()
            st.markdown(response if response else "Sorry, i cant help you with that.")

# --- MODE: SRIJAN (VISUAL) ---
elif mode == "SRIJAN (IMAGE)":
    st.markdown("<h1 class='centered-title'>SRIJAN: VISUAL FORGE</h1>", unsafe_allow_html=True)
    img_prompt = st.text_input("Describe visual entity:")
    if st.button("SYNTHESIZE ART"):
        pulse = st.empty()
        pulse.markdown("<div class='thinking-text'>🔱 RENDERING SRIJAN...</div>", unsafe_allow_html=True)
        image_url = f"https://image.pollinations.ai/prompt/{img_prompt.replace(' ', '%20')}?nologo=true&seed={random.randint(0,9999)}&key={st.secrets.get('POLLINATIONS_KEY','')}"
        st.image(image_url, caption="VEDA Srijan Output", use_container_width=True)
        pulse.empty()

# --- MODE: SANGEET (SONIC) ---
elif mode == "SANGEET (MUSIC)":
    st.markdown("<h1 class='centered-title'>SANGEET: SONIC ARCHITECT</h1>", unsafe_allow_html=True)
    audio_prompt = st.text_input("Describe musical structure (e.g. Phonk beats, Cinematic Orchestra):")
    if st.button("GENERATE SANGEET"):
        pulse = st.empty()
        pulse.markdown("<div class='thinking-text'>🔱 COMPOSING SANGEET MESH...</div>", unsafe_allow_html=True)
        audio_url = f"https://text.pollinations.ai/prompt/{audio_prompt.replace(' ', '%20')}?model=audio&seed={random.randint(0,9999)}"
        st.audio(audio_url)
        pulse.empty()

# --- MODE: DRISHYAM (MOTION) ---
elif mode == "DRISHYAM (VIDEO)":
    st.markdown("<h1 class='centered-title'>DRISHYAM: TEMPORAL FLOW</h1>", unsafe_allow_html=True)
    vid_prompt = st.text_input("Describe temporal motion:")
    if st.button("GENERATE DRISHYAM"):
        pulse = st.empty()
        pulse.markdown("<div class='thinking-text'>🔱 INITIATING DRISHYAM FLOW...</div>", unsafe_allow_html=True)
        video_url = f"https://video.pollinations.ai/prompt/{vid_prompt.replace(' ', '%20')}?nologo=true&seed={random.randint(0,9999)}"
        st.video(video_url)
        pulse.empty()
