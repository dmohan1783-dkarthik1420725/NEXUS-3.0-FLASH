import streamlit as st
from google import genai
import requests
import urllib.parse
from datetime import datetime
import pytz
import time
from streamlit_option_menu import option_menu

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="VEDA 3.0 ULTRA", page_icon="🔱", layout="wide")
CREATOR = "Dumpala Karthik"
ist = pytz.timezone('Asia/Kolkata')
def get_now_time(): return datetime.now(ist).strftime("%I:%M %p")

IDENTITY = f"Your name is VEDA 3.0 ULTRA. Created by {CREATOR}."

# --- 2. SESSION STATE ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- 3. INITIALIZATION ---
client = None
if "GOOGLE_API_KEY" in st.secrets:
    try:
        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    except: client = None

# --- 4. INTERFACE ---
ORANGE_TITLE = "<style>.orange-title {font-size: 50px; color: #FF8C00; text-align: center; font-weight: 800; margin-bottom: 20px;}.stPopover { margin-top: 23px; }</style>"
st.markdown(ORANGE_TITLE, unsafe_allow_html=True)
st.markdown('<div class="orange-title">VEDA 3.0 ULTRA</div>', unsafe_allow_html=True)

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

# --- ➕ ACTION BAR ---
act_col1, act_col2 = st.columns([1, 12])
with act_col1:
    plus_menu = st.popover("➕", use_container_width=True)
    cam_file = plus_menu.camera_input("📷 Camera")
    gal_file = plus_menu.file_uploader("🖼️ Gallery", type=['png', 'jpg', 'jpeg'])

active_visual = cam_file or gal_file
if active_visual: st.image(active_visual, width=150)

# 📥 MAIN CHAT INPUT
if prompt := st.chat_input("Command VEDA..."):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    
    with st.chat_message("assistant"):
        answer = ""
        success = False
        
        # --- 🚀 ENGINE 1: GEMINI PIPELINE (3.1 -> 2.0 -> 1.5) ---
        if client:
            model_pipeline = ["gemini-3.1-pro-preview", "gemini-3.1-flash-lite-preview", "gemini-2.0-flash", "gemini-1.5-flash"]
            for model_choice in model_pipeline:
                try:
                    # Give each 3.1 model 2 attempts with a tiny delay
                    for attempt in range(2):
                        try:
                            config = {"thinking_level": "minimal"} if "3.1" in model_choice else None
                            res = client.models.generate_content(
                                model=model_choice,
                                contents=[f"{IDENTITY}\nAnalyze: {prompt}", active_visual] if active_visual else f"{IDENTITY}\n{prompt}",
                                config=config
                            )
                            answer = res.text
                            success = True
                            break
                        except:
                            time.sleep(1) 
                    if success: break
                except: continue

        # --- 🛡️ ENGINE 2: MISTRAL (Silent Backup) ---
        if not success or "IMPORTANT NOTICE" in answer:
            try:
                q_enc = urllib.parse.quote(prompt)
                r = requests.get(f"https://text.pollinations.ai/{q_enc}?model=mistral", timeout=10)
                # Check if it's a real answer or the deprecation notice
                if r.status_code == 200 and "IMPORTANT NOTICE" not in r.text:
                    answer = r.text
                    success = True
            except: pass

        # --- 🛡️ ENGINE 3: LLAMA (Final Fail-Safe) ---
        if not success or "IMPORTANT NOTICE" in answer:
            try:
                r = requests.get(f"https://text.pollinations.ai/{q_enc}?model=llama", timeout=10)
                if r.status_code == 200 and "IMPORTANT NOTICE" not in r.text:
                    answer = r.text
                    success = True
            except: pass

        if not success or "IMPORTANT NOTICE" in answer:
            answer = "🔱 **Neural Synchronizing.** The 3.1 links are currently full. Please try your command again in 5 seconds."

        st.markdown(answer)
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
