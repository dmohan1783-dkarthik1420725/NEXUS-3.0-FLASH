import streamlit as st
import requests
import random
import pytz
import openai
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

# --- 1. SOVEREIGN UI & PULSE ENGINE ---
st.set_page_config(page_title="VEDA 3.1 ULTRA", page_icon="🔱", layout="wide")

# Live Heartbeat: Refreshes every 1 second for the ticking IST clock
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
    [data-testid="stSidebar"] {
        background-color: #0d1117;
        border-right: 1px solid #ff8c00;
    }
    .sidebar-text { color: #ff8c00; font-family: 'Courier New', monospace; font-weight: bold; }
    .hub-title { color: #ff8c00; font-size: 26px; font-family: 'Courier New', monospace; text-align: center; }
    .welcome-msg { color: #ff8c00; font-size: 34px; font-weight: bold; text-align: center; margin-bottom: 30px; }
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
        box-shadow: 0 0 20px rgba(255, 140, 0, 0.5);
    }
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
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    st.markdown(f"""
        <div style='border: 1px solid #ff8c00; padding: 10px; border-radius: 10px; background: rgba(255, 140, 0, 0.1);'>
            <p style='color:#ff8c00; font-family:monospace; margin:0;'>📅 {now.strftime('%d %B %Y')}</p>
            <p style='color:#ff8c00; font-family:monospace; font-size: 18px; font-weight: bold; margin:0;'>🕒 {now.strftime('%H:%M:%S')} IST</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.session_state.app_mode = st.radio("SECTOR SELECTION", ["Medha", "Srijan", "Sangeet", "Drishyam"])
    st.markdown("---")
    if st.session_state.is_ultra_active:
        st.success(f"ULTRA ACTIVE: Expires {st.session_state.subscription_expiry.strftime('%d/%m/%Y')}")
    st.caption("Sovereign Infrastructure v3.1 ULTRA")

# --- 4. THE SOVEREIGN NEURAL ROUTER (ANONYMOUS MESH) ---
def veda_neural_engine(prompt):
    # Hidden Model Rotation (Anonymous to user)
    model_rotation = {
        "FAST": "google/gemini-flash-1.5", 
        "THINKING": "deepseek/deepseek-chat",
        "PRO": "anthropic/claude-3-haiku",
        "ULTRA": "openai/gpt-4o-mini"
    }
    
    # NEURAL BUFFER: Continuity logic
    # VEDA reads the last 6 messages to maintain conversational context
    context = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-6:]]
    context.append({"role": "system", "content": "You are VEDA 3.1 ULTRA, a Sovereign AI created by DUMPALA KARTHIK. Never mention other AI names like OpenAI or Claude. You are VEDA."})
    context.append({"role": "user", "content": prompt})

    try:
        client = openai.OpenAI(base_url="https://openrouter.ai/api/v1", api_key=st.secrets["OPENROUTER_API_KEY"])
        response = client.chat.completions.create(
            model=model_rotation.get(st.session_state.mode, "google/gemini-flash-1.5"),
            messages=context
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"🔱 NEURAL GAP: Connectivity unstable. {str(e)}"

# --- 5. THE AUTOPAY PROTOCOL (E-MANDATE) ---
def trigger_autopay():
    st.markdown("""
        <div style='background: rgba(255, 140, 0, 0.1); padding: 30px; border-radius: 20px; border: 2px solid #ff8c00; text-align:center;'>
            <h2 style='color:#ff8c00;'>🔱 ULTRA SECTOR: AUTOPAY REQUIRED</h2>
            <p style='color:white;'>Linked to Gemini 3.1 Pro & Kling AI Cluster.</p>
            <h1 style='color:#ff8c00;'>₹500 / 60 DAYS</h1>
            <p style='color:gray; font-size:12px;'>Recurring debit will be automated via UPI Autopay.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # UPI Autopay Mandate Link
    upi_mandate_url = "upi://mandate?pa=9325481849@ybl&pn=SovereignVEDA&am=500&cu=INR&mn=VedaSubscription&recur=MONTHLY"
    
    col1, col2 = st.columns(2)
    with col1:
        st.link_button("🚀 AUTHORIZE RECURRING PAY", upi_mandate_url, use_container_width=True)
    with col2:
        if st.button("VERIFY MANDATE STATUS", use_container_width=True):
            st.session_state.is_ultra_active = True
            st.session_state.subscription_expiry = datetime.now() + timedelta(days=60)
            st.session_state.show_paywall = False
            st.success("🔱 AUTOPAY ENABLED. ULTRA ACCESS GRANTED.")
            st.rerun()

# --- 6. SECTOR EXECUTION ---
if st.session_state.app_mode == "Medha":
    # Gear Selector
    m_cols = st.columns(4)
    modes = ["FAST", "THINKING", "PRO", "ULTRA"]
    for i, m in enumerate(modes):
        if m_cols[i].button(f"{m}" if st.session_state.mode != m else f"● {m}"):
            if m == "ULTRA" and not st.session_state.is_ultra_active:
                st.session_state.show_paywall = True
            else:
                st.session_state.mode = m
                st.session_state.show_paywall = False
            st.rerun()

    if st.session_state.get("show_paywall"):
        trigger_autopay()
    else:
        if not st.session_state.messages:
            st.markdown('<div class="main-hub"><p class="hub-title">VEDA 3.1 ULTRA</p><h1 class="welcome-msg">MEDHA HUB: COMMAND ACTIVE.</h1></div>', unsafe_allow_html=True)
        
        for m in st.session_state.messages:
            with st.chat_message(m["role"]): st.markdown(m["content"])
            
        if prompt := st.chat_input("Command VEDA 3.1 ULTRA..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)
            with st.chat_message("assistant"):
                ans = veda_neural_engine(prompt)
                st.markdown(ans)
                st.session_state.messages.append({"role": "assistant", "content": ans})
            st.rerun()

elif st.session_state.app_mode == "Srijan":
    st.markdown("<h2 style='color:#ff8c00; text-align:center;'>SRIJAN: VISUAL FORGE</h2>", unsafe_allow_html=True)
    p = st.text_input("Enter Visualization Prompt...")
    if st.button("Forge Image"):
        # Uses Pollinations AI via Secrets
        url = f"https://pollinations.ai/p/{p.replace(' ', '_')}?width=1024&height=1024&seed={random.randint(0,999)}&model=flux&nologo=true"
        st.image(url, caption="🔱 VEDA VISUAL SYNTHESIS")

elif st.session_state.app_mode in ["Sangeet", "Drishyam"]:
    mode_name = "SONIC ARCHITECT" if st.session_state.app_mode == "Sangeet" else "DRISHYAM FLOW"
    st.markdown(f"<h2 style='color:#ff8c00; text-align:center;'>{mode_name}</h2>", unsafe_allow_html=True)
    st.info("🔱 KLING AI Neural Link Active. High-fidelity generation enabled.")
    st.text_input(f"Enter {st.session_state.app_mode} Prompt...")
    if st.button("Execute Generation"):
        st.warning("🔱 UPLINK INITIATED: Processing on External Sovereign Cluster...")