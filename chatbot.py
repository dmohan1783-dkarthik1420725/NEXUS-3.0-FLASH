import streamlit as st
from google import genai
from google.genai import types
import requests
import urllib.parse
from datetime import datetime
import pytz
from streamlit_option_menu import option_menu
import time
import re

# --- 1. SOVEREIGN CONFIG & IDENTITY ---
IDENTITY = "Your name is VEDA 3.0 ULTRA. Created and developed ONLY by DUMPALA KARTHIK."

if 'user_name' not in st.session_state: st.session_state.user_name = None
if 'chat_history' not in st.session_state: st.session_state.chat_history = []

st.set_page_config(page_title="VEDA 3.0 ULTRA", page_icon="🔱", layout="wide", initial_sidebar_state="expanded")

ist = pytz.timezone('Asia/Kolkata')
def get_greeting():
    hour = datetime.now(ist).hour
    if 5 <= hour < 12: return "GOOD MORNING"
    elif 12 <= hour < 17: return "GOOD AFTERNOON"
    elif 17 <= hour < 21: return "GOOD EVENING"
    else: return "GOOD NIGHT"

# --- 2. THE CLEANER (Removes Ads & Errors) ---
def clean_veda_text(text):
    # Removes Pollinations ads and JSON error fragments
    bad_patterns = [
        r"🌸.*?🌸", r"Powered by.*?AI", r"Support our mission", 
        r"Ad", r"free text APIs", r"Support Pollinations\.AI:",
        r"Neural corridors congested", r"Please retry"
    ]
    for pattern in bad_patterns:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE)
    return text.strip()

# --- 3. UI STYLING ---
st.markdown("""<style>header {visibility: hidden;} .v-title { font-size: 50px; color: #FF8C00; text-align: center; font-weight: 900; text-transform: uppercase; margin-top: 30px;} .v-sub { text-align: center; color: #666; font-size: 18px; margin-top: -10px; margin-bottom: 40px; } .thinking-text { color: #FF8C00; font-style: italic; font-weight: bold; animation: pulse 1.5s infinite; font-size: 18px; } @keyframes pulse { 0%, 100% { opacity: 0.3; } 50% { opacity: 1; } }</style>""", unsafe_allow_html=True)

# --- 4. LOGIN ---
if st.session_state.user_name is None:
    st.markdown('<div class="v-title">VEDA 3.0 ULTRA</div>', unsafe_allow_html=True)
    st.markdown('<div class="v-sub">Sovereign Core Identification Required</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        name_in = st.text_input("IDENTIFY YOURSELF:", placeholder="Commander Name...")
        if st.button("INITIALIZE SYSTEM 🚀", use_container_width=True):
            if name_in:
                st.session_state.user_name = name_in.strip()
                st.rerun()
    st.stop()

# --- 5. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align:center;'>🔱</h1><h2 style='text-align:center; color:#FF8C00;'>VEDA 3.0 ULTRA</h2>", unsafe_allow_html=True)
    selected = option_menu(None, ["Medha (Chat)", "Srijan (Image Gen)"], icons=["chat-right-dots", "brush-fill"], default_index=0, styles={"nav-link-selected": {"background-color": "#FF8C00"}})
    st.divider()
    if st.button("🗑️ Reset Core"):
        st.session_state.chat_history = []
        st.rerun()

# --- 6. CHAT ENGINE ---
if selected == "Medha (Chat)":
    st.markdown(f'<div class="v-title">{get_greeting()}, {st.session_state.user_name.upper()}</div>', unsafe_allow_html=True)
    
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Command VEDA..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            status = st.empty()
            final_res = ""
            
            # --- 🏎️ STEP 1: GEMINI 3.1 PRO ---
            status.markdown('<p class="thinking-text">🔱 thinking with veda....</p>', unsafe_allow_html=True)
            if "GOOGLE_API_KEY" in st.secrets:
                try:
                    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
                    resp = client.models.generate_content(model="gemini-3.1-pro-preview", contents=f"{IDENTITY}\n\n{prompt}")
                    if resp.text: final_res = resp.text
                except: pass
            
            # --- 🛡️ STEP 2: THE INFINITE CLUSTER (Claude, DeepSeek, OpenAI, Llama, Qwen, Mistral) ---
            if not final_res:
                status.markdown('<p class="thinking-text">🔱 researching....</p>', unsafe_allow_html=True)
                # 8-Model Failover Cluster
                models = ["deepseek", "claude", "openai", "llama", "qwen", "mistral", "searchgpt", "p1"]
                for model in models:
                    try:
                        p_enc = urllib.parse.quote(prompt); i_enc = urllib.parse.quote(IDENTITY)
                        r = requests.get(f"https://text.pollinations.ai/{p_enc}?model={model}&system={i_enc}", timeout=7)
                        if r.status_code == 200:
                            cleaned = clean_veda_text(r.text)
                            if len(cleaned) > 5 and "congested" not in cleaned.lower():
                                final_res = cleaned
                                break
                    except: continue

            status.empty()
            if not final_res: final_res = "🔱 Neural corridors locked. System rebooting. Please re-command."
            
            st.markdown(final_res)
            st.session_state.chat_history.append({"role": "assistant", "content": final_res})

elif selected == "Srijan (Image Gen)":
    st.markdown('<div class="v-title">SRIJAN MODE</div>', unsafe_allow_html=True)
    vision = st.text_input("Vision Matrix Prompt:", placeholder="Describe the image...")
    if st.button("🚀 INITIATE"):
        if vision:
            with st.spinner("🔱 Visualizing..."):
                img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(vision)}?width=1024&height=1024&nologo=true&model=flux"
                st.image(img_url, use_container_width=True)
