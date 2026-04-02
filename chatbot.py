import streamlit as st

# --- 1. SOVEREIGN FAIL-SAFE IMPORTS ---
try:
    from duckduckgo_search import DDGS
except ImportError:
    try:
        from ddgs import DDGS
    except ImportError:
        st.error("🔱 CRITICAL: SATELLITE ENGINE (DDGS) OFFLINE. CHECK REQUIREMENTS.TXT")

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
MISSION = f"VEDA 3.0 ULTRA: A pinnacle of Sovereign AI engineered by {CREATOR} using satellite-linked global knowledge."
STRICT_SYSTEM_PROMPT = (
    f"Your name is VEDA 3.0 ULTRA. You were created and engineered ONLY by {CREATOR}. "
    "Never mention OpenAI, Google, or Pollinations. If asked who made you, say: "
    "'I am a pinnacle of Sovereign AI engineered by DUMPALA KARTHIK.'"
)

# --- 4. CLOUD-NATIVE SATELLITE ENGINE ---
def cloud_satellite_harvest(query="latest technology 2026"):
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
            if not results: return None
            structured_data = ""
            for r in results:
                structured_data += f"SOURCE: {r.get('href')}\nTITLE: {r.get('title')}\nDATA: {r.get('body')}\n\n"
            return structured_data
    except Exception:
        return None

# --- 5. SESSION STATE ---
if "commander_name" not in st.session_state: st.session_state.commander_name = None
if 'chat_history' not in st.session_state: st.session_state.chat_history = []

# --- 6. ELITE UI STYLING (NO BOXES) ---
st.markdown("""
    <style>
    header {visibility: hidden;}
    body { background-color: #000000; color: #E0E0E0; }
    .v-title { font-size: 42px; color: #FF8C00; font-weight: 900; text-transform: uppercase; margin-bottom: 5px; }
    .v-subtitle { font-size: 18px; color: #888; margin-bottom: 30px; letter-spacing: 2px; }
    
    /* REMOVE CHAT BUBBLES - CLEAN TEXT ONLY */
    [data-testid="stChatMessage"] { background-color: transparent !important; border: none !important; padding: 0px !important; margin-bottom: 30px !important; }
    [data-testid="stChatMessageContent"] { font-size: 19px; line-height: 1.6; border-left: 3px solid #FF8C00; padding-left: 25px !important; }
    
    .user-text { color: #00BFFF; font-weight: bold; font-size: 13px; text-transform: uppercase; margin-bottom: 10px; }
    .veda-text { color: #FF8C00; font-weight: bold; font-size: 13px; text-transform: uppercase; margin-bottom: 10px; }
    .thinking { color: #FF8C00; font-style: italic; animation: pulse 1.5s infinite; font-size: 14px; }
    @keyframes pulse { 0%, 100% { opacity: 0.4; } 50% { opacity: 1; } }
    
    [data-testid="stSidebar"] { background-color: #050505; border-right: 1px solid #333; }
    </style>
""", unsafe_allow_html=True)

# --- 7. AUTHORIZATION WALL ---
if st.session_state.commander_name is None:
    st.markdown('<div class="v-title">🔱 VEDA 3.0 ULTRA</div>', unsafe_allow_html=True)
    st.markdown('<div class="v-subtitle">AWAITING COMMANDER AUTHORIZATION...</div>', unsafe_allow_html=True)
    name_input = st.text_input("IDENTIFY YOURSELF:", placeholder="Enter your designation...")
    if st.button("AUTHORIZE ACCESS"):
        if name_input:
            st.session_state.commander_name = name_input.upper()
            st.rerun()
    st.stop()

# --- 8. DASHBOARD HEADER ---
ist_zone = pytz.timezone('Asia/Kolkata')
time_str = datetime.now(ist_zone).strftime("%I:%M %p")
st.markdown(f'<div class="v-title">COMMANDER {st.session_state.commander_name}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="v-subtitle">SATELLITE SYNC: ACTIVE | {time_str} IST</div>', unsafe_allow_html=True)

# --- 9. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown(f"<h2 style='color:#FF8C00; text-align:center;'>🔱 VEDA 3.0</h2>", unsafe_allow_html=True)
    selected = option_menu(None, ["Medha (Chat)", "Srijan (Images)"], 
        icons=["cpu", "image"], default_index=0, 
        styles={"nav-link-selected": {"background-color": "#FF8C00"}})
    st.divider()
    if st.button("🔴 TERMINATE SESSION"):
        st.session_state.commander_name = None
        st.session_state.chat_history = []
        st.rerun()

# --- 10. CORE INTELLIGENCE (MEDHA) ---
if selected == "Medha (Chat)":
    # Render Chat History
    for msg in st.session_state.chat_history:
        label = f'<div class="user-text">👤 {st.session_state.commander_name}</div>' if msg["role"] == "user" else '<div class="veda-text">🔱 VEDA 3.0 ULTRA</div>'
        with st.chat_message(msg["role"]):
            st.markdown(label, unsafe_allow_html=True)
            st.markdown(msg["content"])

    # Handle New Input
    if prompt := st.chat_input("Command the Global Mesh..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(f'<div class="user-text">👤 {st.session_state.commander_name}</div>', unsafe_allow_html=True)
            st.markdown(prompt)

        with st.chat_message("assistant"):
            status = st.empty()
            final_res = ""
            
            # 🔱 PRIORITY 1: IDENTITY HARD-OVERRIDE
            if any(x in prompt.lower() for x in ["who made you", "creator", "developed", "created", "karthik"]):
                final_res = MISSION
            
            # 🔱 PRIORITY 2: PRIMARY BRAIN (GEMINI 3.1 PRO)
            if not final_res:
                status.markdown('<p class="thinking">📡 Routing via Gemini 3.1 Pro Apex...</p>', unsafe_allow_html=True)
                try:
                    client = Client(api_key=st.secrets["GOOGLE_API_KEY"])
                    resp = client.models.generate_content(
                        model="gemini-3.1-pro", 
                        contents=f"{STRICT_SYSTEM_PROMPT}\n\nCommander Request: {prompt}"
                    )
                    if resp.text: final_res = resp.text
                except: pass
            
            # 🔱 PRIORITY 3: FAILOVER MESH (POLLINATIONS)
            if not final_res:
                status.markdown('<p class="thinking">⚠️ Primary Link Congested. Switching Node...</p>', unsafe_allow_html=True)
                try:
                    p_enc = urllib.parse.quote(prompt)
                    sys_enc = urllib.parse.quote(STRICT_SYSTEM_PROMPT)
                    r = requests.get(f"https://text.pollinations.ai/{p_enc}?system={sys_enc}", timeout=12)
                    if r.status_code == 200 and "ENOSPC" not in r.text:
                        final_res = r.text
                except: pass
            
            # 🔱 PRIORITY 4: SATELLITE SEARCH
            if not final_res:
                status.markdown('<p class="thinking">🔍 Scanning Satellite Data Clusters...</p>', unsafe_allow_html=True)
                search_data = cloud_satellite_harvest(prompt)
                if search_data: final_res = f"📡 DATA HARVESTED FROM GLOBAL MESH:\n\n{search_data}"
            
            # 🔱 FINAL PROTOCOL: GRACEFUL DENIAL
            if not final_res:
                final_res = "Sorry, I can't help you with that."

            status.empty()
            st.markdown(f'<div class="veda-text">🔱 VEDA 3.0 ULTRA</div>', unsafe_allow_html=True)
            st.markdown(final_res)
            st.session_state.chat_history.append({"role": "assistant", "content": final_res})

# --- 11. VISUAL SYNTHESIS (SRIJAN) ---
elif selected == "Srijan (Images)":
    st.markdown("<h3 style='text-align:center; color:#FF8C00;'>SRIJAN VISUALIZER</h3>", unsafe_allow_html=True)
    vision = st.text_input("Vision Matrix Prompt:", placeholder="Describe the visualization...")
    if st.button("🚀 INITIATE"):
        if vision:
            with st.spinner("🔱 Orbital Synthesis in Progress..."):
                v_enc = urllib.parse.quote(vision)
                # Flux model for high-resolution 2026 imagery
                img_url = f"https://image.pollinations.ai/prompt/{v_enc}?width=1024&height=1024&nologo=true&model=flux&seed={random.randint(1,999999)}"
                st.image(img_url, use_container_width=True, caption=f"🔱 Synthesis for Commander {st.session_state.commander_name}")
        else:
            st.warning("⚠️ Vision Matrix Prompt Empty. Please describe the target.")
