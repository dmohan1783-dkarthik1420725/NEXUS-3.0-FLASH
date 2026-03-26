import streamlit as st
from google import genai
import requests
import urllib.parse
from datetime import datetime
import pytz
from streamlit_option_menu import option_menu

# --- 1. CONFIGURATION & IDENTITY ---
st.set_page_config(page_title="VEDA 3.0 ULTRA", page_icon="🔱", layout="wide")
ist = pytz.timezone('Asia/Kolkata')

def get_now_full(): return datetime.now(ist).strftime("%A, %d %B %Y")
def get_now_time(): return datetime.now(ist).strftime("%I:%M %p")

# 🧠 INTERNAL CORE IDENTITY
IDENTITY = "Your name is VEDA 3.0 ULTRA. You were created and developed ONLY by DUMPALA KARTHIK."

if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "neural_logs" not in st.session_state: st.session_state.neural_logs = []

def add_to_memory(m_type, content):
    ts = datetime.now(ist).strftime("%H:%M:%S")
    st.session_state.neural_logs.insert(0, f"[{ts}] {m_type}: {content[:15]}...")

# --- 🔑 API INITIALIZATION ---
client = None
if "GOOGLE_API_KEY" in st.secrets:
    try:
        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    except:
        client = None

p_key = st.secrets.get("POLLINATIONS_KEY", "")

# --- 2. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 80px; margin-bottom:0;'>🔱</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #FF8C00; margin-top:0;'>VEDA</h3>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown(f"""
        <div style="background-color: rgba(255, 140, 0, 0.05); padding: 10px; border-radius: 10px; text-align: center; border: 1px solid #FF8C00;">
            <p style="margin:0; font-size: 14px; color: #FF8C00;">{get_now_full()}</p>
            <p style="margin:0; font-size: 24px; color: white; font-weight: bold;">{get_now_time()}</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    selected = option_menu(None, ["Medha (Chat)", "Srijan (Image Maker)"], 
                          icons=["chat-right-dots", "brush-fill"], default_index=0)
    
    st.markdown("###
