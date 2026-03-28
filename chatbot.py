import streamlit as st
from google import genai
from google.genai import types
import requests
import urllib.parse
from datetime import datetime
import pytz
from streamlit_option_menu import option_menu
import time

# --- 1. SESSION STATE & LOGIN CHECK ---
if 'user_name' not in st.session_state:
    st.session_state.user_name = None
if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = "expanded"

st.set_page_config(
    page_title="VEDA 3.0 ULTRA", 
    page_icon="🔱", 
    layout="wide", 
    initial_sidebar_state="expanded" 
)

ist = pytz.timezone('Asia/Kolkata')
def get_now_time(): return datetime.now(ist).strftime("%I:%M %p")
def get_now_full(): return datetime.now(ist).strftime("%A, %d %B %Y")

# 🧠 SOVEREIGN IDENTITY
IDENTITY = "Your name is VEDA 3.0 ULTRA. Created and developed ONLY by DUMPALA KARTHIK."

if "chat_history" not in st.session_state: st.session_state.chat_history = []

# --- 🔑 API INITIALIZATION ---
client = None
if "GOOGLE_API_KEY" in st.secrets:
    try:
        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"], http_options=types.HttpOptions(timeout=15000))
    except: client = None

def fetch_backup_ai(q_enc, sys_p):
    try:
        url = f"https://text.pollinations.ai/{q_enc}?model=openai&system={sys_p}"
        r = requests.get(url, timeout=12)
        if r.status_code == 200: return r.text
    except: return None

# --- 2. CSS STYLING ---
st.markdown("""
    <style>
    header {visibility: hidden;}
    .v-title { font-size: 60px; color: #FF8C00; text-align: center; font-weight: 900; margin-top: 50px; text-transform: uppercase; }
    .v-sub { text-align: center; color: #666; font-size: 18px; margin-top: -10px; margin-bottom: 40px; }
    .thinking-text { color: #FF8C00; font-style: italic; font-weight: bold; animation: pulse 1.5s infinite; font-size: 18px; }
    @keyframes pulse { 0% { opacity: 0.3; } 50% { opacity: 1; } 100% { opacity: 0.3; } }
    
    /* Login Box Styling */
    .login-card { background: rgba(255,140,0,0.1); padding: 30px; border-radius: 15px; border: 1px solid #FF8C00; text-align: center; max-width: 500px; margin: auto; }
    </style>
""", unsafe_allow_html=True)

# --- 3. LOGIN PHASE ---
if not st.session_state.user_name:
    st.markdown('<div class="v-title">VEDA 3.0 ULTRA</div>', unsafe_allow_html=True)
    st.markdown('<div class="v-sub">Please identify yourself to the Sovereign Core</div>', unsafe_allow_html=True)
    
    with st.container():
        name_input = st.text_input("ENTER YOUR NAME:", placeholder="Type here...", key="name_box")
        if st.button("INITIALIZE CORE 🚀"):
            if name_input:
                st.session_state.user_name = name_input.strip()
                st.rerun()
            else:
                st.warning("Identification required.")
    st.stop() # Stops the rest of the app from loading until name is given

# --- 4. SIDEBAR (Only shows after Login) ---
with st.sidebar:
    st.markdown("<h1 style='text-align:center;'>🔱</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center; color:#FF8C00; margin-top:-10px;'>VEDA 3.0 ULTRA</h2>", unsafe_allow_html=True)
    
    selected = option_menu(
        None, ["Medha (Chat)", "Srijan (Image Gen)"], 
        icons=["chat-right-dots", "brush-fill"], 
        default_index=0,
        styles={"nav-link-selected": {"background-color": "#FF8C00"}}
    )

    st.markdown(f"""
        <div style="background-color:rgba(255,140,0,0.1); padding:15px; border-radius:12px; text-align:center; border:1px solid #FF8C00; margin-top:20px;">
            <p style="margin:0; font-size:12px; color:#FF8C00;">{get_now_full()}</p>
            <p style="margin:0; font-size:24px; color:white; font-weight:900;">{get_now_time()}</p>
        </div>
    """, unsafe_allow_html=True)

    st.divider()
    if st.button("🗑️ Reset All"):
        st.session_state.user_name = None
        st.session_state.chat_history = []
        st.rerun()

# --- 5. MAIN INTERFACE ---
if selected == "Medha (Chat)":
    # 🔱 THE PERSONALIZED GREETING
    st.markdown(f'<div class="v-title">HI, {st.session_state.user_name.upper()}</div>', unsafe_allow_html=True)
    st.markdown('<div class="v-sub">Sovereign Neural Interface Active</div>', unsafe_allow_html=True)

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input(f"Command VEDA, {st.session_state.user_name}..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            status_area = st.empty()
            final_answer = ""
            
            status_area.markdown('<p class="thinking-text">🔱 thinking with veda....</p>', unsafe_allow_html=True)
            
            if client:
                try:
                    resp = client.models.generate_content(model="gemini-3.1-pro-preview", contents=f"{IDENTITY}\n\n{prompt}")
                    final_answer = resp.text
                except:
                    status_area.markdown('<p class="thinking-text">🔱 researching....</p>', unsafe_allow_html=True)
                    sys_p = urllib.parse.quote(IDENTITY); q_enc = urllib.parse.quote(prompt)
                    final_answer = fetch_backup_ai(q_enc, sys_p)
            
            status_area.empty()
            st.markdown(final_answer)
            st.session_state.chat_history.append({"role": "assistant", "content": final_answer})

elif selected == "Srijan (Image Gen)":
    st.markdown(f'<div class="v-title">SRIJAN MODE</div>', unsafe_allow_html=True)
    vision = st.text_input("Vision Matrix Prompt:", placeholder="Describe...")
    if st.button("🚀 INITIATE"):
        if vision:
            with st.spinner("🔱 Visualizing..."):
                try:
                    v_enc = urllib.parse.quote(vision)
                    img = f"https://image.pollinations.ai/prompt/{v_enc}?width=1024&height=1024&nologo=true&model=flux"
                    st.image(img, use_container_width=True)
                except: st.error("Link Busy.")
