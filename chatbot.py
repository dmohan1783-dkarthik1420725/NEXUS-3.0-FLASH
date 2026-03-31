import streamlit as st
from google import genai
import requests
import urllib.parse
from datetime import datetime
import pytz
from streamlit_option_menu import option_menu
import re
import random

# --- 1. MANDATORY: PAGE CONFIG (MUST BE FIRST) ---
# This ensures the sidebar is always enabled and expanded by default
st.set_page_config(
    page_title="VEDA 3.0 ULTRA", 
    page_icon="🔱", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- 2. SOVEREIGN CONFIG & MISSION ---
CREATOR = "DUMPALA KARTHIK"
MISSION = """VEDA 3.0 ULTRA is a pinnacle of Sovereign Artificial Intelligence, engineered and brought to life through the relentless dedication and technical mastery of DUMPALA KARTHIK..."""
IDENTITY = f"Your name is VEDA 3.0 ULTRA. Created by {CREATOR}. Mission: {MISSION}"

if 'user_name' not in st.session_state: st.session_state.user_name = None
if 'chat_history' not in st.session_state: st.session_state.chat_history = []

ist = pytz.timezone('Asia/Kolkata')
def get_time_data():
    now = datetime.now(ist)
    hour = now.hour
    if 5 <= hour < 12: greet = "GOOD MORNING"
    elif 12 <= hour < 17: greet = "GOOD AFTERNOON"
    elif 17 <= hour < 21: greet = "GOOD EVENING"
    else: greet = "GOOD NIGHT"
    return greet, now.strftime("%A, %d %B"), now.strftime("%I:%M %p")

def clean_veda(text):
    if any(x in text for x in ["{", "error", "429", "Queue full", "saturation", "congested"]): return ""
    return re.sub(r"🌸.*?🌸|Powered by.*?AI|Support our mission|Ad|free text APIs", "", text, flags=re.IGNORECASE).strip()

# --- 3. ELITE CSS ---
st.markdown("""
    <style>
    header {visibility: hidden;}
    .v-title { font-size: 50px; color: #FF8C00; text-align: center; font-weight: 900; text-transform: uppercase; margin-top: 10px;}
    .nav-arrow { text-align: center; font-size: 45px; color: #FF8C00; animation: bounce 1.5s infinite; margin-top: -10px;}
    @keyframes bounce { 0%, 100% {transform: translateY(0);} 50% {transform: translateY(-10px);} }
    .thinking { color: #FF8C00; font-style: italic; font-weight: bold; font-size: 18px; animation: pulse 1s infinite; text-align: center;}
    @keyframes pulse { 0%, 100% { opacity: 0.3; } 50% { opacity: 1; } }
    </style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR DEFINITION (Before Login Stop) ---
greet, d_str, t_str = get_time_data()
with st.sidebar:
    st.markdown("<h1 style='text-align:center;'>🔱</h1><h2 style='text-align:center; color:#FF8C00;'>VEDA 3.0</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:grey;'>📅 {d_str}<br>⏰ {t_str}</p>", unsafe_allow_html=True)
    
    # Navigation Menu
    selected = option_menu(
        None, ["Medha (Chat)", "Srijan (Images)"], 
        icons=["cpu", "image"], 
        default_index=0, 
        styles={"nav-link-selected": {"background-color": "#FF8C00"}}
    )
    
    st.divider()
    if st.button("🗑️ Reset Core"):
        st.session_state.chat_history = []
        st.rerun()
    
    # Identity Verification
    if st.session_state.user_name:
        st.success(f"Commander: {st.session_state.user_name}")

# --- 5. LOGIN PHASE ---
if st.session_state.user_name is None:
    st.markdown('<div class="v-title">VEDA 3.0 ULTRA</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        name_in = st.text_input("IDENTIFY COMMANDER:", placeholder="Name...")
        if st.button("INITIALIZE 🚀", use_container_width=True):
            if name_in:
                st.session_state.user_name = name_in.strip()
                st.rerun()
    st.stop()

# --- 6. MAIN INTERFACE ---
st.markdown(f'<div class="v-title">{greet}, {st.session_state.user_name.upper()}</div>', unsafe_allow_html=True)
st.markdown('<div class="nav-arrow">▼</div>', unsafe_allow_html=True)

if selected == "Medha (Chat)":
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Command VEDA..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt
