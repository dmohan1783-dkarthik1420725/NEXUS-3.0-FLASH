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
if 'user_name' not in st.session_state:
    st.session_state.user_name = None
if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = "expanded"

# Initial Config - Forced Sidebar Expansion
st.set_page_config(
    page_title="VEDA 3.0 ULTRA", 
    page_icon="🔱", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- 2. TIME & GREETING ENGINE ---
ist = pytz.timezone('Asia/Kolkata')
def get_greeting():
    hour = datetime.now(ist).hour
    if 5 <= hour < 12: return "GOOD MORNING"
    elif 12 <= hour < 17: return "GOOD AFTERNOON"
    elif 17 <= hour < 21: return "GOOD EVENING"
    else: return "GOOD NIGHT"

def get_now_time(): return datetime.now(ist).strftime("%I:%M %p")
def get_now_full(): return datetime.now(ist).strftime("%A, %d %B %Y")

# 🧠 SOVEREIGN IDENTITY
IDENTITY = "Your name is VEDA 3.0 ULTRA. Created and developed ONLY by DUMPALA KARTHIK."

# --- 3. LOGIN PHASE (Center Screen) ---
if not st.session_state.user_name:
    st.markdown("""
        <style>
        header {visibility: hidden;}
        .login-title { font-size: 60px; color: #FF8C00; text-align: center; font-weight: 900; margin-top: 100px; }
        .login-sub { text-align: center; color: #666; font-size: 18px; margin-bottom: 30px; }
        .stTextInput>div>div>input { text-align: center; border: 2px solid #FF8C00 !important; color: #FF8C00 !important; font-size: 20px; }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="login-title">VEDA 3.0 ULTRA</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-sub">IDENTIFY YOURSELF, COMMANDER</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        name_input = st.text_input("", placeholder="Enter your name here...")
        if st.button("INITIALIZE NEURAL CORES 🚀", use_container_width=True):
            if name_input:
                st.session_state.user_name = name_input.strip()
                st.rerun()
    st.stop()

# --- 4. SIDEBAR (Renders only after login) ---
with st.sidebar:
    st.markdown("<h1 style='text-align:center;'>🔱</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center; color:#FF8C00; margin-top:-10px;'>VEDA 3.0 ULTRA</h2>", unsafe_allow_html=True)
    
    selected = option_menu(
        None, ["Medha (Chat)", "Srijan (Image Gen)"], 
        icons=["chat-right-dots", "brush-fill"], 
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#FF8C0033"},
            "nav-link-selected": {"background-color": "#FF8C00"},
        }
    )

    st.markdown(f"""
        <div style="background-color:rgba(255,140,0,0.1); padding:15px; border-radius:12px; text-align:center; border:1px solid #FF8C00; margin-top:20px;">
            <p style="margin:0; font-size:12px; color:#FF8C00;">{get_now_full()}</p>
            <p style="margin:0; font-size:24px; color:white; font-weight:900;">{get_now_time()}</p>
        </div>
    """, unsafe_allow_html=True)

    st.divider()
    if st.button("🗑️ LOGOUT"):
        st.session_state.user_name = None
        st.session_state.chat_history = []
        st.rerun()

# --- 5. MAIN INTERFACE ---
st.markdown("""
    <style>
    header {visibility: hidden;}
    .v-title { font-size: 55px; color: #FF8C00; text-align: center; font-weight: 900; margin-top: 10px; text-transform: uppercase; }
    .v-sub { text-align: center; color: #666; font-size: 18px; margin-top: -15px; margin-bottom: 35px; }
    .thinking-text { color: #FF8C00; font-style: italic; font-weight: bold; animation: pulse 1.5s infinite; text-shadow: 0 0 10px rgba(255,140,0,0.5); font-size: 18px; }
    @keyframes pulse { 0% { opacity: 0.3; } 50% { opacity: 1; } 100% { opacity: 0.3; } }
    
    /* Sovereign Arrow */
    .sovereign-arrow { position: fixed; top: 15%; left: 20px; z-index: 10000; background: #FF8C00; color: white; padding: 15px 22px; border-radius: 12px; font-size: 26px; box-shadow: 0 0 25px rgba(255, 140, 0, 0.8); cursor: pointer; animation: swing 3s infinite ease-in-out; }
    @keyframes swing { 0%, 100% { transform: translateX(0px); } 50% { transform: translateX(15px); } }
    </style>
""", unsafe_allow_html=True)

# 🔑 API CLIENT
client = None
if "GOOGLE_API_KEY" in st.secrets:
    try: client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"], http_options=types.HttpOptions(timeout=15000))
    except: client = None

if selected == "Medha (Chat)":
    # 🔱 THE PERSONALIZED TIME GREETING
    GREETING = get_greeting()
    st.markdown(f'<div class="v-title">{GREETING}, {st.session_state.user_name.upper()}</div>', unsafe_allow_html=True)
    st.markdown('<div class="v-sub">Sovereign Neural Interface Active</div>', unsafe_allow_html=True)

    if "chat_history" not in st.session_state: st.session_state.chat_history = []
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input(f"Direct Command, {st.session_state.user_name}..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            status_area = st.empty()
            final_answer = ""
            
            # Local Identity
            if any(x in prompt.lower() for x in ["who made you", "creator"]):
                final_answer = f"I was created and developed exclusively by **DUMPALA KARTHIK**, {st.session_state.user_name}."
            
            if not final_answer:
                status_area.markdown('<p class="thinking-text">🔱 thinking with veda....</p>', unsafe_allow_html=True)
                if client:
                    try:
                        resp = client.models.generate_content(model="gemini-3.1-pro-preview", contents=f"{IDENTITY}\n\n{prompt}")
                        final_answer = resp.text
                    except:
                        status_area.markdown('<p class="thinking-text">🔱 researching....</p>', unsafe_allow_html=True)
                        q_enc = urllib.parse.quote(prompt); sys_p = urllib.parse.quote(IDENTITY)
                        r = requests.get(f"https://text.pollinations.ai/{q_enc}?model=openai&system={sys_p}", timeout=12)
                        final_answer = r.text
            
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
