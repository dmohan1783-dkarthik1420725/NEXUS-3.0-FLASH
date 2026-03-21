import streamlit as st
from google import genai
from streamlit_option_menu import option_menu

# --- 1. CORE CONFIGURATION ---
st.set_page_config(page_title="NEXUS Flash India", page_icon="⚡", layout="wide")

CREATOR = "Dumpala Karthik"
SYSTEM_PROMPT = f"Your name is NEXUS 3.1. You were developed and created by {CREATOR}."

# Check for Pollinations API Key in the URL
query_params = st.query_params
pollinations_key = query_params.get("api_key", None)

# --- 2. THE SIDEBAR (Facilities & Connect) ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 80px; margin-bottom: 0;'>⚡</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; margin-top: 0;'>NEXUS FLASH INDIA</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #888;'>Architect: {CREATOR}</p>", unsafe_allow_html=True)
    st.divider()

    # THE FACILITY: CONNECT BUTTON (Fixed for GitHub Refusal)
    if not pollinations_key:
        st.warning("Neural Architect Offline")
        # Opens in a NEW TAB to prevent 'Refused to Connect' errors
        auth_url = "https://enter.pollinations.ai/authorize?redirect_url=https://nexus-flash-india.streamlit.app"
        st.markdown(f"""
            <a href="{auth_url}" target="_blank">
                <button style="
                    width:100%; 
                    background-color:#ff4b4b; 
                    color:white; 
                    border:none; 
                    padding:12px; 
                    border-radius:8px; 
                    font-weight:bold;
                    cursor:pointer;
                    box-shadow: 0px 4px 10px rgba(255, 75, 75, 0.3);">
                    🔌 CONNECT POLLINATIONS
                </button>
            </a>
            """, unsafe_allow_html=True)
        st.caption("Login to GitHub in the new tab to unlock images.")
    else:
        st.success("Neural Architect Linked 🌸")
        if st.button("🔌 DISCONNECT"):
            st.query_params.clear()
            st.rerun()

    st.divider()
    selected = option_menu(
        menu_title="Main Systems",
        options=["Intelligence", "Neural Architect", "Share Hub"],
        icons=["cpu", "layers", "share"], 
        default_index=0,
        styles={"nav-link-selected": {"background-color": "#ff4b4b"}}
    )

# --- 3. MAIN INTERFACE ---

# [TAB 1: INTELLIGENCE]
if selected == "Intelligence":
    st.markdown("<br><h1 style='text-align: center; color: #ff4b4b; font-size: 60px;'>HI, HOW ARE YOU!</h1>", unsafe_allow_html=True)
    
    if prompt := st.chat_input("Command NEXUS..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            try:
                client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=f"{SYSTEM_PROMPT}\n\nUser: {prompt}"
                )
                st.markdown(response.text)
            except Exception:
                st.error("Intelligence Error: Please check your Google API Key.")

# [TAB 2: NEURAL ARCHITECT]
elif selected == "Neural Architect":
    st.title("🏗️ Neural Architect")
    
    if not pollinations_key:
        st.info("⚡ Please click the 'CONNECT' button in the sidebar to enable the Image Facility.")
    else:
        design_prompt = st.text_input("Describe the visual you want to build:")
        
        if st.button("EXECUTE RENDER"):
            if design_prompt:
                with st.spinner("Decoding Neural Structure..."):
                    try:
                        # 1. Generate the 150-word "Hacker Code" block
                        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
                        code_query = f"Write 150 words of complex HTML/CSS code for: {design_prompt
