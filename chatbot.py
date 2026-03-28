import streamlit as st
from google import genai
from google.genai import types
import requests
import urllib.parse
from datetime import datetime
import pytz
from streamlit_option_menu import option_menu
import time

# --- 1. CORE CONFIG ---
if 'user_name' not in st.session_state: st.session_state.user_name = None
ist = pytz.timezone('Asia/Kolkata')

def get_greeting():
    hour = datetime.now(ist).hour
    if 5 <= hour < 12: return "GOOD MORNING"
    elif 12 <= hour < 17: return "GOOD AFTERNOON"
    elif 17 <= hour < 21: return "GOOD EVENING"
    else: return "GOOD NIGHT"

st.set_page_config(page_title="VEDA 3.0 ULTRA", page_icon="🔱", layout="wide", initial_sidebar_state="expanded")

# --- 2. THE APEX CLUSTER (8-Model Failover) ---
def call_apex_cluster(prompt, identity):
    """The absolute fail-safe: tried in order of speed and stability."""
    # DeepSeek and Groq-powered models are now prioritized for speed
    models = ["deepseek", "claude", "searchgpt", "openai", "llama", "qwen", "mistral"]
    q_enc = urllib.parse.quote(prompt)
    sys_p = urllib.parse.quote(identity)
    
    for model in models:
        try:
            url = f"https://text.pollinations.ai/{q_enc}?model={model}&system={sys_p}"
            r = requests.get(url, timeout=8) # Ultra-fast 8s timeout to keep things moving
            if r.status_code == 200 and "Queue full" not in r.text and len(r.text) > 2:
                return r.text
        except: continue
    return None

# --- 3. LOGIN PHASE ---
if not st.session_state.user_name:
    st.markdown("<h1 style='text-align:center; color:#FF8C00; margin-top:100px;'>VEDA 3.0 ULTRA</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        name_in = st.text_input("IDENTIFY YOURSELF:", placeholder="Commander Name...")
        if st.button("INITIALIZE SOVEREIGN CORE 🚀", use_container_width=True):
            if name_in: 
                st.session_state.user_name = name_in.strip()
                st.rerun()
    st.stop()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align:center;'>🔱</h1><h2 style='text-align:center; color:#FF8C00; margin-top:-10px;'>VEDA 3.0 ULTRA</h2>", unsafe_allow_html=True)
    selected = option_menu(None, ["Medha (Chat)", "Srijan (Image Gen)"], icons=["chat-right-dots", "brush-fill"], default_index=0, styles={"nav-link-selected": {"background-color": "#FF8C00"}})
    st.divider()
    if st.button("🗑️ Reset Session"):
        st.session_state.user_name = None
        st.session_state.chat_history = []
        st.rerun()

# --- 5. MAIN UI ---
st.markdown("""<style>header {visibility: hidden;} .v-title { font-size: 55px; color: #FF8C00; text-align: center; font-weight: 900; text-transform: uppercase; } .thinking-text { color: #FF8C00; font-style: italic; font-weight: bold; animation: pulse 1.5s infinite; font-size: 18px; } @keyframes pulse { 0%, 100% { opacity: 0.3; } 50% { opacity: 1; } }</style>""", unsafe_allow_html=True)

# API PRIMARY
client = None
if "GOOGLE_API_KEY" in st.secrets:
    try: client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"], http_options=types.HttpOptions(timeout=8000))
    except: client = None

if selected == "Medha (Chat)":
    st.markdown(f'<div class="v-title">{get_greeting()}, {st.session_state.user_name.upper()}</div>', unsafe_allow_html=True)
    if "chat_history" not in st.session_state: st.session_state.chat_history = []
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Command the Sovereign Core..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            status = st.empty()
            final_res = ""
            
            # --- PHASE 1: GEMINI 3.1 PRO ---
            status.markdown('<p class="thinking-text">🔱 thinking with veda....</p>', unsafe_allow_html=True)
            if client:
                try:
                    resp = client.models.generate_content(model="gemini-3.1-pro-preview", contents=f"{IDENTITY}\n\n{prompt}")
                    final_res = resp.text
                except: pass
            
            # --- PHASE 2: APEX CLUSTER (DeepSeek/Claude/Groq-Llama) ---
            if not final_res:
                status.markdown('<p class="thinking-text">🔱 researching....</p>', unsafe_allow_html=True)
                final_res = call_apex_cluster(prompt, IDENTITY)
            
            # --- PHASE 3: ANALYSIS ---
            if final_res:
                status.markdown('<p class="thinking-text">🔱 analysis....</p>', unsafe_allow_html=True)
                time.sleep(0.3)

            status.empty()
            if not final_res: final_res = "🔱 Neural corridors jammed. Re-attempting connection..."
            
            st.markdown(final_res)
            st.session_state.chat_history.append({"role": "assistant", "content": final_res})

elif selected == "Srijan (Image Gen)":
    st.markdown(f'<div class="v-title">SRIJAN MODE</div>', unsafe_allow_html=True)
    vision = st.text_input("Vision Matrix Prompt:", placeholder="Describe...")
    if st.button("🚀 INITIATE"):
        if vision:
            with st.spinner("🔱 Visualizing..."):
                v_enc = urllib.parse.quote(vision)
                img = f"https://image.pollinations.ai/prompt/{v_enc}?width=1024&height=1024&nologo=true&model=flux"
                st.image(img, use_container_width=True)
