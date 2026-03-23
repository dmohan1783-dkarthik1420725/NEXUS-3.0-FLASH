import streamlit as st
from google import genai
import requests
import urllib.parse
from datetime import datetime
import pytz
import time
from streamlit_option_menu import option_menu

# --- 1. CONFIGURATION & IDENTITY ---
st.set_page_config(page_title="VEDA 3.0 ULTRA", page_icon="🔱", layout="wide")
CREATOR = "Dumpala Karthik"

ist = pytz.timezone('Asia/Kolkata')
def get_now_full(): return datetime.now(ist).strftime("%A, %d %B %Y")
def get_now_time(): return datetime.now(ist).strftime("%I:%M %p")

IDENTITY = f"Your name is VEDA 3.0 ULTRA. Created and developed by {CREATOR}."

# --- 🧠 NEURAL MEMORY & HISTORY ---
if "neural_logs" not in st.session_state:
    st.session_state.neural_logs = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "active_prompt" not in st.session_state:
    st.session_state.active_prompt = ""

def add_to_memory(m_type, content):
    ts = datetime.now(ist).strftime("%H:%M:%S")
    st.session_state.neural_logs.insert(0, {"time": ts, "type": m_type, "text": content})

# --- 🔑 GEMINI INITIALIZATION ---
client = None
if "GOOGLE_API_KEY" in st.secrets:
    try:
        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    except: client = None

# --- 2. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 80px; margin-bottom:0;'>🔱</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; color: #FF8C00; margin-top:0;'>VEDA 3.0 ULTRA</h3>", unsafe_allow_html=True)
    
    # 🕒 SIDEBAR CLOCK
    st.markdown(f"""
        <div style="background-color: rgba(255, 140, 0, 0.1); padding: 10px; border-radius: 10px; border-left: 5px solid #FF8C00; text-align: center;">
            <p style="margin:0; font-size: 12px; color: #FF8C00;">📅 {get_now_full()}</p>
            <p style="margin:0; font-size: 22px; color: white; font-weight: bold;">{get_now_time()}</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("### 🧠 NEURAL MEMORY")
    st.caption("Click to reload a memory")
    for i, log in enumerate(st.session_state.neural_logs[:8]):
        if st.button(f"🕒 {log['time']} | {log['text'][:15]}...", key=f"log_{i}", use_container_width=True):
            st.session_state.active_prompt = log['text']
            st.rerun() 
    
    st.divider()
    if st.button("🗑️ Wipe Neural Core"):
        st.session_state.chat_history = []
        st.session_state.neural_logs = []
        st.session_state.active_prompt = ""
        st.rerun()

    st.divider()
    selected = option_menu(None, ["Medha (Chat)", "Srijan (Images)"], icons=["cpu", "layers"], default_index=0)

# --- 3. MAIN INTERFACE ---
ORANGE_TITLE = "<style>.orange-title {font-size: 50px; color: #FF8C00; text-align: center; font-weight: 800; margin-bottom: 20px;}.stPopover { margin-top: 23px; }</style>"

if selected == "Medha (Chat)":
    st.markdown(ORANGE_TITLE, unsafe_allow_html=True)
    st.markdown('<div class="orange-title">VEDA 3.0 ULTRA</div>', unsafe_allow_html=True)
    
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    # --- ➕ THE REPAIRED FACILITY ---
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

    # 📥 INPUT BOX
    prompt = st.chat_input("Command VEDA...")
    if st.session_state.active_prompt:
        st.info(f"💡 Reloaded Memory: **{st.session_state.active_prompt}**")
        if st.button("Send Reloaded Memory"):
            prompt = st.session_state.active_prompt
            st.session_state.active_prompt = "" 

    if prompt:
        add_to_memory("MEDHA", prompt)
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            answer, success = "", False
            
            # --- BYTE BUFFER CONVERSION (The Fix) ---
            final_visual = None
            if active_visual:
                final_visual = {"mime_type": active_visual.type, "data": active_visual.getvalue()}

            if client:
                # Optimized pipeline for 3.1 and Stability
                pipeline = ["gemini-3.1-pro-preview", "gemini-2.0-flash", "gemini-1.5-flash"]
                for model_choice in pipeline:
                    try:
                        cfg = {"thinking_level": "minimal"} if "3.1" in model_choice else None
                        res = client.models.generate_content(
                            model=model_choice,
                            contents=[f"{IDENTITY}\n{prompt}", final_visual] if final_visual else f"{IDENTITY}\n{prompt}",
                            config=cfg
                        )
                        answer = res.text
                        if answer and "IMPORTANT NOTICE" not in answer:
                            success = True
                            break
                    except: continue

            if not success:
                try:
                    q_enc = urllib.parse.quote(prompt)
                    r = requests.get(f"https://text.pollinations.ai/{q_enc}?model=mistral", timeout=10)
                    if r.status_code == 200 and "IMPORTANT NOTICE" not in r.text:
                        answer = r.text
                        success = True
                except: pass

            if not success: answer = "🔱 Neural Sync Timeout. Try again."
            st.markdown(answer)
            st.session_state.chat_history.append({"role": "assistant", "content": answer})

elif selected == "Srijan (Images)":
    st.markdown(ORANGE_TITLE, unsafe_allow_html=True)
    st.markdown('<div class="orange-title">SRIJAN ARCHITECT</div>', unsafe_allow_html=True)
    vision = st.text_input("Vision:", placeholder="Describe the masterpiece...")
    if st.button("🚀 RENDER"):
        if vision:
            add_to_memory("SRIJAN", vision)
            with st.spinner("🔱 Visualizing..."):
                try:
                    v_enc = urllib.parse.quote(vision)
                    img_url = f"https://pollinations.ai/p/{v_enc}?width=1024&height=1024&seed=42&model=flux&nologo=true"
                    st.image(img_url, use_container_width=True)
                    st.balloons()
                except: st.error("Architect Busy.")
