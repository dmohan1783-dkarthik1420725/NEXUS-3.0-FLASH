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
IDENTITY = f"Your name is VEDA 3.0 ULTRA. Created and developed by {CREATOR}."

# --- 2. NEURAL MEMORY INITIALIZATION ---
if "neural_logs" not in st.session_state:
    st.session_state.neural_logs = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def add_to_memory(m_type, content):
    ts = datetime.now(ist).strftime("%H:%M:%S")
    st.session_state.neural_logs.insert(0, {"time": ts, "type": m_type, "text": content})

# --- 3. THE HEART: INITIALIZATION ---
client = None
api_status = "🔴 Offline"
if "GOOGLE_API_KEY" in st.secrets:
    try:
        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
        api_status = "🟢 Ready (2.0 Flash)"
    except Exception as e:
        api_status = f"❌ Error: {str(e)[:20]}"

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 80px; margin-bottom:0;'>🔱</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; color: #FF8C00; margin-top:0;'>VEDA 3.0 ULTRA</h3>", unsafe_allow_html=True)
    st.info(f"🛰️ System: {api_status}")
    st.markdown(f"📅 **{get_now_full()}**\n\n🕒 **{get_now_time()} IST**")
    
    st.divider()
    st.markdown("### 🧠 NEURAL LOGS")
    for log in st.session_state.neural_logs[:5]:
        st.code(f"{log['time']} | {log['text'][:15]}...", language="text")

    if st.button("🗑️ Wipe Neural Core"):
        st.session_state.chat_history = []
        st.session_state.neural_logs = []
        st.rerun()

    st.divider()
    selected = option_menu(None, ["Medha (Chat)", "Srijan (Images)"], icons=["cpu", "layers"], default_index=0)

# --- 5. MAIN INTERFACE ---
ORANGE_TITLE = "<style>.orange-title {font-size: 50px; color: #FF8C00; text-align: center; font-weight: 800; margin-bottom: 20px;}.stPopover { margin-top: 23px; }</style>"

if selected == "Medha (Chat)":
    st.markdown(ORANGE_TITLE, unsafe_allow_html=True)
    st.markdown('<div class="orange-title">VEDA 3.0 ULTRA</div>', unsafe_allow_html=True)
    
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    # --- ➕ ACTION BAR (Left Lower Side) ---
    st.markdown("---")
    act_col1, act_col2 = st.columns([1, 12])
    with act_col1:
        plus_menu = st.popover("➕", use_container_width=True)
        cam_file = plus_menu.camera_input("📷 Camera")
        gal_file = plus_menu.file_uploader("🖼️ Gallery", type=['png', 'jpg', 'jpeg'])
        doc_file = plus_menu.file_uploader("📁 Files", type=['pdf', 'txt'])

    active_visual = cam_file or gal_file
    if active_visual:
        st.image(active_visual, caption="📎 Attachment Ready", width=150)

    # 📥 MAIN CHAT INPUT
    if prompt := st.chat_input("Command VEDA..."):
        add_to_memory("MEDHA", prompt)
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            answer = ""
            success = False
            time_ctx = f"Time: {get_now_time()} IST."
            
            # --- ENGINE 1: GEMINI 2.0 FLASH (Silent) ---
            if client:
                try:
                    vision_content = [f"{IDENTITY}\n{time_ctx}\n\nUser: {prompt}", active_visual] if active_visual else f"{IDENTITY}\n{time_ctx}\n\nUser: {prompt}"
                    res = client.models.generate_content(model="gemini-2.0-flash", contents=vision_content)
                    answer = res.text
                    success = True
                except: pass

            # --- ENGINE 2: MISTRAL (Text Fallback) ---
            if not success:
                try:
                    q_enc = urllib.parse.quote(f"Vision busy. Answer as VEDA: {prompt}")
                    r = requests.get(f"https://text.pollinations.ai/{q_enc}?model=mistral&system={urllib.parse.quote(IDENTITY)}", timeout=7)
                    if r.status_code == 200:
                        prefix = "⚠️ *Vision Engine Busy (Text Analysis):*\n\n" if active_visual else ""
                        answer = prefix + r.text
                        success = True
                except: pass

            # --- ENGINE 3: LLAMA ---
            if not success:
                try:
                    q_enc = urllib.parse.quote(prompt)
                    r = requests.get(f"https://text.pollinations.ai/{q_enc}?model=llama&system={urllib.parse.quote(IDENTITY)}", timeout=7)
                    if r.status_code == 200:
                        answer = r.text
                        success = True
                except: pass

            if not success:
                answer = "🔱 Connection lines are heavy. Please try again in 10s."

            st.markdown(answer)
            st.session_state.chat_history.append({"role": "assistant", "content": answer})

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
                    img = f"https://gen.pollinations.ai/image/{v_enc}?width=1024&height=1024&nologo=true&model=flux"
                    st.image(img, caption=f"Created by {CREATOR}", use_column_width=True)
                    st.balloons()
                except: st.error("Architect Busy.")
