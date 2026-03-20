import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
import google.generativeai as genai

# --- 1. CONFIGURATION & API SETUP ---
st.set_page_config(page_title="NEXUS 3.0 ULTRA", layout="wide", initial_sidebar_state="expanded")

# Replace these with your actual keys or use Streamlit Secrets
GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY"
POLLUTANTS_API_KEY = "YOUR_POLLUTANTS_API_KEY"

# Initialize Google AI (Gemini)
try:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error("AI Configuration Error. Please check your Google API Key.")

# --- 2. SIDEBAR NAVIGATION & SHARE HUB ---
with st.sidebar:
    st.title("🚀 NEXUS 3.0 ULTRA")
    st.markdown("---")
    
    # Navigation Menu
    selection = option_menu(
        menu_title="Systems",
        options=["Intelligence", "Neural Architect"],
        icons=["cpu-fill", "layers-half"], 
        menu_icon="robot",
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "#0e1117"},
            "nav-link-selected": {"background-color": "#ff4b4b"},
        }
    )
    
    st.markdown("---")
    st.subheader("🌐 Share Hub")
    
    # Social Media Sharing Links
    st.markdown("""
    <div style="display: flex; gap: 15px; justify-content: center; padding-bottom: 20px;">
        <a href="https://wa.me/?text=Check%20out%20NEXUS%203.0%20ULTRA!" target="_blank"><img src="https://img.icons8.com/color/48/whatsapp.png" width="35"/></a>
        <a href="https://www.instagram.com/" target="_blank"><img src="https://img.icons8.com/color/48/instagram-new.png" width="35"/></a>
        <a href="https://www.facebook.com/sharer/sharer.php" target="_blank"><img src="https://img.icons8.com/color/48/facebook-new.png" width="35"/></a>
        <a href="https://www.youtube.com/" target="_blank"><img src="https://img.icons8.com/color/48/youtube-play.png" width="35"/></a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.write("📲 **Mobile Access**")
    # Replace the URL below with your actual deployed app link
    app_url = "https://your-app-name.streamlit.app" 
    st.image(f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={app_url}", 
             caption="Scan to visit on Mobile", width=150)

# --- 3. MAIN INTERFACE LOGIC ---

if selection == "Intelligence":
    # Centered Header
    st.markdown("<br><br><h1 style='text-align: center; color: #ff4b4b; font-size: 60px;'>HI, HOW ARE YOU!</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 20px;'>NEXUS 3.0 ULTRA Intelligence System Online.</p>", unsafe_allow_html=True)
    
    # Chat History Setup
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display Chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input
    if prompt := st.chat_input("Input command for NEXUS..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Processing through Google API..."):
                try:
                    response = model.generate_content(prompt)
                    answer = response.text
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                except Exception as e:
                    st.error(f"Intelligence Error: {e}")

elif selection == "Neural Architect":
    st.title("🏗️ Neural Architect")
    st.info("NEXUS Protocol: Analyzing and rendering visual architecture via HTML input.")
    st.warning(f"**WARNING:** Using Pollutants API Key: `{POLLUTANTS_API_KEY[:5]}***` to verify generation.")
    
    # HTML Input for Image Generation
    st.subheader("Visual Code Engine")
    html_input = st.text_area(
        "Paste your HTML/CSS code here to generate the visual image:", 
        height=300, 
        placeholder="""<div style="background: linear-gradient(45deg, #ff4b4b, #8a2be2); height: 250px; width: 100%; border-radius: 20px; display: flex; align-items: center; justify-content: center; color: white; font-family: sans-serif; font-weight: bold; font-size: 30px;">
    NEXUS GENERATED VISUAL
</div>"""
    )
    
    if st.button("Generate Architectural Visual"):
        if html_input:
            st.divider()
            st.markdown("### 🖼️ Rendered Output")
            # This allows the "reading of HTML" to create the visual
            st.markdown('<div style="border: 2px solid #333; padding: 10px; border-radius: 15px; background-color: #000;">', unsafe_allow_html=True)
            components.html(html_input, height=500, scrolling=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.success("Visual architecture successfully rendered.")
        else:
            st.error("NEXUS Error: No HTML code provided.")
