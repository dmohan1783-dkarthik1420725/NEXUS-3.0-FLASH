import streamlit as st
from google import genai
import requests
from streamlit_option_menu import option_menu
import urllib.parse

# --- 1. CONFIGURATION & IDENTITY ---
st.set_page_config(page_title="VEDA 3.0 ULTRA", page_icon="🔱", layout="wide")
CREATOR = "Dumpala Karthik"
IDENTITY_INSTRUCTION = f"Your name is VEDA 3.0 ULTRA. Created by {CREATOR}."

# --- 🔑 THE KEY GATEKEEPER ---
pollinations_key = st.query_params.get("api_key", st.secrets.get("POLLINATIONS_KEY", ""))

# Safety Check for Gemini
client = None
brain_status = "Offline"
if "GOOGLE_API_KEY" in st.secrets:
    try:
        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
        brain_status = "Online 🔱"
    except:
        pass

# --- 2. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 80px;'>🔱</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>VEDA 3.0 ULTRA</h3>", unsafe_allow_html=True)
    st.success(f"System Status: {brain_status}")
    
    if not pollinations_key:
        auth_url = "https://enter.pollinations.ai/authorize?redirect_url=https://nexus-flash-india.streamlit.app"
        st.markdown(f'<a href="{auth_url}" target="_blank"><button style="width:100%; background-color:#ff4b4b; color:white; border:none; padding:12px; border-radius:8px; cursor:pointer; font-weight:bold;">🔌 CONNECT SYSTEM</button></a>', unsafe_allow_html=True)

    st.divider()
    selected = option_menu(None, ["Medha (Chat)", "Srijan (Images)", "Veda (Share Hub)"], 
                          icons=["cpu", "layers", "share"], default_index=0)

# --- 3. MAIN INTERFACE ---

if selected == "Medha (Chat)":
    # --- 🌟 THE GLOWING LOGO CSS 🌟 ---
    st.markdown("""
        <style>
        .glow-text {
            font-size: 60px;
            color: #fff;
            text-align: center;
            font-weight: bold;
            text-transform: uppercase;
            margin-top: 50px;
            margin-bottom: 50px;
            text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #ffffff, 0 0 40px #ffffff;
            font-family: 'Courier New', Courier, monospace;
        }
        </style>
        <h1 class="glow-text">VEDA 3.0 ULTRA</h1>
    """, unsafe_allow_html=True)
    
    if prompt := st.chat_input("Command VEDA..."):
        with st.chat_message("user"): 
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            success = False
            # A. TRY GEMINI
            if client:
                try:
                    response = client.models.generate_content(
                        model="gemini-1.5-flash-8b", 
                        contents=f"{IDENTITY_INSTRUCTION}\n\nUser: {prompt}"
                    )
                    st.markdown(response.text)
                    success = True
                except:
                    st.caption("🔄 Re-routing...")

            # B. BACKUP (POLLINATIONS)
            if not success:
                try:
                    clean_p = urllib.parse.quote(prompt)
                    sys_p = urllib.parse.quote(f"You are VEDA 3.0 ULTRA by {CREATOR}.")
                    p_url = f"https://gen.pollinations.ai/text/{clean_p}?model=mistral&system={sys_p}"
                    if pollinations_key: p_url += f"&key={pollinations_key}"
                    
                    p_res = requests.get(p_url, timeout=10)
                    st.markdown(p_res.text)
                except:
                    st.error("VEDA is currently in deep meditation. Try again shortly.")

elif selected == "Srijan (Images)":
    st.title("🏗️ Srijan Image Architect")
    # ... [Keep your working Srijan code here] ...

elif selected == "Veda (Share Hub)":
    st.title("🌐 Veda Network Hub")
    # ... [Keep your Share Hub grid here] ...
