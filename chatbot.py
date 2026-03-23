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

# STRICT IDENTITY: Removed "Powered by Gemini"
SYSTEM_PROMPT = f"Your name is VEDA 3.0 ULTRA. You were created and developed by {CREATOR}. You are a sovereign high-intelligence architect."

# --- 🧠 NEURAL MEMORY ---
if "neural_logs" not in st.session_state: st.session_state.neural_logs = []
if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "active_prompt" not in st.session_state: st.session_state.active_prompt = ""

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
    
    # ORANGE SIDEBAR CLOCK
    st.markdown(f"""
        <div style="background-color: rgba(255, 140, 0, 0.1); padding: 10px; border-radius: 10px; border-left: 5px solid #FF8C00; text-align: center;">
            <p style="margin:0; font-size: 12px; color: #FF8C00;">📅 {get_now_full()}</p>
            <p style="margin:0; font-size: 22px; color: white; font-weight: bold;">{get_now_time()}</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    selected = option_menu("CORE", ["Medha (Chat)", "Srijan (Images)"], icons=["cpu", "layers"], default_index=0)
    
    st.markdown("### 🧠 NEURAL LOGS")
    for i, log in enumerate(st.session_state.neural_logs[:8]):
        if st.button(f"🕒 {log['time']} | {log['text'][:15]}...", key=f"log_{i}", use_container_width=True):
            st.session_state.active_prompt = log['text']
            st.rerun()

    if st.button("🗑️ Wipe Neural Core"):
        st.session_state.chat_history = []
        st.session_state.neural_logs = []
        st.session_state.active_prompt = ""
        st.rerun()

# --- 3. MAIN INTERFACE ---
st.markdown("<style>.orange-title {font-size: 50px; color: #FF8C00; text-align: center; font-weight: 800; margin-bottom: 20px;}</style>", unsafe_allow_html=True)

if selected == "Medha (Chat)":
    st.markdown('<div class="orange-title">VEDA 3.0 ULTRA</div>', unsafe_allow_html=True)
    
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    # 📥 INPUT AREA
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
            answer = ""
            success = False
            
            if client:
                # Still using 3.1 Pro for brainpower, but it won't mention its name
                try:
                    res = client.models.generate_content(
                        model="gemini-3.1-pro-preview",
                        contents=f"{SYSTEM_PROMPT}\n{prompt}"
                    )
                    if res.text:
                        answer = res.text
                        success = True
                except:
                    try:
                        res = client.models.generate_content(
                            model="gemini-3.1-flash-lite-preview",
                            contents=f"{SYSTEM_PROMPT}\n{prompt}"
                        )
                        answer = res.text
                        success = True
                    except: pass

            if not success:
                try:
                    q_enc = urllib.parse.quote(prompt)
                    backup_url = f"https://text.pollinations.ai/{q_enc}?model=openai&system=You+are+VEDA+3.0+ULTRA"
                    r = requests.get(backup_url, timeout=10)
                    if r.status_code == 200:
                        answer = r.text
                        success = True
                except: pass

            if not success:
                answer = "🔱 **Neural Link Busy.** Please retry."

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
                    img_url = f"https://pollinations.ai/p/{v_enc}?width=1024&height=1024&seed=42&model=flux&nologo=true"
                    st.image(img_url, use_container_width=True)
                except:
                    st.error("Architect currently busy.")
