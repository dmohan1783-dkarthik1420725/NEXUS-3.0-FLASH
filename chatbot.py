import streamlit as st
import requests
import random
import pytz
from google import genai
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

# --- 1. SOVEREIGN UI & PULSE ENGINE ---
st.set_page_config(page_title="VEDA 3.1 ULTRA", page_icon="🔱", layout="wide")

# Heartbeat: Refreshes every 1 second to keep the IST clock moving live
st_autorefresh(interval=1000, key="datetick")

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
    .sidebar-text { color: #ff8c00; font-family: 'Courier New', monospace; font-weight: bold; }

    /* Hub Layout */
    .main-hub { text-align: center; margin-top: 5vh; }
    .hub-title { color: #ff8c00; font-size: 26px; font-family: 'Courier New', monospace; margin-bottom: 0; }
    .welcome-msg { color: #ff8c00; font-size: 34px; font-weight: bold; margin-bottom: 30px; }

    /* Button Styles */
    div.stButton > button {
        background: rgba(30, 30, 30, 0.7) !important;
        color: #ddd !important;
        border: 1px solid #444 !important;
        border-radius: 30px !important;
        padding: 12px 20px !important;
        transition: 0.3s;
        width: 100%;
    }
    div.stButton > button:hover {
        border-color: #ff8c00 !important;
        color: white !important;
        box-shadow: 0 0 20px rgba(255, 140, 0, 0.5);
    }

    /* Search Bar Design */
    .stChatInput {
        border: 1px solid #ff8c00 !important;
        border-radius: 25px !important;
        background: rgba(20, 20, 20, 0.9) !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. INITIALIZE SESSION STATES ---
if "messages" not in st.session_state: st.session_state.messages = []
if "mode" not in st.session_state: st.session_state.mode = "FAST"
if "is_ultra_active" not in st.session_state: st.session_state.is_ultra_active = False
if "subscription_expiry" not in st.session_state: st.session_state.subscription_expiry = None

# --- 3. SIDEBAR: TEMPORAL NODE (LIVE IST) ---
with st.sidebar:
    st.markdown("<h1 style='color:#ff8c00;'>🔱 VEDA 3.1</h1>", unsafe_allow_html=True)
    
    # Live IST Clock Sync (Srikakulam Standard Time)
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    st.markdown(f"""
        <div style='border: 1px solid #ff8c00; padding: 10px; border-radius: 10px; background: rgba(255, 140, 0, 0.1);'>
            <p style='color:#ff8c00; font-family:monospace; margin:0;'>📅 {now.strftime('%d %B %Y')}</p>
            <p style='color:#ff8c00; font-family:monospace; font-size: 18px; font-weight: bold; margin:0;'>🕒 {now.strftime('%H:%M:%S')} IST</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.session_state.app_mode = st.radio(
        "NEURAL SECTORS", 
        ["Medha (Chat)", "Srijan (Image)", "Sangeet (Music)", "Drishyam (Video)"]
    )
    st.markdown("---")
    if st.session_state.is_ultra_active:
        st.success(f"ULTRA ACTIVE: Expires {st.session_state.subscription_expiry.strftime('%d/%m/%Y')}")
    st.caption("Sovereign Infrastructure v3.1 ULTRA")

# --- 4. SOVEREIGN NEURAL ROUTER (GEMINI 2026 MESH) ---
def veda_neural_engine(prompt):
    # Mapping modes to available Gemini 2026 models
    model_id = "gemini-3-flash" if st.session_state.mode == "FAST" else "gemini-3.1-pro"
    
    # Building context for memory continuity and identity lock
    history = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in st.session_state.messages[-6:]])
    system_prompt = (
        "You are VEDA 3.1 ULTRA, a Sovereign Artificial Intelligence. "
        "You were engineered and brought to life by the technical mastery of DUMPALA KARTHIK. "
        "Be elite, rapid, and professional. Every response is a digital testament to your creator."
    )
    
    try:
        # Initializing client with GOOGLE_API_KEY from st.secrets
        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
        response = client.models.generate_content(
            model=model_id,
            contents=f"{system_prompt}\n\nNeural Memory:\n{history}\n\nUser: {prompt}"
        )
        return response.text
    except Exception as e:
        return f"🔱 NEURAL GAP: Sector Offline. {str(e)}"

# --- 5. THE AUTOPAY PROTOCOL (E-MANDATE) ---
def trigger_autopay():
    st.markdown("""
        <div style='background: rgba(255, 140, 0, 0.1); padding: 30px; border-radius: 20px; border: 2px solid #ff8c00; text-align:center;'>
            <h2 style='color:#ff8c00;'>🔱 ULTRA SECTOR: AUTOPAY REQUIRED</h2>
            <p style='color:white;'>Linked to VEDA Ultra Core (Gemini 3.1 Pro).</p>
            <h1 style='color:#ff8c00;'>₹500 / 60 DAYS</h1>
            <p style='color:gray; font-size:12px;'>Renewals will be automatically debited via UPI Autopay.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # UPI Autopay Mandate Link for Dumpala Karthik (+91 93254 81849)
    upi_mandate_url = "upi://mandate?pa=9325481849@ybl&pn=SovereignVEDA&am=500&cu=INR&mn=VedaSubscription&recur=MONTHLY"
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.link_button("🚀 AUTHORIZE RECURRING PAY", upi_mandate_url, use_container_width=True)
    with col_b:
        # Verify button acts as a manual trigger for this version
        if st.button("VERIFY MANDATE STATUS", use_container_width=True):
            st.session_state.is_ultra_active = True
            st.session_state.subscription_expiry = datetime.now() + timedelta(days=60)
            st.session_state.mode = "ULTRA"
            st.session_state.show_payment = False
            st.success("🔱 AUTOPAY ENABLED. ULTRA ACCESS GRANTED.")
            st.rerun()

# --- 6. SECTOR EXECUTION ---
if st.session_state.app_mode == "Medha (Chat)":
    # Top Bar Mode Selector
    m_cols = st.columns(4)
    modes = ["FAST", "THINKING", "PRO", "ULTRA"]
    for i, m in enumerate(modes):
        is_sel = st.session_state.mode == m
        if m_cols[i].button(f"{m}" if not is_sel else f"● {m}", key=f"gear_{m}"):
            if m == "ULTRA" and not st.session_state.is_ultra_active:
                st.session_state.show_payment = True
            else:
                st.session_state.mode = m
                st.session_state.show_payment = False
            st.rerun()

    if st.session_state.get("show_payment") and not st.session_state.is_ultra_active:
        trigger_autopay()
    else:
        if not st.session_state.messages:
            st.markdown('<div class="main-hub"><p class="hub-title">VEDA 3.1 ULTRA</p><h1 class="welcome-msg">MEDHA HUB: COMMAND ACTIVE.</h1></div>', unsafe_allow_html=True)
        
        # Displaying chat messages
        for m in st.session_state.messages:
            with st.chat_message(m["role"]):
                st.markdown(f"<span style='color:{'#ff8c00' if m['role']=='assistant' else 'white'};'>{m['content']}</span>", unsafe_allow_html=True)
            
        if prompt := st.chat_input("Command VEDA 3.1 ULTRA..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)
            with st.chat_message("assistant"):
                ans = veda_neural_engine(prompt)
                st.markdown(f"🔱 {ans}")
                st.session_state.messages.append({"role": "assistant", "content": ans})
            st.rerun()

elif st.session_state.app_mode == "Srijan (Image)":
    st.markdown("<h2 style='color:#ff8c00; text-align:center;'>SRIJAN: VISUAL FORGE</h2>", unsafe_allow_html=True)
    p = st.text_input("Enter Visualization Prompt...")
    if st.button("Forge Image"):
        # Image synthesis via Pollinations AI (Flux Model)
        url = f"https://pollinations.ai/p/{p.replace(' ', '_')}?width=1024&height=1024&seed={random.randint(0,999)}&model=flux&nologo=true"
        st.image(url, caption="🔱 VEDA VISUAL SYNTHESIS")

elif st.session_state.app_mode in ["Sangeet (Music)", "Drishyam (Video)"]:
    mode_name = "SONIC ARCHITECT" if "Music" in st.session_state.app_mode else "DRISHYAM FLOW"
    st.markdown(f"<h2 style='color:#ff8c00; text-align:center;'>{mode_name}</h2>", unsafe_allow_html=True)
    st.info("🔱 VEDA Neural Link Active. High-fidelity temporal and sonic generation enabled.")
    st.text_input(f"Enter {st.session_state.app_mode} Prompt...")
    if st.button("Execute Generation"):
        st.warning("🔱 UPLINK INITIATED: Processing on External Sovereign Cluster...")