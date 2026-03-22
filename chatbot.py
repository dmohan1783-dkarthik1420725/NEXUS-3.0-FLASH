import streamlit as st
from google import genai
import requests
import urllib.parse
from datetime import datetime
import pytz
from streamlit_option_menu import option_menu

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="VEDA 3.0 ULTRA", page_icon="🔱", layout="wide")
CREATOR = "Dumpala Karthik"

# 🌍 GLOBAL TIME
ist = pytz.timezone('Asia/Kolkata')
def get_now():
    return datetime.now(ist).strftime("%I:%M %p")

# --- 🧠 NEURAL MEMORY ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "neural_logs" not in st.session_state:
    st.session_state.neural_logs = []

def add_to_memory(m_type, content):
    ts = datetime.now(ist).strftime("%H:%M:%S")
    log_entry = f"[{ts}] {m_type}: {content[:15]}..."
    st.session_state.neural_logs.insert(0, log_entry)

# --- 🔑 KEYS ---
p_key = st.query_params.get("api_key", st.secrets.get("POLLINATIONS_KEY", ""))

# --- 🧠 BRAIN CHECK ---
client = None
gemini_online = False
if "GOOGLE_API_KEY" in st.secrets:
    try:
        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
        gemini_online = True
    except: gemini_online = False

# --- 2. SIDEBAR ---
with st.sidebar:
    st.markdown(f"<h3 style='text-align: center; color: #FF8C00;'>VEDA 3.0 ULTRA</h3>", unsafe_allow_html=True)
    
    # 🛰️ LIVE HEALTH
    st.markdown("### 🛰️ System Health")
    st.write(f"Primary: {'🟢' if gemini_online else '🔴'}")
    st.write(f"Backup: {'🟢' if p_key else '🟡'}")
    
    if st.button("♻️ Reboot Neural Core"):
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
    
    # Show History
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Command VEDA..."):
        add_to_memory("MEDHA", prompt)
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            # 🚀 LIGHTWEIGHT IDENTITY
            short_id = f"Identity: VEDA AI. Creator: {CREATOR}. Time: {get_now()}."
            
            answer = ""
            success = False
            
            # --- BRAIN 1: GEMINI ---
            if client:
                try:
                    res = client.models.generate_content(model="gemini-1.5-flash-8b", contents=f"{short_id}\nUser: {prompt}")
                    answer = res.text
                    success = True
                except:
                    st.caption("🔄 Primary Busy. Rotating...")

            # --- BRAIN 2: TURBO BACKUP ---
            if not success:
                try:
                    q = urllib.parse.quote(prompt)
                    # Use 'p1' model - it's faster for basic chat
                    p_url = f"https://text.pollinations.ai/{q}?model=p1&system=You+are+VEDA+by+{CREATOR}"
                    if p_key: p_url += f"&key={p_key}"
                    
                    r = requests.get(p_url, timeout=20) # Long timeout
                    if r.status_code == 200:
                        answer = r.text
                    else:
                        answer = "⚠️ System traffic is very high. Please retry in a moment."
                except:
                    answer = "🔌 VEDA is re-syncing. One moment."

            st.markdown(answer)
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
