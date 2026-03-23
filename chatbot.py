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

IDENTITY = f"Your name is VEDA 3.0 ULTRA. Created and developed by {CREATOR}."

# --- 🧠 NEURAL MEMORY & HISTORY ---
if "neural_logs" not in st.session_state:
    st.session_state.neural_logs = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "active_prompt" not in st.session_state:
    st.session_state.active_prompt = ""

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

# --- 2. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 80px; margin-bottom:0;'>🔱</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; color: #FF8C00; margin-top:0;'>VEDA 3.0 ULTRA</h3>", unsafe_allow_html=True)
    
    # 🕒 SIDEBAR CLOCK
    st.markdown(f"""
        <div style="background-color: rgba(255, 140, 0, 0.1); padding: 10px; border-radius: 10px; border-left: 5px solid #FF8C00; text-align: center;">
            <p style="margin:0; font-size: 12px; color: #FF8C00;">📅 {get_now_full()}</p>
            <p style="margin:0; font-size: 22px; color: white; font-weight: bold;">{get_now_time()}</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    selected = option_menu(
        menu_title="CORE SYSTEMS",
        options=["Medha (Chat)", "Srijan (Images)"],
        icons=["cpu", "layers"],
        menu_icon="cast",
        default_index=0,
        styles={
            "icon": {"color": "#FF8C00"}, 
            "nav-link-selected": {"background-color": "#FF8C00"},
        }
    )
    
    st.divider()
    st.markdown("### 🧠 NEURAL LOGS")
    for i, log in enumerate(st.session_state.neural_logs[:5]):
        if st.button(f"🕒 {log['time']} | {log['text'][:15]}...", key=f"log_{i}", use_container_width=True):
            st.session_state.active_prompt = log['text']
            st.rerun() 

    if st.button("🗑️ Wipe Neural Core"):
        st.session_state.chat_history = []
        st.session_state.neural_logs = []
        st.rerun()

# --- 3. MAIN INTERFACE LOGIC ---
# FIXED: Using triple quotes to prevent SyntaxError with long strings
ORANGE_TITLE_CSS = """
<style>
.orange-title {
    font-size: 50px; 
    color: #FF8C00; 
    text-align: center; 
    font-weight: 800; 
    margin-bottom: 20px;
}
.stPopover { margin-top: 0px; }
</style>
"""
st.markdown(ORANGE_TITLE_CSS, unsafe_allow_html=True)

if selected == "Medha (Chat)":
    st.markdown('<div class="orange-title">VEDA 3.0 ULTRA</div>', unsafe_allow_html=True)
    
    # Chat Display
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    # --- ➕ ACTION BAR & INPUT (Left Aligned) ---
    st.markdown("---")
    input_col1, input_col2 = st.columns([1, 10])
    
    with input_col1:
        plus_menu = st.popover("➕", use_container_width=True)
        cam_file = plus_menu.camera_input("📷 Camera")
        gal_file = plus_menu.file_uploader("🖼️ Gallery", type=['png', 'jpg', 'jpeg'])

    with input_col2:
        prompt = st.chat_input("Command VEDA...")

    active_visual = cam_file or gal_file
    if active_visual:
        st.image(active_visual, caption="📎 Attachment Ready", width=120)

    # Memory Reload Logic
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
            # Byte Buffer conversion for stability
            final_visual = {"mime_type": active_visual.type, "data": active_visual.getvalue()} if active_visual else None

            if client:
                # Prioritizing 3.1 Pro then 2.0 Flash
                for model_choice in ["gemini-3.1-pro-preview", "gemini-2.0-flash"]:
                    try:
                        res = client.models.generate_content(
                            model=model_choice,
                            contents=[f"{IDENTITY}\n{prompt}", final_visual] if final_visual else f"{IDENTITY}\n{prompt}"
                        )
                        answer = res.text
                        success = True
                        break
                    except: continue

            if not success:
                try:
                    q_enc = urllib.parse.quote(prompt)
                    r = requests.get(f"https://text.pollinations.ai/{q_enc}?model=openai", timeout=10)
                    answer = r.text
                    success = True
                except: answer = "🔱 Neural Sync Offline."

            st.markdown(answer)
            st.session_state.chat_history.append({"role": "assistant", "content": answer})

elif selected == "Srijan (Images)":
    st.markdown('<div class="orange-title">SRIJAN ARCHITECT</div>', unsafe_allow_html=True)
    vision = st.text_input("Vision:", placeholder="Describe the image...")
    if st.button("🚀 RENDER"):
        if vision:
            add_to_memory("SRIJAN", vision)
            with st.spinner("🔱 Visualizing..."):
                try:
                    v_enc = urllib.parse.quote(vision)
                    img_url = f"https://pollinations.ai/p/{v_enc}?width=1024&height=1024&seed=42&model=flux&nologo=true"
                    st.image(img_url, use_container_width=True)
                    st.balloons()
                except: st.error("Architect Busy.")
