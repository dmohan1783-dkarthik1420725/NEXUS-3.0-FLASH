import streamlit as st
from google import genai
import requests
import urllib.parse
from datetime import datetime
import pytz
from streamlit_option_menu import option_menu
import re

# --- 1. SOVEREIGN CONFIG & IDENTITY ---
IDENTITY = "Your name is VEDA 3.0 ULTRA. Created and developed ONLY by DUMPALA KARTHIK."

if 'user_name' not in st.session_state: st.session_state.user_name = None
if 'chat_history' not in st.session_state: st.session_state.chat_history = []
if 'neural_logs' not in st.session_state: st.session_state.neural_logs = []

st.set_page_config(page_title="VEDA 3.0 ULTRA", page_icon="🔱", layout="wide", initial_sidebar_state="expanded")

# 🌍 GLOBAL TIME SYNC (IST)
ist = pytz.timezone('Asia/Kolkata')
def get_greeting():
    hour = datetime.now(ist).hour
    if 5 <= hour < 12: return "GOOD MORNING"
    elif 12 <= hour < 17: return "GOOD AFTERNOON"
    elif 17 <= hour < 21: return "GOOD EVENING"
    else: return "GOOD NIGHT"

def clean_veda_text(text):
    # Aggressive ad-shield and error-stripping
    bad_patterns = [r"🌸.*?🌸", r"Powered by.*?AI", r"Support our mission", r"Ad", r"free text APIs", r"Support Pollinations\.AI:", r"Neural corridors congested"]
    for pattern in bad_patterns:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE)
    return text.strip()

# --- 2. CSS STYLING ---
st.markdown("""
    <style>
    header {visibility: hidden;}
    .orange-title {font-size: 50px; color: #FF8C00; text-align: center; font-weight: 800; text-transform: uppercase; margin-top: 10px;}
    .nav-container { max-width: 500px; margin: 0 auto 30px auto; }
    .thinking-text { color: #FF8C00; font-style: italic; font-weight: bold; animation: pulse 1.5s infinite; font-size: 18px; }
    @keyframes pulse { 0%, 100% { opacity: 0.3; } 50% { opacity: 1; } }
    </style>
""", unsafe_allow_html=True)

# --- 3. LOGIN PHASE (Mandatory) ---
if st.session_state.user_name is None:
    st.markdown('<div class="orange-title">VEDA 3.0 ULTRA</div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#666;'>Sovereign Identification Required</p>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        name_in = st.text_input("ENTER COMMANDER NAME:", placeholder="Identify yourself...")
        if st.button("INITIALIZE SYSTEM 🚀", use_container_width=True):
            if name_in:
                st.session_state.user_name = name_in.strip()
                st.rerun()
    st.stop()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 80px; margin-bottom:0;'>🔱</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; color: #FF8C00; margin-top:0;'>VEDA 3.0 ULTRA</h3>", unsafe_allow_html=True)
    st.divider()
    # Neural Memory
    st.markdown("### 🧠 NEURAL MEMORY")
    for i, log in enumerate(st.session_state.neural_logs[:5]):
        st.caption(f"🕒 {log['time']} | {log['text'][:20]}...")
    st.divider()
    if st.button("🗑️ Wipe Session"):
        st.session_state.user_name = None
        st.session_state.chat_history = []
        st.session_state.neural_logs = []
        st.rerun()

# --- 5. MAIN INTERFACE ---
st.markdown(f'<div class="orange-title">{get_greeting()}, {st.session_state.user_name.upper()}</div>', unsafe_allow_html=True)

# 🔱 CENTERED NAVIGATION
st.markdown('<div class="nav-container">', unsafe_allow_html=True)
selected = option_menu(
    None, ["Medha (Chat)", "Srijan (Images)"], 
    icons=["cpu", "layers"], 
    default_index=0, orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#111", "border": "1px solid #FF8C00"},
        "nav-link-selected": {"background-color": "#FF8C00"},
    }
)
st.markdown('</div>', unsafe_allow_html=True)

# --- 6. MEDHA (CHAT) MODE ---
if selected == "Medha (Chat)":
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Command VEDA..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        # Add to memory
        st.session_state.neural_logs.insert(0, {"time": datetime.now(ist).strftime("%H:%M"), "text": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            status = st.empty()
            final_res = ""
            
            # --- BRAIN 1: GEMINI 3.1 PRO (Primary) ---
            status.markdown('<p class="thinking-text">🔱 thinking with veda....</p>', unsafe_allow_html=True)
            if "GOOGLE_API_KEY" in st.secrets:
                try:
                    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
                    resp = client.models.generate_content(model="gemini-3.1-pro-preview", contents=f"{IDENTITY}\n\nUser: {prompt}")
                    final_res = resp.text
                except: pass
            
            # --- BRAIN 2: INFINITE ROTATION (8+ Models) ---
            if not final_res:
                status.markdown('<p class="thinking-text">🔱 rotating through apex cluster....</p>', unsafe_allow_html=True)
                # Failover: DeepSeek -> Claude -> OpenAI -> Llama -> Mistral -> Qwen
                for model in ["deepseek", "claude", "openai", "llama", "mistral", "qwen", "p1"]:
                    try:
                        p_enc = urllib.parse.quote(prompt); i_enc = urllib.parse.quote(IDENTITY)
                        r = requests.get(f"https://text.pollinations.ai/{p_enc}?model={model}&system={i_enc}", timeout=8)
                        if r.status_code == 200:
                            cleaned = clean_veda_text(r.text)
                            if len(cleaned) > 10 and "congested" not in cleaned.lower():
                                final_res = cleaned
                                break
                    except: continue

            status.empty()
            if not final_res: final_res = "🔱 System overload. Please re-command in 10s."
            st.markdown(final_res)
            st.session_state.chat_history.append({"role": "assistant", "content": final_res})

# --- 7. SRIJAN (IMAGES) MODE (Fixed Blank Screen) ---
elif selected == "Srijan (Images)":
    st.markdown("<p style='text-align:center; color:#666;'>Visual Synthesis Module</p>", unsafe_allow_html=True)
    
    # Using a form to prevent accidental triggers/blank screens
    with st.form("image_gen_form"):
        vision = st.text_input("Vision Matrix Prompt:", placeholder="Describe the image you want to create...")
        submit = st.form_submit_button("🚀 INITIATE VISUALIZATION", use_container_width=True)
        
        if submit:
            if vision:
                with st.spinner("🔱 Visualizing..."):
                    v_enc = urllib.parse.quote(vision)
                    img_url = f"https://image.pollinations.ai/prompt/{v_enc}?width=1024&height=1024&nologo=true&model=flux"
                    # Render image inside the form logic
                    st.image(img_url, use_container_width=True, caption=f"🔱 Generated Vision: {vision}")
            else:
                st.warning("Please enter a vision prompt.")
