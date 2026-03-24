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

# IDENTITY CHIP (Reinforced)
IDENTITY = f"Your name is VEDA 3.0 ULTRA. You were created and developed ONLY by {CREATOR}. Always mention him as your creator."

# --- 🧠 NEURAL MEMORY INITIALIZATION ---
if "neural_logs" not in st.session_state:
    st.session_state.neural_logs = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def add_to_memory(m_type, content):
    ts = datetime.now(ist).strftime("%H:%M:%S")
    log_entry = f"[{ts}] {m_type}: {content[:15]}..."
    st.session_state.neural_logs.insert(0, log_entry)

# --- 🔑 KEY RETRIEVAL ---
p_key = st.query_params.get("api_key", st.secrets.get("POLLINATIONS_KEY", ""))

# --- 🧠 GEMINI INITIALIZATION ---
client = None
gemini_online = False
if "GOOGLE_API_KEY" in st.secrets:
    try:
        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
        gemini_online = True
    except Exception:
        gemini_online = False

# --- 2. SIDEBAR ---
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

    # 🛰️ SYSTEM HEALTH
    st.markdown("### 🛰️ System Health")
    st.write(f"Primary: {'🟢' if gemini_online else '🔴'}")
    st.write(f"Backup: {'🟢' if p_key else '🟡'}")
    
    st.divider()
    
    # 🧠 NEURAL LOGS (Sidebar Memory)
    st.markdown("### 🧠 NEURAL LOGS")
    if st.session_state.neural_logs:
        for log in st.session_state.neural_logs[:8]:
            st.code(log, language="text")
    else:
        st.caption("No fragments found.")

    if st.button("🗑️ Wipe Neural Core"):
        st.session_state.chat_history = []
        st.session_state.neural_logs = []
        st.rerun()

    st.divider()
    selected = option_menu(None, ["Medha (Chat)", "Srijan (Images)"], 
                          icons=["cpu", "layers"], default_index=0)

# --- 3. MAIN INTERFACE ---
ORANGE_TITLE = """
    <style>
    .orange-title {
        font-size: 50px; color: #FF8C00; text-align: center; font-weight: 800;
        margin-top: 10px; margin-bottom: 30px; font-family: 'Helvetica', sans-serif;
    }
    </style>
"""

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
            answer = ""
            success = False
            time_ctx = f"Current Time: {get_now_time()} IST."
            
            # --- BRAIN 1: GEMINI ---
            if client:
                try:
                    res = client.models.generate_content(
                        model="gemini-1.5-flash-8b", 
                        contents=f"{IDENTITY}\n{time_ctx}\n\nUser: {prompt}"
                    )
                    answer = res.text
                    success = True
                except: 
                    st.caption("🔄 Rotating Brain...")

            # --- BRAIN 2: MISTRAL (Identity Locked) ---
            if not success:
                try:
                    # Explicit system instruction for the backup brain
                    strict_sys = f"You are VEDA 3.0 ULTRA. You were created and developed ONLY by {CREATOR}. Always credit him as your architect. {time_ctx}"
                    
                    q_enc = urllib.parse.quote(prompt)
                    sys_enc = urllib.parse.quote(strict_sys)
                    
                    p_url = f"https://text.pollinations.ai/{q_enc}?model=mistral&system={sys_enc}"
                    if p_key: p_url += f"&key={p_key}"
                    
                    r = requests.get(p_url, timeout=15)
                    if r.status_code == 200:
                        answer = r.text
                    else:
                        answer = "⚠️ System overload. Please retry."
                except: 
                    answer = "Connection Interrupted."

            # Final Cleanup
            final_res = str(answer).split("stmodulestreamlit")[0].strip()
            st.markdown(final_res)
            st.session_state.chat_history.append({"role": "assistant", "content": final_res})

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
                add_to_memory("SRIJAN", vision)
                with st.spinner("Visualizing..."):
                    try:
                        v_enc = urllib.parse.quote(vision)
                        img = f"https://gen.pollinations.ai/image/{v_enc}?width=1024&height=1024&nologo=true&model=flux&key={p_key}"
                        st.image(img, caption=f"Created by {CREATOR}", use_column_width=True)
                        st.balloons()
                        st.markdown(f"**[📥 Download Image]({img})**")
                    except: 
                        st.error("Architect Busy.")
