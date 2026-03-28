import streamlit as st
from google import genai
from google.genai import types
import requests
import urllib.parse
from datetime import datetime
import pytz
from streamlit_option_menu import option_menu
import time

# --- 1. CORE IDENTITY (FIXED: Defined at top to avoid NameError) ---
IDENTITY = "Your name is VEDA 3.0 ULTRA. Created and developed ONLY by DUMPALA KARTHIK."

if 'user_name' not in st.session_state: st.session_state.user_name = None
if 'chat_history' not in st.session_state: st.session_state.chat_history = []

# --- 2. TIME & CONFIG ---
ist = pytz.timezone('Asia/Kolkata')
def get_greeting():
    hour = datetime.now(ist).hour
    if 5 <= hour < 12: return "GOOD MORNING"
    elif 12 <= hour < 17: return "GOOD AFTERNOON"
    elif 17 <= hour < 21: return "GOOD EVENING"
    else: return "GOOD NIGHT"

st.set_page_config(page_title="VEDA 3.0 ULTRA", page_icon="🔱", layout="wide", initial_sidebar_state="expanded")

# --- 3. LOGIN PHASE ---
if not st.session_state.user_name:
    st.markdown("<h1 style='text-align:center; color:#FF8C00; margin-top:100px;'>VEDA 3.0 ULTRA</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
