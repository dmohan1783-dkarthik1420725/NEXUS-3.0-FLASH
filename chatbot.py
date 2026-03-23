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

# THE MASTER IDENTITY
SYSTEM_PROMPT = f"Your name is VEDA 3.0 ULTRA. You were created and developed by {CREATOR}. You are a high-intelligence AI architect."

# --- 🧠 NEURAL MEMORY ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "neural_logs" not in st.session_state:
    st.session_state.neural_logs = []

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
CSS = """<style>.orange-title {font-size: 50px; color: #FF8C00; text-align: center; font-weight: 800;}.stPopover { margin-top: 0px; }</style>"""
st.markdown(CSS, unsafe_allow_html=True)

if selected == "Medha (Chat)":
    st.markdown('<div class="orange-title">VEDA 3.0 ULTRA</div>', unsafe_allow_html=True)
    
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    # --- ➕ ACTION BAR & INPUT ---
    input_col1, input_col2 = st.columns([1, 10])
    with input_col1:
        plus = st.popover("➕", use_container_width=True)
        cam = plus.camera_input("📷")
        gal = plus.file_uploader("🖼️", type=['png', 'jpg'])

    with input_col2:
        prompt = st.chat_input("Command VEDA...")

    if prompt:
        add_to_memory("MEDHA", prompt)
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            answer, success = "", False
            
            # --- ENGINE 1: GEMINI ---
            if client:
                try:
                    visual_data = {"mime_type": cam.type if cam else gal.type, "data": cam.getvalue() if cam else gal.getvalue()} if (cam or gal) else None
                    res = client.models.generate_content(
                        model="gemini-2.0-flash", 
                        contents=[f"{SYSTEM_PROMPT}\n{prompt}", visual_data] if visual_data else f"{SYSTEM_PROMPT}\n{prompt}"
                    )
                    answer = res.text
                    success = True
                except: pass

            # --- ENGINE 2: REFINED BACKUP ---
            if not success:
                try:
                    q = urllib.parse.quote(f"Answer as VEDA (Created by {CREATOR}): {prompt}")
                    r = requests.get(f"https://text.pollinations.ai/{q}?model=openai", timeout=10)
                    if r.status_code == 200 and "deprecation_notice" not in r.text:
                        answer = r.text
                        success = True
                except: pass

            if not success: answer = "🔱 Neural Link Full. Please try in 5 seconds."
            
            st.markdown(answer)
            st.session_state.chat_history.append({"role": "assistant", "content": answer})

elif selected == "Srijan (Images)":
    st.markdown('<div class="orange-title">SRIJAN ARCHITECT</div>', unsafe_allow_html=True)
    v = st.text_input("Vision:")
    if st.button("🚀 RENDER"):
        if v:
            img = f"https://pollinations.ai/p/{urllib.parse.quote(v)}?width=1024&height=1024&seed=42&model=flux&nologo=true"
            st.image(img, use_container_width=True)
