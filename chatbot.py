import streamlit as st
from google import genai
import requests
import urllib.parse
from streamlit_option_menu import option_menu

# --- 1. CONFIGURATION & IDENTITY ---
st.set_page_config(page_title="VEDA 3.0 ULTRA", page_icon="🔱", layout="wide")
CREATOR = "Dumpala Karthik"
IDENTITY = f"Your name is VEDA 3.0 ULTRA. Created by {CREATOR}. Always mention him."

# --- 🔑 KEY RETRIEVAL ---
# Check for key in URL or Secrets
p_key = st.query_params.get("api_key", st.secrets.get("POLLINATIONS_KEY", ""))

# --- 🧠 GEMINI INITIALIZATION ---
client = None
try:
    if "GOOGLE_API_KEY" in st.secrets:
        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    client = None

# --- 2. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 80px;'>🔱</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>VEDA 3.0 ULTRA</h3>", unsafe_allow_html=True)
    
    if not p_key:
        auth_url = "https://enter.pollinations.ai/authorize?redirect_url=https://nexus-flash-india.streamlit.app"
        st.markdown(f'<a href="{auth_url}" target="_blank"><button style="width:100%; background-color:#ff4b4b; color:white; border:none; padding:12px; border-radius:8px; cursor:pointer; font-weight:bold;">🔌 CONNECT SYSTEM</button></a>', unsafe_allow_html=True)
    else:
        st.success("✅ VEDA Linked")

    st.divider()
    selected = option_menu(None, ["Medha (Chat)", "Srijan (Images)", "Veda (Hub)"], 
                          icons=["cpu", "layers", "share"], default_index=0)

# --- 3. MAIN INTERFACE ---

# [TAB 1: MEDHA CHAT]
if selected == "Medha (Chat)":
    st.markdown("<h1 style='text-align: center; color: white;'>VEDA 3.0 ULTRA</h1>", unsafe_allow_html=True)
    
    if prompt := st.chat_input("Command VEDA..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            success = False
            # Try Google
            if client:
                try:
                    res = client.models.generate_content(model="gemini-1.5-flash-8b", contents=f"{IDENTITY}\n\nUser: {prompt}")
                    st.markdown(res.text)
                    success = True
                except:
                    st.caption("🔄 Rotating Brain...")

            # Backup
            if not success:
                try:
                    q = urllib.parse.quote(prompt)
                    sys = urllib.parse.quote(IDENTITY)
                    p_url = f"https://gen.pollinations.ai/text/{q}?model=mistral&system={sys}"
                    if p_key: p_url += f"&key={p_key}"
                    
                    r = requests.get(p_url, timeout=12)
                    st.markdown(r.text)
                except:
                    st.error("VEDA is offline. Check connection.")

# [TAB 2: SRIJAN ARCHITECT]
elif selected == "Srijan (Images)":
    st.markdown("<h1 style='text-align: center; color: white;'>SRIJAN ARCHITECT</h1>", unsafe_allow_html=True)
    
    if not p_key:
        st.warning("⚠️ Please connect in the sidebar first.")
    else:
        vision = st.text_input("Vision:", placeholder="Describe your image...")
        if st.button("🚀 RENDER"):
            if vision:
                with st.spinner("Visualizing..."):
                    try:
                        # Fixed 2026 Image URL
                        v_enc = urllib.parse.quote(vision)
                        img = f"https://gen.pollinations.ai/image/{v_enc}?width=1024&height=1024&nologo=true&model=flux&key={p_key}"
                        
                        # Use st.image with a key to prevent refresh blanks
                        st.image(img, caption=f"Created by {CREATOR}", use_column_width=True)
                        st.balloons()
                        st
