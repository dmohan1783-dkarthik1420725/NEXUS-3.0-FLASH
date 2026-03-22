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

# --- 2. NEURAL MEMORY ---
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
if "GOOGLE_API_KEY" in st.secrets:
    try:
        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    except: client = None

# --- 5. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 80px; margin-bottom:0;'>🔱</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; color: #FF8C00; margin-top:0;'>VEDA 3.0 ULTRA</h3>", unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style="background-color: rgba(255, 140, 0, 0.1); padding: 10px; border-radius: 10px; border-left: 5px solid #FF8C00; text-align: center;">
            <p style="margin:0; font-size: 12px; color: #FF8C00;">📅 {get_now_full()}</p>
            <p style="margin:0; font-size: 22px; color: white; font-weight: bold;">{get_now_time()}</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🧠 NEURAL LOGS")
    if st.session_state.neural_logs:
        for log in st.session_state.neural_logs[:5]:
            st.code(f"{log['time']} | {log['text'][:15]}...", language="text")

    if st.button("🗑️ Wipe Neural Core"):
        st.session_state.chat_history = []
        st.session_state.neural_logs = []
        st.rerun()

    st.divider()
    selected = option_menu(None, ["Medha (Chat)", "Srijan (Images)"], 
                          icons=["cpu", "layers"], default_index=0)

# --- 6. MAIN INTERFACE ---
ORANGE_TITLE = "<style>.orange-title {font-size: 50px; color: #FF8C00; text-align: center; font-weight: 800; margin-bottom: 20px;}.stPopover { margin-top: 23px; }</style>"

if selected == "Medha (Chat)":
    st.markdown(ORANGE_TITLE, unsafe_allow_html=True)
    st.markdown('<div class="orange-title">VEDA 3.0 ULTRA</div>', unsafe_allow_html=True)
    
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    # --- ➕ ACTION BAR ---
    act_col1, act_col2 = st.columns([1, 12])
    with act_col1:
        plus_menu = st.popover("➕", use_container_width=True)
        cam_file = plus_menu.camera_input("📷 Camera")
        gal_file = plus_menu.file_uploader("🖼️ Gallery", type=['png', 'jpg', 'jpeg'])
        doc_file = plus_menu.file_uploader("📁 Files", type=['pdf', 'txt'])

    active_visual = cam_file or gal_file
    if active_visual: st.image(active_visual, caption="📎 Attachment Ready", width=150)

    # 📥 MAIN CHAT INPUT
    if prompt := st.chat_input("Command VEDA..."):
        add_to_memory("MEDHA", prompt)
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            answer = ""
            success = False
            time_ctx = f"Time: {get_now_time()} IST."
            q_enc = urllib.parse.quote(prompt)
            sys_msg = f"You are VEDA 3.0 ULTRA by {CREATOR}. {time_ctx}"
            sys_enc = urllib.parse.quote(sys_msg)

            # --- ENGINE 1: GEMINI (Silent) ---
            if client:
                try:
                    res = client.models.generate_content(
                        model="gemini-1.5-flash-8b", 
                        contents=[f"{sys_msg}\n{prompt}", active_visual] if active_visual else f"{sys_msg}\n{prompt}"
                    )
                    answer = res.text
                    success = True
                except: pass # Move to next engine silently

            # --- ENGINE 2: MISTRAL (Silent) ---
            if not success:
                try:
                    r = requests.get(f"https://text.pollinations.ai/{q_enc}?model=mistral&system={sys_enc}", timeout=8)
                    if r.status_code == 200 and "System Overload" not in r.text:
                        answer = r.text
                        success = True
                except: pass

            # --- ENGINE 3: LLAMA (Silent) ---
            if not success:
                try:
                    r = requests.get(f"https://text.pollinations.ai/{q_enc}?model=llama&system={sys_enc}", timeout=8)
                    if r.status_code == 200 and "System Overload" not in r.text:
                        answer = r.text
                        success = True
                except: pass

            # Final check if all failed
            if not success:
                answer = "🔱 Connection lines are heavy. Please try again in a few moments."

            st.markdown(answer)
            st.session_state.chat_history.append({"role": "assistant", "content": answer})

elif selected == "Srijan (Images)":
    st.markdown(ORANGE_TITLE, unsafe_allow_html=True)
    st.markdown('<div class="orange-title">SRIJAN ARCHITECT</div>', unsafe_allow_html=True)
    # [Srijan logic remains the same]
