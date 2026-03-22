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

IDENTITY = f"Your name is VEDA 3.0 ULTRA. Created by {CREATOR}. Always mention him."

# --- 🧠 NEURAL MEMORY INITIALIZATION ---
if "neural_logs" not in st.session_state:
    st.session_state.neural_logs = []

def add_to_memory(m_type, content):
    ts = datetime.now(ist).strftime("%H:%M:%S")
    log_entry = f"[{ts}] {m_type}: {content[:15]}..."
    st.session_state.neural_logs.insert(0, log_entry)

# --- 🔑 KEY RETRIEVAL ---
p_key = st.query_params.get("api_key", st.secrets.get("POLLINATIONS_KEY", ""))

# --- 🧠 GEMINI INITIALIZATION ---
client = None
try:
    if "GOOGLE_API_KEY" in st.secrets:
        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception:
    client = None

# --- 2. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 80px; margin-bottom:0;'>🔱</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; margin-top:0;'>VEDA 3.0 ULTRA</h3>", unsafe_allow_html=True)
    
    # --- 🕒 SIDEBAR CLOCK WIDGET ---
    st.markdown("---")
    st.markdown(f"""
        <div style="background-color: rgba(255, 140, 0, 0.1); padding: 15px; border-radius: 10px; border-left: 5px solid #FF8C00; text-align: center;">
            <p style="margin:0; font-size: 14px; color: #FF8C00; font-weight: bold; letter-spacing: 1px;">📅 {get_now_full()}</p>
            <p style="margin:5px 0 0 0; font-size: 28px; color: white; font-weight: 800; font-family: 'Courier New', monospace;">{get_now_time()}</p>
            <p style="margin:0; font-size: 10px; color: #888;">INDIAN STANDARD TIME</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    
    # 🧠 NEURAL MEMORY LOG
    st.markdown("### 🧠 NEURAL LOGS")
    if st.session_state.neural_logs:
        for log in st.session_state.neural_logs[:5]:
            st.code(log, language="text")
    else:
        st.caption("Memory empty...")

    if st.button("🗑️ Wipe Logs"):
        st.session_state.neural_logs = []
        st.rerun()

    st.divider()
    
    if not p_key:
        auth_url = "https://enter.pollinations.ai/authorize?redirect_url=https://nexus-flash-india.streamlit.app"
        st.markdown(f'<a href="{auth_url}" target="_blank"><button style="width:100%; background-color:#ff4b4b; color:white; border:none; padding:12px; border-radius:8px; cursor:pointer; font-weight:bold;">🔌 CONNECT SYSTEM</button></a>', unsafe_allow_html=True)
    else:
        st.success("✅ VEDA Linked")

    st.divider()
    # Removed Veda Hub from here
    selected = option_menu(None, ["Medha (Chat)", "Srijan (Images)"], 
                          icons=["cpu", "layers"], default_index=0)

# --- 3. MAIN INTERFACE ---

ORANGE_TITLE = """
    <style>
    .orange-title {
        font-size: 55px; color: #FF8C00; text-align: center; font-weight: 800;
        margin-top: 20px; margin-bottom: 40px; font-family: 'Helvetica', sans-serif;
        letter-spacing: 2px;
    }
    </style>
"""

# [TAB 1: MEDHA CHAT]
if selected == "Medha (Chat)":
    st.markdown(ORANGE_TITLE, unsafe_allow_html=True)
    st.markdown('<div class="orange-title">VEDA 3.0 ULTRA</div>', unsafe_allow_html=True)
    
    if prompt := st.chat_input("Command VEDA..."):
        add_to_memory("MEDHA", prompt) # Store in sidebar
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            success = False
            time_context = f"Current Time: {get_now_time()} on {get_now_full()}"
            
            if client:
                try:
                    res = client.models.generate_content(
                        model="gemini-1.5-flash-8b", 
                        contents=f"{IDENTITY}\n{time_context}\n\nUser: {prompt}"
                    )
                    st.markdown(res.text)
                    success = True
                except Exception:
                    st.caption("🔄 Rotating Brain...")

            if not success:
                try:
                    q = urllib.parse.quote(prompt)
                    sys_encoded = urllib.parse.quote(f"{IDENTITY}\n{time_context}")
                    p_url = f"https://gen.pollinations.ai/text/{q}?model=mistral&system={sys_encoded}"
                    if p_key: p_url += f"&key={p_key}"
                    
                    r = requests.get(p_url, timeout=12)
                    if r.status_code == 200:
                        st.markdown(r.text)
                    else:
                        st.error("Backup brain busy.")
                except Exception:
                    st.error("VEDA connection lost.")

# [TAB 2: SRIJAN ARCHITECT]
elif selected == "Srijan (Images)":
    st.markdown(ORANGE_TITLE, unsafe_allow_html=True)
    st.markdown('<div class="orange-title">SRIJAN ARCHITECT</div>', unsafe_allow_html=True)
    
    if not p_key:
        st.warning("⚠️ Please connect in the sidebar first.")
    else:
        vision = st.text_input("Vision:", placeholder="Describe your image...")
        if st.button("🚀 RENDER"):
            if vision:
                add_to_memory("SRIJAN", vision) # Store in sidebar
                with st.spinner("Visualizing..."):
                    try:
                        v_enc = urllib.parse.quote(vision)
                        img_url = f"https://gen.pollinations.ai/image/{v_enc}?width=1024&height=1024&nologo=true&model=flux&key={p_key}"
                        st.image(img_url, caption=f"Created by {CREATOR}", use_column_width=True)
                        st.balloons()
                        st.markdown(f"**[📥 Download Image]({img_url})**")
                    except Exception:
                        st.error("Srijan is busy. Try again.")
            else:
                st.warning("Please enter a description.")
