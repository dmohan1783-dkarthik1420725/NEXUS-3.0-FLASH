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
def get_now_full():
    return datetime.now(ist).strftime("%A, %d %B %Y")

def get_now_time():
    return datetime.now(ist).strftime("%I:%M %p")

# IDENTITY CHIP
IDENTITY = f"Your name is VEDA 3.0 ULTRA. Created and developed by {CREATOR}. Current time is {get_now_time()}."

# --- 🧠 NEURAL MEMORY INITIALIZATION ---
if "neural_logs" not in st.session_state:
    st.session_state.neural_logs = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def add_to_memory(m_type, content):
    ts = datetime.now(ist).strftime("%H:%M:%S")
    log_entry = {"time": ts, "type": m_type, "text": content}
    st.session_state.neural_logs.insert(0, log_entry)

# --- 🔑 KEY RETRIEVAL ---
p_key = st.query_params.get("api_key", st.secrets.get("POLLINATIONS_KEY", ""))

# --- 🧠 GEMINI INITIALIZATION ---
client = None
gemini_online = False
if "GOOGLE_API_KEY" in st.secrets:
    try:
        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
        gemini_online = True
    except Exception:
        gemini_online = False

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
            <p style="margin:0; font-size: 10px; color: #888;">SYSTEM TIME (IST)</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    # 🧠 NEURAL LOGS
    st.markdown("### 🧠 NEURAL LOGS")
    if st.session_state.neural_logs:
