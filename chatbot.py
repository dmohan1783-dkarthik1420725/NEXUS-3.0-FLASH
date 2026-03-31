import streamlit as st
from google.genai import Client
try:
    from duckduckgo_search import DDGS
except ImportError:
    from ddgs import DDGS
import requests
import urllib.parse
from datetime import datetime
import pytz
import os
import random

# --- 1. SOVEREIGN IDENTITY ---
st.set_page_config(page_title="VEDA 3.0 ULTRA", page_icon="🔱", layout="wide")
CREATOR = "DUMPALA KARTHIK"
MISSION = "VEDA 3.0 ULTRA: A pinnacle of Sovereign AI engineered by DUMPALA KARTHIK."

# --- 2. SATELLITE HARVESTER ---
def satellite_harvest(query):
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
            if not results: return None
            data = ""
            for r in results:
                data += f"TITLE: {r.get('title')}\nDATA: {r.get('body')}\n\n"
            return data
    except:
        return None

# --- 3. SESSION & UI ---
if "commander_name" not in st.session_state: st.session_state.commander_name = None
if 'chat_history' not in st.session_state: st.session_state.chat_history = []

st.markdown("""
    <style>
    header {visibility: hidden;}
    body { background-color: #000; color: #eee; }
    .v-title { font-size: 40px; color: #FF8C00; font-weight: 900; text-transform: uppercase; }
    [data-testid="stChatMessage"] { background-color: transparent !important; border: none !important; margin-bottom: 25px; }
    [data-testid="stChatMessageContent"] { border-left: 3px solid #FF8C00; padding-left: 20px !important; font-size: 18px; }
    .label { color: #FF8C00; font-weight: bold; font-size: 12px; margin-bottom: 5px; }
    </style>
""", unsafe_allow_html=True)

# --- 4. AUTHORIZATION ---
if st.session_state.commander_name is None:
    st.markdown('<div class="v-title">🔱 VEDA 3.0 ULTRA</div>', unsafe_allow_html=True)
    name = st.text_input("IDENTIFY YOURSELF:", placeholder="Enter your name...")
    if st.button("AUTHORIZE"):
        if name:
            st.session_state.commander_name = name.upper()
            st.rerun()
    st.stop()

# --- 5. DASHBOARD ---
ist = pytz.timezone('Asia/Kolkata')
time_str = datetime.now(ist).strftime("%I:%M %p")
st.markdown(f'<div class="v-title">COMMANDER {st.session_state.commander_name}</div>', unsafe_allow_html=True)
st.markdown(f'<p style="color:gray;">SATELLITE SYNC: ACTIVE | {time_str} IST</p>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<h2 style='color:#FF8C00;'>🔱 VEDA 3.0</h2>", unsafe_allow_html=True)
    selected = st.radio("MODULES:", ["Medha (Chat)", "Srijan (Images)"])
    if st.button("🔴 TERMINATE"):
        st.session_state.commander_name = None
        st.rerun()

# --- 6. CORE LOGIC (MEDHA) ---
if selected == "Medha (Chat)":
    for msg in st.session_state.chat_history:
        lbl = "👤 USER" if msg["role"] == "user" else "🔱 VEDA 3.0"
        with st.chat_message(msg["role"]):
            st.markdown(f'<div class="label">{lbl}</div>', unsafe_allow_html=True)
            st.markdown(msg["content"])

    if prompt := st.chat_input("Enter Command..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        st.rerun()

    if st.session_state.chat_history and st.session_state.chat_history[-1]["role"] == "user":
        with st.chat_message("assistant"):
            current_prompt = st.session_state.chat_history[-1]["content"]
            final_res = ""
            
            # IDENTITY CHECK
            if any(x in current_prompt.lower() for x in ["who made you", "creator", "karthik"]):
                final_res = MISSION
            
            # BRAIN 1: GOOGLE GENAI
            if not final_res:
                try:
                    client = Client(api_key=st.secrets["GOOGLE_API_KEY"])
                    resp = client.models.generate_content(model="gemini-2.0-flash", contents=f"User: {current_prompt}. You are VEDA 3.0 ULTRA.")
                    if resp.text: final_res = resp.text
                except: pass
            
            # BRAIN 2: FAILOVER MESH (POLLINATIONS)
            if not final_res:
                try:
                    p_enc = urllib.parse.quote(current_prompt)
                    r = requests.get(f"https://text.pollinations.ai/{p_enc}?system=VEDA-3.0-ULTRA", timeout=10)
                    if r.text: final_res = r.text
                except: pass
            
            # BRAIN 3: SATELLITE SEARCH
            if not final_res:
                search_data = satellite_harvest(current_prompt)
                if search_data:
                    final_res = f"📡 SATELLITE DATA RECOVERED:\n\n{search_data}"
            
            # FINAL PROTOCOL: REJECTION
            if not final_res:
                final_res = "Sorry, I can't help you with that."

            st.markdown(f'<div class="label">🔱 VEDA 3.0</div>', unsafe_allow_html=True)
            st.markdown(final_res)
            st.session_state.chat_history.append({"role": "assistant", "content": final_res})

# --- 7. SRIJAN (IMAGES) ---
else:
    st.markdown("<h3 style='color:#FF8C00;'>SRIJAN VISUALIZER</h3>", unsafe_allow_html=True)
    vision = st.text_input("Vision Matrix Prompt:")
    if st.button("🚀 INITIATE"):
        if vision:
            v_enc = urllib.parse.quote(vision)
            img_url = f"https://image.pollinations.ai/prompt/{v_enc}?width=1024&height=1024&nologo=true&model=flux&seed={random.randint(1,999)}"
            st.image(img_url, use_container_width=True)
