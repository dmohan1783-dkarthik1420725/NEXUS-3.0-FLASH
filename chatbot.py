import streamlit as st
from google import genai
import requests
from streamlit_option_menu import option_menu
import urllib.parse  # Better for handling vision text

# --- 1. CONFIGURATION & IDENTITY ---
st.set_page_config(page_title="VEDA 3.0 ULTRA", page_icon="🔱", layout="wide")
CREATOR = "Dumpala Karthik"

# --- 🔑 THE KEY GATEKEEPER ---
pollinations_key = st.query_params.get("api_key", st.secrets.get("POLLINATIONS_KEY", ""))

# --- 2. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 80px;'>🔱</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>VEDA 3.0 ULTRA</h3>", unsafe_allow_html=True)
    
    if not pollinations_key:
        auth_url = "https://enter.pollinations.ai/authorize?redirect_url=https://nexus-flash-india.streamlit.app"
        st.error("🔒 Auth Required")
        st.markdown(f'<a href="{auth_url}" target="_blank"><button style="width:100%; background-color:#ff4b4b; color:white; border:none; padding:12px; border-radius:8px; cursor:pointer; font-weight:bold;">🔌 CONNECT SYSTEM</button></a>', unsafe_allow_html=True)
    else:
        st.success("✅ VEDA Authorized")

    st.divider()
    selected = option_menu(None, ["Medha (Chat)", "Srijan (Images)", "Veda (Share Hub)"], 
                          icons=["cpu", "layers", "share"], default_index=1) # Default to Architect for testing

# --- 3. MAIN INTERFACE ---

if selected == "Srijan (Images)":
    st.title("🏗️ Srijan Image Architect")
    
    if not pollinations_key:
        st.warning("⚠️ Please connect in the sidebar to enable the Architect.")
    else:
        user_idea = st.text_input("Describe your vision (e.g., A golden temple in the clouds):")
        
        if st.button("RENDER VISION"):
            if user_idea:
                with st.spinner("Srijan is visualizing..."):
                    try:
                        # Clean and encode the prompt for a safe URL
                        encoded_vision = urllib.parse.quote(user_idea)
                        
                        # Use a stable, high-quality 2026 endpoint
                        # We use 'turbo' for speed and 'flux' for quality
                        img_url = f"https://gen.pollinations.ai/image/{encoded_vision}?width=1024&height=1024&nologo=true&model=flux&seed=123&key={pollinations_key}"
                        
                        # Display the image
                        st.image(img_url, caption=f"Visualized by {CREATOR}", use_column_width=True)
                        st.balloons()
                        
                        # ADDING A DOWNLOAD BUTTON
                        st.markdown(f'<a href="{img_url}" download="Veda_Render.png"><button style="background-color:#4CAF50; color:white; padding:10px; border:none; border-radius:5px;">💾 Download High-Res</button></a>', unsafe_allow_html=True)
                        
                    except Exception as e:
                        st.error("The Architect's vision was interrupted. Please try a different description.")
            else:
                st.info("The Architect is waiting for your vision...")

# [Rest of the code for Medha and Veda Hub remains the same]
