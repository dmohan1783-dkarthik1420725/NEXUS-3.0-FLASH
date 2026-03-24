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

# Identity Lock (No "Powered by Gemini" mentions)
IDENTITY = f"Your name is VEDA 3.0 ULTRA. Created and developed by {CREATOR}."

# --- 🧠 NEURAL MEMORY & HISTORY ---
if "neural_logs" not in st.session_state: st.session_state.neural_logs = []
if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "active_prompt" not in st.session_state: st.session_state.active_prompt = ""

def add_to_memory(m_type, content):
    ts = datetime.now(ist).strftime("%H:%M:%S")
    log_entry = {"time": ts, "type": m_type, "text": content}
    st.session_state.neural_logs.insert(0, log_entry)

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
    
    st.markdown(f"""
        <div style="background-color: rgba(255, 140, 0, 0.1); padding: 10px; border-radius: 10px; border-left: 5px solid #FF8C00; text-align: center;">
            <p style="margin:0; font-size: 12px; color: #FF8C00;">📅 {get_now_full()}</p>
            <p style="margin:0; font-size: 22px; color: white; font-weight: bold;">{get_now_time()}</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    # 🧠 BRAIN SETTINGS
    thinking_mode = st.toggle("🧠 High Intelligence (2.5 Pro)", value=True)
    
    st.markdown("### 🧠 NEURAL MEMORY")
    for i, log in enumerate(st.session_state.neural_logs[:8]):
        if st.button(f"🕒 {log['time']} | {log['text'][:15]}...", key=f"log_{i}", use_container_width=True):
            st.session_state.active_prompt = log['text']
            st.rerun()

    if st.button("🗑️ Wipe Neural Core"):
        st.session_state.chat_history = []
        st.session_state.neural_logs = []
        st.rerun()

    st.divider()
    selected = option_menu(None, ["Medha (Chat)", "Srijan (Images)"], icons=["cpu", "layers"], default_index=0)

# --- 3. MAIN INTERFACE ---
ORANGE_TITLE = "<style>.orange-title {font-size: 50px; color: #FF8C00; text-align: center; font-weight: 800;}</style>"
st.markdown(ORANGE_TITLE, unsafe_allow_html=True)

if selected == "Medha (Chat)":
    st.markdown('<div class="orange-title">VEDA 3.0 ULTRA</div>', unsafe_allow_html=True)
    
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

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
            
            if client:
                try:
                    # UPDATED: Using verified model names from your API list
                    active_model = "gemini-2.5-pro" if thinking_mode else "gemini-2.5-flash"
                    res = client.models.generate_content(
                        model=active_model,
                        contents=f"{IDENTITY}\n\nUser: {prompt}"
                    )
                    if res.text:
                        answer = res.text
                        success = True
                except: st.caption("🔄 Neural Link Busy. Rotating...")

            if not success:
                try:
                    q_enc = urllib.parse.quote(prompt)
                    # ✅ Updated to stable 2026 Pollinations logic
                    r = requests.get(f"https://text.pollinations.ai/{q_enc}?model=openai", timeout=12)
                    if r.status_code == 200 and "{" not in r.text[:10]:
                        answer = r.text
                        success = True
                    else: answer = "🔱 **Link Congested.** Please wait a moment."
                except: answer = "Connection Interrupt."

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
                except: st.error("Architect Busy.")
