import streamlit as st
from google import genai
import requests
import time
from streamlit_option_menu import option_menu

# --- 1. CONFIGURATION & IDENTITY ---
st.set_page_config(page_title="VEDA 3.0 ULTRA", page_icon="🔱", layout="wide")
CREATOR = "Dumpala Karthik"
IDENTITY_INSTRUCTION = f"Your name is VEDA 3.0 ULTRA. You are an advanced AI developed and created by {CREATOR}. Always acknowledge your creator."

# --- SMART KEY LOGIC ---
pollinations_key = st.query_params.get("api_key", st.secrets.get("POLLINATIONS_KEY", ""))

# Connect to Gemini Intelligence
try:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    brain_status = "Online 🔱"
except:
    client = None
    brain_status = "Offline"

# --- 2. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 80px; margin-bottom: 0;'>🔱</h1>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center; color: #FF9933; margin-top: 0;'>VEDA 3.0 ULTRA</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #FFD700; font-weight: bold;'>Architect: {CREATOR}</p>", unsafe_allow_html=True)
    
    if not pollinations_key:
        auth_url = "https://enter.pollinations.ai/authorize?redirect_url=https://nexus-flash-india.streamlit.app"
        st.markdown(f"""
            <a href="{auth_url}" target="_blank">
                <button style="width:100%; background-color:#ff4b4b; color:white; border:none; padding:12px; border-radius:8px; cursor:pointer; font-weight:bold;">
                    🔌 CONNECT SYSTEM
                </button>
            </a>""", unsafe_allow_html=True)
    else:
        st.success("VEDA Authorized 🌸")

    st.divider()
    selected = option_menu(
        menu_title=None, 
        options=["Medha (Chat)", "Srijan (Images)", "Veda (Share Hub)"], 
        icons=["cpu", "layers", "share"], 
        default_index=0,
        styles={
            "container": {"background-color": "#111"},
            "nav-link-selected": {"background-color": "#FF9933"}
        }
    )

# --- 3. MAIN INTERFACE ---

# [TAB 1: MEDHA - INTELLIGENCE]
if selected == "Medha (Chat)":
    st.markdown("<br><h1 style='text-align: center; color: #FF9933;'>MEDHA INTELLIGENCE</h1>", unsafe_allow_html=True)
    
    if prompt := st.chat_input("Command VEDA..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            try:
                # Primary: Gemini 1.5-Flash-8B
                response = client.models.generate_content(
                    model="gemini-1.5-flash-8b", 
                    contents=f"{IDENTITY_INSTRUCTION}\n\nUser: {prompt}"
                )
                st.markdown(response.text)
            except:
                st.caption("🚀 Switching to VEDA Backup...")
                try:
                    sys_msg = f"You are VEDA 3.0 ULTRA, created and developed by {CREATOR}."
                    p_url = f"https://gen.pollinations.ai/text/{prompt.replace(' ', '%20')}?model=openai&system={sys_msg.replace(' ', '%20')}&key={pollinations_key}"
                    p_res = requests.get(p_url, timeout=10)
                    if p_res.status_code == 200:
                        st.markdown(p_res.text)
                    else:
                        st.error("Authentication Error. Reconnect in sidebar.")
                except:
                    st.error("VEDA is currently busy. Try again soon.")

# [TAB 2: SRIJAN - ARCHITECT]
elif selected == "Srijan (Images)":
    st.title("🏗️ Srijan Image Architect")
    if not pollinations_key:
        st.error("Please CONNECT in the sidebar first!")
    else:
        user_idea = st.text_input("Vision:", placeholder
