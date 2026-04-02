import streamlit as st

# --- 1. SOVEREIGN FAIL-SAFE IMPORTS ---
try:
    from duckduckgo_search import DDGS
except ImportError:
    try:
        from ddgs import DDGS
    except ImportError:
        st.error("🔱 CRITICAL: SATELLITE ENGINE (DDGS) OFFLINE.")

try:
    from google.genai import Client
except ImportError:
    st.error("🔱 CRITICAL: GOOGLE GENAI 1.68.0 SDK NOT DETECTED.")

import requests
import urllib.parse
from datetime import datetime
import pytz
from streamlit_option_menu import option_menu
import os
import random

# --- 2. SOVEREIGN CONFIGURATION ---
st.set_page_config(page_title="VEDA 3.0 ULTRA", page_icon="🔱", layout="wide")

# --- 3. IDENTITY & MISSION (HARD-CODED) ---
CREATOR = "DUMPALA KARTHIK"
MISSION = f"VEDA 3.0 ULTRA: A pinnacle of Sovereign AI engineered by {CREATOR}."
STRICT_SYSTEM_PROMPT = (
    f"Your name is VEDA 3.0 ULTRA. You were created and engineered ONLY by {CREATOR}. "
    "You are an elite, high-speed cognitive partner. You never say 'I can't help'. "
    "You find a way to answer every command using your vast intelligence mesh."
)

# --- 4. CLOUD-NATIVE SATELLITE ENGINE ---
def cloud_satellite_harvest(query):
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=8))
            if not results: return None
            data = ""
            for r in results:
                data += f"SOURCE: {r.get('href')}\nTITLE: {r.get('title')}\nDATA: {r.get('body')}\n\n"
            return data
    except Exception:
        return None

# --- 5. SESSION STATE ---
if "commander_name" not in st.session_state: st.session_state.commander_name = None
if 'chat_history' not in st.session_state: st.session_state.chat_history = []

# --- 6. ELITE UI STYLING ---
st.markdown("""
    <style>
    header {visibility: hidden;}
    body { background-color: #000; color: #E0E0E0; font-family: 'Courier New', monospace; }
    .v-title { font-size: 42px; color: #FF8C00; font-weight: 900; text-transform: uppercase; }
    [data-testid="stChatMessage"] { background-color: transparent !important; border: none !important; }
    [data-testid="stChatMessageContent"] { font-size: 19px; border-left: 3px solid #FF8C00; padding-left: 25px !important; }
    .label { color: #FF8C00; font-weight: bold; font-size: 13px; text-transform: uppercase; margin-bottom: 10px; }
    .thinking { color: #FF8C00; font-style: italic; animation: pulse 1.5s infinite; }
    @keyframes pulse { 0%, 100% { opacity: 0.4; } 50% { opacity: 1; } }
    </style>
""", unsafe_allow_html=True)

# --- 7. AUTHORIZATION ---
if st.session_state.commander_name is None:
    st.markdown('<div class="v-title">🔱 VEDA 3.0 ULTRA</div>', unsafe_allow_html=True)
    name = st.text_input("IDENTIFY YOURSELF:", placeholder="Enter name...")
    if st.button("AUTHORIZE"):
        if name:
            st.session_state.commander_name = name.upper()
            st.rerun()
    st.stop()

# --- 8. HEADER ---
ist = pytz.timezone('Asia/Kolkata')
time_str = datetime.now(ist).strftime("%I:%M %p")
st.markdown(f'<div class="v-title">COMMANDER {st.session_state.commander_name}</div>', unsafe_allow_html=True)
st.markdown(f'<p style="color:gray;">SATELLITE SYNC: ACTIVE | {time_str} IST</p>', unsafe_allow_html=True)

# --- 9. SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color:#FF8C00;'>🔱 VEDA 3.0</h2>", unsafe_allow_html=True)
    selected = option_menu(None, ["Medha (Chat)", "Srijan (Images)"], icons=["cpu", "image"], default_index=0)
    if st.button("🔴 TERMINATE"):
        st.session_state.commander_name = None
        st.rerun()

# --- 10. CHAT (MEDHA) ---
if selected == "Medha (Chat)":
    for msg in st.session_state.chat_history:
        lbl = f"👤 {st.session_state.commander_name}" if msg["role"] == "user" else "🔱 VEDA 3.0 ULTRA"
        with st.chat_message(msg["role"]):
            st.markdown(f'<div class="label">{lbl}</div>', unsafe_allow_html=True)
            st.markdown(msg["content"])

    if prompt := st.chat_input("Input Command..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(f'<div class="label">👤 {st.session_state.commander_name}</div>', unsafe_allow_html=True)
            st.markdown(prompt)

        with st.chat_message("assistant"):
            status = st.empty()
            final_res = ""
            
            # IDENTITY BYPASS
            if any(x in prompt.lower() for x in ["who made you", "creator", "karthik"]):
                final_res = MISSION

            # BRAIN 1: GEMINI 3.1 PRO (PRIMARY)
            if not final_res:
                status.markdown('<p class="thinking">📡 Uplinking to Gemini 3.1 Pro...</p>', unsafe_allow_html=True)
                try:
                    client = Client(api_key=st.secrets["GOOGLE_API_KEY"])
                    resp = client.models.generate_content(
                        model="gemini-3.1-pro-preview",
                        config={'thinking_level': 'high'},
                        contents=f"{STRICT_SYSTEM_PROMPT}\n\nCommand: {prompt}"
                    )
                    if resp.text: final_res = resp.text
                except: pass

            # BRAIN 2:
