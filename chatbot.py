import streamlit as st
from google import genai
from google.genai import types
import requests
import urllib.parse
from datetime import datetime
import pytz
from streamlit_option_menu import option_menu
import time
import re

# --- 1. SOVEREIGN CONFIG & IDENTITY ---
IDENTITY = "Your name is VEDA 3.0 ULTRA. Created and developed ONLY by DUMPALA KARTHIK."

if 'user_name' not in st.session_state: st.session_state.user_name = None
if 'chat_history' not in st.session_state: st.session_state.chat_history = []

st.set_page_config(
    page_title="VEDA 3.0 ULTRA", 
    page_icon="🔱", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

ist = pytz.timezone('Asia/Kolkata')
def get_greeting():
    hour = datetime.now(ist).hour
    if 5 <= hour < 12: return "GOOD MORNING"
    elif 12 <= hour < 17: return "GOOD AFTERNOON"
    elif 17 <= hour < 21: return "GOOD EVENING"
    else: return "GOOD NIGHT"

def clean_veda_text(text):
    # Aggressive ad-shield logic to keep output clean
    bad_patterns = [r"🌸.*?🌸", r"Powered by.*?AI", r"Support our mission", r"Ad", r"free text APIs", r"Support Pollinations\.AI:"]
    for pattern in bad_patterns:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE)
    return text.strip()

# --- 2. CSS STYLING ---
st.markdown("""
    <style>
    header {visibility: hidden;}
    .v-title { font-size: 50px; color: #FF8C00; text-align: center; font-weight: 900; text-transform: uppercase; margin-top: 10px;}
    .v-sub { text-align: center; color: #666; font-size: 16px; margin-top: -10px; margin-bottom: 20px; }
    .thinking-text { color: #FF8C00; font-style: italic; font-weight: bold; animation: pulse 1.5s infinite; font-size: 18px; }
    @keyframes pulse { 0%, 100% { opacity: 0.3; } 50% { opacity: 1; } }
    .nav-container { max-width: 400px; margin: 0 auto 30px auto; }
    </style>
""", unsafe_allow_html=True)

# --- 3. LOGIN PHASE ---
if st.session_state.user_name is None:
    st.markdown('<div class="v-title">VEDA 3.0 ULTRA</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        name_in = st.text_input("IDENTIFY COMMANDER:", placeholder="Name...")
        if st.button("INITIALIZE SYSTEM 🚀", use_container_width=True):
            if name_in:
                st.session_state.user_name = name_in.strip()
                st.rerun()
    st.stop()

# --- 4. MAIN INTERFACE ---
st.markdown(f'<div class="v-title">{get_greeting()}, {st.session_state.user_name.upper()}</div>', unsafe_allow_html=True)

# 🔱 PURE CHAT INTERFACE
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if prompt := st.chat_input("Command VEDA..."):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    
    with st.chat_message("assistant"):
        status = st.empty()
        final_res = ""
        status.markdown('<p class="thinking-text">🔱 thinking with veda....</p>', unsafe_allow_html=True)
        
        # --- PHASE 1: GEMINI 3.1 PRO ---
        if "GOOGLE_API_KEY" in st.secrets:
            try:
                client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
                resp = client.models.generate_content(model="gemini-3.1-pro-preview", contents=f"{IDENTITY}\n\n{prompt}")
                final_res = resp.text
            except: pass
        
        # --- PHASE 2: SILENT ROTATION TO POLLINATIONS ---
        if not final_res:
            status.markdown('<p class="thinking-text">🔱 rotating to pollination core....</p>', unsafe_allow_html=True)
            try:
                p_enc = urllib.parse.quote(prompt); i_enc = urllib.parse.quote(IDENTITY)
                r = requests.get(f"https://text.pollinations.ai/{p_enc}?model=openai&system={i_enc}", timeout=10)
                final_res = clean_veda_text(r.text)
            except: final_res = "🔱 Neural corridors congested. Please retry."

        status.empty()
        st.markdown(final_res)
        st.session_state.chat_history.append({"role": "assistant", "content": final_res})

# Sidebar reset (as a backup)
with st.sidebar:
    st.markdown("<h1 style='text-align:center;'>🔱</h1><h2 style='text-align:center; color:#FF8C00;'>VEDA 3.0 ULTRA</h2>", unsafe_allow_html=True)
    if st.button("🗑️ Reset All Data"):
        st.session_state.chat_history = []
        st.session_state.user_name = None
        st.rerun()
