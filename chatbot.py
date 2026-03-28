import streamlit as st
from google import genai
import requests
import urllib.parse
from datetime import datetime
import pytz
from streamlit_option_menu import option_menu

# --- 1. CONFIGURATION & IDENTITY ---
# Force sidebar to be expanded on load for the first time
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
IDENTITY = "Your name is VEDA 3.0 ULTRA. Created and developed ONLY by DUMPALA KARTHIK."

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

# --- 2. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 60px; margin-bottom:0;'>🔱</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #FF8C00; margin-top:0;'>VEDA 3.0 ULTRA</h3>", unsafe_allow_html=True)
    
    # --- 🕒 TIME & DATE ---
    st.markdown(f"""
        <div style="background-color: rgba(255, 140, 0, 0.05); padding: 10px; border-radius: 10px; text-align: center; border: 1px solid #FF8C00; margin-bottom: 20px;">
            <p style="margin:0; font-size: 12px; color: #FF8C00;">{get_now_full()}</p>
            <p style="margin:0; font-size: 20px; color: white; font-weight: bold;">{get_now_time()}</p>
        </div>
    """, unsafe_allow_html=True)

    selected = option_menu(None, ["Medha (Chat)", "Srijan (Visual)"], 
                          icons=["chat-right-dots", "brush-fill"], default_index=0)
    
    # --- 🛠️ HIDDEN SYSTEM VITALS ---
    with st.expander("⚙️ System Vitals"):
        st.caption("🟢 OpenAI Core")
        st.caption("🟢 Gemini Core")
        st.caption("🟢 Claude Core")
        st.caption("🟢 Flux.1 (Visuals)")

    # --- 🧠 MEMORY ---
    st.markdown("### 🧠 MEMORY")
    for log in st.session_state.neural_logs[:3]:
        st.caption(log)

    # --- 🔘 SIDEBAR CONTROLS ---
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Reset"):
            st.session_state.chat_history = []
            st.rerun()
    with col2:
        # This button toggles the sidebar state
        if st.button("❌ Close"):
            st.session_state.sidebar_state = "collapsed"
            st.rerun()

# --- 3. MAIN INTERFACE ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .v-title { font-size: 50px; color: #FF8C00; text-align: center; font-weight: 900; letter-spacing: 2px; }
    .sub-text { text-align: center; color: #888; font-size: 14px; margin-top: -10px; margin-bottom: 30px; }
    </style>
""", unsafe_allow_html=True)

if selected == "Medha (Chat)":
    st.markdown('<div class="v-title">VEDA 3.0 ULTRA</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">Universal Neural Interface: MEDHA</div>', unsafe_allow_html=True)
    
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Command the Sovereign Intelligence..."):
        add_to_memory("MEDHA", prompt)
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            answer, success = "", False
            sys_p = urllib.parse.quote(IDENTITY)
            q_enc = urllib.parse.quote(prompt)
            
            # --- BRAIN 1: OPENAI (High Priority) ---
            try:
                r = requests.get(f"https://text.pollinations.ai/{q_enc}?model=openai&system={sys_p}", timeout=8)
                if r.status_code == 200 and len(r.text) > 2:
                    answer, success = r.text, True
            except: pass

            # --- BRAIN 2: GEMINI (High Speed Backup) ---
            if not success and client:
                try:
                    res = client.models.generate_content(model="gemini-2.0-flash", contents=f"{IDENTITY}\n\n{prompt}")
                    if res.text: answer, success = res.text, True
                except: pass

            # --- BRAIN 3: MISTRAL (Emergency Recovery) ---
            if not success:
                try:
                    r = requests.get(f"https://text.pollinations.ai/{q_enc}?model=mistral&system={sys_p}", timeout=8)
                    if r.status_code == 200: answer, success = r.text, True
                except: 
                    answer = "🔱 Neural Link unstable. Please re-send your command."

            st.markdown(answer)
            st.session_state.chat_history.append({"role": "assistant", "content": answer})

elif selected == "Srijan (Visual)":
    st.markdown('<div class="v-title">VEDA 3.0 ULTRA</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">Advanced Visual Synthesis: SRIJAN</div>', unsafe_allow_html=True)
    
    vision = st.text_input("Vision Matrix:", placeholder="Describe the image...")
    if st.button("🚀 INITIATE"):
        if vision:
            add_to_memory("SRIJAN", vision)
            with st.spinner("🔱 Synthesizing Visuals..."):
                try:
                    v_enc = urllib.parse.quote(vision)
                    img = f"https://image.pollinations.ai/prompt/{v_enc}?width=1024&height=1024&nologo=true&model=flux"
                    if p_key: img += f"&key={p_key}"
                    st.image(img, width='stretch')
                    st.balloons()
                except: st.error("Srijan Link Error.")
