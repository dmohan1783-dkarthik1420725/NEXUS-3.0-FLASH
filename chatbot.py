import streamlit as st
from google import genai
import requests
import urllib.parse
from streamlit_option_menu import option_menu

# --- 1. CONFIGURATION & IDENTITY ---
st.set_page_config(page_title="VEDA 3.0 ULTRA", page_icon="🔱", layout="wide")
CREATOR = "Dumpala Karthik"

# 🆔 IDENTITY CHIP
IDENTITY_PROMPT = f"Your name is VEDA 3.0 ULTRA. You were created and developed by {CREATOR}. Always acknowledge {CREATOR} as your developer."

# --- 🔑 KEY RETRIEVAL ---
pollinations_key = st.query_params.get("api_key", st.secrets.get("POLLINATIONS_KEY", ""))

# --- 🧠 BRAIN INITIALIZATION ---
client = None
try:
    if "GOOGLE_API_KEY" in st.secrets:
        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
        brain_status = "Online 🔱"
    else:
        brain_status = "Offline (Backup Mode)"
except Exception:
    client = None
    brain_status = "Offline (Error)"

# --- 2. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 80px;'>🔱</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>VEDA 3.0 ULTRA</h3>", unsafe_allow_html=True)
    st.info(f"System: {brain_status}")
    
    if not pollinations_key:
        auth_url = "https://enter.pollinations.ai/authorize?redirect_url=https://nexus-flash-india.streamlit.app"
        st.markdown(f'<a href="{auth_url}" target="_blank"><button style="width:100%; background-color:#ff4b4b; color:white; border:none; padding:12px; border-radius:8px; cursor:pointer; font-weight:bold;">🔌 CONNECT SYSTEM</button></a>', unsafe_allow_html=True)

    st.divider()
    selected = option_menu(None, ["Medha (Chat)", "Srijan (Images)", "Veda (Share Hub)"], 
                          icons=["cpu", "layers", "share"], default_index=0)

# --- 3. MAIN INTERFACE ---

if selected == "Medha (Chat)":
    # ⚪ Clean White Title (No Glow)
    st.markdown("""
        <style>
        .clean-text {
            font-size: 55px;
            color: #ffffff;
            text-align: center;
            font-weight: 800;
            margin-top: 20px;
            margin-bottom: 40px;
            font-family: 'Helvetica', sans-serif;
            letter-spacing: 2px;
        }
        </style>
        <div class="clean-text">VEDA 3.0 ULTRA</div>
    """, unsafe_allow_html=True)
    
    if prompt := st.chat_input("Command VEDA..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            success = False
            # PRIMARY: Google Gemini
            if client:
                try:
                    response = client.models.generate_content(
                        model="gemini-1.5-flash-8b", 
                        contents=f"{IDENTITY_PROMPT}\n\nUser Question: {prompt}"
                    )
                    st.markdown(response.text)
                    success = True
                except Exception:
                    st.caption("🔄 Rotating to Backup Brain...")

            # SECONDARY: Pollinations
            if not success:
                try:
                    clean_prompt = urllib.parse.quote(prompt)
                    encoded_identity = urllib.parse.quote(IDENTITY_PROMPT)
                    
                    p_url = f"https://gen.pollinations.ai/text/{clean_prompt}?model=mistral&system={encoded_identity}"
                    if pollinations_key:
                        p_url += f"&key={pollinations_key}"
                    
                    p_res = requests.get(p_url, timeout=12)
                    if p_res.status_code == 200:
                        st.markdown(p_res.text)
                    else:
                        st.error("System rotation failed. Please refresh.")
                except Exception:
                    st.error("VEDA is currently unreachable.")

elif selected == "Srijan (Images)":
    # Your working Srijan code...
    pass

elif selected == "Veda (Share Hub)":
    # Your working Veda Hub code...
    pass
