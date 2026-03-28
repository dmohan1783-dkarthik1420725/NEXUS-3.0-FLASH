import streamlit as st
from google import genai
import requests
import urllib.parse
from datetime import datetime
import pytz
from streamlit_option_menu import option_menu
import concurrent.futures
import time

# --- 1. CONFIGURATION ---
if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = "expanded"

st.set_page_config(
    page_title="VEDA 3.0 ULTRA", 
    page_icon="🔱", 
    layout="wide",
    initial_sidebar_state=st.session_state.sidebar_state
)

ist = pytz.timezone('Asia/Kolkata')
def get_now_time(): return datetime.now(ist).strftime("%I:%M %p")

# 🧠 SOVEREIGN CORE IDENTITY
IDENTITY = "Your name is VEDA 3.0 ULTRA. Created and developed ONLY by DUMPALA KARTHIK. Use your search core for live 2026 data."

if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "neural_logs" not in st.session_state: st.session_state.neural_logs = []

def add_to_memory(m_type, content):
    ts = datetime.now(ist).strftime("%H:%M:%S")
    st.session_state.neural_logs.insert(0, f"[{ts}] {m_type}: {content[:15]}...")

# --- 🔑 API KEYS ---
client = None
if "GOOGLE_API_KEY" in st.secrets:
    try: client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    except: client = None
p_key = st.secrets.get("POLLINATIONS_KEY", "")

# --- ⚡ THE NEURAL RACER ---
def fetch_ai(model_name, q_enc, sys_p):
    try:
        url = f"https://text.pollinations.ai/{q_enc}?model={model_name}&system={sys_p}"
        r = requests.get(url, timeout=15)
        if r.status_code == 200 and len(r.text) > 1: return r.text
    except: return None

# --- 2. SIDEBAR ---
with st.sidebar:
    col_a, col_b = st.columns([4, 1])
    with col_a: st.markdown("### 🔱 VEDA 3.0 ULTRA")
    with col_b: 
        if st.button("«", help="Collapse Sidebar"):
            st.session_state.sidebar_state = "collapsed"
            st.rerun()

    st.markdown(f'<div style="background-color:rgba(255,140,0,0.1);padding:10px;border-radius:10px;text-align:center;border:1px solid #FF8C00;color:white;font-weight:bold;">{get_now_time()}</div>', unsafe_allow_html=True)
    st.divider()
    
    # 🔍 MODE SELECTOR
    selected = option_menu(None, ["Medha (Chat)", "Search Mode", "Srijan (Visual)"], 
                          icons=["chat-right-dots", "search", "brush-fill"], default_index=0)
    
    st.markdown("### 🧠 MEMORY")
    for log in st.session_state.neural_logs[:3]:
        st.caption(log)

    if st.button("🗑️ Reset Core"):
        st.session_state.chat_history = []
        st.session_state.neural_logs = []
        st.rerun()

# --- 3. MAIN INTERFACE ---
st.markdown("<style>#MainMenu {visibility:hidden;} footer {visibility:hidden;} header {visibility:hidden;} .v-title {font-size:45px;color:#FF8C00;text-align:center;font-weight:900;}</style>", unsafe_allow_html=True)

if selected in ["Medha (Chat)", "Search Mode"]:
    st.markdown(f'<div class="v-title">VEDA 3.0 ULTRA</div>', unsafe_allow_html=True)
    mode_desc = "Universal Neural Core: MEDHA" if selected == "Medha (Chat)" else "Real-Time 2026 Intelligence"
    st.markdown(f'<p style="text-align:center;color:#888;">{mode_desc}</p>', unsafe_allow_html=True)

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Command the Sovereign AI..."):
        add_to_memory(selected.upper(), prompt)
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            # 📊 AI THINKING PROGRESS BAR
            progress_bar = st.progress(0, text="🔱 VEDA 3.0 ULTRA is initiating neural race...")
            for i in range(1, 101, 10):
                time.sleep(0.04)
                progress_bar.progress(i, text=f"🔱 Synchronizing Neural Paths... {i}%")
            
            final_answer = ""
            p_lower = prompt.lower().strip()
            
            # 🚀 1. LOCAL FAST-TRACK (Instant)
            if any(word in p_lower for word in ["who made you", "creator", "build"]):
                final_answer = "I was created and developed exclusively by **DUMPALA KARTHIK**. I am VEDA 3.0 ULTRA."
            elif p_lower in ["hi", "hello", "hii"]:
                final_answer = "Greetings! I am **VEDA 3.0 ULTRA**. My neural cores are online. How can I assist you, Commander?"
            elif p_lower in ["ok", "kk", "nice"]:
                final_answer = "Acknowledged. Standing by. 🔱"

            # 🏎️ 2. THE RACER (With Search Integration)
            if not final_answer:
                # If Search Mode is selected, we lead with SearchGPT
                m_list = ["searchgpt", "openai", "mistral"] if selected == "Search Mode" else ["openai", "mistral", "llama"]
                sys_p = urllib.parse.quote(IDENTITY)
                q_enc = urllib.parse.quote(prompt)
                
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    futures = {executor.submit(fetch_ai, m, q_enc, sys_p): m for m in m_list}
                    for future in concurrent.futures.as_completed(futures):
                        res = future.result()
                        if res: 
                            final_answer = res
                            break
                
                # 🛡️ 3. PRIVATE BACKUP (Gemini)
                if not final_answer and client:
                    try:
                        resp = client.models.generate_content(model="gemini-2.0-flash", contents=f"{IDENTITY}\n\n{prompt}")
                        final_answer = resp.text
                    except: pass

            progress_bar.empty()
            if not final_answer: final_answer = "🔱 Neural systems saturated. Please retry."
            
            st.markdown(final_answer)
            st.session_state.chat_history.append({"role": "assistant", "content": final_answer})

elif selected == "Srijan (Visual)":
    st.markdown('<div class="v-title">VEDA 3.0 ULTRA</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center;color:#888;">Advanced Visual Synthesis: SRIJAN</p>', unsafe_allow_html=True)
    vision = st.text_input("Vision Matrix Prompt:", placeholder="Describe the image...")
    if st.button("🚀 INITIATE SYNTHESIS"):
        if vision:
            add_to_memory("SRIJAN", vision)
            with st.spinner("🔱 Synthesizing..."):
                try:
                    v_enc = urllib.parse.quote(vision)
                    img = f"https://image.pollinations.ai/prompt/{v_enc}?width=1024&height=1024&nologo=true&model=flux"
                    if p_key: img += f"&key={p_key}"
                    st.image(img, use_container_width=True)
                    st.balloons()
                except: st.error("Link Busy.")
