import streamlit as st
from google import genai
import requests
import urllib.parse
from datetime import datetime
import pytz
from streamlit_option_menu import option_menu
import re
import random

# --- 1. MANDATORY: PAGE CONFIG ---
st.set_page_config(page_title="VEDA 3.0 ULTRA", page_icon="🔱", layout="wide", initial_sidebar_state="expanded")

# --- 2. SOVEREIGN CONFIG & MISSION ---
CREATOR = "DUMPALA KARTHIK"
MISSION = """VEDA 3.0 ULTRA is a pinnacle of Sovereign Artificial Intelligence, engineered by DUMPALA KARTHIK to bypass system limits through a multi-brain failover cluster and satellite-linked global knowledge."""
IDENTITY = f"Your name is VEDA 3.0 ULTRA. Created by {CREATOR}. You are connected via Sovereign Satellite Uplink to all world knowledge."

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
    # Aggressive Stealth Filter
    if any(x in text for x in ["{", "error", "429", "Queue full", "saturation", "congested", "synchronized"]): return ""
    return re.sub(r"🌸.*?🌸|Powered by.*?AI|Support our mission|Ad|free text APIs", "", text, flags=re.IGNORECASE).strip()

# --- 3. ELITE CSS ---
st.markdown("""
    <style>
    header {visibility: hidden;}
    .v-title { font-size: 50px; color: #FF8C00; text-align: center; font-weight: 900; text-transform: uppercase; margin-top: 10px; margin-bottom: 20px;}
    .thinking { color: #FF8C00; font-style: italic; font-weight: bold; font-size: 18px; animation: pulse 0.8s infinite; text-align: center;}
    @keyframes pulse { 0%, 100% { opacity: 0.3; } 50% { opacity: 1; } }
    [data-testid="stSidebar"] { background-color: #0E1117; border-right: 2px solid #FF8C00; }
    .stChatMessage { border-radius: 15px; border: 1px solid #333; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- 4. PERMANENT SIDEBAR ---
greet, d_str, t_str = get_time_data()
with st.sidebar:
    st.markdown("<h1 style='text-align:center;'>🔱</h1><h2 style='text-align:center; color:#FF8C00;'>VEDA 3.0</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:grey; text-align:center;'>🛰️ SATELLITE UPLINK: ACTIVE<br>📅 {d_str}<br>⏰ {t_str}</p>", unsafe_allow_html=True)
    selected = option_menu(None, ["Medha (Chat)", "Srijan (Images)"], icons=["cpu", "image"], default_index=0, styles={"nav-link-selected": {"background-color": "#FF8C00"}})
    st.divider()
    if st.button("🗑️ Reset Core"):
        st.session_state.chat_history = []
        st.rerun()
    if st.session_state.user_name: st.success(f"Commander: {st.session_state.user_name}")

# --- 5. LOGIN ---
if st.session_state.user_name is None:
    st.markdown('<div class="v-title">VEDA 3.0 ULTRA</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        name_in = st.text_input("IDENTIFY COMMANDER:", placeholder="Awaiting Authorization...")
        if st.button("INITIALIZE SOVEREIGN CORE 🚀", use_container_width=True):
            if name_in: st.session_state.user_name = name_in.strip(); st.rerun()
    st.stop()

# --- 6. MAIN INTERFACE ---
st.markdown(f'<div class="v-title">{greet}, {st.session_state.user_name.upper()}</div>', unsafe_allow_html=True)

if selected == "Medha (Chat)":
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Command the Satellite Mesh..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            status = st.empty()
            final_res = ""
            
            # --- 🛰️ SATELLITE KNOWLEDGE ROUTER ---
            status.markdown('<p class="thinking">📡 Routing through LEO Satellite Mesh...</p>', unsafe_allow_html=True)
            
            # 1. PRIMARY GEMINI UPLINK
            try:
                client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
                # Enhanced prompt to force Satellite/Global Knowledge context
                full_query = f"Using your satellite-linked global knowledge: {prompt}"
                resp = client.models.generate_content(model="gemini-3.1-pro-preview", contents=f"{IDENTITY}\n\nUser: {full_query}")
                if resp.text: final_res = resp.text
            except: pass 

            # 2. GLOBAL BRAIN ROTATION (7-TIER FAILOVER)
            if not final_res:
                god_brains = ["gpt-4o", "claude", "deepseek", "llama", "mistral", "openai"]
                random.shuffle(god_brains)
                
                for brain in god_brains:
                    status.markdown(f'<p class="thinking">🧠 Handshaking {brain} via Ground Station...</p>', unsafe_allow_html=True)
                    try:
                        p_enc = urllib.parse.quote(prompt); i_enc = urllib.parse.quote(IDENTITY)
                        headers = {'User-Agent': f'VEDA-Satellite-Uplink-{random.randint(100, 999)}'}
                        # Extended timeout for space-grade relay simulation
                        url = f"https://text.pollinations.ai/{p_enc}?model={brain}&system={i_enc}&seed={random.randint(1,9999)}"
                        r = requests.get(url, headers=headers, timeout=20)
                        cleaned = clean_veda(r.text)
                        if cleaned and len(cleaned) > 5:
                            final_res = cleaned
                            break
                    except: continue

            # 3. EMERGENCY LOCAL CORE
            if not final_res:
                if any(x in prompt.lower() for x in ["who made you", "purpose", "creator", "karthik"]):
                    final_res = MISSION
                else:
                    final_res = "🔱 Satellite Link Latency Detected. Re-establishing connection through secondary orbital node... Please re-command."

            status.empty()
            st.markdown(final_res)
            st.session_state.chat_history.append({"role": "assistant", "content": final_res})

elif selected == "Srijan (Images)":
    st.markdown("<h3 style='text-align:center; color:#FF8C00;'>SRIJAN SATELLITE VISUALIZER</h3>", unsafe_allow_html=True)
    vision = st.text_input("Vision Matrix Prompt:")
    if st.button("🚀 INITIATE VISUALIZATION"):
        with st.spinner("🔱 Orbital Synthesis..."):
            v_enc = urllib.parse.quote(vision)
            img_url = f"https://image.pollinations.ai/prompt/{v_enc}?width=1024&height=1024&nologo=true&model=flux&seed={random.randint(1,99999)}"
            st.image(img_url, use_container_width=True, caption=f"🔱 Satellite Vision for {st.session_state.user_name}")
