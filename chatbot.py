import streamlit as st
from google import genai
from google.genai import types
from datetime import datetime
import pytz
import requests
import random
from duckduckgo_search import DDGS

# --- VEDA 3.1 ULTRA: LEGACY-FIX CONFIGURATION ---
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
    font-weight: bold; border: 1px solid #ff8c00; padding: 15px;
    text-align: center; border-radius: 5px; background: rgba(255, 140, 0, 0.1);
    margin-bottom: 10px;
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

# --- AUTHENTICATION & SEARCH HELPERS ---
pollinations_key = st.secrets.get("POLLINATIONS_API_KEY", "")

def web_search(query):
    try:
        with DDGS() as ddgs:
            results = [r['body'] for r in ddgs.text(query, max_results=3)]
            return "\n".join(results)
    except: return ""

# 2. UNIVERSAL CHAT FAILOVER (MEDHA) - FIXED MODEL PATHS
def all_powerful_chat(prompt):
    live_data = web_search(prompt)
    system_instr = "You are VEDA 3.1 ULTRA, an elite Sovereign AI created and developed solely by DUMPALA KARTHIK. Use this live data if needed: " + live_data
    
    # 1. Primary: Gemini 2.0 Flash (Apex)
    try:
        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
        res = client.models.generate_content(
            model='gemini-2.0-flash', 
            contents=prompt,
            config=types.GenerateContentConfig(system_instruction=system_instr)
        )
        return res.text
    except:
        # 2. Fallback: Updated Pollinations Mesh (Using OpenAI model instead of Search)
        try:
            # Encoding identity directly into the URL to force recognition
            safe_prompt = f"System: {system_instr}\nUser: {prompt}"
            url = f"https://text.pollinations.ai/{requests.utils.quote(safe_prompt)}?model=openai"
            response = requests.get(url, timeout=12)
            return response.text
        except:
            return "Sorry, connection lost. Check Neural Link."

# --- MODES ---
if mode == "MEDHA (CHAT)":
    st.markdown("<h1 class='centered-title'>MEDHA: INTELLIGENCE HUB</h1>", unsafe_allow_html=True)
    if "messages" not in st.session_state: st.session_state.messages = []
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])
    if prompt := st.chat_input("Command Medha..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            pulse = st.empty()
            pulse.markdown("<div class='thinking-text'>🔱 ACCESSING ALL POWERFUL AIs...</div>", unsafe_allow_html=True)
            response = all_powerful_chat(prompt)
            pulse.empty()
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

elif mode == "SRIJAN (IMAGE)":
    st.markdown("<h1 class='centered-title'>SRIJAN: VISUAL FORGE</h1>", unsafe_allow_html=True)
    img_prompt = st.text_input("Describe visual entity:")
    if st.button("SYNTHESIZE ART"):
        pulse = st.empty()
        pulse.markdown("<div class='thinking-text'>🔱 RENDERING (POLLINATIONS MESH)...</div>", unsafe_allow_html=True)
        image_url = f"https://image.pollinations.ai/prompt/{img_prompt.replace(' ', '%20')}?nologo=true&seed={random.randint(0,9999)}&key={pollinations_key}"
        st.image(image_url, caption="VEDA Srijan Output", use_container_width=True)
        pulse.empty()

elif mode == "SANGEET (MUSIC)":
    st.markdown("<h1 class='centered-title'>SANGEET: SONIC ARCHITECT</h1>", unsafe_allow_html=True)
    audio_prompt = st.text_input("Describe musical structure:")
    if st.button("GENERATE SANGEET"):
        wip = st.empty()
        wip.markdown("<div class='wip-text'>🔱 WORK IN PROGRESS. PLEASE WAIT FOR 1-2 MINS...</div>", unsafe_allow_html=True)
        # Using a direct audio synthesis link
        audio_url = f"https
