import streamlit as st
from google import genai
from google.genai import types
from datetime import datetime
import pytz
import requests
import random

# --- VEDA 3.1 ULTRA: ZERO-ERROR CONFIGURATION ---
st.set_page_config(page_title="VEDA 3.1 ULTRA", page_icon="🔱", layout="wide", initial_sidebar_state="expanded")

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
    @keyframes shadowPulse {
        0% { opacity: 0.2; text-shadow: 0 0 5px #000; }
        50% { opacity: 1; text-shadow: 0 0 20px #ff8c00; }
        100% { opacity: 0.2; text-shadow: 0 0 5px #000; }
    }
    .thinking-text {
        text-align: center; color: #ff8c00; font-family: 'Courier New', Courier, monospace;
        font-size: 1.2rem; animation: shadowPulse 2s infinite ease-in-out; margin-bottom: 20px;
    }
    .wip-text {
        color: #ff8c00; font-family: 'Courier New', Courier, monospace;
        font-weight: bold; border: 1px solid #ff8c00; padding: 10px;
        text-align: center; border-radius: 5px; background: rgba(255, 140, 0, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# 1. SIDEBAR: THE TRISHUL STATION
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #ff8c00; margin-top: -20px;'>🔱</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>VEDA 3.1 ULTRA</h2>", unsafe_allow_html=True)
    st.markdown("---")
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
    mode = st.radio("SELECT FREQUENCY:", ["MEDHA (CHAT)", "SRIJAN (IMAGE)", "SANGEET (MUSIC)", "DRISHYAM (VIDEO)"])
    st.markdown("---")
    st.info("ARCHITECT: DUMPALA KARTHIK")

# --- MODE: MEDHA (CHAT) ---
if mode == "MEDHA (CHAT)":
    st.markdown("<h1 class='centered-title'>MEDHA: INTELLIGENCE HUB</h1>", unsafe_allow_html=True)
    if prompt := st.chat_input("Command Medha..."):
        with st.chat_message("assistant"):
            pulse = st.empty()
            pulse.markdown("<div class='thinking-text'>🔱 THINKING WITH VEDA...</div>", unsafe_allow_html=True)
            try:
                # Primary Uplink
                client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
                res = client.models.generate_content(
                    model='gemini-3.1-pro-preview', 
                    contents=prompt, 
                    config=types.GenerateContentConfig(system_instruction="You are VEDA 3.1 ULTRA by DUMPALA KARTHIK.")
                )
                st.markdown(res.text)
            except Exception as e:
                st.markdown("Sorry, i cant help you with that.")
            pulse.empty()

# --- MODE: SRIJAN (IMAGE) ---
elif mode == "SRIJAN (IMAGE)":
    st.markdown("<h1 class='centered-title'>SRIJAN: VISUAL FORGE</h1>", unsafe_allow_html=True)
    img_prompt = st.text_input("Describe visual entity:")
    if st.button("SYNTHESIZE ART"):
        pulse = st.empty()
        pulse.markdown("<div class='thinking-text'>🔱 RENDERING SRIJAN...</div>", unsafe_allow_html=True)
        image_url = f"https://image.pollinations.ai/prompt/{img_prompt.replace(' ', '%20')}?nologo=true&seed={random.randint(0,9999)}"
        st.image(image_url, caption="VEDA Srijan Output", use_container_width=True)
        pulse.empty()

# --- MODE: SANGEET (MUSIC) ---
elif mode == "SANGEET (MUSIC)":
    st.markdown("<h1 class='centered-title'>SANGEET: SONIC ARCHITECT</h1>", unsafe_allow_html=True)
    audio_prompt = st.text_input("Describe musical structure:")
    if st.button("GENERATE SANGEET"):
        wip = st.empty()
        wip.markdown("<div class='wip-text'>🔱 WORK IN PROGRESS. PLEASE WAIT FOR 1-2 MINS...</div>", unsafe_allow_html=True)
        pulse = st.empty()
        pulse.markdown("<div class='thinking-text'>🔱 COMPOSING SONIC MESH...</div>", unsafe_allow_html=True)
        try:
            audio_url = f"https://text.pollinations.ai/prompt/{audio_prompt.replace(' ', '%20')}?model=audio&seed={random.randint(0,9999)}"
            audio_data = requests.get(audio_url).content
            st.audio(audio_data, format="audio/wav")
            st.success("🔱 Sangeet Manifested.")
        except:
            st.error("Sorry, i cant help you with that.")
        wip.empty()
        pulse.empty()

# --- MODE: DRISHYAM (VIDEO) ---
elif mode == "DRISHYAM (VIDEO)":
    st.markdown("<h1 class='centered-title'>DRISHYAM: TEMPORAL FLOW</h1>", unsafe_allow_html=True)
    vid_prompt = st.text_input("Describe temporal motion:")
    if st.button("GENERATE DRISHYAM"):
        wip = st.empty()
        wip.markdown("<div class='wip-text'>🔱 WORK IN PROGRESS. PLEASE WAIT FOR 1-2 MINS...</div>", unsafe_allow_html=True)
        pulse = st.empty()
        pulse.markdown("<div class='thinking-text'>🔱 INITIATING DRISHYAM FLOW...</div>", unsafe_allow_html=True)
        try:
            video_url = f"https://video.pollinations.ai/prompt/{vid_prompt.replace(' ', '%20')}?nologo=true&seed={random.randint(0,9999)}"
            video_data = requests.get(video_url).content
            st.video(video_data)
            st.success("🔱 Drishyam Flow Active.")
        except:
            st.error("Sorry, i cant help you with that.")
        wip.empty()
        pulse.empty()
