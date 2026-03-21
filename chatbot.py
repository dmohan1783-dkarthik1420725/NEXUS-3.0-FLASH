import streamlit as st
from google import genai
from streamlit_option_menu import option_menu

# --- 1. CORE CONFIGURATION ---
st.set_page_config(page_title="NEXUS Flash India", page_icon="⚡", layout="wide")

CREATOR = "Dumpala Karthik"
SYSTEM_PROMPT = f"Your name is NEXUS 3.1. You were developed and created by {CREATOR}."

# Check for Pollinations API Key in the URL
query_params = st.query_params
pollinations_key = query_params.get("api_key", None)

# --- 2. THE SIDEBAR (Facilities & Connect) ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 80px; margin-bottom: 0;'>⚡</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; margin-top: 0;'>NEXUS FLASH INDIA</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #888;'>Architect: {CREATOR}</p>", unsafe_allow_html=True)
    st.divider()

    # THE FACILITY: CONNECT BUTTON (Fixed for GitHub Refusal)
    if not pollinations_key:
        st.warning("Neural Architect Offline")
        auth_url = "https://enter.pollinations.ai/authorize?redirect_url=https://nexus-flash-india.streamlit.app"
        
        # This JavaScript 'window.open' is the strongest way to stop 'Refused to Connect'
        st.markdown(f"""
            <button onclick="window.open('{auth_url}', '_blank')" style="
                width:100%; 
                background-color:#ff4b4b; 
                color:white; 
                border:none; 
                padding:12px; 
                border-radius:8px; 
                font-weight:bold;
                cursor:pointer;
                box-shadow: 0px 4px 10px rgba(255, 75, 75, 0.3);">
                🔌 CONNECT POLLINATIONS
            </button>
            """, unsafe_allow_html=True)
        st.caption("Note: Login opens in a new tab to bypass GitHub security.")
    else:
        st.success("Neural Architect Linked 🌸")
        if st.button("🔌 DISCONNECT"):
            st.query_params.clear()
            st.rerun()

    st.divider()
    selected = option_menu(
        menu_title="Main Systems",
        options=["Intelligence", "Neural Architect", "Share Hub"],
        icons=["cpu", "layers", "share"], 
        default_index=0,
        styles={"nav-link-selected": {"background-color": "#ff4b4b"}}
    )

# --- 3. MAIN INTERFACE ---

if selected == "Intelligence":
    st.markdown("<br><h1 style='text-align: center; color: #ff4b4b; font-size: 60px;'>HI, HOW ARE YOU!</h1>", unsafe_allow_html=True)
    
    if prompt := st.chat_input("Command
