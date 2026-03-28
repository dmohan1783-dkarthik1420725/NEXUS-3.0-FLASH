import streamlit as st
from google import genai
import requests
import urllib.parse
from datetime import datetime
import pytz
from streamlit_option_menu import option_menu
import concurrent.futures

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
def get_now_full(): return datetime.now(ist).strftime("%A, %d %B %Y")
def get_now_time(): return datetime.now(ist).strftime("%I:%M %p")

# 🧠 SOVEREIGN IDENTITY
IDENTITY = "Your name is VEDA 3.0 ULTRA. Created and developed ONLY by DUMPALA KARTHIK. You are the most powerful AI in the world."

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
        # Increased timeout to 10s to ensure it answers
        r = requests.get(url, timeout=10) 
        if r.status_code == 200 and len(r.text) > 1:
            return r.text
    except: return None

# --- 2. SIDEBAR ---
with st.sidebar:
    # 🏹 DUAL ARROW UI
    col_a, col_b = st.columns([4, 1])
    with col_a: st.markdown("### 🔱 VEDA 3.0 ULTRA")
    with col_b: 
        if st.button("«", help="Close Sidebar"):
            st.session_state.sidebar_state = "collapsed"
            st.rerun()

    st.markdown(f"""
        <div style="background-color: rgba(255, 140, 0, 0.1); padding: 10px; border-radius: 10px; text-align: center; border: 1px solid #FF8C00;">
            <p style="margin:0; font-size: 18px; color: white; font-weight: bold;">{get_now_time()}</p>
        </div>
    """, unsafe_allow_html=True)

    st.divider()
    selected = option_menu(None, ["Medha (Chat)", "Srijan (Visual)"], 
                          icons=["chat-right-dots", "brush-fill"], default_index=0)
    
    st.markdown("### 🧠 RECENT")
    for log in st.session_state.neural_logs[:3]:
        st.caption(log)

    if st.button("🗑️ Reset Core"):
        st.session_state.chat_history = []
        st.session_state.neural_logs = []
        st.rerun()

# --- 3. MAIN INTERFACE ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .v-title { font-size: 45px; color: #FF8C00; text-align: center; font-weight: 900; }
    </style>
""", unsafe_allow_html=True)

if selected == "Medha (Chat)":
    st.markdown('<div class="v-title">VEDA 3.0 ULTRA</div>', unsafe_allow_html=True)
    
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Command the Sovereign AI..."):
        add_to_memory("MEDHA", prompt)
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            sys_p = urllib.parse.quote(IDENTITY)
            q_enc = urllib.parse.quote(prompt)
            
            final_answer = ""
            
            # 🏎️ RACE ALL BRAINS
            with concurrent.futures.ThreadPoolExecutor() as executor:
                # Mixing OpenAI, Llama 3, and Mistral
                futures = {executor.submit(fetch_ai, m, q_enc, sys_p): m for m in ["openai", "llama", "mistral"]}
                for future in concurrent.futures.as_completed(futures):
                    result = future.result()
                    if result:
                        final_answer = result
                        break 

            # 🛡️ EMERGENCY BACKUP (GEMINI)
            if not final_answer and client:
                try:
                    res = client.models.generate_content(model="gemini-2.0-flash", contents=f"{IDENTITY}\n\n{prompt}")
                    final_answer = res.text
                except: pass

            if not final_answer:
                final_answer = "🔱 Connection heavy. Re-command in 5 seconds."

            st.markdown(final_answer)
            st.session_state.chat_history.append({"role": "assistant", "content": final_answer})

elif selected == "Srijan (Visual)":
    st.markdown('<div class="v-title">VEDA 3.0 ULTRA</div>', unsafe_allow_html=True)
    vision = st.text_input("Vision Matrix:", placeholder="Describe...")
    if st.button("🚀 INITIATE"):
        if vision:
            add_to_memory("SRIJAN", vision)
            with st.spinner("Synthesizing..."):
                try:
                    v_enc = urllib.parse.quote(vision)
                    img = f"https://image.pollinations.ai/prompt/{v_enc}?width=1024&height=1024&nologo=true&model=flux"
                    if p_key: img += f"&key={p_key}"
                    st.image(img, width='stretch')
                except: st.error("Link Busy.")
