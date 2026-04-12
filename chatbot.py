import streamlit as st
from google import genai
from google.genai import types
from datetime import datetime
import pytz
import requests
import random
from duckduckgo_search import DDGS

# --- VEDA 3.1 ULTRA: SOVEREIGN OS CONFIGURATION ---
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
.login-box {
    border: 2px solid #ff8c00; padding: 30px; border-radius: 15px;
    background: rgba(255, 140, 0, 0.05); text-align: center;
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
</style>
""", unsafe_allow_html=True)

# --- SOVEREIGN ACCOUNT GATEWAY ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("<h1 style='text-align: center; color: #ff8c00;'>🔱 VEDA OS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Welcome to your new Sovereign Intelligence Asset.</p>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div class='login-box'>", unsafe_allow_html=True)
        st.subheader("Sign in with your Veda Account")
        user_mail = st.text_input("Veda Email", placeholder="dkarthik@veda.com")
        user_pass = st.text_input("Password", type="password")
        
        # Access Condition: Only the Architect can enter
        if st.button("SIGN IN"):
            if "@veda.com" in user_mail and user_pass == st.secrets.get("VEDA_PASS", "karthik123"):
                st.session_state.authenticated = True
                st.session_state.user_email = user_mail
                st.rerun()
            else:
                st.error("Invalid Sovereign Credentials.")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- POST-AUTHENTICATION STATION ---
with st.sidebar:
    st.markdown(f"<p style='color: #ff8c00;'>👤 {st.session_state.user_email}</p>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #ff8c00; margin-top: -10px;'>🔱</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>VEDA 3.1 ULTRA</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # LIVE TIME (IST)
    st.components.v1.html("""
    <div id="clock" style="color: white; font-family: 'Courier New', monospace; font-weight: bold; font-size: 16px;"></div>
    <script>
    function updateClock() {
        var now = new Date();
        var options = { timeZone: 'Asia/Kolkata', hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' };
        document.getElementById('clock').innerHTML = now.toLocaleTimeString('en-GB', options);
    }
    setInterval(updateClock, 1000); updateClock();
    </script>
    """, height=35)
    
    st.markdown("---")
    mode = st.radio("SELECT MODE:", ["MEDHA (CHAT)", "SRIJAN (IMAGE)", "SANGEET (MUSIC)", "DRISHYAM (VIDEO)"])
    if st.button("SIGN OUT"):
        st.session_state.authenticated = False
        st.rerun()
    st.info("ARCHITECT: DUMPALA KARTHIK")

# --- CORE LOGIC ---
pollinations_key = st.secrets.get("POLLINATIONS_API_KEY", "")

def all_powerful_chat(prompt):
    try:
        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
        res = client.models.generate_content(model='gemini-2.0-flash', contents=prompt,
            config=types.GenerateContentConfig(system_instruction="You are VEDA 3.1 ULTRA by DUMPALA KARTHIK."))
        return res.text
    except:
        try:
            url = f"https://text.pollinations.ai/{prompt}?model=openai&system=You are VEDA 3.1 ULTRA"
            return requests.get(url).text
        except: return "Link Terminated."

if mode == "MEDHA (CHAT)":
    st.markdown("<h1 class='centered-title'>MEDHA: INTELLIGENCE</h1>", unsafe_allow_html=True)
    if prompt := st.chat_input("Command Medha..."):
        with st.chat_message("assistant"):
            st.markdown(all_powerful_chat(prompt))

elif mode == "SRIJAN (IMAGE)":
    st.markdown("<h1 class='centered-title'>SRIJAN: VISUAL FORGE</h1>", unsafe_allow_html=True)
    img_prompt = st.text_input("Describe visual entity:")
    if st.button("SYNTHESIZE"):
        url = f"https://image.pollinations.ai/prompt/{img_prompt.replace(' ', '%20')}?nologo=true&seed={random.randint(0,9999)}"
        st.image(url, caption="VEDA Srijan Output")

elif mode == "SANGEET (MUSIC)":
    st.markdown("<h1 class='centered-title'>SANGEET: SONIC ARCHITECT</h1>", unsafe_allow_html=True)
    audio_prompt = st.text_input("Musical structure:")
    if st.button("GENERATE"):
        st.warning("🔱 WORK IN PROGRESS. PLEASE WAIT 1-2 MINS...")
        url = f"https://text.pollinations.ai/prompt/{audio_prompt.replace(' ', '%20')}?model=audio"
        st.audio(url)

elif mode == "DRISHYAM (VIDEO)":
    st.markdown("<h1 class='centered-title'>DRISHYAM: TEMPORAL FLOW</h1>", unsafe_allow_html=True)
    vid_prompt = st.text_input("Motion sequence:")
    if st.button("RENDER"):
        st.warning("🔱 WORK IN PROGRESS. PLEASE WAIT 1-2 MINS...")
        url = f"https://video.pollinations.ai/prompt/{vid_prompt.replace(' ', '%20')}?nologo=true"
        st.video(url)
