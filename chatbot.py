import streamlit as st
import time

# --- 1. SIDEBAR STATE ---
if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = "expanded"

st.set_page_config(page_title="VEDA 3.0 ULTRA", page_icon="🔱", layout="wide", initial_sidebar_state=st.session_state.sidebar_state)

# --- 2. CSS FOR THE FLOATING ARROW ---
st.markdown("""
    <style>
    /* Hide default Streamlit headers */
    header {visibility: hidden;}
    
    /* 🔱 THE SOVEREIGN ARROW (Left Upper Side of Middle Page) */
    .sovereign-arrow {
        position: fixed;
        top: 20%;      /* Upper side */
        left: 30px;    /* Moved away from edge into the middle page */
        z-index: 99999;
        background: linear-gradient(135deg, #FF8C00, #ffae42);
        color: white;
        padding: 15px 20px;
        border-radius: 12px;
        font-size: 24px;
        font-weight: bold;
        box-shadow: 0 0 20px rgba(255, 140, 0, 0.8);
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        animation: pulse-glow 2s infinite;
    }

    @keyframes pulse-glow {
        0% { box-shadow: 0 0 10px rgba(255, 140, 0, 0.6); transform: scale(1); }
        50% { box-shadow: 0 0 30px rgba(255, 140, 0, 1); transform: scale(1.1); }
        100% { box-shadow: 0 0 10px rgba(255, 140, 0, 0.6); transform: scale(1); }
    }

    .v-title { font-size: 50px; color: #FF8C00; text-align: center; font-weight: 900; margin-top: 50px; }
    .v-sub { text-align: center; color: #666; font-size: 16px; margin-top: -10px; }
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR LOGIC ---
with st.sidebar:
    st.markdown("### 🔱 VEDA 3.0 ULTRA")
    if st.button("« Collapse Menu"):
        st.session_state.sidebar_state = "collapsed"
        st.rerun()
    st.divider()
    st.write("Sovereign Intelligence Mode Active")

# --- 4. DISPLAY ARROW ONLY IF COLLAPSED ---
if st.session_state.sidebar_state == "collapsed":
    # This renders the glowing arrow at the left-upper middle page
    st.markdown('<div class="sovereign-arrow">➤</div>', unsafe_allow_html=True)

# --- 5. MAIN CONTENT ---
st.markdown('<div class="v-title">VEDA 3.0 ULTRA</div>', unsafe_allow_html=True)
st.markdown('<div class="v-sub">Sovereign Neural Interface</div>', unsafe_allow_html=True)

# Your chat input and other logic goes here...
prompt = st.chat_input("Command VEDA 3.0 ULTRA...")
