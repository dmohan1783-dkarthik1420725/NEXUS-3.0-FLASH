import streamlit as st
from google import genai
import requests
from streamlit_option_menu import option_menu

# --- 1. CONFIGURATION & IDENTITY ---
st.set_page_config(page_title="VEDA 3.0 ULTRA", page_icon="🔱", layout="wide")
CREATOR = "Dumpala Karthik"
IDENTITY_INSTRUCTION = f"Your name is VEDA 3.0 ULTRA. Created by {CREATOR}."

# --- 🔑 SMART KEY RETRIEVAL ---
# In 2026, Streamlit handles query params via st.query_params
# We check the URL first, then check Streamlit Secrets as a fallback
pollinations_key = st.query_params.get("api_key", st.secrets.get("POLLINATIONS_KEY", ""))

# Connect to Gemini Intelligence
try:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    brain_status = "Online 🔱"
except:
    client = None
    brain_status = "Offline"

# --- 2. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 80px; margin-bottom: 0;'>🔱</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; margin-top: 0;'>VEDA 3.0 ULTRA</h3>", unsafe_allow_html=True)
    
    if not pollinations_key:
        # If no key is found, show the red Connect button
        auth_url = "https://enter.pollinations.ai/authorize?redirect_url=https://nexus-flash-india.streamlit.app"
        st.error("🔒 System Locked")
        st.markdown(f"""
            <a href="{auth_url}" target="_blank">
                <button style="width:100%; background-color:#ff4b4b; color:white; border:none; padding:12px; border-radius:8px; cursor:pointer; font-weight:bold;">
                    🔌 CONNECT POLLINATIONS
                </button>
            </a>""", unsafe_allow_html=True)
        st.caption("Click above to unlock AI features.")
    else:
        st.success("✅ VEDA Authorized")
        st.caption(f"Key Active: {pollinations_key[:6]}***")

    st.divider()
    selected = option_menu(
        menu_title=None, 
        options=["Intelligence", "Neural Architect", "Share Hub"], 
        icons=["cpu", "layers", "share"], 
        default_index=0,
        styles={"nav-link-selected": {"background-color": "#ff4b4b"}}
    )

# --- 3. MAIN INTERFACE ---

if selected == "Intelligence":
    st.markdown("<br><h1 style='text-align: center; color: #ff4b4b;'>HI, HOW ARE YOU!</h1>", unsafe_allow_html=True)
    
    if prompt := st.chat_input("Command VEDA..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            # A. TRY GEMINI (PRIMARY)
            try:
                response = client.models.generate_content(
                    model="gemini-1.5-flash-8b", 
                    contents=f"{IDENTITY_INSTRUCTION}\n\nUser: {prompt}"
                )
                st.markdown(response.text)
            except:
                # B. FAILOVER TO POLLINATIONS (Requires Key)
                if pollinations_key:
                    st.caption("🚀 Switching to VEDA Backup...")
                    try:
                        # 2026 Updated gen.pollinations.ai endpoint
                        sys_msg = f"You are VEDA 3.0 ULTRA by {CREATOR}."
                        # Encode URL parameters properly
                        p_url = f"https://gen.pollinations.ai/text/{prompt.replace(' ', '%20')}?model=openai&system={sys_msg.replace(' ', '%20')}&key={pollinations_key}"
                        p_res = requests.get(p_url, timeout=15)
                        
                        if p_res.status_code == 200:
                            st.markdown(p_res.text)
                        elif p_res.status_code == 401:
                            st.error("Error 401: Key expired. Please click 'CONNECT' again.")
                        else:
                            st.error(f"Backup busy (Status {p_res.status_code}).")
                    except Exception as e:
                        st.error("Connection lost. Check your internet.")
                else:
                    st.warning("Please connect in the sidebar to use the Backup Brain.")

elif selected == "Neural Architect":
    st.title("🏗️ Neural Architect")
    if not pollinations_key:
        st.warning("⚠️ Access Denied. Please connect Pollinations in the sidebar.")
    else:
        user_idea = st.text_input("Vision:", placeholder="e.g. A futuristic landscape")
        if st.button("EXECUTE RENDER"):
            if user_idea:
                with st.spinner("Visualizing..."):
                    # Use the new 2026 flux model for best quality
                    img_url = f"https://gen.pollinations.ai/image/{user_idea.replace(' ', '%20')}?width=1024&height=1024&model=flux&nologo=true&key={pollinations_key}"
                    st.image(img_url, caption=f"Neural Render for {CREATOR}", use_column_width=True)
                    st.balloons()

elif selected == "Share Hub":
    st.title("🌐 VEDA Share Hub")
    st.markdown(f"**VEDA 3.0 ULTRA Architect: {CREATOR}**")
    # ... [Keep your social grid here] ...
    st.info("The Share Hub is ready for your social links!")
