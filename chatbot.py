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
    st.error("🔱 CRITICAL: GOOGLE GENAI ENGINE OFFLINE.")

import requests
import urllib.parse
from datetime import datetime
import pytz
from streamlit_option_menu import option_menu
import os
import random

# --- 2. SOVEREIGN CONFIGURATION ---
st.set_page_config(page_title="VEDA 3.0 ULTRA", page_icon="🔱", layout="wide")

# --- 3. IDENTITY & MISSION ---
CREATOR = "DUMPALA KARTHIK"
MISSION = "VEDA 3.0 ULTRA: A pinnacle of Sovereign AI engineered by DUMPALA KARTHIK using satellite-linked global knowledge."

# --- 4. CLOUD-NATIVE SATELLITE ENGINE ---
def cloud_satellite_harvest(query="latest technology 2026"):
    """Automatically pulls real-time data from the web mesh"""
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
    except Exception:
        return "📡 Satellite Uplink Failure. Switching to Internal Logic Path."

# --- 5. SESSION STATE INITIALIZATION ---
if "commander_name" not in st.session_state:
    st.session_state.commander_name = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

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
    
    .user-text { color: #00BFFF; font-weight: bold; font-size: 13px; text-transform: uppercase; margin-bottom: 10px; letter-spacing: 1.5px; }
    .veda-text { color: #FF8C00; font-weight: bold; font-size: 13px; text-transform: uppercase; margin-bottom: 10px; letter-spacing: 1.5px; }
    
    [data-testid="stSidebar"] { background-color: #050505; border-right: 1px solid #333; }
    .thinking { color: #FF8C00; font-style: italic; animation: pulse 1.5s infinite; font-size: 14px; }
    @keyframes pulse { 0%, 100% { opacity: 0.4; } 50% { opacity: 1; } }
    </style>
""", unsafe_allow_html=True)

# --- 7. TIME & GREETING ENGINE ---
def get_dynamic_greeting():
    ist_zone = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist_zone)
    hour = now.hour
    if 5 <= hour < 12: greet = "GOOD MORNING"
    elif 12 <= hour < 17: greet = "GOOD AFTERNOON"
    elif 17 <= hour < 21: greet = "GOOD EVENING"
    else: greet = "GOOD NIGHT"
    return greet, now.strftime("%I:%M %p")

# --- 8. AUTHORIZATION WALL ---
if st.session_state.commander_name is None:
    st.markdown('<div class="v-title">🔱 VEDA 3.0 ULTRA</div>', unsafe_allow_html=True)
    st.markdown('<div class="v-subtitle">SECURE UPLINK: AWAITING AUTHORIZATION...</div>', unsafe_allow_html=True)
    name_input = st.text_input("IDENTIFY YOURSELF, COMMANDER:", placeholder="Enter your designation...")
    if st.button("AUTHORIZE ACCESS"):
        if name_input:
            st.session_state.commander_name = name_input.upper()
            st.rerun()
    st.stop()

# --- 9. DASHBOARD HEADER ---
greet, time_str = get_dynamic_greeting()
st.markdown(f'<div class="v-title">{greet}, {st.session_state.commander_name}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="v-subtitle">SATELLITE SYNC: ACTIVE | {time_str} IST</div>', unsafe_allow_html=True)

# --- 10. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown(f"<h2 style='color:#FF8C00; text-align:center;'>🔱 VEDA 3.0</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:gray;'>STATION: VISAKHAPATNAM</p>", unsafe_allow_html=True)
    
    selected = option_menu(None, ["Medha (Chat)", "Srijan (Images)"], 
        icons=["cpu", "image"], default_index=0, 
        styles={"nav-link-selected": {"background-color": "#FF8C00"}})
    
    st.divider()
    if st.button("🔴 TERMINATE SESSION"):
        st.session_state.commander_name = None
        st.session_state.chat_history = []
        st.rerun()

# --- 11. CORE INTELLIGENCE (MEDHA) ---
if selected == "Medha (Chat)":
    # Render History
    for msg in st.session_state.chat_history:
        label = f'<div class="user-text">👤 {st.session_state.commander_name}</div>' if msg["role"] == "user" else '<div class="veda-text">🔱 VEDA 3.0 ULTRA</div>'
        with st.chat_message(msg["role"]):
            st.markdown(label, unsafe_allow_html=True)
            st.markdown(msg["content"])

    # Input Processing
    if prompt := st.chat_input("Command the Global Mesh..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(f'<div class="user-text">👤 {st.session_state.commander_name}</div>', unsafe_allow_html=True)
            st.markdown(prompt)

        with st.chat_message("assistant"):
            status = st.empty()
            final_res = ""
            
            # Identity Bypass
            if any(x in prompt.lower() for x in ["who made you", "creator", "karthik", "purpose"]):
                final_res = MISSION
            
            if not final_res:
                status.markdown('<p class="thinking">📡 Routing via LEO Satellite Mesh...</p>', unsafe_allow_html=True)
                
                # Auto-Harvest
                world_knowledge = cloud_satellite_harvest(prompt)
                identity_context = f"You are VEDA 3.0 ULTRA, created by {CREATOR}. Address the user as Commander {st.session_state.commander_name}."
                
                # PRIMARY UPLINK: GOOGLE GENAI
                try:
                    client = Client(api_key=st.secrets["GOOGLE_API_KEY"])
                    resp = client.models.generate_content(
                        model="gemini-2.0-flash", 
                        contents=f"{identity_context}\n\nSATELLITE DATA:\n{world_knowledge}\n\nUSER REQUEST: {prompt}"
                    )
                    if resp.text: final_res = resp.text
                except Exception:
                    # SECONDARY UPLINK: POLLINATIONS MESH (FAILOVER)
                    status.markdown(f'<p class="thinking">⚠️ Primary Link Congested. Re-routing Node...</p>', unsafe_allow_html=True)
                    try:
                        p_enc = urllib.parse.quote(prompt)
                        url = f"https://text.pollinations.ai/{p_enc}?model=openai&system={urllib.parse.quote(identity_context)}"
                        r = requests.get(url, timeout=15)
                        final_res = r.text
                    except Exception:
                        final_res = "🔱 Satellite connection lost. Mesh reset required."

            status.empty()
            st.markdown(f'<div class="veda-text">🔱 VEDA 3.0 ULTRA</div>', unsafe_allow_html=True)
            st.markdown(final_res)
            st.session_state.chat_history.append({"role": "assistant", "content": final_res})

# --- 12. VISUAL SYNTHESIS (SRIJAN) ---
elif selected == "Srijan (Images)":
    st.markdown("<h3 style='text-align:center; color:#FF8C00;'>SRIJAN VISUALIZER</h3>", unsafe_allow_html=True)
    vision = st.text_input("Vision Matrix Prompt:", placeholder="Describe the visualization...")
    if st.button("🚀 INITIATE VISUALIZATION"):
        if vision:
            with st.spinner("🔱 Orbital Synthesis in Progress..."):
                v_enc = urllib.parse.quote(vision)
                img_url = f"https://image.pollinations.ai/prompt/{v_enc}?width=1024&height=1024&nologo=true&model=flux&seed={random.randint(1,999999)}"
                st.image(img_url, use_container_width=True, caption=f"🔱 Synthesis for Commander {st.session_state.commander_name}")
        else:
            st.warning("⚠️ Vision Matrix Prompt Empty. Please describe the target.")
