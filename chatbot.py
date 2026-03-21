import streamlit as st
from google import genai
import requests
import urllib.parse # CRITICAL: This must be at the top!
from streamlit_option_menu import option_menu

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="VEDA 3.0 ULTRA", page_icon="🔱", layout="wide")
CREATOR = "Dumpala Karthik"

# --- 🔑 THE KEY GATEKEEPER ---
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
    st.markdown("<br><h1 style='text-align: center; color: #fff; text-shadow: 0 0 10px #fff;'>SRIJAN ARCHITECT</h1>", unsafe_allow_html=True)
    
    # 🛠️ STATUS CHECK 🛠️
    if not pollinations_key:
        st.error("🔒 ACCESS DENIED: System Not Linked.")
        auth_url = "https://enter.pollinations.ai/authorize?redirect_url=https://nexus-flash-india.streamlit.app"
        st.markdown(f'<a href="{auth_url}" target="_blank"><button style="width:100%; background-color:#ff4b4b; color:white; border:none; padding:12px; border-radius:8px; cursor:pointer; font-weight:bold;">🔌 CLICK TO CONNECT POLLINATIONS</button></a>', unsafe_allow_html=True)
        st.info("The Architect requires a Pollinations link to visualize images.")
    else:
        # THE INPUT BOX
        user_idea = st.text_input("Describe your vision (e.g., A futuristic Indian city):", key="srijan_input")
        
        col1, col2, col3 = st.columns([1,1,1])
        with col2:
            render_btn = st.button("✨ EXECUTE RENDER", use_container_width=True)

        if render_btn:
            if user_idea:
                with st.spinner("🌀 Srijan is visualizing your vision..."):
                    try:
                        # 1. Encode the text correctly
                        encoded_prompt = urllib.parse.quote(user_idea)
                        
                        # 2. Build the 2026 stable URL
                        # We use model=flux for the highest quality
                        img_url = f"https://gen.pollinations.ai/image/{encoded_prompt}?width=1024&height=1024&nologo=true&model=flux&key={pollinations_key}"
                        
                        # 3. Display with a nice border
                        st.markdown("---")
                        st.image(img_url, caption=f"Architectural Render by {CREATOR}", use_column_width=True)
                        st.balloons()
                        
                        # 4. Download Link
                        st.success("Vision Rendered Successfully!")
                        st.markdown(f"[📥 Click here to Download High-Res]({img_url})")
                        
                    except Exception as e:
                        st.error(f"Render Failed: {e}")
            else:
                st.warning("Please enter a description for the Architect.")

# [Rest of your Medha and Veda Hub code follows below...]
