import streamlit as st
import requests
import urllib.parse
from datetime import datetime
import pytz
from streamlit_option_menu import option_menu

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="VEDA 3.0 ULTRA", page_icon="🔱", layout="wide")
CREATOR = "Dumpala Karthik"
ist = pytz.timezone('Asia/Kolkata')

def get_now_full(): return datetime.now(ist).strftime("%A, %d %B %Y")
def get_now_time(): return datetime.now(ist).strftime("%I:%M %p")

IDENTITY = f"Your name is VEDA 3.0 ULTRA. Created by {CREATOR}. Core: GPT-5.4."

# --- 🧠 NEURAL MEMORY ---
if "neural_logs" not in st.session_state: st.session_state.neural_logs = []
if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "active_prompt" not in st.session_state: st.session_state.active_prompt = ""

def add_to_memory(m_type, content):
    ts = datetime.now(ist).strftime("%H:%M:%S")
    st.session_state.neural_logs.insert(0, {"time": ts, "type": m_type, "text": content})

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
    selected = option_menu(None, ["Medha (Chat)", "Srijan (Images)"], icons=["cpu", "layers"], default_index=0)
    
    st.markdown("### 🧠 NEURAL LOGS")
    for i, log in enumerate(st.session_state.neural_logs[:8]):
        if st.button(f"🕒 {log['time']} | {log['text'][:15]}...", key=f"log_{i}", use_container_width=True):
            st.session_state.active_prompt = log['text']
            st.rerun()

    if st.button("🗑️ Wipe Neural Core"):
        st.session_state.chat_history = []
        st.session_state.neural_logs = []
        st.rerun()

# --- 3. MAIN INTERFACE ---
st.markdown("<style>.orange-title {font-size: 50px; color: #FF8C00; text-align: center; font-weight: 800;}</style>", unsafe_allow_html=True)

if selected == "Medha (Chat)":
    st.markdown('<div class="orange-title">VEDA 3.0 ULTRA</div>', unsafe_allow_html=True)
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Command VEDA (GPT-5.4)...")
    
    if st.session_state.active_prompt:
        st.info(f"💡 Reloaded Memory: **{st.session_state.active_prompt}**")
        if st.button("Send Reloaded"):
            prompt = st.session_state.active_prompt
            st.session_state.active_prompt = ""

    if prompt:
        add_to_memory("MEDHA", prompt)
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("🔱 Reasoning via GPT-5.4..."):
                try:
                    q_enc = urllib.parse.quote(prompt)
                    sys_enc = urllib.parse.quote(IDENTITY)
                    # ✅ Pollinations GPT-5.4 Stable Link
                    api_url = f"https://text.pollinations.ai/{q_enc}?model=openai&system={sys_enc}"
                    r = requests.get(api_url, timeout=20)
                    
                    if r.status_code == 200 and "{" not in r.text[:10]:
                        answer = r.text
                    else:
                        answer = "🔱 **Neural Link Congested.** Please wait 10s and retry."
                except:
                    answer = "🔱 **Connection Error.** Please check your internet."

            st.markdown(answer)
            st.session_state.chat_history.append({"role": "assistant", "content": answer})

elif selected == "Srijan (Images)":
    st.markdown('<div class="orange-title">SRIJAN ARCHITECT</div>', unsafe_allow_html=True)
    v = st.text_input("Vision:", placeholder="Describe the masterpiece...")
    if st.button("🚀 RENDER"):
        if v:
            add_to_memory("SRIJAN", v)
            with st.spinner("🔱 Visualizing..."):
                try:
                    v_enc = urllib.parse.quote(v)
                    img_url = f"https://image.pollinations.ai/prompt/{v_enc}?width=1024&height=1024&nologo=true&model=flux"
                    st.image(img_url, use_container_width=True)
                    st.balloons()
                except:
                    st.error("Architect currently busy.")
