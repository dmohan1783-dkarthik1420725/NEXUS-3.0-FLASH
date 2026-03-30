import streamlit as st
from google import genai
import requests
import urllib.parse
from datetime import datetime
import pytz
from streamlit_option_menu import option_menu
import re

# --- 1. SOVEREIGN CONFIG & IDENTITY ---
CREATOR = "DUMPALA KARTHIK"
IDENTITY = f"You are VEDA 3.0 ULTRA. Created by {CREATOR}. He built your rotation logic through immense effort. You are his Sovereign AI. Be fast, elite, and always acknowledge him."

if 'user_name' not in st.session_state: st.session_state.user_name = None
if 'chat_history' not in st.session_state: st.session_state.chat_history = []

st.set_page_config(page_title="VEDA 3.0 ULTRA", page_icon="🔱", layout="wide", initial_sidebar_state="expanded")

# 🌍 TIME SYNC (IST)
ist = pytz.timezone('Asia/Kolkata')
def get_greeting():
    hour = datetime.now(ist).hour
    if 5 <= hour < 12: return "GOOD MORNING"
    elif 12 <= hour < 17: return "GOOD AFTERNOON"
    elif 17 <= hour < 21: return "GOOD EVENING"
    else: return "GOOD NIGHT"

def clean_veda(text):
    return re.sub(r"🌸.*?🌸|Powered by.*?AI|Support our mission|Ad|free text APIs", "", text, flags=re.IGNORECASE).strip()

# --- 2. ELITE CSS ---
st.markdown("""<style>header {visibility: hidden;} .v-title { font-size: 50px; color: #FF8C00; text-align: center; font-weight: 900; text-transform: uppercase;} .thinking { color: #FF8C00; font-style: italic; animation: pulse 1s infinite; } @keyframes pulse { 0%, 100% { opacity: 0.2; } 50% { opacity: 1; } } .sidebar-clock { background: rgba(255, 140, 0, 0.1); border-left: 4px solid #FF8C00; padding: 10px; border-radius: 5px; margin-bottom: 20px; }</style>""", unsafe_allow_html=True)

# --- 3. LOGIN ---
if st.session_state.user_name is None:
    st.markdown('<div class="v-title">VEDA 3.0 ULTRA</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        name_in = st.text_input("IDENTIFY COMMANDER:", placeholder="Name...")
        if st.button("INITIALIZE 🚀", use_container_width=True):
            if name_in: st.session_state.user_name = name_in.strip(); st.rerun()
    st.stop()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align:center;'>🔱</h1><h2 style='text-align:center; color:#FF8C00;'>VEDA 3.0</h2>", unsafe_allow_html=True)
    
    # 🕒 CLOCK BAR
    st.markdown(f"""
        <div class="sidebar-clock">
            <p style="margin:0; font-size: 12px; color: #FF8C00; font-weight: bold;">📅 {datetime.now(ist).strftime("%A, %d %B %Y")}</p>
            <p style="margin:0; font-size: 20px; color: white; font-weight: 900;">{datetime.now(ist).strftime("%I:%M %p")}</p>
        </div>
    """, unsafe_allow_html=True)
    
    selected = option_menu(None, ["Medha (Chat)", "Srijan (Images)"], icons=["cpu", "image"], default_index=0, styles={"nav-link-selected": {"background-color": "#FF8C00"}})
    st.divider()
    if st.button("🗑️ Reset Core"): st.session_state.chat_history = []; st.rerun()

# --- 5. MAIN INTERFACE ---
st.markdown(f'<div class="v-title">{get_greeting()}, {st.session_state.user_name.upper()}</div>', unsafe_allow_html=True)

if selected == "Medha (Chat)":
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Command VEDA..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            status = st.empty()
            final_res = ""
            
            # 🏎️ IMPROVED FAILOVER (Switched order for speed)
            models = ["openai", "mistral", "claude", "llama"]
            
            for model in models:
                status.markdown(f'<p class="thinking">🔱 accessing {model} core...</p>', unsafe_allow_html=True)
                try:
                    p_enc = urllib.parse.quote(prompt); i_enc = urllib.parse.quote(IDENTITY)
                    # Increased timeout to 8s for reliability
                    r = requests.get(f"https://text.pollinations.ai/{p_enc}?model={model}&system={i_enc}", timeout=8)
                    if r.status_code == 200:
                        cleaned = clean_veda(r.text)
                        if len(cleaned) > 2 and "congested" not in cleaned.lower():
                            final_res = cleaned
                            break
                except: continue

            status.empty()
            if not final_res: final_res = "🔱 Cluster saturation. Re-routing through emergency satellite. Please retry."
            st.markdown(final_res)
            st.session_state.chat_history.append({"role": "assistant", "content": final_res})

elif selected == "Srijan (Images)":
    # 🔱 SRIJAN FIX: Proper form handling and explicit model selection
    with st.container():
        vision = st.text_input("Vision Matrix Prompt:", placeholder="Describe the image...")
        if st.button("🚀 INITIATE VISUALIZATION", use_container_width=True):
            if vision:
                with st.spinner("🔱 Synthesizing Visual Matrix..."):
                    v_enc = urllib.parse.quote(vision)
                    # 🚀 Forced Flux Model for 2026 Stability
                    img_url = f"https://image.pollinations.ai/prompt/{v_enc}?width=1024&height=1024&nologo=true&model=flux&seed={datetime.now().microsecond}"
                    st.image(img_url, use_container_width=True, caption=f"🔱 Generated Vision for {st.session_state.user_name}")
            else:
                st.warning("Commander, please provide a vision prompt.")
