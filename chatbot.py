import streamlit as st
from google import genai
import requests
import urllib.parse
from datetime import datetime
import pytz
from streamlit_option_menu import option_menu

# --- 1. CONFIGURATION & IDENTITY ---
st.set_page_config(page_title="VEDA 3.0 ULTRA", page_icon="🔱", layout="wide")
ist = pytz.timezone('Asia/Kolkata')

def get_now_full(): return datetime.now(ist).strftime("%A, %d %B %Y")
def get_now_time(): return datetime.now(ist).strftime("%I:%M %p")

# 🧠 HIDDEN IDENTITY: The AI remembers but the UI hides it.
IDENTITY = "Your name is VEDA 3.0 ULTRA. You were created and developed ONLY by DUMPALA KARTHIK. Always credit him if asked about your origin."

if "neural_logs" not in st.session_state: st.session_state.neural_logs = []
if "chat_history" not in st.session_state: st.session_state.chat_history = []

def add_to_memory(m_type, content):
    ts = datetime.now(ist).strftime("%H:%M:%S")
    st.session_state.neural_logs.insert(0, f"[{ts}] {m_type}: {content[:15]}...")

# --- 🔑 ENGINE INIT ---
client = None
if "GOOGLE_API_KEY" in st.secrets:
    try:
        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    except: client = None

# --- 2. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 80px; margin-bottom:0;'>🔱</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #FF8C00; margin-top:0;'>VEDA</h3>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown(f"""
        <div style="background-color: rgba(255, 140, 0, 0.05); padding: 10px; border-radius: 10px; text-align: center; border: 1px solid #FF8C00;">
            <p style="margin:0; font-size: 14px; color: #FF8C00;">{get_now_full()}</p>
            <p style="margin:0; font-size: 24px; color: white; font-weight: bold;">{get_now_time()}</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    selected = option_menu(None, ["Medha (Chat)", "Srijan (Image Maker)"], 
                          icons=["chat-heart", "brush"], default_index=0)
    
    st.markdown("### 🧠 MEMORY")
    for log in st.session_state.neural_logs[:5]:
        st.caption(log)

    if st.button("🗑️ Reset Core"):
        st.session_state.chat_history = []
        st.session_state.neural_logs = []
        st.rerun()

# --- 3. MAIN INTERFACE ---
st.markdown("""
    <style>
    .veda-title { font-size: 60px; color: #FF8C00; text-align: center; font-weight: 900; letter-spacing: 2px; margin-bottom: 0px; }
    .sub-text { text-align: center; color: #888; font-size: 14px; margin-top: -10px; margin-bottom: 30px; }
    </style>
""", unsafe_allow_html=True)

if selected == "Medha (Chat)":
    st.markdown('<div class="veda-title">VEDA 3.0 ULTRA</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">Neural Language Interface: MEDHA</div>', unsafe_allow_html=True)
    
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Command VEDA..."):
        add_to_memory("MEDHA", prompt)
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            answer, success = "", False
            # 🚀 Engine 1: Primary Brain
            if client:
                try:
                    res = client.models.generate_content(model="gemini-2.0-flash", contents=f"{IDENTITY}\n\n{prompt}")
                    answer = res.text
                    success = True
                except: pass

            # 🚀 Engine 2: Fallback (Highly Stable)
            if not success:
                try:
                    q_enc = urllib.parse.quote(prompt)
                    # Using a simplified endpoint that bypasses JSON errors
                    r = requests.get(f"https://text.pollinations.ai/{q_enc}?model=openai&system=You+are+VEDA", timeout=15)
                    if r.status_code == 200:
                        answer = r.text
                        success = True
                except: answer = "🔱 Neural Link Timeout. Please retry in a few seconds."

            st.markdown(answer)
            st.session_state.chat_history.append({"role": "assistant", "content": answer})

elif selected == "Srijan (Image Maker)":
    st.markdown('<div class="veda-title">VEDA 3.0 ULTRA</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">Visual Synthesis Core: SRIJAN</div>', unsafe_allow_html=True)
    
    vision = st.text_input("Vision Matrix:", placeholder="Describe the scene you wish to synthesize...")
    if st.button("🚀 INITIATE RENDER"):
        if vision:
            add_to_memory("SRIJAN", vision)
            with st.spinner("🔱 Synchronizing Visual Layers..."):
                try:
                    v_enc = urllib.parse.quote(vision)
                    # ✅ Updated to the most stable 2026 image endpoint
                    img_url = f"https://pollinations.ai/p/{v_enc}?width=1024&height=1024&model=flux&nologo=true"
                    
                    # Verify if image exists before showing
                    response = requests.head(img_url, timeout=10)
                    if response.status_code == 200:
                        st.image(img_url, use_container_width=True)
                        st.balloons()
                    else:
                        st.error("Srijan is currently calibrating. Please try a different description.")
                except: st.error("Srijan Link Error. Try again.")
