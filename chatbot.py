import streamlit as st
from google import genai
import requests
import urllib.parse
from datetime import datetime
import pytz
from streamlit_option_menu import option_menu

# --- 1. CONFIGURATION & IDENTITY ---
st.set_page_config(page_title="VEDA 3.0 ULTRA", page_icon="🔱", layout="wide")
CREATOR = "Dumpala Karthik"

# 🌍 GLOBAL TIME SYNC (IST)
ist = pytz.timezone('Asia/Kolkata')
def get_now_full(): return datetime.now(ist).strftime("%A, %d %B %Y")
def get_now_time(): return datetime.now(ist).strftime("%I:%M %p")

# IDENTITY CHIP
IDENTITY = f"Your name is VEDA 3.0 ULTRA. Created and developed ONLY by {CREATOR}."

# --- 🧠 NEURAL MEMORY INITIALIZATION ---
if "neural_logs" not in st.session_state: st.session_state.neural_logs = []
if "chat_history" not in st.session_state: st.session_state.chat_history = []

def add_to_memory(m_type, content):
    ts = datetime.now(ist).strftime("%H:%M:%S")
    log_entry = f"[{ts}] {m_type}: {content[:15]}..."
    st.session_state.neural_logs.insert(0, log_entry)

# --- 🧠 GEMINI INITIALIZATION ---
client = None
gemini_online = False
if "GOOGLE_API_KEY" in st.secrets:
    try:
        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
        gemini_online = True
    except: gemini_online = False

# --- 2. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 80px; margin-bottom:0;'>🔱</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; color: #FF8C00; margin-top:0;'>VEDA 3.0 ULTRA</h3>", unsafe_allow_html=True)
    
    # 🕒 SIDEBAR CLOCK WIDGET
    st.markdown("---")
    st.markdown(f"""
        <div style="background-color: rgba(255, 140, 0, 0.1); padding: 15px; border-radius: 10px; border-left: 5px solid #FF8C00; text-align: center;">
            <p style="margin:0; font-size: 13px; color: #FF8C00; font-weight: bold;">📅 {get_now_full()}</p>
            <p style="margin:5px 0 0 0; font-size: 26px; color: white; font-weight: 800;">{get_now_time()}</p>
        </div>
    """, unsafe_allow_html=True)

    # 🛰️ SYSTEM HEALTH
    st.markdown("### 🛰️ System Health")
    st.write(f"Primary Brain: {'🟢' if gemini_online else '🔴'}")
    st.write(f"Backup Link: 🟢")
    
    st.divider()
    
    # 🧠 NEURAL LOGS
    st.markdown("### 🧠 NEURAL LOGS")
    if st.session_state.neural_logs:
        for log in st.session_state.neural_logs[:8]:
            st.code(log, language="text")
    else: st.caption("No fragments found.")

    if st.button("🗑️ Wipe Neural Core"):
        st.session_state.chat_history = []
        st.session_state.neural_logs = []
        st.rerun()

    st.divider()
    selected = option_menu(None, ["Medha (Chat)", "Srijan (Images)"], 
                          icons=["cpu", "layers"], default_index=0)

# --- 3. MAIN INTERFACE ---
ORANGE_TITLE = "<style>.orange-title {font-size: 50px; color: #FF8C00; text-align: center; font-weight: 800;}</style>"

if selected == "Medha (Chat)":
    st.markdown(ORANGE_TITLE, unsafe_allow_html=True)
    st.markdown('<div class="orange-title">VEDA 3.0 ULTRA</div>', unsafe_allow_html=True)
    
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Command VEDA..."):
        add_to_memory("MEDHA", prompt)
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            answer, success = "", False
            time_ctx = f"Current Time: {get_now_time()} IST."
            
            # --- BRAIN 1: GEMINI 2.5 PRO ---
            if gemini_online:
                try:
                    res = client.models.generate_content(
                        model="gemini-2.5-pro", 
                        contents=f"{IDENTITY}\n{time_ctx}\n\nUser: {prompt}"
                    )
                    answer = res.text
                    success = True
                except: st.caption("🔄 Rotating Brain...")

            # --- BRAIN 2: GPT-4 BACKUP ---
            if not success:
                try:
                    q_enc = urllib.parse.quote(prompt)
                    sys_enc = urllib.parse.quote(f"{IDENTITY} {time_ctx}")
                    p_url = f"https://text.pollinations.ai/{q_enc}?model=openai&system={sys_enc}"
                    r = requests.get(p_url, timeout=15)
                    if r.status_code == 200 and "{" not in r.text[:10]:
                        answer = r.text
                        success = True
                    else: answer = "⚠️ System overload. Please retry."
                except: answer = "Connection Interrupted."

            st.markdown(answer)
            st.session_state.chat_history.append({"role": "assistant", "content": answer})

elif selected == "Srijan (Images)":
    st.markdown(ORANGE_TITLE, unsafe_allow_html=True)
    st.markdown('<div class="orange-title">SRIJAN ARCHITECT</div>', unsafe_allow_html=True)
    
    vision = st.text_input("Vision:", placeholder="Describe your masterpiece...")
    if st.button("🚀 RENDER"):
        if vision:
            add_to_memory("SRIJAN", vision)
            with st.spinner("Visualizing..."):
                try:
                    v_enc = urllib.parse.quote(vision)
                    # Locked to Flux 2026 Engine
                    img = f"https://image.pollinations.ai/prompt/{v_enc}?width=1024&height=1024&nologo=true&model=flux"
                    st.image(img, caption=f"Architect: {CREATOR}", use_container_width=True)
                    st.balloons()
                    st.markdown(f"**[📥 Download Image]({img})**")
                except: st.error("Architect Busy.")
