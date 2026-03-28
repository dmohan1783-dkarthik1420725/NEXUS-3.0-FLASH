import streamlit as st
from google import genai
from google.genai import types
import requests
import urllib.parse
from datetime import datetime
import pytz
from streamlit_option_menu import option_menu
import time

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

# --- 2. CSS STYLING ---
st.markdown("""<style>header {visibility: hidden;} .v-title { font-size: 50px; color: #FF8C00; text-align: center; font-weight: 900; text-transform: uppercase; margin-top: 30px;} .v-sub { text-align: center; color: #666; font-size: 18px; margin-top: -10px; margin-bottom: 40px; } .thinking-text { color: #FF8C00; font-style: italic; font-weight: bold; animation: pulse 1.5s infinite; font-size: 18px; } @keyframes pulse { 0%, 100% { opacity: 0.3; } 50% { opacity: 1; } }</style>""", unsafe_allow_html=True)

# --- 3. LOGIN / MAIN INTERFACE LOGIC ---
if st.session_state.user_name is None:
    st.markdown('<div class="v-title">VEDA 3.0 ULTRA</div>', unsafe_allow_html=True)
    st.markdown('<div class="v-sub">Sovereign Core Identification Required</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        name_in = st.text_input("ENTER COMMANDER NAME:", placeholder="Type name and press Enter...")
        if st.button("INITIALIZE SYSTEM 🚀", use_container_width=True):
            if name_in:
                st.session_state.user_name = name_in.strip()
                st.rerun()
else:
    with st.sidebar:
        st.markdown("<h1 style='text-align:center;'>🔱</h1><h2 style='text-align:center; color:#FF8C00;'>VEDA 3.0 ULTRA</h2>", unsafe_allow_html=True)
        selected = option_menu(None, ["Medha (Chat)", "Srijan (Image Gen)"], 
                              icons=["chat-right-dots", "brush-fill"], default_index=0, 
                              styles={"nav-link-selected": {"background-color": "#FF8C00"}})
        st.divider()
        if st.button("🗑️ Reset / Logout"):
            st.session_state.user_name = None
            st.session_state.chat_history = []
            st.rerun()

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
                
                # --- STAGE 1: GEMINI 3.1 PRO (Primary) ---
                status.markdown('<p class="thinking-text">🔱 thinking with veda....</p>', unsafe_allow_html=True)
                if "GOOGLE_API_KEY" in st.secrets:
                    try:
                        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
                        resp = client.models.generate_content(model="gemini-3.1-pro-preview", contents=f"{IDENTITY}\n\n{prompt}")
                        final_res = resp.text
                    except: pass
                
                # --- STAGE 2: THE APEX CLUSTER (DeepSeek, Claude, Llama, Qwen) ---
                if not final_res:
                    status.markdown('<p class="thinking-text">🔱 researching....</p>', unsafe_allow_html=True)
                    # DeepSeek and Qwen are prioritized for high-speed bypass
                    for model in ["deepseek", "qwen", "claude", "mistral", "llama"]:
                        try:
                            p_enc = urllib.parse.quote(prompt)
                            i_enc = urllib.parse.quote(IDENTITY)
                            r = requests.get(f"https://text.pollinations.ai/{p_enc}?model={model}&system={i_enc}", timeout=10)
                            if r.status_code == 200 and "Queue full" not in r.text:
                                final_res = r.text
                                break
                        except: continue

                status.empty()
                if not final_res: final_res = "🔱 Neural pathways congested. Re-routing through secondary core. Please retry in 5s."
                st.markdown(final_res)
                st.session_state.chat_history.append({"role": "assistant", "content": final_res})

    elif selected == "Srijan (Image Gen)":
        st.markdown('<div class="v-title">SRIJAN MODE</div>', unsafe_allow_html=True)
        vision = st.text_input("Vision Matrix Prompt:", placeholder="Describe...")
        if st.button("🚀 INITIATE"):
            if vision:
                with st.spinner("🔱 Visualizing..."):
                    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(vision)}?width=1024&height=1024&nologo=true&model=flux"
                    st.image(img_url, use_container_width=True)
