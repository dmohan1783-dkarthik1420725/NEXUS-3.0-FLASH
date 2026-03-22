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

# Time Setup (IST)
ist = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(ist).strftime("%I:%M %p")

# 🆔 IDENTITY CHIP
IDENTITY = f"Your name is VEDA 3.0 ULTRA. Created by {CREATOR}. Current time: {current_time}."

# --- 🧠 NEURAL MEMORY INITIALIZATION ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "neural_logs" not in st.session_state:
    st.session_state.neural_logs = []

def add_to_memory(m_type, content):
    timestamp = datetime.now(ist).strftime("%H:%M:%S")
    log_entry = f"[{timestamp}] {m_type}: {content[:15]}..."
    st.session_state.neural_logs.insert(0, log_entry)

# --- 🔑 KEY RETRIEVAL ---
p_key = st.query_params.get("api_key", st.secrets.get("POLLINATIONS_KEY", ""))

# --- 🧠 GEMINI INITIALIZATION ---
client = None
if "GOOGLE_API_KEY" in st.secrets:
    try:
        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    except: client = None

# --- 2. SIDEBAR (Neural Memory Bank) ---
with st.sidebar:
    st.markdown(f"<h3 style='text-align: center; color: #FF8C00;'>VEDA 3.0 ULTRA</h3>", unsafe_allow_html=True)
    st.info(f"🕒 {current_time}")
    
    st.divider()
    st.markdown("### 🧠 NEURAL MEMORY")
    for log in st.session_state.neural_logs[:8]:
        st.code(log, language="text")

    if st.button("🗑️ Wipe Memory"):
        st.session_state.chat_history = []
        st.session_state.neural_logs = []
        st.rerun()

    st.divider()
    selected = option_menu(None, ["Medha (Chat)", "Srijan (Images)", "Veda (Hub)"], 
                          icons=["cpu", "layers", "share"], default_index=0)

# --- 3. MAIN INTERFACE ---
ORANGE_TITLE = "<style>.orange-title {font-size: 50px; color: #FF8C00; text-align: center; font-weight: 800; margin-bottom: 30px;}</style>"

# [TAB 1: MEDHA CHAT]
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
            answer = ""
            success = False
            
            # --- PRIMARY: GEMINI ---
            if client:
                try:
                    res = client.models.generate_content(model="gemini-1.5-flash-8b", contents=f"{IDENTITY}\n\nUser: {prompt}")
                    answer = res.text
                    success = True
                except: st.caption("🔄 Rotating...")

            # --- BACKUP: POLLINATIONS ---
            if not success:
                try:
                    q = urllib.parse.quote(prompt)
                    sys_msg = urllib.parse.quote(IDENTITY)
                    p_url = f"https://gen.pollinations.ai/text/{q}?model=mistral&system={sys_msg}"
                    if p_key: p_url += f"&key={p_key}"
                    r = requests.get(p_url, timeout=12)
                    answer = r.text
                except: answer = "System Offline."

            # ✨ CLEANING LOGIC ✨
            # We strip any accidental Streamlit object mentions to stop the "Help" wall
            final_response = str(answer).split("stmodulestreamlit")[0].strip()
            
            st.markdown(final_response)
            st.session_state.chat_history.append({"role": "assistant", "content": final_response})

# [TAB 2: SRIJAN ARCHITECT]
elif selected == "Srijan (Images)":
    st.markdown(ORANGE_TITLE, unsafe_allow_html=True)
    st.markdown('<div class="orange-title">SRIJAN ARCHITECT</div>', unsafe_allow_html=True)
    
    vision = st.text_input("Vision:", placeholder="Describe your image...")
    if st.button("🚀 RENDER"):
        if vision:
            add_to_memory("SRIJAN", vision)
            with st.spinner("Visualizing..."):
                try:
                    v_enc = urllib.parse.quote(vision)
                    img = f"https://gen.pollinations.ai/image/{v_enc}?width=1024&height=1024&nologo=true&model=flux&key={p_key}"
                    st.image(img, caption=f"Created by {CREATOR}", use_column_width=True)
                    st.balloons()
                except: st.error("Architect Busy.")

# [TAB 3: VEDA HUB]
elif selected == "Veda (Hub)":
    st.markdown(ORANGE_TITLE, unsafe_allow_html=True)
    st.markdown('<div class="orange-title">VEDA NETWORK HUB</div>', unsafe_allow_html=True)
    st.write(f"Architect: {CREATOR}")
