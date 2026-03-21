import streamlit as st
from google import genai
import requests
from streamlit_option_menu import option_menu

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="NEXUS 3.0 ULTRA", page_icon="⚡", layout="wide")
CREATOR = "Dumpala Karthik"

# This is the "Identity Chip" for the AI
IDENTITY_INSTRUCTION = f"Your name is NEXUS 3.0 ULTRA. You were created and developed by {CREATOR}. Always acknowledge this if asked who you are."

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
    st.markdown(f"<h3 style='text-align: center;'>NEXUS 3.0 ULTRA</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #888;'>Architect: {CREATOR}</p>", unsafe_allow_html=True)
    
    if not pollinations_key:
        auth_url = "https://enter.pollinations.ai/authorize?redirect_url=https://nexus-flash-india.streamlit.app"
        st.markdown(f'<a href="{auth_url}" target="_blank"><button style="width:100%; background-color:#ff4b4b; color:white; border:none; padding:12px; border-radius:8px; cursor:pointer; font-weight:bold;">🔌 CONNECT POLLINATIONS</button></a>', unsafe_allow_html=True)
    else:
        st.success("Architect Linked 🌸")

    st.divider()
    selected = option_menu(None, ["Intelligence", "Neural Architect", "Share Hub"], 
                          icons=["cpu", "layers", "share"], default_index=0)

# --- 3. MAIN INTERFACE ---

if selected == "Intelligence":
    st.markdown("<br><h1 style='text-align: center; color: #ff4b4b;'>HI, HOW ARE YOU!</h1>", unsafe_allow_html=True)
    
    if prompt := st.chat_input("Command NEXUS..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            # TRY GEMINI FIRST
            try:
                response = client.models.generate_content(
                    model="gemini-1.5-flash-8b", 
                    contents=f"{IDENTITY_INSTRUCTION}\n\nUser Question: {prompt}"
                )
                st.markdown(response.text)
            except:
                # BACKUP BRAIN (Authorized Pollinations)
                st.caption("🚀 Switching to NEXUS Backup Brain...")
                try:
                    # Clean the system prompt for the URL
                    system_msg = f"You are NEXUS 3.0 ULTRA, created and developed by {CREATOR}."
                    p_url = f"https://gen.pollinations.ai/text/{prompt.replace(' ', '%20')}?model=openai&system={system_msg.replace(' ', '%20')}&key={pollinations_key}"
                    p_res = requests.get(p_url, timeout=10)
                    
                    if p_res.status_code == 200:
                        st.markdown(p_res.text)
                    else:
                        st.error("Authentication failed. Please re-connect in the sidebar.")
                except:
                    st.error("System Overloaded. Please try again.")

elif selected == "Neural Architect":
    st.title("🏗️ Neural Architect")
    if not pollinations_key:
        st.error("Please click 'CONNECT POLLINATIONS' in the sidebar!")
    else:
        user_idea = st.text_input("Vision:")
        if st.button("EXECUTE RENDER"):
            if user_idea:
                with st.spinner("Visualizing..."):
                    img_url = f"https://gen.pollinations.ai/image/{user_idea.replace(' ', '%20')}?width=1024&height=1024&nologo=true&model=flux&key={pollinations_key}"
                    st.image(img_url, caption=f"Render by {CREATOR}", use_column_width=True)
                    st.balloons()

elif selected == "Share Hub":
    st.title("🌐 Share Hub")
    st.markdown(f"**NEXUS 3.0 ULTRA developed by {CREATOR}**")
    st.markdown("""
        <div style="display: flex; gap: 20px; margin-top: 10px;">
            <a href="https://wa.me/" target="_blank">WhatsApp</a> | <a href="https://instagram.com/" target="_blank">Instagram</a>
        </div>
    """, unsafe_allow_html=True)
