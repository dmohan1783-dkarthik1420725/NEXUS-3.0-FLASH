import streamlit as st
from google import genai
from streamlit_option_menu import option_menu

# --- 1. PAGE CONFIG & BRAIN ---
st.set_page_config(page_title="NEXUS Flash India", page_icon="⚡", layout="wide")

# Setup the Gemini Client using your Secret Key
try:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception as e:
    st.error("NEXUS Brain Offline. Check Streamlit Secrets.")

# --- 2. SIDEBAR (The Facilities) ---
with st.sidebar:
    # Big ⚡ Logo
    st.markdown("<h1 style='text-align: center; font-size: 80px; margin-bottom: 0;'>⚡</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; margin-top: 0;'>NEXUS FLASH INDIA</h3>", unsafe_allow_html=True)
    st.divider()

    # THE OPTIONS MENU (Facilities)
    selected = option_menu(
        menu_title="Main Systems",
        options=["Intelligence", "Neural Architect", "Share Hub"],
        icons=["cpu", "layers", "share"], 
        menu_icon="cast", 
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "#1e1e1e"},
            "icon": {"color": "#ff4b4b", "font-size": "20px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#333"},
            "nav-link-selected": {"background-color": "#ff4b4b"},
        }
    )

    st.divider()
    
    # THE QR CODE (Facility 1)
    st.write("📲 **Scan to Launch**")
    # This generates a real QR code for your specific URL
    qr_url = "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=https://nexus-flash-india.streamlit.app"
    st.image(qr_url, width=150)

# --- 3. MAIN INTERFACE ---

if selected == "Intelligence":
    st.markdown("<br><h1 style='text-align: center; color: #ff4b4b; font-size: 50px;'>HI, HOW ARE YOU!</h1>", unsafe_allow_html=True)
    
    # Simple Chat Interface
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Command NEXUS..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

elif selected == "Neural Architect":
    st.title("🏗️ Neural Architect")
    st.write("Input HTML/CSS to render designs instantly.")
    code_input = st.text_area("Enter Code:", height=200, placeholder="<div style='background:red; padding:20px;'>HELLO</div>")
    if st.button("GENERATE VISUAL"):
        st.components.v1.html(code_input, height=400, scrolling=True)

elif selected == "Share Hub":
    st.title("🌐 Share Hub")
    st.write("Spread the NEXUS network to your friends:")
    
    # Social Icons (Facility 2)
    st.markdown("""
    <div style="display: flex; gap: 20px; align-items: center;">
        <a href="https://wa.me/?text=Check%20out%20NEXUS%20Flash%20India!%20https://nexus-flash-india.streamlit.app" target="_blank">
            <img src="https://img.icons8.com/color/48/whatsapp.png" width="50"/>
        </a>
        <a href="https://www.instagram.com" target="_blank">
            <img src="https://img.icons8.com/color/48/instagram-new.png" width="50"/>
        </a>
        <a href="https://www.facebook.com" target="_blank">
            <img src="https://img.icons8.com/color/48/facebook-new.png" width="50"/>
        </a>
    </div>
    """, unsafe_allow_html=True)
