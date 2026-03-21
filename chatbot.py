import streamlit as st
from google import genai
import requests
import urllib.parse
from streamlit_option_menu import option_menu

# --- 1. CONFIGURATION & IDENTITY ---
st.set_page_config(page_title="VEDA 3.0 ULTRA", page_icon="🔱", layout="wide")
CREATOR = "Dumpala Karthik"

# --- 🔑 KEY RETRIEVAL ---
pollinations_key = st.query_params.get("api_key", st.secrets.get("POLLINATIONS_KEY", ""))

# --- 2. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 80px;'>🔱</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>VEDA 3.0 ULTRA</h3>", unsafe_allow_html=True)
    st.divider()
    selected = option_menu(None, ["Medha (Chat)", "Srijan (Images)", "Veda (Share Hub)"], 
                          icons=["cpu", "layers", "share"], default_index=1)

# --- 3. MAIN INTERFACE ---

if selected == "Srijan (Images)":
    # ⚪ Clean White Title (No Glow)
    st.markdown("""
        <style>
        .clean-title {
            font-size: 45px;
            color: #ffffff;
            text-align: center;
            font-weight: 800;
            margin-top: 10px;
            margin-bottom: 30px;
            font-family: 'Helvetica', sans-serif;
        }
        </style>
        <div class="clean-title">SRIJAN ARCHITECT</div>
    """, unsafe_allow_html=True)

    # 🛠️ Safety Check for the Architect
    if not pollinations_key:
        st.error("🔒 SYSTEM LOCKED: Please connect in the sidebar to enable the Architect.")
        auth_url = "https://enter.pollinations.ai/authorize?redirect_url=https://nexus-flash-india.streamlit.app"
        st.markdown(f'<a href="{auth_url}" target="_blank"><button style="width:100%; background-color:#ff4b4b; color:white; border:none; padding:12px; border-radius:8px; cursor:pointer; font-weight:bold;">🔌 CLICK HERE TO CONNECT</button></a>', unsafe_allow_html=True)
    else:
        # The Architect Interface
        user_idea = st.text_input("Enter your vision:", placeholder="e.g. A futuristic glass palace in India...")
        
        # Center the button
        col1, col2, col3 = st.columns([1,1,1])
        with col2:
            execute = st.button("🚀 EXECUTE RENDER", use_container_width=True)

        if execute:
            if user_idea:
                with st.spinner("🌀 Srijan is visualizing your creation..."):
                    try:
                        # 1. Properly encode the vision text
                        encoded_vision = urllib.parse.quote(user_idea)
                        
                        # 2. Stable 2026 URL for Srijan
                        img_url = f"https://gen.pollinations.ai/image/{encoded_vision}?width=1024&height=1024&nologo=true&model=flux&key={pollinations_key}"
                        
                        # 3. Display the result
                        st.markdown("---")
                        st.image(img_url, caption=f"Architectural Vision by {CREATOR}", use_column_width=True)
                        st.balloons()
                        
                        # 4. Download Option
                        st.success("Render Complete!")
                        st.markdown(f"**[📥 Download High-Resolution Image]({img_url})**")
                        
                    except Exception as e:
                        st.error(f"Srijan encountered an interruption: {e}")
            else:
                st.warning("Please provide a vision for the Architect to build.")

# [Keep your Medha and Veda Hub code below this...]
