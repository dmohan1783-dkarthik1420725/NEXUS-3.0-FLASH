import streamlit as st
from google import genai
import requests
import urllib.parse
from datetime import datetime
import pytz
from streamlit_option_menu import option_menu
import concurrent.futures
import time

# --- 1. CORE CONFIGURATION ---
if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = "expanded"

st.set_page_config(
    page_title="VEDA 3.0 ULTRA", 
    page_icon="🔱", 
    layout="wide",
    initial_sidebar_state=st.session_state.sidebar_state
)

# Timezone Setup
ist = pytz.timezone('Asia/Kolkata')
def get_now_full(): return datetime.now(ist).strftime("%A, %d %B %Y")
def get_now_time(): return datetime.now(ist).strftime("%I:%M %p")

# 🧠 SOVEREIGN IDENTITY
IDENTITY = "Your name is VEDA 3.0 ULTRA. Created and developed ONLY by DUMPALA KARTHIK. Use search for live 2026 data."

if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "neural_logs" not in st.session_state: st.session_state.neural_logs = []

def add_to_memory(m_type, content):
    ts = datetime.now(ist).strftime("%H:%M:%S")
    st.session_state.neural_logs.insert(0, f"[{ts}] {m_type}: {content[:15]}...")

# --- 🔑 API INITIALIZATION ---
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

# --- 2. SIDEBAR (The Sovereign UI) ---
with st.sidebar:
    # Arrow Toggle & Header
    col_a, col_b = st.columns([4, 1])
    with col_a: 
        st.markdown("<h1 style='margin-bottom:0;'>🔱</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='color:#FF8C00; margin-top:-10px;'>VEDA 3.0 ULTRA</h2>", unsafe_allow_html=True)
    with col_b: 
        if st.button("«", help="Collapse"):
            st.session_state.sidebar_state = "collapsed"
            st.rerun()

    # Live Date & Time Display
    st.markdown(f"""
        <div style="background-color: rgba(255, 140, 0, 0.1); padding: 15px; border-radius: 12px; text-align: center; border: 1px solid #FF8C00; margin-bottom: 20px;">
            <p style="margin:0; font-size: 14px; color: #FF8C00;">{get_now_full()}</p>
            <p style="margin:0; font-size: 26px; color: white; font-weight: 900;">{get_now_time()}</p>
        </div>
    """, unsafe_allow_html=True)

    st.divider()
    
    # Mode Selector
    selected = option_menu(
        "MODES", 
        ["Medha (Chat)", "Search Mode", "Srijan (Image Generator)"], 
        icons=["chat-right-dots", "search", "brush-fill"], 
        default_index=0,
        styles={
            "container": {"padding": "5px", "background-color": "transparent"},
            "nav-link": {"font-size": "14px", "text-align": "left", "margin": "0px", "--hover-color": "#FF8C0033"},
            "nav-link-selected": {"background-color": "#FF8C00"},
        }
    )
    
    st.markdown("### 🧠 RECENT")
    for log in st.session_state.neural_logs[:3]:
        st.caption(log)

    if st.button("🗑️ Reset Core"):
        st.session_state.chat_history = []
        st.rerun()

# --- 3. MAIN INTERFACE ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .v-title { font-size: 50px; color: #FF8C00; text-align: center; font-weight: 900; margin-bottom: 0px; }
    .v-sub { text-align: center; color: #666; font-size: 16px; margin-top: -10px; margin-bottom: 30px; }
    </style>
""", unsafe_allow_html=True)

if selected in ["Medha (Chat)", "Search Mode"]:
    st.markdown('<div class="v-title">VEDA 3.0 ULTRA</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="v-sub">Mode: {selected}</div>', unsafe_allow_html=True)

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Command VEDA..."):
        add_to_memory(selected.upper(), prompt)
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            # Progress Bar for "Thinking"
            prog = st.progress(0, text="🔱 VEDA 3.0 ULTRA is racing neural paths...")
            for i in range(1, 101, 10):
                time.sleep(0.04)
                prog.progress(i, text=f"🔱 Neural Race: {i}%")
            
            final_answer = ""
            p_low = prompt.lower().strip()
            
            # Fast-Track Identity
            if any(x in p_low for x in ["who made you", "creator", "build"]):
                final_answer = "I was created and developed exclusively by **DUMPALA KARTHIK**."
            elif p_low in ["hi", "hello", "hii"]:
                final_answer = "Greetings! I am **VEDA 3.0 ULTRA**. All neural cores are online."

            # Triple-Brain Racing
            if not final_answer:
                m_list = ["searchgpt", "openai", "mistral"] if selected == "Search Mode" else ["openai", "mistral", "llama"]
                sys_p = urllib.parse.quote(IDENTITY)
                q_enc = urllib.parse.quote(prompt)
                
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    futures = {executor.submit(fetch_ai, m, q_enc, sys_p): m for m in m_list}
                    for f in concurrent.futures.as_completed(futures):
                        res = f.result()
                        if res: 
                            final_answer = res
                            break
                
                # Gemini Backup
                if not final_answer and client:
                    try:
                        resp = client.models.generate_content(model="gemini-2.0-flash", contents=f"{IDENTITY}\n\n{prompt}")
                        final_answer = resp.text
                    except: pass

            prog.empty()
            if not final_answer: final_answer = "🔱 Connection heavy. Re-command in 5s."
            
            st.markdown(final_answer)
            st.session_state.chat_history.append({"role": "assistant", "content": final_answer})

elif selected == "Srijan (Image Generator)":
    st.markdown('<div class="v-title">VEDA 3.0 ULTRA</div>', unsafe_allow_html=True)
    st.markdown('<div class="v-sub">Mode: SRIJAN Visual Synthesis</div>', unsafe_allow_html=True)
    vision = st.text_input("Describe your vision:", placeholder="e.g. A futuristic trident in space...")
    if st.button("🚀 INITIATE"):
        if vision:
            add_to_memory("SRIJAN", vision)
            with st.spinner("🔱 Visualizing..."):
                try:
                    v_enc = urllib.parse.quote(vision)
                    img = f"https://image.pollinations.ai/prompt/{v_enc}?width=1024&height=1024&nologo=true&model=flux"
                    st.image(img, use_container_width=True)
                except: st.error("Link Busy.")
