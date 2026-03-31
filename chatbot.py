import streamlit as st
from google.genai import Client
from ddgs import DDGS
import requests
import urllib.parse
from datetime import datetime
import pytz
from streamlit_option_menu import option_menu
import os
import random

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="VEDA 3.0 ULTRA", page_icon="🔱", layout="wide")

# --- 2. IDENTITY & MISSION ---
CREATOR = "DUMPALA KARTHIK"
MISSION = "VEDA 3.0 ULTRA: A pinnacle of Sovereign AI engineered by DUMPALA KARTHIK using satellite-linked global knowledge."

# --- 3. CLOUD SATELLITE ENGINE ---
def cloud_satellite_harvest(query="latest technology 2026"):
    """Automatically harvests real-time data from the web mesh"""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
            if not results:
                return "⚠️ Satellite Node Silent. No data returned."
            structured_data = ""
            for r in results:
                structured_data += f"SOURCE: {r.get('href', 'N/A')}\n"
                structured_data += f"TITLE: {r.get('title', 'N/A')}\n"
                structured_data += f"DATA: {r.get('body', 'N/A')}\n\n"
            return structured_data
    except Exception as e:
        return f"📡 Satellite Uplink Failure: {e}"

# --- 4. THE COMMANDER'S NAME LOGIC ---
if "commander_name" not in st.session_state:
    st.session_state.commander_name = None

# --- 5. ELITE UI STYLING (NO BOXES) ---
st.markdown("""
    <style>
    header {visibility: hidden;}
    body { background-color: #000000; color: #E0E0E0; }
    .v-title { font-size: 40px; color: #FF8C00; font-weight: 900; text-transform: uppercase; margin-bottom: 5px; }
    .v-subtitle { font-size: 18px; color: #888; margin-bottom: 25px; }
    
    /* ELITE TEXT STYLING (REMOVES CHAT BUBBLES) */
    [data-testid="stChatMessage"] { background-color: transparent !important; border: none !important; padding: 0px !important; margin-bottom: 25px !important; }
    [data-testid="stChatMessageContent"] { font-size: 18px; line-height: 1.6; border-left: 3px solid #FF8C00; padding-left: 20px !important; }
    
    .user-text { color: #00BFFF; font-weight: bold; font-size: 14px; text-transform: uppercase; margin-bottom: 8px; letter-spacing: 1px; }
    .veda-text { color: #FF8C00; font-weight: bold; font-size: 14px; text-transform: uppercase; margin-bottom: 8px; letter-spacing: 1px; }
    
    [data-testid="stSidebar"] { background-color: #050505; border-right: 1px solid #333; }
    .thinking { color: #FF8C00; font-style: italic; animation: pulse 1.5s infinite; }
    @keyframes pulse { 0%, 100% { opacity: 0.5; } 50% { opacity: 1; } }
    </style>
""", unsafe_allow_html=True)

# --- 6. TIME & GREETING ENGINE ---
def get_dynamic_greeting():
    ist_zone = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist_zone)
    hour = now.hour
    if 5 <= hour < 12: greet = "GOOD MORNING"
    elif 12 <= hour < 17: greet = "GOOD AFTERNOON"
    elif 17 <= hour < 21: greet = "GOOD EVENING"
    else: greet = "GOOD NIGHT"
    return greet, now.strftime("%I:%M %p")

# --- 7. AUTHORIZATION WALL ---
if st.session_state.commander_name is None:
    st.markdown('<div class="v-title">🔱 VEDA 3.0 ULTRA</div>', unsafe_allow_html=True)
    st.markdown('<div class="v-subtitle">WAITING FOR COMMANDER IDENTIFICATION...</div>', unsafe_allow_html=True)
    name_input = st.text_input("IDENTIFY YOURSELF:", placeholder="Enter your name...")
    if st.button("AUTHORIZE UPLINK"):
        if name_input:
            st.session_state.commander_name = name_input.upper()
            st.rerun()
    st.stop()

# --- 8. DASHBOARD HEADER ---
greet, time_str = get_dynamic_greeting()
st.markdown(f'<div class="v-title">{greet}, {st.session_state.commander_name}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="v-subtitle">SATELLITE SYNC: ACTIVE | {time_str} IST</div>', unsafe_allow_html=True)

# --- 9. SIDEBAR OPERATIONS ---
with st.sidebar:
    st.markdown(f"<h2 style='color:#FF8C00; text-align:center;'>🔱 VEDA 3.0</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:gray;'>LOGGED AS: {st.session_state.commander_name}</p>", unsafe_allow_html=True)
    
    selected = option_menu(None, ["Medha (Chat)", "Srijan (Images)"], 
        icons=["cpu", "image"], default_index=0, 
        styles={"nav-link-selected": {"background-color": "#FF8C00"}})
    
    st.divider()
    if st.button("🔴 TERMINATE SESSION"):
        st.session_state.commander_name = None
        st.session_state.chat_history = []
        st.rerun()

# --- 10. CORE INTELLIGENCE (MEDHA) ---
if 'chat_history' not in st.session_state: st.session_state.chat_history = []

if selected == "Medha (Chat)":
    for msg in st.session_state.chat_history:
        label = f'<div class="user-text">👤 COMMANDER {st.session_state.commander_name}</div>' if msg["role"] == "user" else '<div class="veda-text">🔱 VEDA 3.0 ULTRA</div>'
        with st.chat_message(msg["role"]):
            st.markdown(label, unsafe_allow_html=True)
            st.markdown(msg["content"])

    if prompt := st.chat_input("Input Command to the Mesh..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(f'<div class="user-text">👤 COMMANDER {st.session_state.commander_name}</div>', unsafe_allow_html=True)
            st.markdown(prompt)

        with st.chat_message("assistant"):
            status = st.empty()
            final_res = ""
            
            if any(x in prompt.lower() for x in ["who made you", "creator", "karthik", "purpose"]):
                final_res = MISSION
            
            if not final_res:
                status.markdown('<p class="thinking">📡 Accessing Global Satellite Mesh...</p>', unsafe_allow_html=True)
                world_knowledge = cloud_satellite_harvest(prompt)
                identity_context = f"You are VEDA 3.0 ULTRA, created by {CREATOR}. Address the user as Commander {st.session_state.commander_name}."
                
                try:
                    client = Client(api_key=st.secrets["GOOGLE_API_KEY"])
                    resp = client.models.generate_content(model="gemini-2.0-flash", contents=f"{identity_context}\n\nSATELLITE DATA:\n{world_knowledge}\n\nUSER REQUEST: {prompt}")
                    if resp.text: final_res = resp.text
                except:
                    try:
                        p_enc = urllib.parse.quote(prompt)
                        url = f"https://text.pollinations.ai/{p_enc}?model=openai&system={urllib.parse.quote(identity_context)}"
                        r = requests.get(url, timeout=15)
                        final_res = r.text
                    except:
                        final_res = "🔱 Satellite connection lost. Mesh reset required."

            status.empty()
            st.markdown(f'<div class="veda-text">🔱 VEDA 3.0 ULTRA</div>', unsafe_allow_html=True)
            st.markdown(final_res)
            st.session_state.chat_history.append({"role": "assistant", "content": final_res})

# --- 11. VISUAL SYNTHESIS (SRIJAN) ---
elif selected == "Srijan (Images)":
    st.markdown("<h3 style='text-align:center; color:#FF8C00;'>SRIJAN VISUALIZER</h3>", unsafe_allow_html=True)
    vision = st.text_input("Vision Matrix Prompt:", placeholder="Describe the visualization...")
    if st.button("🚀 INITIATE VISUALIZATION"):
        if vision:
            with st.spinner("🔱 Orbital Synthesis..."):
                v_enc = urllib.parse.quote(vision)
                img_url = f"https://image.pollinations.ai/prompt/{v_enc}?width=1024&height=1024&nologo=true&model=flux&seed={random.randint(1,1000)}"
                st.image(img_url, use_container_width=True, caption=f"🔱 Synthesis for {st.session_state.commander_name}")
