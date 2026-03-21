import streamlit as st
from google import genai
import requests
import urllib.parse
from streamlit_option_menu import option_menu

# --- 1. CONFIGURATION & IDENTITY ---
st.set_page_config(page_title="VEDA 3.0 ULTRA", page_icon="🔱", layout="wide")
CREATOR = "Dumpala Karthik"
IDENTITY_INSTRUCTION = f"Your name is VEDA 3.0 ULTRA. Created by {CREATOR}."

# --- 🔑 THE KEY GATEKEEPER ---
# We use .get() so the app doesn't crash if the key is missing
pollinations_key = st.query_params.get("api_key", st.secrets.get("POLLINATIONS_KEY", ""))

# --- 🧠 BRAIN INITIALIZATION ---
client = None
try:
    if "GOOGLE_API_KEY" in st.secrets:
        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
        brain_status = "Online 🔱"
    else:
        brain_status = "Offline (Backup Only)"
except Exception:
    client = None
    brain_status = "Offline (Error)"

# --- 2. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 80px;'>🔱</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>VEDA 3.0 ULTRA</h3>", unsafe_allow_html=True)
    st.info(f"Brain Status: {brain_status}")
    
    if not pollinations_key:
        auth_url = "https://enter.pollinations.ai/authorize?redirect_url=https://nexus-flash-india.streamlit.app"
        st.markdown(f'<a href="{auth_url}" target="_blank"><button style="width:100%; background-color:#ff4b4b; color:white; border:none; padding:12px; border-radius:8px; cursor:pointer; font-weight:bold;">🔌 CONNECT SYSTEM</button></a>', unsafe_allow_html=True)

    st.divider()
    selected = option_menu(None, ["Medha (Chat)", "Srijan (Images)", "Veda (Share Hub)"], 
                          icons=["cpu", "layers", "share"], default_index=0)

# --- 3. MAIN INTERFACE ---

# [TAB 1: MEDHA CHAT]
if selected == "Medha (Chat)":
    # 🌟 Glowing Title
    st.markdown("""
        <style>
        .glow-text {
            font-size: 60px;
            color: #fff;
            text-align: center;
            font-weight: bold;
            text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #ffffff;
            margin-top: 30px;
            margin-bottom: 30px;
        }
        </style>
        <h1 class="glow-text">VEDA 3.0 ULTRA</h1>
    """, unsafe_allow_html=True)
    
    # Chat logic wrapped in a try-block to prevent blank screens
    try:
        if prompt := st.chat_input("Command VEDA..."):
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                success = False
                # Try Google Gemini
                if client:
                    try:
                        response = client.models.generate_content(
                            model="gemini-1.5-flash-8b", 
                            contents=f"{IDENTITY_INSTRUCTION}\n\nUser: {prompt}"
                        )
                        st.markdown(response.text)
                        success = True
                    except Exception:
                        st.caption("🔄 Primary brain busy...")

                # Try Pollinations Backup
                if not success:
                    try:
                        clean_prompt = urllib.parse.quote(prompt)
                        sys_msg = urllib.parse.quote(f"You are VEDA 3.0 ULTRA by {CREATOR}.")
                        p_url = f"https://gen.pollinations.ai/text/{clean_prompt}?model=mistral&system={sys_msg}"
                        if pollinations_key:
                            p_url += f"&key={pollinations_key}"
                        
                        p_res = requests.get(p_url, timeout=10)
                        st.markdown(p_res.text)
                    except Exception:
                        st.error("VEDA is resting. Please try again.")
    except Exception as e:
        st.error(f"Medha encountered a localized error: {e}")

# [TAB 2: SRIJAN ARCHITECT]
elif selected == "Srijan (Images)":
    st.markdown("<h1 style='text-align: center; color: #fff; text-shadow: 0 0 10px #fff;'>SRIJAN ARCHITECT</h1>", unsafe_allow_html=True)
    
    if not pollinations_key:
        st.warning("⚠️ Please connect in the sidebar to enable images.")
    else:
        user_idea = st.text_input("Vision:", placeholder="Describe your image...")
        if st.button("RENDER"):
            if user_idea:
                with st.spinner("Visualizing..."):
                    img_url = f"https://gen.pollinations.ai/image/{urllib.parse.quote(user_idea)}?width=1024&height=1024&nologo=true&model=flux&key={pollinations_key}"
                    st.image(img_url, caption=f"Created by {CREATOR}", use_column_width=True)
                    st.balloons()

# [TAB 3: VEDA HUB]
elif selected == "Veda (Share Hub)":
    st.title("🌐 Veda Network Hub")
    st.markdown(f"**Developed by {CREATOR}**")
    cols = st.columns(4)
    apps = [("WhatsApp", "whatsapp"), ("Instagram", "instagram-new"), ("YouTube", "youtube-play"), ("Facebook", "facebook-new")]
    for i, (name, icon) in enumerate(apps):
        with cols[i]:
            st.markdown(f'[![{name}](https://img.icons8.com/color/96/{icon}.png)](https://google.com)')
            st.caption(name)
