import streamlit as st
import requests
import random
from datetime import datetime
import pytz

# --- VEDA 3.1 ULTRA: SHADOW-PULSE ARCHITECTURE ---
st.set_page_config(page_title="VEDA 3.1 ULTRA", page_icon="🔱", layout="wide")

# SOVEREIGN UI: Shadow-to-Text Animation Logic
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

/* SHADOW-PULSE ANIMATION: MIMICKING GEMINI'S FLOW */
@keyframes shadowPulse {
    0% { opacity: 0.2; text-shadow: 0 0 5px #000; }
    50% { opacity: 1; text-shadow: 0 0 20px #ff8c00; }
    100% { opacity: 0.2; text-shadow: 0 0 5px #000; }
}

.thinking-text {
    text-align: center;
    color: #ff8c00;
    font-family: 'Courier New', Courier, monospace;
    font-size: 1.2rem;
    animation: shadowPulse 2s infinite ease-in-out;
    margin-bottom: 20px;
}

.wip-text {
    color: #ff8c00; font-family: 'Courier New', Courier, monospace;
    font-weight: bold; border: 1px solid #ff8c00; padding: 15px;
    text-align: center; border-radius: 5px; background: rgba(255, 140, 0, 0.1);
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR: THE ELITE HIERARCHY ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #ff8c00; margin-bottom: -10px;'>🔱</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #ffffff; letter-spacing: 1px;'>VEDA 3.1 ULTRA</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("📅 **System Chronometer (IST):**")
    st.components.v1.html("""
    <div id="chronos" style="color: #ff8c00; font-family: 'Courier New', monospace; font-weight: bold; font-size: 14px; text-align: center;"></div>
    <script>
    function updateChronos() {
        var now = new Date();
        var options = { timeZone: 'Asia/Kolkata', day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false };
        document.getElementById('chronos').innerHTML = now.toLocaleString('en-GB', options);
    }
    setInterval(updateChronos, 1000); updateChronos();
    </script>
    """, height=40)
    st.markdown("---")
    
    mode = st.radio("SELECT FREQUENCY:", ["MEDHA (CHAT)", "SRIJAN (IMAGE MAKER)", "SANGEET (MUSIC MAKER)", "DRISHYAM (VIDEO MAKER)"])
    st.markdown("---")
    st.info("ARCHITECT: DUMPALA KARTHIK")

# --- MODES LOGIC WITH SHADOW ANIMATION ---

if mode == "MEDHA (CHAT)":
    st.markdown("<h1 class='centered-title'>MEDHA: INTELLIGENCE HUB</h1>", unsafe_allow_html=True)
    if prompt := st.chat_input("Command Medha..."):
        with st.chat_message("assistant"):
            # Stage 1: Thinking Shadow
            status_placeholder = st.empty()
            status_placeholder.markdown("<div class='thinking-text'>🔱 THINKING WITH VEDA...</div>", unsafe_allow_html=True)
            
            # Fetch Answer
            url = f"https://text.pollinations.ai/{prompt}?model=openai&system=You are VEDA 3.1 ULTRA by DUMPALA KARTHIK"
            response = requests.get(url).text
            
            # Stage 2: Analysis Shadow
            status_placeholder.markdown("<div class='thinking-text'>🔱 ANALYSIS IN PROGRESS...</div>", unsafe_allow_html=True)
            
            status_placeholder.empty()
            st.markdown(response)

elif mode == "SRIJAN (IMAGE MAKER)":
    st.markdown("<h1 class='centered-title'>SRIJAN: VISUAL FORGE</h1>", unsafe_allow_html=True)
    img_prompt = st.text_input("Describe visual entity:")
    if st.button("SYNTHESIZE ART"):
        status = st.empty()
        status.markdown("<div class='thinking-text'>🔱 THINKING WITH VEDA...</div>", unsafe_allow_html=True)
        # Transition to Analysis
        status.markdown("<div class='thinking-text'>🔱 ANALYSIS IN PROGRESS...</div>", unsafe_allow_html=True)
        url = f"https://image.pollinations.ai/prompt/{img_prompt.replace(' ', '%20')}?nologo=true"
        st.image(url, caption="VEDA Srijan Output")
        status.empty()

elif mode == "SANGEET (MUSIC MAKER)":
    st.markdown("<h1 class='centered-title'>SANGEET: SONIC ARCHITECT</h1>", unsafe_allow_html=True)
    audio_prompt = st.text_input("Describe musical structure:")
    if st.button("GENERATE AUDIO"):
        status = st.empty()
        status.markdown("<div class='thinking-text'>🔱 THINKING WITH VEDA...</div>", unsafe_allow_html=True)
        status.markdown("<div class='wip-text'>🔱 ANALYSIS IN PROGRESS. PLEASE WAIT FOR 1-2 MINS...</div>", unsafe_allow_html=True)
        url = f"https://text.pollinations.ai/prompt/{audio_prompt.replace(' ', '%20')}?model=audio"
        st.audio(url)
        status.empty()

elif mode == "DRISHYAM (VIDEO MAKER)":
    st.markdown("<h1 class='centered-title'>DRISHYAM: TEMPORAL FLOW</h1>", unsafe_allow_html=True)
    vid_prompt = st.text_input("Describe motion:")
    if st.button("GENERATE VIDEO"):
        status = st.empty()
        status.markdown("<div class='thinking-text'>🔱 THINKING WITH VEDA...</div>", unsafe_allow_html=True)
        status.markdown("<div class='wip-text'>🔱 ANALYSIS IN PROGRESS. PLEASE WAIT FOR 1-2 MINS...</div>", unsafe_allow_html=True)
        url = f"https://video.pollinations.ai/prompt/{vid_prompt.replace(' ', '%20')}?nologo=true"
        st.video(url)
        status.empty()
