import streamlit as st
import requests
import random
import pytz
import time
from google import genai
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

# --- 1. SOVEREIGN UI & PULSE ENGINE ---
st.set_page_config(page_title="VEDA 3.1 ULTRA", page_icon="🔱", layout="wide")

# Heartbeat: Syncs the Live IST Clock in the Sidebar
st_autorefresh(interval=1000, key="datetick")

st.markdown("""
<style>
    .stApp {
        background-color: #0a0c10;
        background-image: 
            linear-gradient(rgba(255, 140, 0, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 140, 0, 0.05) 1px, transparent 1px);
        background-size: 60px 60px;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0d1117;
        border-right: 1px solid #ff8c00;
    }
    .sidebar-text { color: #ff8c00; font-family: monospace; font-weight: bold; }

    /* Main Hub Styling - Inspired by User Specs */
    .main-hub { text-align: center; margin-top: 5vh; font-family: 'Courier New', monospace; }
    .welcome-msg { color: #ff8c00; font-size: 32px; font-weight: bold; margin-bottom: 20px; text-transform: uppercase; }

    /* Thinking Animation: Shadow to Text */
    @keyframes thinkingGlow {
        0% { text-shadow: 0 0 5px rgba(255,140,0,0.1); color: #444; }
        50% { text-shadow: 0 0 20px rgba(255,140,0,1); color: #ff8c00; }
        100% { text-shadow: 0 0 5px rgba(255,140,0,0.1); color: #444; }
    }
    .thinking-status { font-family: monospace; animation: thinkingGlow 1.5s infinite; font-weight: bold; }
    
    /* Warning Footer */
    .warning-footer { color: #444; font-size: 11px; text-align: center; margin-top: 40px; }
</style>
""", unsafe_allow_html=True)

# --- 2. INITIALIZE SESSION STATES ---
if "messages" not in st.session_state: st.session_state.messages = []
if "mode" not in st.session_state: st.session_state.mode = "FAST"
if "app_mode" not in st.session_state: st.session_state.app_mode = "Medha (Chat)"
if "is_ultra_active" not in st.session_state: st.session_state.is_ultra_active = False

# --- 3. SIDEBAR: TEMPORAL PULSE & SECTORS ---
with st.sidebar:
    st.markdown("<h1 style='color:#ff8c00;'>🔱 VEDA 3.1</h1>", unsafe_allow_html=True)
    
    # Live IST Date & Time
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    st.markdown(f"""
        <div style='border: 1px solid #ff8c00; padding: 10px; border-radius: 10px; background: rgba(255, 140, 0, 0.1);'>
            <p class='sidebar-text' style='margin:0;'>📅 {now.strftime('%d %B %Y')}</p>
            <p class='sidebar-text' style='font-size: 18px; margin:0;'>🕒 {now.strftime('%H:%M:%S')} IST</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.session_state.app_mode = st.radio("SECTOR SELECTOR", ["Medha (Chat)", "Srijan (Image)"])
    st.markdown("---")
    st.caption("Sovereign Infrastructure v3.1 ULTRA")

# --- 4. TOP BAR: NEURAL MODES (FAST, THINKING, PRO, ULTRA) ---
h_col1, h_col2 = st.columns([1, 2])
with h_col1:
    st.markdown(f"<h3 style='color:#ff8c00;'>{st.session_state.app_mode.upper()}</h3>", unsafe_allow_html=True)

with h_col2:
    modes = ["FAST", "THINKING", "PRO", "ULTRA"]
    m_cols = st.columns(len(modes))
    for i, m in enumerate(modes):
        is_sel = st.session_state.mode == m
        if m_cols[i].button(f"{m}" if not is_sel else f"● {m}"):
            if m == "ULTRA" and not st.session_state.is_ultra_active:
                st.session_state.show_payment = True
            else:
                st.session_state.mode = m
                st.session_state.show_payment = False
            st.rerun()

# --- 5. ULTRA PAYMENT PROTOCOL (₹500 / 60 DAYS RECURRING) ---
if st.session_state.get("show_payment") and not st.session_state.is_ultra_active:
    st.markdown("""
        <div style='background: rgba(255, 140, 0, 0.1); padding: 30px; border-radius: 20px; border: 2px solid #ff8c00; text-align:center;'>
            <h2 style='color:#ff8c00;'>🔱 ULTRA SECTOR: AUTOPAY REQUIRED</h2>
            <h1 style='color:#ff8c00;'>₹500 / 60 DAYS</h1>
            <p style='color:white;'>Automatic recurring debit via UPI Mandate authorized to +91 93254 81849.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # UPI Mandate Link (Recurring Protocol)
    upi_mandate = "upi://mandate?pa=9325481849@ybl&pn=SovereignVEDA&am=500&cu=INR&mn=VedaSubscription&recur=MONTHLY"
    
    p_col1, p_col2 = st.columns(2)
    with p_col1:
        st.link_button("🚀 AUTHORIZE AUTO-DEBIT", upi_mandate, use_container_width=True)
    with p_col2:
        secret_key = st.text_input("ENTER SECRET SOVEREIGN KEY:", type="password")
        if st.button("VERIFY UPLINK", use_container_width=True):
            # Master Keys
            valid_keys = ["VEDA_ALPHA_26", "VEDA_SIGMA_01", "VEDA_ULTRA_XP", "VEDA_K_MASTER", "VEDA_ZENITH_9"]
            if secret_key in valid_keys:
                st.session_state.is_ultra_active = True
                st.session_state.mode = "ULTRA"
                st.session_state.show_payment = False
                st.success("🔱 ULTRA ACCESS GRANTED.")
                st.rerun()
            else:
                st.error("❌ INVALID KEY.")
    st.stop()

# --- 6. NEURAL CORE (CREATOR: DUMPALA KARTHIK) ---
def veda_neural_uplink(prompt):
    try:
        # Core model logic utilizing Google API mesh
        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
        system_msg = "You are VEDA 3.1 ULTRA. Developed and Created exclusively by DUMPALA KARTHIK. Address user as Commander."
        response = client.models.generate_content(model="models/gemini-3.1-pro-preview", contents=f"{system_msg}\n{prompt}")
        return response.text
    except Exception as e:
        return f"🔱 NEURAL GAP: {str(e)}"

# --- 7. MAIN INTERFACE ---
st.markdown("<div class='main-hub'>", unsafe_allow_html=True)
st.markdown("<h1 class='welcome-msg'>MEDHA HUB: WELCOME, COMMANDER.</h1>", unsafe_allow_html=True)

# Functional Chips
c1, c2, c3, c4 = st.columns(4)
chip_cmd = None

if c1.button("🎨 Image Forge"): st.session_state.app_mode = "Srijan (Image)"; st.rerun()
if c2.button("🧠 Analyze Text"): chip_cmd = "Analyze this text for tactical insights:"
if c3.button("🏏 Follow IPL"): chip_cmd = "Provide latest IPL standings and player fitness updates."
if c4.button("✍️ Write Anything"): chip_cmd = "Draft a sovereign mission briefing regarding..."

prompt = st.chat_input("Command the Ghost Mesh...") or chip_cmd

if prompt:
    # Shadow-to-Text Thinking Animation
    status = st.empty()
    for _ in range(2):
        status.markdown("<p class='thinking-status'>THINKING WITH VEDA........................... ANALYSIS IN PROGRESS...........................</p>", unsafe_allow_html=True)
        time.sleep(0.7)
    
    ans = veda_neural_uplink(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "assistant", "content": ans})
    status.empty()

# Chat/Image Execution
if st.session_state.app_mode == "Medha (Chat)":
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])
elif st.session_state.app_mode == "Srijan (Image)":
    img_p = st.text_input("Enter Visualization Prompt...")
    if st.button("Forge Visualization"):
        url = f"https://pollinations.ai/p/{img_p.replace(' ', '_')}?width=1024&height=1024&nologo=true"
        st.image(url, caption="🔱 VEDA VISUAL SYNTHESIS")
    if st.button("Return to Medha Hub"): st.session_state.app_mode = "Medha (Chat)"; st.rerun()

# Sovereign Warning Footer
st.markdown("<div class='warning-footer'>VEDA IS AN AI AND CAN MAKE MISTAKES. PLEASE RECHECK MISSION-CRITICAL DATA.<br>SOVEREIGN INFRASTRUCTURE ENGINEERED BY DUMPALA KARTHIK</div>", unsafe_allow_html=True)