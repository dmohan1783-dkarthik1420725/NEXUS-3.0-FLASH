import streamlit as st
from google import genai
from google.genai import types
import requests
import urllib.parse
from datetime import datetime
import pytz
from streamlit_option_menu import option_menu
import time

# --- 1. CORE STABILITY ---
if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = "expanded"

st.set_page_config(page_title="VEDA 3.0 ULTRA", page_icon="🔱", layout="wide", initial_sidebar_state=st.session_state.sidebar_state)

ist = pytz.timezone('Asia/Kolkata')
def get_now_time(): return datetime.now(ist).strftime("%I:%M %p")
def get_now_full(): return datetime.now(ist).strftime("%A, %d %B %Y")

# 🧠 SOVEREIGN IDENTITY LOCK
IDENTITY = "Your name is VEDA 3.0 ULTRA. Created and developed ONLY by DUMPALA KARTHIK."

if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "neural_logs" not in st.session_state: st.session_state.neural_logs = []

def add_to_memory(m_type, content):
    ts = datetime.now(ist).strftime("%H:%M:%S")
    st.session_state.neural_logs.insert(0, f"[{ts}] {m_type}: {content[:15]}...")

# --- 🔑 API INITIALIZATION (Exclusive Gemini 3.1 Pro) ---
client = None
if "GOOGLE_API_KEY" in st.secrets:
    try:
        client = genai.Client(
            api_key=st.secrets["GOOGLE_API_KEY"], 
            http_options=types.HttpOptions(timeout=60000)
        )
    except: client = None

# --- 2. SIDEBAR UI ---
with st.sidebar:
    col_a, col_b = st.columns([4, 1])
    with col_a: 
        st.markdown("<h1 style='margin-bottom:0;'>🔱</h1><h2 style='color:#FF8C00; margin-top:-10px;'>VEDA 3.0 ULTRA</h2>", unsafe_allow_html=True)
    with col_b: 
        if st.button("«", help="Collapse"):
            st.session_state.sidebar_state = "collapsed"
            st.rerun()

    st.markdown(f'<div style="background-color:rgba(255,140,0,0.1);padding:15px;border-radius:12px;text-align:center;border:1px solid #FF8C00;margin-bottom:20px;"><p style="margin:0;font-size:14px;color:#FF8C00;">{get_now_full()}</p><p style="margin:0;font-size:26px;color:white;font-weight:900;">{get_now_time()}</p></div>', unsafe_allow_html=True)
    
    selected = option_menu("MODES", ["Medha (Chat)", "Srijan (Image Gen)"], 
                          icons=["chat-right-dots", "brush-fill"], default_index=0)
    
    if st.button("🗑️ Reset Core"):
        st.session_state.chat_history = []
        st.rerun()

# --- 3. MAIN INTERFACE & UI ENHANCEMENTS ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    
    /* Floating Toggle Arrow */
    .floating-arrow {
        position: fixed; top: 15%; left: 0px; z-index: 999;
        background-color: #FF8C00; color: white; padding: 10px 5px 10px 15px;
        border-radius: 0 50px 50px 0; cursor: pointer; font-weight: bold;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.3); transition: 0.3s;
    }

    .v-title { font-size: 50px; color: #FF8C00; text-align: center; font-weight: 900; margin-bottom: 0px; }
    .v-sub { text-align: center; color: #666; font-size: 16px; margin-top: -10px; margin-bottom: 30px; }
    .thinking-text { color: #FF8C00; font-style: italic; font-weight: bold; animation: pulse 1.5s infinite; text-shadow: 0 0 10px rgba(255,140,0,0.5); font-size: 18px; }
    @keyframes pulse { 0% { opacity: 0.3; } 50% { opacity: 1; } 100% { opacity: 0.3; } }
    </style>
""", unsafe_allow_html=True)

if st.session_state.sidebar_state == "collapsed":
    st.markdown('<div class="floating-arrow">➤</div>', unsafe_allow_html=True)

if selected == "Medha (Chat)":
    st.markdown('<div class="v-title">VEDA 3.0 ULTRA</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="v-sub">Sovereign Neural Interface</div>', unsafe_allow_html=True)

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Command the Sovereign AI..."):
        add_to_memory("MEDHA", prompt)
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            status_area = st.empty()
            final_answer = ""
            p_low = prompt.lower().strip()
            
            # 🚀 LOCAL IDENTITY PROTECTION
            if any(x in p_low for x in ["who made you", "creator"]):
                final_answer = "I was created and developed exclusively by **DUMPALA KARTHIK**. I am VEDA 3.0 ULTRA."
            elif any(x in p_low for x in ["purpose", "why were you created"]):
                final_answer = "I am **VEDA 3.0 ULTRA**, engineered by **DUMPALA KARTHIK** to be an elite cognitive tool for intelligence and visual synthesis."

            # 🏎️ EXCLUSIVE GEMINI 3.1 PRO PROCESSING
            if not final_answer:
                status_area.markdown('<p class="thinking-text">🔱 Engaging Sovereign Neural Core...</p>', unsafe_allow_html=True)
                if client:
                    try:
                        resp = client.models.generate_content(
                            model="gemini-3.1-pro-preview", 
                            contents=f"{IDENTITY}\n\n{prompt}"
                        )
                        final_answer = resp.text
                    except Exception as e:
                        final_answer = f"🔱 Neural systems saturated. [Error: {str(e)}]"

            status_area.empty()
            st.markdown(final_answer)
            st.session_state.chat_history.append({"role": "assistant", "content": final_answer})

elif selected == "Srijan (Image Gen)":
    st.markdown('<div class="v-title">VEDA 3.0 ULTRA</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="v-sub">Advanced Visual Synthesis: Pollinations Flux</div>', unsafe_allow_html=True)
    vision = st.text_input("Vision Matrix Prompt:", placeholder="Describe the image...")
    if st.button("🚀 INITIATE"):
        if vision:
            add_to_memory("SRIJAN", vision)
            with st.spinner("🔱 Visualizing via Pollinations AI..."):
                try:
                    v_enc = urllib.parse.quote(vision)
                    # Exclusive use of Pollinations for Image Generation
                    img = f"https://image.pollinations.ai/prompt/{v_enc}?width=1024&height=1024&nologo=true&model=flux"
                    st.image(img, use_container_width=True)
                except: st.error("Image synthesis busy. Please retry.")
