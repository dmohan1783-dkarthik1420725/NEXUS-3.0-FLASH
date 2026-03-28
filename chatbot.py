import streamlit as st
from google import genai
from google.genai import types
import requests
import urllib.parse
from datetime import datetime
import pytz
from streamlit_option_menu import option_menu
import time

# --- 1. SESSION STATE & LOGIN ---
if 'user_name' not in st.session_state: st.session_state.user_name = None
if 'sidebar_state' not in st.session_state: st.session_state.sidebar_state = "expanded"

st.set_page_config(page_title="VEDA 3.0 ULTRA", page_icon="🔱", layout="wide", initial_sidebar_state="expanded")

# --- 2. TIME & GREETING ENGINE ---
ist = pytz.timezone('Asia/Kolkata')
def get_greeting():
    hour = datetime.now(ist).hour
    if 5 <= hour < 12: return "GOOD MORNING"
    elif 12 <= hour < 17: return "GOOD AFTERNOON"
    elif 17 <= hour < 21: return "GOOD EVENING"
    else: return "GOOD NIGHT"

# 🧠 SOVEREIGN IDENTITY
IDENTITY = "Your name is VEDA 3.0 ULTRA. Created and developed ONLY by DUMPALA KARTHIK."

# --- 3. LOGIN PHASE ---
if not st.session_state.user_name:
    st.markdown("""
        <style>
        header {visibility: hidden;}
        .login-title { font-size: 60px; color: #FF8C00; text-align: center; font-weight: 900; margin-top: 100px; }
        .login-sub { text-align: center; color: #666; font-size: 18px; margin-bottom: 30px; }
        .stTextInput>div>div>input { text-align: center; border: 2px solid #FF8C00 !important; color: #FF8C00 !important; }
        </style>
    """, unsafe_allow_html=True)
    st.markdown('<div class="login-title">VEDA 3.0 ULTRA</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-sub">IDENTIFY YOURSELF, COMMANDER</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        name_input = st.text_input("", placeholder="Enter your name...")
        if st.button("INITIALIZE NEURAL CORES 🚀", use_container_width=True):
            if name_input:
                st.session_state.user_name = name_input.strip()
                st.rerun()
    st.stop()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align:center;'>🔱</h1><h2 style='text-align:center; color:#FF8C00; margin-top:-10px;'>VEDA 3.0 ULTRA</h2>", unsafe_allow_html=True)
    selected = option_menu(None, ["Medha (Chat)", "Srijan (Image Gen)"], icons=["chat-right-dots", "brush-fill"], default_index=0, styles={"nav-link-selected": {"background-color": "#FF8C00"}})
    st.divider()
    if st.button("🗑️ LOGOUT"):
        st.session_state.user_name = None
        st.rerun()

# --- 5. MAIN INTERFACE ---
st.markdown("""
    <style>
    header {visibility: hidden;}
    .v-title { font-size: 55px; color: #FF8C00; text-align: center; font-weight: 900; margin-top: 10px; text-transform: uppercase; }
    .v-sub { text-align: center; color: #666; font-size: 18px; margin-top: -15px; margin-bottom: 35px; }
    .thinking-text { color: #FF8C00; font-style: italic; font-weight: bold; animation: pulse 1.5s infinite; font-size: 18px; }
    @keyframes pulse { 0% { opacity: 0.3; } 50% { opacity: 1; } 100% { opacity: 0.3; } }
    </style>
""", unsafe_allow_html=True)

# 🔑 API CLIENT
client = None
if "GOOGLE_API_KEY" in st.secrets:
    try: client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"], http_options=types.HttpOptions(timeout=10000))
    except: client = None

if selected == "Medha (Chat)":
    st.markdown(f'<div class="v-title">{get_greeting()}, {st.session_state.user_name.upper()}</div>', unsafe_allow_html=True)
    st.markdown('<div class="v-sub">Sovereign Neural Interface Active</div>', unsafe_allow_html=True)

    if "chat_history" not in st.session_state: st.session_state.chat_history = []
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Command VEDA..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            status_area = st.empty()
            final_answer = ""
            
            # 🚀 STAGE 1: GEMINI 3.1 PRO
            status_area.markdown('<p class="thinking-text">🔱 thinking with veda....</p>', unsafe_allow_html=True)
            if client:
                try:
                    resp = client.models.generate_content(model="gemini-3.1-pro-preview", contents=f"{IDENTITY}\n\n{prompt}")
                    final_answer = resp.text
                except: pass
            
            # 🚀 STAGE 2: POLLINATIONS (OpenAI)
            if not final_answer:
                status_area.markdown('<p class="thinking-text">🔱 researching....</p>', unsafe_allow_html=True)
                try:
                    q_enc = urllib.parse.quote(prompt); sys_p = urllib.parse.quote(IDENTITY)
                    r = requests.get(f"https://text.pollinations.ai/{q_enc}?model=openai&system={sys_p}", timeout=10)
                    if "error" not in r.text: final_answer = r.text
                except: pass

            # 🚀 STAGE 3: EMERGENCY MISTRAL TUNNEL
            if not final_answer:
                status_area.markdown('<p class="thinking-text">🔱 analysis....</p>', unsafe_allow_html=True)
                try:
                    r = requests.get(f"https://text.pollinations.ai/{urllib.parse.quote(prompt)}?model=mistral", timeout=10)
                    final_answer = r.text
                except: final_answer = "🔱 Neural pathways congested. Please re-command in 10s."

            status_area.empty()
            st.markdown(final_answer)
            st.session_state.chat_history.append({"role": "assistant", "content": final_answer})

elif selected == "Srijan (Image Gen)":
    st.markdown(f'<div class="v-title">SRIJAN MODE</div>', unsafe_allow_html=True)
    vision = st.text_input("Vision Matrix Prompt:", placeholder="Describe...")
    if st.button("🚀 INITIATE"):
        if vision:
            with st.spinner("🔱 Visualizing..."):
                v_enc = urllib.parse.quote(vision)
                img = f"https://image.pollinations.ai/prompt/{v_enc}?width=1024&height=1024&nologo=true&model=flux"
                st.image(img, use_container_width=True)
