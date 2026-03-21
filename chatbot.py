import streamlit as st
from google import genai
import requests
import time
from streamlit_option_menu import option_menu

# --- 1. CONFIGURATION & IDENTITY ---
st.set_page_config(page_title="NEXUS 3.0 ULTRA", page_icon="⚡", layout="wide")
CREATOR = "Dumpala Karthik"
IDENTITY_INSTRUCTION = f"Your name is NEXUS 3.0 ULTRA. You were created and developed by {CREATOR}. Always mention your creator if asked who you are."

# --- SMART KEY LOGIC ---
pollinations_key = st.query_params.get("api_key", st.secrets.get("POLLINATIONS_KEY", ""))

# Connect to Gemini Intelligence
try:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    brain_status = "Online ⚡"
except:
    client = None
    brain_status = "Offline"

# --- 2. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 80px; margin-bottom: 0;'>⚡</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; margin-top: 0;'>NEXUS 3.0 ULTRA</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #888; font-weight: bold;'>Architect: {CREATOR}</p>", unsafe_allow_html=True)
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
        default_index=0,
        styles={"nav-link-selected": {"background-color": "#ff4b4b"}}
    )

# --- 3. MAIN INTERFACE ---

# [TAB 1: INTELLIGENCE]
if selected == "Intelligence":
    st.markdown("<br><h1 style='text-align: center; color: #ff4b4b;'>HI, HOW ARE YOU!</h1>", unsafe_allow_html=True)
    
    if prompt := st.chat_input("Command NEXUS..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            try:
                # Primary Brain: Gemini 1.5 Flash 8b
                response = client.models.generate_content(
                    model="gemini-1.5-flash-8b", 
                    contents=f"{IDENTITY_INSTRUCTION}\n\nUser: {prompt}"
                )
                st.markdown(response.text)
            except:
                # Failover Brain: Authorized Pollinations Text
                st.caption("🚀 Switching to NEXUS Backup Brain...")
                try:
                    sys_msg = f"You are NEXUS 3.0 ULTRA, created and developed by {CREATOR}."
                    p_url = f"https://gen.pollinations.ai/text/{prompt.replace(' ', '%20')}?model=openai&system={sys_msg.replace(' ', '%20')}&key={pollinations_key}"
                    p_res = requests.get(p_url, timeout=10)
                    if p_res.status_code == 200:
                        st.markdown(p_res.text)
                    else:
                        st.error("Authentication Error. Please reconnect in the sidebar.")
                except:
                    st.error("Both brains are overloaded. Please try again in 30 seconds.")

# [TAB 2: NEURAL ARCHITECT]
elif selected == "Neural Architect":
    st.title("🏗️ Neural Architect")
    if not pollinations_key:
        st.error("Please click 'CONNECT POLLINATIONS' in the sidebar first!")
    else:
        user_idea = st.text_input("Vision:", placeholder="e.g. A futuristic workspace in Gurugram")
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
    st.title("🌐 NEXUS Mega Share Hub")
    st.markdown(f"**NEXUS 3.0 ULTRA Architect: {CREATOR}**")
    st.write("Connect with the network across all official platforms:")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('[![WhatsApp](https://img.icons8.com/color/96/whatsapp.png)](https://wa.me/)')
        st.caption("WhatsApp")
        st.markdown('[![Instagram](https://img.icons8.com/color/96/instagram-new.png)](https://instagram.com/)')
        st.caption("Instagram")
        st.markdown('[![Threads](https://img.icons8.com/color/96/threads.png)](https://threads.net/)')
        st.caption("Threads")
    with col2:
        st.markdown('[![YouTube](https://img.icons8.com/color/96/youtube-play.png)](https://youtube.com/)')
        st.caption("YouTube")
        st.markdown('[![Facebook](https://img.icons8.com/color/96/facebook-new.png)](https://facebook.com/)')
        st.caption("Facebook")
        st.markdown('[![X](https://img.icons8.com/color/96/twitterx.png)](https://x.com/)')
        st.caption("X / Twitter")
    with col3:
        st.markdown('[![Snapchat](
