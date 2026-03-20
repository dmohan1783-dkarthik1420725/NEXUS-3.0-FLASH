import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
import google.generativeai as genai

# --- 1. CONFIGURATION & LOGO SETUP ---
# 'page_icon' sets the ⚡ in the browser tab
st.set_page_config(
    page_title="NEXUS 3.0 ULTRA", 
    page_icon="⚡", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# API Keys (Best practice: use st.secrets["KEY_NAME"] on Streamlit Cloud)
GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY"
POLLUTANTS_API_KEY = "YOUR_POLLUTANTS_API_KEY"

# Initialize Google AI
try:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
except Exception:
    st.warning("Connect your Google API Key in the code or secrets to enable Intelligence.")

# --- 2. SIDEBAR NAVIGATION & SHARE HUB ---
with st.sidebar:
    # Main App Logo and Title
    st.markdown("<h1 style='text-align: center; font-size: 50px;'>⚡</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>NEXUS 3.0</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    selection = option_menu(
        menu_title="Systems",
        options=["Intelligence", "Neural Architect"],
        icons=["cpu-fill", "layers-half"], 
        menu_icon="robot",
        default_index=0,
        styles={
            "container": {"background-color": "#0e1117"},
            "nav-link-selected": {"background-color": "#ff4b4b"},
        }
    )
    
    st.markdown("---")
    st.subheader("🌐 Share Hub")
    
    # Social Media Icons
    st.markdown("""
    <div style="display: flex; gap: 15px; justify-content: center; padding-bottom: 20px;">
        <a href="https://wa.me/" target="_blank"><img src="https://img.icons8.com/color/48/whatsapp.png" width="35"/></a>
        <a href="https://www.instagram.com/" target="_blank"><img src="https://img.icons8.com/color/48/instagram-new.png" width="35"/></a>
        <a href="https://www.facebook.com/" target="_blank"><img src="https://img.icons8.com/color/48/facebook-new.png" width="35"/></a>
        <a href="https://www.youtube.com/" target="_blank"><img src="https://img.icons8.com/color/48/youtube-play.png" width="35"/></a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.write("📲 **Mobile Access**")
    app_url = "https://your-app-link.streamlit.app" 
    st.image(f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={app_url}", width=150)

# --- 3. MAIN INTERFACE LOGIC ---

if selection == "Intelligence":
    # Centered Header
    st.markdown("<br><br><h1 style='text-align: center; color: #ff4b4b; font-size: 60px;'>HI, HOW ARE YOU!</h1>", unsafe_allow_html=True)
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Input command for NEXUS..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except:
                st.write("NEXUS Intelligence is processing...")

elif selection == "Neural Architect":
    st.title("🏗️ Neural Architect")
    st.warning(f"**WARNING:** NEXUS is reading HTML using Pollutants API Key: `{POLLUTANTS_API_KEY[:4]}***`")
    
    html_input = st.text_area("Paste HTML/CSS code to generate visual:", height=250, 
                             placeholder="<div style='background: gold; padding: 20px;'>⚡ NEXUS DESIGN</div>")
    
    if st.button("Generate Architectural Visual"):
        if html_input:
            st.divider()
            components.html(html_input, height=500, scrolling=True)
            st.success("
