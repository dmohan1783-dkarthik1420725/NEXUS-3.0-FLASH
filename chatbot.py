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

# --- 2. NEURAL MEMORY INITIALIZATION ---
if "neural_logs" not in st.session_state:
    st.session_state.neural_logs = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def add_to_memory(m_type, content):
    ts = datetime.now(ist).strftime("%H:%M:%S")
    log_entry = {"time": ts, "type": m_type, "text": content}
    st.session_state.neural_logs.insert(0, log_entry)

# --- 3. KEY RETRIEVAL ---
p_key = st.query_params.get("api_key", st.secrets.get("POLLINATIONS_KEY", ""))

# --- 4. GEMINI INITIALIZATION ---
client = None
gemini_online = False
if "GOOGLE_API_KEY" in st.secrets:
    try:
        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
        gemini_online = True
    except Exception:
        gemini_online = False

# --- 5. SIDEBAR ---
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
        for log in st.session_state.neural_logs[:5]:
            st.code(f"{log['time']} | {log['text'][:15]}...", language="text")
    else:
        st.caption("Neural fragments offline.")

    if st.button("🗑️ Wipe Neural Core"):
        st.session_state.chat_history = []
        st.session_state.neural_logs = []
        st.rerun()

    st.divider()
    selected = option_menu(None, ["Medha (Chat)", "Srijan (Images)"], 
                          icons=["cpu", "layers"], default_index=0)

# --- 6. MAIN INTERFACE ---
ORANGE_TITLE = "<style>.orange-title {font-size: 50px; color: #FF8C00; text-align: center; font-weight: 800; margin-bottom: 20px;}</style>"

if selected == "Medha (Chat)":
    st.markdown(ORANGE_TITLE, unsafe_allow_html=True)
    st.markdown('<div class="orange-title">VEDA 3.0 ULTRA</div>', unsafe_allow_html=True)
    
    # Render History
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]): 
            st.markdown(msg["content"])

    # --- 📸 MULTIMEDIA INPUT AREA ---
    st.markdown("---")
    multi_cols = st.columns([1, 1, 1, 1, 6]) 
    
    with multi_cols[0]:
        cam_pop = st.popover("📷")
        cam_file = cam_pop.camera_input("Capture Vision")
    
    with multi_cols[1]:
        gal_pop = st.popover("🖼️")
        gal_file = gal_pop.file_uploader("Gallery", type=['png', 'jpg', 'jpeg'])

    with multi_cols[2]:
        file_pop = st.popover("📁")
        doc_file = file_pop.file_uploader("Upload Files", type=['pdf', 'txt', 'docx'])

    with multi_cols[3]:
        if st.button("🎤"):
            st.toast("Voice synthesis initializing...")

    # Visual Preview Logic
    active_visual = cam_file or gal_file
    if active_visual:
        st.image(active_visual, caption="Visual Data Detected", width=200)

    # 📥 MAIN CHAT INPUT
    if prompt := st.chat_input("Command VEDA..."):
        add_to_memory("MEDHA", prompt)
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): 
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            answer = ""
            success = False
            time_ctx = f"Current Time: {get_now_time()} IST."
            
            # --- BRAIN 1: GEMINI (Multi-Modal Support) ---
            if client:
                try:
                    sys_msg = f"{IDENTITY}\n{time_ctx}\n\nUser: {prompt}"
                    content_list = [sys_msg]
                    if active_visual:
                        content_list.append(active_visual)
                    
                    res = client.models.generate_content(
                        model="gemini-1.5-flash-8b", 
                        contents=content_list
                    )
                    answer = res.text
                    success = True
                except Exception: 
                    st.caption("🔄 Rotating Brain...")

            # --- BRAIN 2: BACKUP (Pollinations) ---
            if not success:
                try:
                    q_enc = urllib.parse.quote(prompt)
                    p_url = f"https://text.pollinations.ai/{q_enc}?model=openai"
                    r = requests.get(p_url, timeout=15)
                    answer = r.text if r.status_code == 200 else "⚠️ System Overload."
                except Exception: 
                    answer = "Connection Interrupted."

            st.markdown(answer)
            st.session_state.chat_history.append({"role": "assistant", "content": answer})

elif selected == "Srijan (Images)":
    st.markdown(ORANGE_TITLE, unsafe_allow_html=True)
    st.markdown('<div class="orange-title">SRIJAN ARCHITECT</div>', unsafe_allow_html=True)
    
    if not p_key:
        st.warning("⚠️ Please connect in the sidebar first.")
    else:
        vision = st.text_input("Vision:", placeholder="Describe your image...")
        if st.button("🚀 RENDER"):
            if vision:
                add_to_memory("SRIJAN", vision)
                with st.spinner("Visualizing..."):
                    try:
                        v_enc = urllib.parse.quote(vision)
                        img = f"https://gen.pollinations.ai/image/{v_enc}?width=1024&height=1024&nologo=true&model=flux&key={p_key}"
                        st.image(img, caption=f"Created by {CREATOR}", use_column_width=True)
                        st.balloons()
                    except Exception: 
                        st.error("Architect Busy.")
