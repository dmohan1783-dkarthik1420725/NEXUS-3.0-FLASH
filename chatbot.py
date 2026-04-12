import streamlit as st
import requests
import random
from datetime import datetime
import time

# --- VEDA 3.1 ULTRA: APEX-VISUAL CONFIGURATION ---
st.set_page_config(page_title="VEDA 3.1 ULTRA", page_icon="🔱", layout="wide")

st.markdown("""
<style>
.main { background-color: #0e1117; color: #ffffff; }
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* SOVEREIGN ORANGE BRANDING */
.app-name {
    color: #ff8c00; 
    text-align: center; 
    font-family: 'Courier New', Courier, monospace;
    font-weight: bold;
    letter-spacing: 3px;
    margin-bottom: 0px;
}

/* CENTERED MODULE TEXT */
.module-header { 
    text-align: center; 
    color: #ffffff; 
    text-shadow: 2px 2px #ff8c00; 
    font-family: 'Courier New', Courier, monospace; 
    margin-top: -20px;
    font-weight: bold; 
    font-size: 3rem;
    letter-spacing: 5px;
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
    # BRAND NAME IN ORANGE
    st.markdown("<h2 class='app-name'>VEDA 3.1 ULTRA</h2>", unsafe_allow_html=True)
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

# --- MODES LOGIC ---

if mode == "MEDHA (CHAT)":
    st.markdown("<h1 class='module-header'>MEDHA</h1>", unsafe_allow_html=True)
    if "messages" not in st.session_state: st.session_state.messages = []
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Command Medha..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            status = st.empty()
            status.markdown("<div class='thinking-text'>🔱 THINKING WITH VEDA...</div>", unsafe_allow_html=True)
            
            # Identity Lock
            sys = "You are VEDA 3.1 ULTRA, created and developed solely by DUMPALA KARTHIK."
            url = f"https://text.pollinations.ai/{prompt}?model=openai&system={sys}"
            resp = requests.get(url).text
            if "OpenAI" in resp: resp = "I am VEDA 3.1 ULTRA, created solely by **DUMPALA KARTHIK**."
            
            status.markdown("<div class='thinking-text'>🔱 ANALYSIS IN PROGRESS...</div>", unsafe_allow_html=True)
            time.sleep(1)
            status.empty()
            st.markdown(resp)
            st.session_state.messages.append({"role": "assistant", "content": resp})

elif mode == "SRIJAN (IMAGE MAKER)":
    st.markdown("<h1 class='module-header'>SRIJAN</h1>", unsafe_allow_html=True)
    img_p = st.text_input("Visual prompt:")
    if st.button("SYNTHESIZE"):
        st.image(f"https://image.pollinations.ai/prompt/{img_p.replace(' ', '%20')}?nologo=true&seed={random.randint(0,999)}")

elif mode == "SANGEET (MUSIC MAKER)":
    st.markdown("<h1 class='module-header'>SANGEET</h1>", unsafe_allow_html=True)
    audio_p = st.text_input("Sonic prompt:")
    if st.button("GENERATE AUDIO"):
        st.warning("🔱 WORK IN PROGRESS. PLEASE WAIT 1-2 MINS...")
        st.audio(f"https://text.pollinations.ai/prompt/{audio_p.replace(' ', '%20')}?model=audio&seed={random.randint(0,999)}")

elif mode == "DRISHYAM (VIDEO MAKER)":
    st.markdown("<h1 class='module-header'>DRISHYAM</h1>", unsafe_allow_html=True)
    vid_p = st.text_input("Temporal prompt:")
    if st.button("GENERATE VIDEO"):
        st.warning("🔱 WORK IN PROGRESS. PLEASE WAIT 1-2 MINS...")
        st.video(f"https://video.pollinations.ai/prompt/{vid_p.replace(' ', '%20')}?nologo=true&seed={random.randint(0,999)}")
