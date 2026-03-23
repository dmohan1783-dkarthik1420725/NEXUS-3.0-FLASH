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
ist = pytz.timezone('Asia/Kolkata')

def get_now_full(): return datetime.now(ist).strftime("%A, %d %B %Y")
def get_now_time(): return datetime.now(ist).strftime("%I:%M %p")

SYSTEM_PROMPT = f"Your name is VEDA 3.0 ULTRA. Created and developed by {CREATOR}."

# --- 🧠 NEURAL MEMORY ---
if "neural_logs" not in st.session_state: st.session_state.neural_logs = []
if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "active_prompt" not in st.session_state: st.session_state.active_prompt = ""

def add_to_memory(m_type, content):
    ts = datetime.now(ist).strftime("%H:%M:%S")
    st.session_state.neural_logs.insert(0, {"time": ts, "type": m_type, "text": content})

# --- 🔑 INITIALIZATION ---
client = None
if "GOOGLE_API_KEY" in st.secrets:
    try:
        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    except: client = None

# --- 2. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 80px; margin-bottom:0;'>🔱</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; color: #FF8C00; margin-top:0;'>VEDA 3.0 ULTRA</h3>", unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style="background-color: rgba(255, 140, 0, 0.1); padding: 10px; border-radius: 10px; border-left: 5px solid #FF8C00; text-align: center;">
            <p style="margin:0; font-size: 12px; color: #FF8C00;">📅 {get_now_full()}</p>
            <p style="margin:0; font-size: 22px; color: white; font-weight: bold;">{get_now_time()}</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    selected = option_menu("CORE", ["Medha (Chat)", "Srijan (Images)"], icons=["cpu", "layers"], default_index=0)
    
    if st.button("🗑️ Wipe Neural Core"):
        st.session_state.chat_history = []
        st.session_state.neural_logs = []
        st.rerun()

# --- 3. MAIN INTERFACE ---
st.markdown("<style>.orange-title {font-size: 50px; color: #FF8C00; text-align: center; font-weight: 800; margin-bottom: 20px;}</style>", unsafe_allow_html=True)

if selected == "Medha (Chat)":
    st.markdown('<div class="orange-title">VEDA 3.0 ULTRA</div>', unsafe_allow_html=True)
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    prompt = st.chat_input("Command VEDA...")
    if prompt:
        add_to_memory("MEDHA", prompt)
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            answer, success = "", False
            if client:
                try:
                    res = client.models.generate_content(model="gemini-3.1-pro-preview", contents=f"{SYSTEM_PROMPT}\n{prompt}")
                    answer = res.text
                    success = True
                except: pass

            if not success:
                try:
                    q = urllib.parse.quote(prompt)
                    r = requests.get(f"https://text.pollinations.ai/{q}?model=openai", timeout=10)
                    answer = r.text
                    success = True
                except: answer = "🔱 Neural Link Busy."

            st.markdown(answer)
            st.session_state.chat_history.append({"role": "assistant", "content": answer})

elif selected == "Srijan (Images)":
    st.markdown('<div class="orange-title">SRIJAN ARCHITECT</div>', unsafe_allow_html=True)
    vision = st.text_input("Vision:", placeholder="Describe the masterpiece...")
    
    if st.button("🚀 RENDER"):
        if vision:
            add_to_memory("SRIJAN", vision)
            with st.spinner("🔱 Visualizing..."):
                try:
                    # Logic to ensure the Nexus logo text appears correctly
                    clean_v = urllib.parse.quote(vision)
                    
                    # Primary Stable Engine for 2026
                    img_url = f"https://image.pollinations.ai/prompt/{clean_v}?width=1024&height=1024&nologo=true&model=flux"
                    
                    # Display the image
                    st.image(img_url, caption=f"Rendering: {vision}", use_container_width=True)
                    st.balloons()
                    
                except Exception as e:
                    # Fixed: Added proper Exception handling to prevent SyntaxError
                    st.error(f"🔱 Architect is congested. Error: {e}")
