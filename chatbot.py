import streamlit as st
from google import genai
from streamlit_option_menu import option_menu

# --- 1. CORE CONFIGURATION ---
st.set_page_config(page_title="NEXUS 3.0 ULTRA", page_icon="⚡", layout="wide")

CREATOR = "Dumpala Karthik"
SYSTEM_PROMPT = f"Your name is NEXUS 3.0 ULTRA. You were developed and created by {CREATOR}."

# --- SMART KEY LOGIC (URL vs Secrets) ---
query_params = st.query_params
url_key = query_params.get("api_key", None)

# Looks for 'POLLINATIONS_KEY' in your Streamlit Secrets
secrets_key = st.secrets.get("POLLINATIONS_KEY", None)

# Use URL key first, fallback to Secrets key
pollinations_key = url_key if url_key else secrets_key

# Connect to Google Gemini (Intelligence)
try:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    st.sidebar.success("NEXUS Brain Online ⚡")
except Exception:
    st.sidebar.error("NEXUS Brain Offline. Check Secrets.")

# --- 2. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 80px; margin-bottom: 0;'>⚡</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; margin-top: 0;'>NEXUS 3.0 ULTRA</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #888;'>Architect: {CREATOR}</p>", unsafe_allow_html=True)
    st.divider()

    # THE FACILITY: SMART CONNECT BUTTON
    if not pollinations_key:
        st.warning("Neural Architect Offline")
        app_url = "https://nexus-flash-india.streamlit.app"
        auth_url = f"https://enter.pollinations.ai/authorize?redirect_url={app_url}"
        
        st.markdown(f"""
            <a href="{auth_url}" target="_blank" style="text-decoration: none;">
                <div style="
                    width: 100%; 
                    background-color: #ff4b4b; 
                    color: white; 
                    text-align: center; 
                    padding: 12px 0px; 
                    border-radius: 8px; 
                    font-weight: bold;
                    box-shadow: 0px 4px 10px rgba(255, 75, 75, 0.3);
                    cursor: pointer;">
                    🔌 CONNECT POLLINATIONS
                </div>
            </a>
            """, unsafe_allow_html=True)
        st.caption("Login via GitHub to unlock images.")
    else:
        st.success("Neural Architect Linked 🌸")
        if st.button("🔌 RESET / DISCONNECT"):
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

    st.divider()
    qr_url = "
