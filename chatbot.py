import streamlit as st
import google.generativeai as genai
from streamlit_option_menu import option_menu

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="NEXUS Flash India", page_icon="⚡", layout="wide")

# Securely get your API Key from Streamlit Secrets
# (You will set this up in Step 3 below)
GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY", "")

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.warning("Please configure your GOOGLE_API_KEY in Streamlit Secrets.")

# --- 2. SIDEBAR: NEXUS HUB ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 60px;'>⚡</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>NEXUS Flash India</h2>", unsafe_allow_html=True)
    st.divider()

    selection = option_menu(
        menu_title="Main Systems",
        options=["Intelligence", "Neural Architect"],
        icons=["cpu", "layers"],
        default_index=0,
        styles={"nav-link-selected": {"background-color": "#ff4b4b"}}
    )

    st.divider()
    st.subheader("🌐 Share Hub")
    # Social Share Links
    st.markdown("""
    <div style="display: flex; gap: 15px; justify-content: center;">
        <a href="https://wa.me/" target="_blank"><img src="https://img.icons8.com/color/48/whatsapp.png" width="35"/></a>
        <a href="https://instagram.com/" target="_blank"><img src="https://img.icons8.com/color/48/instagram-new.png" width="35"/></a>
        <a href="https://facebook.com/" target="_blank"><img src="https://img.icons8.com/color/48/facebook-new.png" width="35"/></a>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.write("📲 **Scan for Mobile**")
    # This points to your actual app URL
    st.image(f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=https://nexus-flash-india.streamlit.app", width=130)

# --- 3. MAIN DASHBOARD ---
if selection == "Intelligence":
    st.markdown("<br><h1 style='text-align: center; color: #ff4b4b; font-size: 55px;'>HI, HOW ARE YOU!</h1>", unsafe_allow_html=True)
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Command NEXUS..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error("NEXUS Brain Offline. Check API Key.")

elif selection == "Neural Architect":
    st.title("🏗️ Neural Architect")
    st.info("NEXUS is reading HTML architecture...")
    html_code = st.text_area("Input design code:", height=200, placeholder="<div style='color:red;'>NEXUS DESIGN</div>")
    if st.button("Generate Visual"):
        st.components.v1.html(html_code, height=400)
