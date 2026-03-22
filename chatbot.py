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
def get_now_full():
    return datetime.now(ist).strftime("%A, %d %B %Y")
def get_now_time():
    return datetime.now(ist).strftime("%I:%M %p")

IDENTITY = f"Your name is VEDA 3.0 ULTRA. Created and developed by {CREATOR}."

# --- 2. NEURAL MEMORY ---
if "neural_logs" not in st.session_state:
    st.session_state.neural_logs = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def add_to_memory(m_type, content):
    ts = datetime.now(ist).strftime("%H:%M:%S")
    st.session_state.neural_logs.insert(0, {"time": ts, "type": m_type, "text": content})

# --- 3. INITIALIZATION (STRICT 3.1) ---
client = None
api_status = "🔴 Offline"
# Using the specific 3.1 models from your authorized list
MODELS_31 = ["gemini-3.1-pro-preview", "gemini-3.1-flash-lite-preview"]

if "GOOGLE_API_KEY" in st.secrets:
    try:
        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
        api_status = "🟢 Ready (Gemini 3.1)"
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
            
            if client:
                # Optimized prompt for the 3.1 "Thinking" models
                content = [f"{IDENTITY}\n\nUser Question: {prompt}", active_visual] if active_visual else f"{IDENTITY}\n\nUser Question: {prompt}"
                
                # Try 3.1 Pro first, then 3.1 Flash Lite
                for model_name in MODELS_31:
                    try:
                        res = client.models.generate_content(model=model_name, contents=content)
                        answer = res.text
                        success = True
                        break # Stop if successful
                    except:
                        continue 

            if not success:
                answer = "🔱 **3.1 Engine Latency.** The 3.1 neural links are currently congested. Please retry in 10 seconds."

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
                    st.image(img, use_column_width=True)
                    st.balloons()
                except: st.error("Architect Busy.")
