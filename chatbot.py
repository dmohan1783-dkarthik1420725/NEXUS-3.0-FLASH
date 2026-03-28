import streamlit as st
from google import genai
from google.genai import types
import requests
import urllib.parse
from datetime import datetime
import pytz
from streamlit_option_menu import option_menu
import time

# --- 1. SESSION & TIME ---
if 'user_name' not in st.session_state: st.session_state.user_name = None
ist = pytz.timezone('Asia/Kolkata')

def get_greeting():
    hour = datetime.now(ist).hour
    if 5 <= hour < 12: return "GOOD MORNING"
    elif 12 <= hour < 17: return "GOOD AFTERNOON"
    elif 17 <= hour < 21: return "GOOD EVENING"
    else: return "GOOD NIGHT"

st.set_page_config(page_title="VEDA 3.0 ULTRA", page_icon="🔱", layout="wide", initial_sidebar_state="expanded")

# 🧠 THE SOVEREIGN IDENTITY
IDENTITY = "Your name is VEDA 3.0 ULTRA. Created and developed ONLY by DUMPALA KARTHIK."

# --- 2. THE ULTIMATE NEURAL CLUSTER (Including Claude) ---
def call_neural_cluster(prompt, identity):
    """Try the world's most powerful free models in order."""
    # CLAUDE is now the first priority backup, followed by SearchGPT and OpenAI
    models = ["claude", "searchgpt", "openai", "mistral", "llama"]
    q_enc = urllib.parse.quote(prompt)
    sys_p = urllib.parse.quote(identity)
    
    for model in models:
        try:
            # Multi-model bypass tunnel
            url = f"https://text.pollinations.ai/{q_enc}?model={model}&system={sys_p}"
            r = requests.get(url, timeout=12)
            
            # Validation: Ensure it's not a 'Queue Full' or '429' error
            if r.status_code == 200 and "Queue full" not in r.text and "error" not in r.text.lower():
                return r.text, model
        except:
            continue
    return None, None

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

# --- 5. MAIN INTERFACE ---
st.markdown("""<style>header {visibility: hidden;} .v-title { font-size: 55px; color: #FF8C00; text-align: center; font-weight: 900; text-transform: uppercase; } .thinking-text { color: #FF8C00; font-style: italic; font-weight: bold; animation: pulse 1.5s infinite; font-size: 18px; } @keyframes pulse { 0%, 100% { opacity: 0.3; } 50% { opacity: 1; } }</style>""", unsafe_allow_html=True)

# 🔑 PRIMARY API (Gemini 3.1)
client = None
if "GOOGLE_API_KEY" in st.secrets:
    try: client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"], http_options=types.HttpOptions(timeout=8000))
    except: client = None

if selected == "Medha (Chat)":
    st.markdown(f'<div class="v-title">{get_greeting()}, {st.session_state.user_name.upper()}</div>', unsafe_allow_html=True)

    if "chat_history" not in st.session_state: st.session_state.chat_history = []
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Command VEDA..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            status = st.empty()
            final_res = ""
            
            # --- STAGE 1: GEMINI 3.1 PRO ---
            status.markdown('<p class="thinking-text">🔱 thinking with veda....</p>', unsafe_allow_html=True)
            if client:
                try:
                    resp = client.models.generate_content(model="gemini-3.1-pro-preview", contents=f"{IDENTITY}\n\n{prompt}")
                    final_res = resp.text
                except: pass
            
            # --- STAGE 2: CLAUDE & POWER CLUSTER ---
            if not final_res:
                status.markdown('<p class="thinking-text">🔱 researching....</p>', unsafe_allow_html=True)
                final_res, model_used = call_neural_cluster(prompt, IDENTITY)
                
            # --- STAGE 3: ANALYSIS ---
            if final_res:
                status.markdown('<p class="thinking-text">🔱 analysis....</p>', unsafe_allow_html=True)
                time.sleep(0.3)

            status.empty()
            if not final_res: final_res = "🔱 Neural pathways congested. Please re-command."
            
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
