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
    initial_sidebar_state="expanded" # Try to force it one last time
)

ist = pytz.timezone('Asia/Kolkata')
def get_greeting():
    hour = datetime.now(ist).hour
    if 5 <= hour < 12: return "GOOD MORNING"
    elif 12 <= hour < 17: return "GOOD AFTERNOON"
    elif 17 <= hour < 21: return "GOOD EVENING"
    else: return "GOOD NIGHT"

def clean_veda_text(text):
    # Aggressive ad-shield logic
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
    
    /* Make the option menu look elite on main screen */
    .nav-container { max-width: 600px; margin: 0 auto 30px auto; }
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

# --- 4. MAIN INTERFACE (Now with Main-Screen Navigation) ---
st.markdown(f'<div class="v-title">{get_greeting()}, {st.session_state.user_name.upper()}</div>', unsafe_allow_html=True)

# 🔱 MAIN SCREEN NAVIGATION (This replaces the Sidebar menu so it NEVER fails)
with st.container():
    st.markdown('<div class="nav-container">', unsafe_allow_html=True)
    selected = option_menu(
        None, ["Medha (Chat)", "Srijan (Image Gen)"], 
        icons=["chat-right-dots", "brush-fill"], 
        menu_icon="cast", default_index=0, orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#111", "border": "1px solid #FF8C00"},
            "nav-link": {"font-size": "16px", "text-align": "center", "margin":"0px", "--hover-color": "#FF8C0033"},
            "nav-link-selected": {"background-color": "#FF8C00"},
        }
    )
    st.markdown('</div>', unsafe_allow_html=True)

# --- 5. MODE LOGIC ---
if selected == "Medha (Chat)":
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Command VEDA..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            status = st.empty()
            final_res = ""
            status.markdown('<p class="thinking-text">🔱 thinking with veda....</p>',
