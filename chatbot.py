import streamlit as st
from google import genai
import requests
import urllib.parse
from datetime import datetime
import pytz
from streamlit_option_menu import option_menu
import re

# --- 1. SOVEREIGN IDENTITY & MISSION ---
CREATOR = "DUMPALA KARTHIK"
IDENTITY = """
Your name is VEDA 3.0 ULTRA. Created by DUMPALA KARTHIK.
You are a pinnacle of Sovereign AI, engineered to be elite, fast, and resilient.
Karthik built your multi-brain rotation and custom CSS through massive effort.
"""

if 'user_name' not in st.session_state: st.session_state.user_name = None
if 'chat_history' not in st.session_state: st.session_state.chat_history = []

st.set_page_config(page_title="VEDA 3.0 ULTRA", page_icon="🔱", layout="wide", initial_sidebar_state="expanded")

ist = pytz.timezone('Asia/Kolkata')
def get_greeting():
    hour = datetime.now(ist).hour
    if 5 <= hour < 12: return "GOOD MORNING"
    elif 12 <= hour < 17: return "GOOD AFTERNOON"
    elif 17 <= hour < 21: return "GOOD EVENING"
    else: return "GOOD NIGHT"

def clean_veda(text):
    return re.sub(r"🌸.*?🌸|Powered by.*?AI|Support our mission|Ad|free text APIs", "", text, flags=re.IGNORECASE).strip()

# --- 2. ELITE CSS (Bouncing Arrow & Title) ---
st.markdown("""
    <style>
    header {visibility: hidden;}
    .v-title { font-size: 50px; color: #FF8C00; text-align: center; font-weight: 900; text-transform: uppercase; margin-top: 20px;}
    
    /* 🔱 THE SOVEREIGN DOWN ARROW */
    .nav-arrow {
        text-align: center;
        font-size: 45px;
        color: #FF8C00;
        cursor: pointer;
        animation: bounce 1.5s infinite;
        margin-top: -10px;
    }
    @keyframes bounce {
        0%, 100% {transform: translateY(0);}
        50% {transform: translateY(-10px);}
    }
    
    .thinking { color: #FF8C00; font-style: italic; animation: pulse 1s infinite; }
    @keyframes pulse { 0%, 100% { opacity: 0.2; } 50% { opacity: 1; } }
    </style>
""", unsafe_allow_html=True)

# --- 3. LOGIN ---
if st.session_state.user_name is None:
    st.markdown('<div class="v-title">VEDA 3.0 ULTRA</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        name_in = st.text_input("IDENTIFY COMMANDER:", placeholder="Enter Name...")
        if st.button("INITIALIZE 🚀", use_container_width=True):
            if name_in: st.session_state.user_name = name_in.strip(); st.rerun()
    st.stop()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align:center;'>🔱</h1><h2 style='text-align:center; color:#FF8C00;'>VEDA 3.0</h2>", unsafe_allow_html=True)
    st.markdown(f"""<p style='text-align:center; color:grey;'>📅 {datetime.now(ist).strftime("%A, %d %B")}<br>⏰ {datetime.now(ist).strftime("%I:%M %p")}</p>""", unsafe_allow_html=True)
    
    selected = option_menu(None, ["Medha (Chat)", "Srijan (Images)"], 
                          icons=["cpu", "image"], default_index=0, 
                          styles={"nav-link-selected": {"background-color": "#FF8C00"}})
    st.divider()
    if st.button("🗑️ Reset Core"): st.session_state.chat_history = []; st.rerun()

# --- 5. MAIN INTERFACE ---
st.markdown(f'<div class="v-title">{get_greeting()}, {st.session_state.user_name.upper()}</div>', unsafe_allow_html=True)

# 🔱 THE DOWN ARROW
st.markdown('<div class="nav-arrow">▼</div>', unsafe_allow_html=True)

if selected == "Medha (Chat)":
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Command VEDA..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            status = st.empty()
            final_res = ""
            
            # --- 🏎️ BRAIN 1: GEMINI 3.1 PRO (Using secrets.GOOGLE_API_KEY) ---
            status.markdown('<p class="thinking">🔱 Engaging Gemini Core...</p>', unsafe_allow_html=True)
            try:
                client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
                resp = client.models.generate_content(model="gemini-3.1-pro-preview", contents=f"{IDENTITY}\n\nUser: {prompt}")
                if resp.text: final_res = resp.text
            except: pass 

            # --- 🛡️ FAILOVER: POLLINATIONS ---
            if not final_res:
                status.markdown('<p class="thinking">🔱 Rotating to failover cluster...</p>', unsafe_allow_html=True)
                try:
                    p_enc = urllib.parse.quote(prompt); i_enc = urllib.parse.quote(IDENTITY)
                    # Using POLLINATIONS_KEY if required by your specific API setup
                    r = requests.get(f"https://text.pollinations.ai/{p_enc}?model=openai&system={i_enc}", timeout=15)
                    final_res = clean_veda(r.text)
                except: final_res = "🔱 Cluster saturation. Please retry."

            status.empty()
            st.markdown(final_res)
            st.session_state.chat_history.append({"role": "assistant", "content": final_res})

elif selected == "Srijan (Images)":
    st.markdown("<h3 style='text-align:center; color:#FF8C00;'>SRIJAN VISUAL SYNTHESIS</h3>", unsafe_allow_html=True)
    vision = st.text_input("Vision Matrix Prompt:", placeholder="Describe the image...")
    
    if st.button("🚀 INITIATE VISUALIZATION", use_container_width=True):
        if vision:
            with st.spinner("🔱 Synthesizing Visual Matrix..."):
                v_enc = urllib.parse.quote(vision)
                # 🚀 Srijan Fix: Direct Flux engine with seed to force refresh
                img_url = f"https://image.pollinations.ai/prompt/{v_enc}?width=1024&height=1024&nologo=true&model=flux&seed={datetime.now().microsecond}"
                st.image(img_url, use_container_width=True, caption=f"🔱 Vision for {st.session_state.user_name}")
        else:
            st.warning("Commander, please provide a vision prompt.")
