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

# --- 🧠 NEURAL MEMORY INITIALIZATION ---
# This stores the full chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
# This stores the sidebar "Memory Fragments" (Short logs)
if "neural_logs" not in st.session_state:
    st.session_state.neural_logs = []

# Function to add to sidebar memory
def add_to_memory(type, content):
    timestamp = datetime.now(ist).strftime("%H:%M:%S")
    log_entry = f"[{timestamp}] {type}: {content[:20]}..."
    st.session_state.neural_logs.insert(0, log_entry) # Add newest to top

# --- 🔑 KEY RETRIEVAL ---
p_key = st.query_params.get("api_key", st.secrets.get("POLLINATIONS_KEY", ""))

# --- 2. SIDEBAR (The Neural Memory Bank) ---
with st.sidebar:
    st.markdown(f"<h3 style='text-align: center; color: #FF8C00;'>VEDA 3.0 ULTRA</h3>", unsafe_allow_html=True)
    st.caption(f"Architect: {CREATOR}")
    
    st.divider()
    st.markdown("### 🧠 NEURAL MEMORY LOG")
    # Display the last 10 activities
    if st.session_state.neural_logs:
        for log in st.session_state.neural_logs[:10]:
            st.code(log, language="text")
    else:
        st.write("Memory is empty...")

    if st.button("🗑️ Wipe Memory"):
        st.session_state.chat_history = []
        st.session_state.neural_logs = []
        st.rerun()

    st.divider()
    selected = option_menu(None, ["Medha (Chat)", "Srijan (Images)", "Veda (Hub)"], 
                          icons=["cpu", "layers", "share"], default_index=0)

# --- 3. MAIN INTERFACE ---
ORANGE_TITLE = "<style>.orange-title {font-size: 50px; color: #FF8C00; text-align: center; font-weight: 800;}</style>"

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
            # Try Brain Rotation (Gemini -> Pollinations)
            # [Insert your existing logic for client.models.generate_content here]
            # For this example, let
