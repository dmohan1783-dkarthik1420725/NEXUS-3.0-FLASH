import streamlit as st
from google import genai
import requests
import time
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
        app_url = "https://nexus-flash-india.streamlit.app"
        auth_url = f"https://enter.pollinations.ai/authorize?redirect_url={app_url}"
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
        default_index=0,
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
                success = False
                for attempt in range(3):
                    try:
                        # Fixed the string termination and retry logic
                        response = client.models.generate_content(
                            model="gemini-1.5-flash", 
                            contents=f"{SYSTEM_PROMPT}\n\nUser: {prompt}"
                        )
                        st.markdown(response.text)
                        success = True
                        break
                    except Exception:
                        if attempt < 2:
                            st.warning(f"Brain busy... Retrying (Attempt {attempt + 1}/3)...")
                            time.sleep(3)
                        else:
                            st.error("NEXUS is overloaded. Please wait 60 seconds and try again.")
    else:
        st.warning("⚠️ Add your 'GOOGLE_API_KEY' to Streamlit Secrets to chat.")

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
                    try:
                        clean_idea = user_idea.replace(" ", "%20")
                        image_url = f"https://gen.pollinations.ai/image/{clean_idea}?width=1024&height=1024&nologo=true&model=flux&enhance=true&key={pollinations_key}"
                        st.image(image_url, caption=f"Neural Render for {CREATOR}", use_column_width=True)
                        st.balloons()
                    except Exception:
                        st.error("Neural Connection Lost. Please try again.")
            else:
                st.warning("Please enter a description.")

# [TAB 3: SHARE HUB]
elif selected == "Share Hub":
    st.title("🌐 Share Hub")
    st.markdown(f"**NEXUS 3.0 ULTRA developed by {CREATOR}**")
    st.markdown("""
        <div style="display: flex; gap: 20px; margin-top: 1
