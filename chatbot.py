import streamlit as st
import requests
import random
import pytz
import time
from google import genai
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

# --- 1. SOVEREIGN UI & PULSE ENGINE ---
st.set_page_config(page_title="VEDA 3.1 ULTRA", page_icon="🔱", layout="wide")
st_autorefresh(interval=1000, key="datetick")

st.markdown("""
<style>
    .stApp {
        background-color: #0a0c10;
        background-image: 
            linear-gradient(rgba(255, 140, 0, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 140, 0, 0.05) 1px, transparent 1px);
        background-size: 60px 60px;
    }
    
    /* Sovereign Header */
    .ultra-tag { background: #ff8c00; color: #000; padding: 5px 15px; border-radius: 20px; font-weight: bold; font-family: monospace; }
    
    /* Main Hub Styling */
    .main-hub { text-align: center; margin-top: 10vh; font-family: 'Courier New', monospace; }
    .hub-title { color: #ff8c00; font-size: 24px; letter-spacing: 3px; opacity: 0.8; }
    .welcome-msg { color: #ff8c00; font-size: 36px; font-weight: bold; margin: 25px 0; text-transform: uppercase; }

    /* Thinking Animation */
    @keyframes thinkingGlow {
        0% { text-shadow: 0 0 5px rgba(255,140,0,0.1); color: #444; }
        50% { text-shadow: 0 0 20px rgba(255,140,0,1); color: #ff8c00; }
        100% { text-shadow: 0 0 5px rgba(255,140,0,0.1); color: #444; }
    }
    .thinking-status {
        font-family: monospace;
        font-size: 16px;
        animation: thinkingGlow 1.5s infinite;
        margin-bottom: 20px;
        font-weight: bold;
    }
    
    /* AI Warning Footer */
    .warning-footer {
        position: fixed;
        bottom: 20px;
        width: 100%;
        color: #444;
        font-size: 11px;
        text-align: center;
        letter-spacing: 1px;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. INITIALIZE SESSION STATES ---
if "messages" not in st.session_state: st.session_state.messages = []
if "app_mode" not in st.session_state: st.session_state.app_mode = "Medha (Chat)"
if "auto_prompt" not in st.session_state: st.session_state.auto_prompt = None

# --- 3. TOP NAVIGATION ---
ist = pytz.timezone('Asia/Kolkata')
now = datetime.now(ist)

nav_col1, nav_col2, nav_col3 = st.columns([1, 3, 1])
with nav_col1:
    st.markdown("<h3 style='color:#ff8c00; margin:0;'>🔱 VEDA 3.1</h3>", unsafe_allow_html=True)
with nav_col3:
    st.markdown(f"<div class='ultra-tag'>ULTRA | {now.strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)

# --- 4. NEURAL CORE (CREATOR: DUMPALA KARTHIK) ---
def veda_neural_uplink(prompt):
    try:
        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
        system_instruction = (
            "You are VEDA 3.1 ULTRA. You were engineered, designed, and developed "
            "exclusively by DUMPALA KARTHIK. Address the user as Commander."
        )
        response = client.models.generate_content(
            model="models/gemini-3.1-pro-preview",
            contents=f"{system_instruction}\n\nCommander: {prompt}"
        )
        return response.text
    except Exception as e:
        return f"🔱 NEURAL GAP: {str(e)}"

# --- 5. MAIN COMMAND HUB ---
st.markdown("<div class='main-hub'>", unsafe_allow_html=True)
st.markdown("<p class='hub-title'>VEDA 3.1 ULTRA</p>", unsafe_allow_html=True)
st.markdown("<h1 class='welcome-msg'>MEDHA HUB: WELCOME, COMMANDER.</h1>", unsafe_allow_html=True)

# Tactical Action Chips
c1, c2, c3, c4, c5 = st.columns(5)
if c1.button("🎨 Image Forge"):
    st.session_state.app_mode = "Srijan (Image)"
    st.rerun()
if c2.button("🧠 Analyze Text"):
    st.session_state.auto_prompt = "Analyze this text for tactical insights:"
if c3.button("🏏 Follow IPL"):
    st.session_state.auto_prompt = "Provide latest IPL standings and player fitness updates."
if c4.button("✍️ Write Anything"):
    st.session_state.auto_prompt = "Draft a sovereign mission briefing regarding..."
if c5.button("☀️ Boost My Day"):
    st.session_state.auto_prompt = "Execute a motivational protocol for the Commander."

# Command Input & Processing
prompt = st.chat_input("Command the Ghost Mesh...") or st.session_state.auto_prompt

if prompt:
    st.session_state.auto_prompt = None # Reset auto-prompt
    status_area = st.empty()
    for _ in range(2):
        status_area.markdown("<p class='thinking-status'>THINKING WITH VEDA... ANALYSIS IN PROGRESS...</p>", unsafe_allow_html=True)
        time.sleep(0.8)
    
    ans = veda_neural_uplink(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "assistant", "content": ans})
    status_area.empty()

# Sector Display
if st.session_state.app_mode == "Medha (Chat)":
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(f"<span style='color:{'#ff8c00' if m['role']=='assistant' else '#fff'};'>{m['content']}</span>", unsafe_allow_html=True)

elif st.session_state.app_mode == "Srijan (Image)":
    st.markdown("<h2 style='color:#ff8c00;'>SRIJAN: VISUAL FORGE</h2>", unsafe_allow_html=True)
    img_prompt = st.text_input("Enter Visualization Coordinates...")
    if st.button("Forge Visualization"):
        url = f"https://pollinations.ai/p/{img_prompt.replace(' ', '_')}?width=1024&height=1024&seed={random.randint(0,999)}&model=flux&nologo=true"
        st.image(url, caption="🔱 VEDA VISUAL SYNTHESIS")
    if st.button("Return to Medha Hub"):
        st.session_state.app_mode = "Medha (Chat)"
        st.rerun()

# --- 6. SOVEREIGN WARNING FOOTER ---
st.markdown("""
    <div class='warning-footer'>
        VEDA IS AN AI AND CAN MAKE MISTAKES. PLEASE RECHECK MISSION-CRITICAL DATA.<br>
        SOVEREIGN INFRASTRUCTURE ENGINEERED BY DUMPALA KARTHIK
    </div>
""", unsafe_allow_html=True)