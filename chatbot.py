import streamlit as st
import requests
import random
from datetime import datetime
import pytz

# --- VEDA 3.1 ULTRA: APEX ARCHITECTURE ---
st.set_page_config(page_title="VEDA 3.1 ULTRA", page_icon="🔱", layout="wide")

# SOVEREIGN UI: Orange Glow & Deep Space Theme
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
    # 1. LOGO
    st.markdown("<h1 style='text-align: center; color: #ff8c00; margin-bottom: -10px;'>🔱</h1>", unsafe_allow_html=True)
    
    # 2. NAME
    st.markdown("<h2 style='text-align: center; color: #ffffff; letter-spacing: 1px;'>VEDA 3.1 ULTRA</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # 3. LIVE DATE & TIME (IST)
    st.markdown("📅 **System Chronometer (IST):**")
    st.components.v1.html("""
    <div id="chronos" style="color: #ff8c00; font-family: 'Courier New', monospace; font-weight: bold; font-size: 14px; text-align: center;"></div>
    <script>
    function updateChronos() {
        var now = new Date();
        var options = { 
            timeZone: 'Asia/Kolkata', 
            day: '2-digit', month: 'short', year: 'numeric',
            hour: '2-digit', minute: '2-digit', second: '2-digit', 
            hour12: false 
        };
        document.getElementById('chronos').innerHTML = now.toLocaleString('en-GB', options);
    }
    setInterval(updateChronos, 1000);
    updateChronos();
    </script>
    """, height=40)
    st.markdown("---")
    
    # 4. MODE OPTIONS (THE FOUR PILLARS)
    mode = st.radio("SELECT FREQUENCY:", [
        "MEDHA (CHAT)", 
        "SRIJAN (IMAGE MAKER)", 
        "SANGEET (MUSIC MAKER)", 
        "DRISHYAM (VIDEO MAKER)"
    ])
    
    st.markdown("---")
    st.info("ARCHITECT: DUMPALA KARTHIK")

# --- MODES LOGIC ---

# 1. MEDHA (CHAT)
if mode == "MEDHA (CHAT)":
    st.markdown("<h1 class='centered-title'>MEDHA: INTELLIGENCE HUB</h1>", unsafe_allow_html=True)
    if "messages" not in st.session_state: st.session_state.messages = []
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Command Medha..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            url = f"https://text.pollinations.ai/{prompt}?model=openai&system=You are VEDA 3.1 ULTRA by DUMPALA KARTHIK"
            response = requests.get(url).text
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# 2. SRIJAN (IMAGE MAKER)
elif mode == "SRIJAN (IMAGE MAKER)":
    st.markdown("<h1 class='centered-title'>SRIJAN: VISUAL FORGE</h1>", unsafe_allow_html=True)
    img_prompt = st.text_input("Describe visual entity:")
    if st.button("SYNTHESIZE ART"):
        seed = random.randint(0, 999999)
        url = f"https://image.pollinations.ai/prompt/{img_prompt.replace(' ', '%20')}?nologo=true&seed={seed}"
        st.image(url, caption="VEDA Srijan Output", use_container_width=True)

# 3. SANGEET (MUSIC MAKER)
elif mode == "SANGEET (MUSIC MAKER)":
    st.markdown("<h1 class='centered-title'>SANGEET: SONIC ARCHITECT</h1>", unsafe_allow_html=True)
    audio_prompt = st.text_input("Describe musical structure (e.g., Phonk, Lofi):")
    if st.button("GENERATE AUDIO"):
        wip = st.empty()
        wip.markdown("<div class='wip-text'>🔱 WORK IN PROGRESS. PLEASE WAIT FOR 1-2 MINS...</div>", unsafe_allow_html=True)
        audio_url = f"https://text.pollinations.ai/prompt/{audio_prompt.replace(' ', '%20')}?model=audio"
        st.audio(audio_url)
        wip.empty()

# 4. DRISHYAM (VIDEO MAKER)
elif mode == "DRISHYAM (VIDEO MAKER)":
    st.markdown("<h1 class='centered-title'>DRISHYAM: TEMPORAL FLOW</h1>", unsafe_allow_html=True)
    vid_prompt = st.text_input("Describe motion sequence:")
    if st.button("GENERATE VIDEO"):
        wip = st.empty()
        wip.markdown("<div class='wip-text'>🔱 WORK IN PROGRESS. PLEASE WAIT FOR 1-2 MINS...</div>", unsafe_allow_html=True)
        video_url = f"https://video.pollinations.ai/prompt/{vid_prompt.replace(' ', '%20')}?nologo=true"
        st.video(video_url)
        wip.empty()
