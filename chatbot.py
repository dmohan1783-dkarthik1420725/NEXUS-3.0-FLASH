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
def get_now_full(): return datetime.now(ist).strftime("%A, %d %B %Y")
def get_now_time(): return datetime.now(ist).strftime("%I:%M %p")

IDENTITY = f"Your name is VEDA 3.0 ULTRA. Created and developed ONLY by {CREATOR}."

# --- 🧠 NEURAL MEMORY ---
if "neural_logs" not in st.session_state: st.session_state.neural_logs = []
if "chat_history" not in st.session_state: st.session_state.chat_history = []

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
    except: gemini_online = False

# --- 2. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 80px; margin-bottom:0;'>🔱</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; color: #FF8C00; margin-top:0;'>VEDA 3.0 ULTRA</h3>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown(f"""
        <div style="background-color: rgba(255, 140, 0, 0.1); padding: 15px; border-radius: 10px; border-left: 5px solid #FF8C00; text-align: center;">
            <p style="margin:0; font-size: 13px; color: #FF8C00; font-weight: bold;">📅 {get_now_full()}</p>
            <p style="margin:5px 0 0 0; font-size: 26px; color: white; font-weight: 800;">{get_now_time()}</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    selected = option_menu(None, ["Medha (Chat)", "Srijan (Images)"], 
                          icons=["cpu", "layers"], default_index=0)
    
    st.markdown("### 🧠 NEURAL LOGS")
    for log in st.session_state.neural_logs[:8]:
        st.code(log, language="text")

    if st.button("🗑️ Wipe Neural Core"):
        st.session_state.chat_history = []
        st.session_state.neural_logs = []
        st.rerun()

# --- 3. MAIN INTERFACE ---
ORANGE_TITLE = "<style>.orange-title {font-size: 50px; color: #FF8C00; text-align: center; font-weight: 800;}</style>"

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
            answer, success = "", False
            
            # --- BRAIN 1: GEMINI 2.0 FLASH (FASTEST & MOST STABLE) ---
            if gemini_online:
                try:
                    res = client.models.generate_content(
                        model="gemini-2.0-flash", 
                        contents=f"{IDENTITY}\n\nUser: {prompt}"
                    )
                    answer = res.text
                    success = True
                except: st.caption("🔄 Neural Link Busy...")

            # --- BRAIN 2: POLLINATIONS BACKUP ---
            if not success:
                try:
                    q_enc = urllib.parse.quote(prompt)
                    # Force a lightweight model for backup to avoid "Heavy" errors
                    p_url = f"https://text.pollinations.ai/{q_enc}?model=openai&system=You+are+VEDA"
                    r = requests.get(p_url, timeout=10)
                    if r.status_code == 200:
                        answer = r.text
                        success = True
                    else: answer = "🔱 **Link Busy.** Please wait 5 seconds."
                except: answer = "Connection Interrupt."

            st.markdown(answer)
            st.session_state.chat_history.append({"role": "assistant", "content": answer})

elif selected == "Srijan (Images)":
    st.markdown(ORANGE_TITLE, unsafe_allow_html=True)
    st.markdown('<div class="orange-title">SRIJAN ARCHITECT</div>', unsafe_allow_html=True)
    
    # Keeping your working Srijan logic exactly as it was
    vision = st.text_input("Vision:", placeholder="Describe your image...")
    if st.button("🚀 RENDER"):
        if vision:
            add_to_memory("SRIJAN", vision)
            with st.spinner("Visualizing..."):
                try:
                    v_enc = urllib.parse.quote(vision)
                    # This is your working Flux link
                    img = f"https://gen.pollinations.ai/image/{v_enc}?width=1024&height=1024&nologo=true&model=flux&key={p_key}"
                    st.image(img, caption=f"Created by {CREATOR}", use_column_width=True)
                    st.balloons()
                    st.markdown(f"**[📥 Download Image]({img})**")
                except: st.error("Architect Busy.")
