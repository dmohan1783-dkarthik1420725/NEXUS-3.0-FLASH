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

# 🌍 Live Time Sync (IST)
ist = pytz.timezone('Asia/Kolkata')
def get_now():
    return datetime.now(ist).strftime("%A, %d %B %Y, %I:%M %p")

# --- 🧠 NEURAL MEMORY INITIALIZATION ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "neural_logs" not in st.session_state:
    st.session_state.neural_logs = []

def add_to_memory(m_type, content):
    # Fixed the variable name here to ensure it uses the function correctly
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
    except Exception: 
        client = None

# --- 2. SIDEBAR ---
with st.sidebar:
    st.markdown(f"<h3 style='text-align: center; color: #FF8C00;'>VEDA 3.0 ULTRA</h3>", unsafe_allow_html=True)
    st.info(f"📅 {get_now()}")
    
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

if selected == "Medha (Chat)":
    st.markdown(ORANGE_TITLE, unsafe_allow_html=True)
    st.markdown('<div class="orange-title">VEDA 3.0 ULTRA</div>', unsafe_allow_html=True)
    
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Command VEDA..."):
        add_to_memory("MEDHA", prompt)
        
        # 🆔 Variable names fixed to prevent NameError
        current_date_time = get_now()
        context_prompt = f"System: You are VEDA 3.0 ULTRA by {CREATOR}. Time: {current_date_time}. User: {prompt}"
        
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            answer = ""
            success = False
            
            # --- PRIMARY: GEMINI ---
            if client:
                try:
                    res = client.models.generate_content(model="gemini-1.5-flash-8b", contents=context_prompt)
                    answer = res.text
                    success = True
                except Exception: 
                    st.caption("🔄 Rotating...")

            # --- BACKUP: POLLINATIONS ---
            if not success:
                try:
                    q_safe = urllib.parse.quote(context_prompt)
                    p_url = f"https://text.pollinations.ai/{q_safe}?model=openai&system=AI"
                    if p_key: p_url += f"&key={p_key}"
                    
                    r = requests.get(p_url, timeout=12)
                    if r.status_code == 200:
                        answer = r.text
                    else:
                        answer = f"Error {r.status_code}: System busy."
                except Exception: 
                    answer = "Connection Interrupt."

            # Clean and Display
            final_response = str(answer).split("stmodulestreamlit")[0].strip()
            st.markdown(final_response)
            st.session_state.chat_history.append({"role": "assistant", "content": final_response})

elif selected == "Srijan (Images)":
    st.markdown(ORANGE_TITLE, unsafe_allow_html=True)
    st.markdown('<div class="orange-title">SRIJAN ARCHITECT</div>', unsafe_allow_html=True)
    
    if not p_key:
