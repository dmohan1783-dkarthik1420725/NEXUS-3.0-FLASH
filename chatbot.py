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

# MASTER IDENTITY
SYSTEM_PROMPT = f"Your name is VEDA 3.0 ULTRA. You were created and developed by {CREATOR}."

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
    selected = option_menu("CORE", ["Medha (Chat)", "Srijan (Images)"], 
                          icons=["cpu", "layers"], default_index=0)
    
    if st.button("🗑️ Wipe Neural Core"):
        st.session_state.chat_history = []
        st.session_state.neural_logs = []
        st.rerun()

# --- 3. MAIN INTERFACE ---
CSS = """
<style>
    .orange-title {font-size: 50px; color: #FF8C00; text-align: center; font-weight: 800;}
    /* Fix for the (+) button to align with bottom chat input */
    .stPopover { position: fixed; bottom: 85px; left: 50px; z-index: 1000; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

if selected == "Medha (Chat)":
    st.markdown('<div class="orange-title">VEDA 3.0 ULTRA</div>', unsafe_allow_html=True)
    
    # 🗨️ Chat History Container
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    # --- ➕ BOTTOM FACILITY (Fixed position) ---
    plus = st.popover("➕")
    cam = plus.camera_input("Take Photo")
    gal = plus.file_uploader("Upload Image", type=['png', 'jpg'])

    # 📥 BOTTOM SEARCH BAR (st.chat_input is always at the bottom by default)
    if prompt := st.chat_input("Command VEDA..."):
        add_to_memory("MEDHA", prompt)
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            answer, success = "", False
            
            # Processing Image Bytes
            visual_data = None
            if cam or gal:
                file = cam if cam else gal
                visual_data = {"mime_type": file.type, "data": file.getvalue()}

            if client:
                try:
                    # Using 2.0 Flash for maximum speed and stability
                    res = client.models.generate_content(
                        model="gemini-2.0-flash", 
                        contents=[f"{SYSTEM_PROMPT}\n{prompt}", visual_data] if visual_data else f"{SYSTEM_PROMPT}\n{prompt}"
                    )
                    answer = res.text
                    success = True
                except: pass

            # Safe Fallback to Text API
            if not success:
                try:
                    q = urllib.parse.quote(f"Response as VEDA (Created by {CREATOR}): {prompt}")
                    r = requests.get(f"https://text.pollinations.ai/{q}?model=openai", timeout=12)
                    if r.status_code == 200 and "deprecation_notice" not in r.text:
                        answer = r.text
                        success = True
                except: pass

            if not success: 
                answer = "🔱 **Neural Link Stabilizing.** Please wait 5 seconds and retry."
            
            st.markdown(answer)
            st.session_state.chat_history.append({"role": "assistant", "content": answer})

elif selected == "Srijan (Images)":
    st.markdown('<div class="orange-title">SRIJAN ARCHITECT</div>', unsafe_allow_html=True)
    v = st.text_input("Vision:")
    if st.button("🚀 RENDER"):
        if v:
            img = f"https://pollinations.ai/p/{urllib.parse.quote(v)}?width=1024&height=1024&seed=42&model=flux&nologo=true"
            st.image(img, use_container_width=True)
