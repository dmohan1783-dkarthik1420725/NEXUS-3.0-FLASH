import streamlit as st
from google import genai
import requests
from streamlit_option_menu import option_menu

# --- 1. CORE CONFIGURATION ---
st.set_page_config(page_title="NEXUS 3.0 ULTRA", page_icon="⚡", layout="wide")
CREATOR = "Dumpala Karthik"
SYSTEM_PROMPT = f"Your name is NEXUS 3.0 ULTRA. You were created by {CREATOR}."

# --- SMART KEY LOGIC ---
pollinations_key = st.query_params.get("api_key", st.secrets.get("POLLINATIONS_KEY", ""))

# Connect to Gemini Intelligence
try:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    brain_status = "Online ⚡"
except Exception:
    client = None
    brain_status = "Offline (Check Secrets)"

# --- 2. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 80px; margin-bottom: 0;'>⚡</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>NEXUS 3.0 ULTRA</h3>", unsafe_allow_html=True)
    st.success(f"NEXUS Brain: {brain_status}")
    
    if not pollinations_key:
        auth_url = "https://enter.pollinations.ai/authorize?redirect_url=https://nexus-flash-india.streamlit.app"
        st.markdown(f"""
            <a href="{auth_url}" target="_blank">
                <button style="width:100%; background-color:#ff4b4b; color:white; border:none; padding:12px; border-radius:8px; cursor:pointer; font-weight:bold;">
                    🔌 CONNECT POLLINATIONS
                </button>
            </a>""", unsafe_allow_html=True)
    else:
        st.info("Architect Linked 🌸")

    st.divider()
    selected = option_menu(
        menu_title=None, 
        options=["Intelligence", "Neural Architect", "Share Hub"], 
        icons=["cpu", "layers", "share"], 
        default_index=0, # Set back to Intelligence as default
        styles={"nav-link-selected": {"background-color": "#ff4b4b"}}
    )

# --- 3. MAIN INTERFACE ---

# [TAB 1: INTELLIGENCE]
if selected == "Intelligence":
    st.markdown("<br><h1 style='text-align: center; color: #ff4b4b;'>HI, HOW ARE YOU!</h1>", unsafe_allow_html=True)
    
    if client:
        if prompt := st.chat_input("Command NEXUS..."):
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                try:
                    response = client.models.generate_content(
                        model="gemini-2.0-flash", 
                        contents=f"{SYSTEM_PROMPT}\n\nUser: {prompt}"
                    )
                    st.markdown(response.text)
                except Exception:
                    st.error("Intelligence is currently busy. Try again in a moment.")
    else:
        st.warning("⚠️ Intelligence Module is locked. Please add your 'GOOGLE_API_KEY' to Streamlit Secrets to chat.")

# [TAB 2: NEURAL ARCHITECT]
elif selected == "Neural Architect":
    st.title("🏗️ Neural Architect")
    if not pollinations_key:
        st.error("Please click 'CONNECT POLLINATIONS' in the sidebar first!")
    else:
        user_idea = st.text_input("Describe your vision:", placeholder="e.g. A futuristic city")
        if st.button("EXECUTE RENDER"):
            if user_idea:
                with st.spinner("Visualizing..."):
                    clean_idea = user_idea.replace(" ", "%20")
                    image_url = f"https://gen.pollinations.ai/image/{clean_idea}?width=1024&height=1024&nologo=true&model=flux&enhance=true&key={pollinations_key}"
                    st.image(image_url, caption=f"Neural Render for {CREATOR}", use_column_width=True)
                    st.balloons()
            else:
                st.warning("Please enter a description.")

# [TAB 3: SHARE HUB]
elif selected == "Share Hub":
    st.title("🌐 Share Hub")
    st.markdown(f"**NEXUS 3.0 ULTRA developed by {CREATOR}**")
    st.markdown("""
        <div style="display: flex; gap: 20px; margin-top: 10px;">
            <a href="https://wa.me/" target="_blank" style="text-decoration:none; color:#25D366; font-weight:bold;">WhatsApp</a>
            <span style="color:#888;">|</span>
            <a href="https://instagram.com/" target="_blank" style="text-decoration:none; color:#E1306C; font-weight:bold;">Instagram</a>
        </div>
    """, unsafe_allow_html=True)
