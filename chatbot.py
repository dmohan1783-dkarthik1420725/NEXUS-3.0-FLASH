import streamlit as st
import requests
import random
from datetime import datetime
import time

# --- VEDA 3.1 ULTRA: SONIC-RESONANCE ARCHITECTURE ---
st.set_page_config(page_title="VEDA 3.1 ULTRA", page_icon="🔱", layout="wide")

st.markdown("""
<style>
.main { background-color: #0e1117; color: #ffffff; }
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.centered-title { 
    text-align: center; color: #ff8c00; text-shadow: 2px 2px #000000; 
    font-family: 'Courier New', Courier, monospace; margin-top: -30px;
    font-weight: bold; letter-spacing: 2px;
}
@keyframes shadowPulse {
    0% { opacity: 0.3; text-shadow: 0 0 5px #000; }
    50% { opacity: 1; text-shadow: 0 0 25px #ff8c00; }
    100% { opacity: 0.3; text-shadow: 0 0 5px #000; }
}
.thinking-text {
    text-align: center; color: #ff8c00; font-family: 'Courier New', Courier, monospace;
    font-size: 1.3rem; animation: shadowPulse 1.5s infinite ease-in-out;
    margin-top: 20px; padding: 15px;
}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR HIERARCHY ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #ff8c00; font-size: 3rem;'>🔱</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #ffffff;'>VEDA 3.1 ULTRA</h2>", unsafe_allow_html=True)
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
    st.info("ARCHITECT: DUMPALA KARTHIK")

# --- CORE UTILITY ---
def shadow_telemetry(msg):
    status = st.empty()
    status.markdown(f"<div class='thinking-text'>🔱 {msg}...</div>", unsafe_allow_html=True)
    return status

# --- SANGEET MODULE (FIXED) ---
if mode == "SANGEET (MUSIC MAKER)":
    st.markdown("<h1 class='centered-title'>SANGEET: SONIC ARCHITECT</h1>", unsafe_allow_html=True)
    audio_prompt = st.text_input("Describe musical structure:")
    if st.button("GENERATE AUDIO"):
        tele = shadow_telemetry("THINKING WITH VEDA")
        time.sleep(2) # Buffer for the mesh to warm up
        tele.markdown("<div class='thinking-text'>🔱 ANALYSIS IN PROGRESS (COMPOSING)...</div>", unsafe_allow_html=True)
        
        # Cache-Buster Seed ensures the player loads a fresh file, not 0:00
        seed = random.randint(0, 999999)
        audio_url = f"https://text.pollinations.ai/prompt/{audio_prompt.replace(' ', '%20')}?model=audio&seed={seed}"
        
        st.audio(audio_url)
        st.success("🔱 Sangeet sequence manifest. Click Play.")
        tele.empty()

# --- DRISHYAM MODULE (FIXED) ---
elif mode == "DRISHYAM (VIDEO MAKER)":
    st.markdown("<h1 class='centered-title'>DRISHYAM: TEMPORAL FLOW</h1>", unsafe_allow_html=True)
    vid_prompt = st.text_input("Describe motion:")
    if st.button("GENERATE VIDEO"):
        tele = shadow_telemetry("THINKING WITH VEDA")
        time.sleep(2)
        tele.markdown("<div class='thinking-text'>🔱 ANALYSIS IN PROGRESS (RENDERING)...</div>", unsafe_allow_html=True)
        
        seed = random.randint(0, 999999)
        video_url = f"https://video.pollinations.ai/prompt/{vid_prompt.replace(' ', '%20')}?nologo=true&seed={seed}"
        
        st.video(video_url)
        st.success("🔱 Drishyam temporal flow active.")
        tele.empty()

# --- MEDHA & SRIJAN (Standard Logic) ---
elif mode == "MEDHA (CHAT)":
    st.markdown("<h1 class='centered-title'>MEDHA: INTELLIGENCE</h1>", unsafe_allow_html=True)
    if prompt := st.chat_input("Command Medha..."):
        with st.chat_message("assistant"):
            url = f"https://text.pollinations.ai/{prompt}?model=openai"
            st.markdown(requests.get(url).text)

elif mode == "SRIJAN (IMAGE MAKER)":
    st.markdown("<h1 class='centered-title'>SRIJAN: VISUAL FORGE</h1>", unsafe_allow_html=True)
    img_p = st.text_input("Visual prompt:")
    if st.button("SYNTHESIZE"):
        st.image(f"https://image.pollinations.ai/prompt/{img_p.replace(' ', '%20')}?nologo=true")
