import streamlit as st
from google import genai
import requests
from duckduckgo_search import DDGS
from datetime import datetime
import time
import random

# --- 1. SOVEREIGN UI ENGINE (ORANGE GEOMETRIC GRID) ---
st.set_page_config(page_title="VEDA 3.1 ULTRA", page_icon="🔱", layout="wide")

st.markdown("""
<style>
    /* Dark Background with Orange Geometric Overlay */
    .stApp {
        background-color: #0a0c10;
        background-image: 
            linear-gradient(rgba(255, 140, 0, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 140, 0, 0.05) 1px, transparent 1px);
        background-size: 60px 60px;
    }
    
    /* Sidebar Branding */
    [data-testid="stSidebar"] {
        background-color: #0d1117;
        border-right: 1px solid #ff8c00;
    }
    .sidebar-text { color: #ff8c00; font-family: 'Courier New', monospace; font-size: 14px; }

    /* Header & Branding */
    .veda-orange { color: #ff8c00 !important; font-family: 'Courier New', monospace; }
    
    /* Centered Hub Layout */
    .main-hub { text-align: center; margin-top: 5vh; }
    .hub-title { color: #ff8c00; font-size: 24px; font-family: 'Courier New', monospace; margin-bottom: 0; }
    .welcome-msg { color: #ff8c00; font-size: 32px; font-weight: bold; margin-bottom: 20px; }

    /* Action Pills Styles */
    div.stButton > button {
        background: rgba(30, 30, 30, 0.7) !important;
        color: #ddd !important;
        border: 1px solid #444 !important;
        border-radius: 30px !important;
        padding: 10px 20px !important;
        transition: 0.3s;
        width: 100%;
    }
    div.stButton > button:hover {
        border-color: #ff8c00 !important;
        color: white !important;
        box-shadow: 0 0 15px rgba(255, 140, 0, 0.4);
    }

    /* Search Bar Design */
    .stChatInput {
        border: 1px solid #ff8c00 !important;
        border-radius: 20px !important;
        background: rgba(20, 20, 20, 0.8) !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. INITIALIZE SESSION STATES ---
if "messages" not in st.session_state: st.session_state.messages = []
if "mode" not in st.session_state: st.session_state.mode = "FAST"
if "app_mode" not in st.session_state: st.session_state.app_mode = "Medha (Chat)"
if "is_ultra_active" not in st.session_state: st.session_state.is_ultra_active = False
if "show_payment" not in st.session_state: st.session_state.show_payment = False

# --- 3. SIDEBAR: IDENTITY & MODES ---
with st.sidebar:
    st.markdown("<h1 style='color:#ff8c00;'>🔱 VEDA 3.1</h1>", unsafe_allow_html=True)
    st.markdown(f"<p class='sidebar-text'>COMMANDER: MOHAN</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='sidebar-text'>DATE: {datetime.now().strftime('%d/%m/2026')}</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='sidebar-text'>TIME: {datetime.now().strftime('%H:%M:%S')}</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # App Modes
    st.session_state.app_mode = st.radio(
        "NEURAL SECTOR", 
        ["Medha (Chat)", "Srijan (Image)", "Sangeet (Music)", "Drishyam (Video)"]
    )
    
    st.markdown("---")
    st.caption("Sovereign AI Infrastructure v3.1.0")

# --- 4. TOP BAR: GEAR SELECTOR & PAYMENT ---
h_col1, h_col2 = st.columns([1, 1])
with h_col1:
    st.markdown(f"<h3 class='veda-orange'>{st.session_state.app_mode.upper()}</h3>", unsafe_allow_html=True)

with h_col2:
    modes = ["FAST", "THINKING", "PRO", "ULTRA"]
    m_cols = st.columns(len(modes))
    for i, m in enumerate(modes):
        is_sel = st.session_state.mode == m
        if m_cols[i].button(f"{m}" if not is_sel else f"● {m}", key=f"gear_{m}"):
            if m == "ULTRA" and not st.session_state.is_ultra_active:
                st.session_state.show_payment = True
            else:
                st.session_state.mode = m
                st.session_state.show_payment = False
            st.rerun()

# --- 5. PAYMENT GATEWAY (ULTRA UNLOCK) ---
if st.session_state.show_payment and not st.session_state.is_ultra_active:
    st.markdown("""
        <div style='background: rgba(255, 140, 0, 0.1); padding: 25px; border-radius: 15px; border: 1px solid #ff8c00; text-align:center;'>
            <h2 style='color:#ff8c00;'>🔱 UNLOCK ULTRA CORRIDOR</h2>
            <p style='color:white;'>Elite Gemini 1.5 Pro + Kling AI + Sonic Architect</p>
            <h1 style='color:#ff8c00;'>₹500 / 2 Months</h1>
        </div>
    """, unsafe_allow_html=True)
    
    # UPI Link: +91 93254 81849
    upi_url = "upi://pay?pa=9325481849@ybl&pn=Mohan&am=500&cu=INR"
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.link_button("🚀 Pay with PhonePe / GPay", upi_url, use_container_width=True)
    with col_b:
        if st.button("✅ I have Paid (Unlock Now)", use_container_width=True):
            with st.spinner("Verifying Transaction..."):
                time.sleep(2)
                st.session_state.is_ultra_active = True
                st.session_state.mode = "ULTRA"
                st.session_state.show_payment = False
                st.success("🔱 ULTRA ACTIVATED.")
                st.rerun()
    st.stop()

# --- 6. NEURAL ROUTER LOGIC ---
def veda_brain_router(prompt):
    model_id = "gemini-1.5-flash" if st.session_state.mode == "FAST" else "gemini-1.5-pro"
    try:
        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
        web_context = ""
        if st.session_state.mode in ["PRO", "ULTRA"]:
            with DDGS() as ddgs:
                web_context = "\n".join([r['body'] for r in ddgs.text(prompt, max_results=3)])
        
        response = client.models.generate_content(
            model=model_id,
            contents=f"System: VEDA 3.1 ULTRA. Mode: {st.session_state.mode}. Context: {web_context}\nUser: {prompt}"
        )
        return response.text
    except Exception as e: return f"🔱 NEURAL GAP: {str(e)}"

# --- 7. MAIN INTERFACE ROUTING ---
if st.session_state.app_mode == "Medha (Chat)":
    if not st.session_state.messages:
        st.markdown('<div class="main-hub"><p class="hub-title">VEDA 3.1 ULTRA</p><h1 class="welcome-msg">MEDHA HUB: WELCOME, COMMANDER.</h1></div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1: st.button("🎨 Image Forge")
        with c2: st.button("🎧 Sonic Architect")
        with c3: st.button("🎬 Drishyam Flow")

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(f"<span style='color:{'#ff8c00' if m['role']=='assistant' else 'white'};'>{m['content']}</span>", unsafe_allow_html=True)

    if prompt := st.chat_input("Command the Ghost Mesh..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            ans = veda_brain_router(prompt)
            st.markdown(f"🔱 {ans}")
            st.session_state.messages.append({"role": "assistant", "content": ans})
        st.rerun()

elif st.session_state.app_mode == "Srijan (Image)":
    st.markdown("<h2 class='veda-orange'>SRIJAN: IMAGE FORGE</h2>", unsafe_allow_html=True)
    p = st.text_input("Enter Visualization Prompt...")
    if st.button("Forge Visualization"):
        seed = random.randint(0, 99999)
        url = f"https://pollinations.ai/p/{p.replace(' ', '_')}?width=1024&height=1024&seed={seed}&model=flux"
        st.image(url, caption="🔱 VEDA VISUAL SYNTHESIS")

elif st.session_state.app_mode in ["Sangeet (Music)", "Drishyam (Video)"]:
    st.markdown(f"<h2 class='veda-orange'>{st.session_state.app_mode.upper()} (KLING AI)</h2>", unsafe_allow_html=True)
    st.info("🔱 KLING AI Neural Link Active. High-fidelity generation enabled.")
    st.text_input("Enter Generative Prompt...")
    st.button("Generate Asset")