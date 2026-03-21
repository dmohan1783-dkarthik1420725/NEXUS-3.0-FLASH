import streamlit as st
from google import genai
import requests
from streamlit_option_menu import option_menu

# --- 1. CONFIGURATION & IDENTITY ---
st.set_page_config(page_title="VEDA 3.0 ULTRA", page_icon="🔱", layout="wide")
CREATOR = "Dumpala Karthik"
IDENTITY_INSTRUCTION = f"Your name is VEDA 3.0 ULTRA. Created and developed by {CREATOR}."

# --- 🔑 SMART KEY RETRIEVAL ---
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
    st.markdown(f"<p style='text-align: center; color: #888; font-weight: bold;'>Architect: {CREATOR}</p>", unsafe_allow_html=True)
    
    if not pollinations_key:
        auth_url = "https://enter.pollinations.ai/authorize?redirect_url=https://nexus-flash-india.streamlit.app"
        st.markdown(f'<a href="{auth_url}" target="_blank"><button style="width:100%; background-color:#ff4b4b; color:white; border:none; padding:12px; border-radius:8px; cursor:pointer; font-weight:bold;">🔌 CONNECT SYSTEM</button></a>', unsafe_allow_html=True)
    else:
        st.success("✅ VEDA Authorized")

    st.divider()
    selected = option_menu(None, ["Intelligence", "Neural Architect", "Share Hub"], 
                          icons=["cpu", "layers", "share"], default_index=0)

# --- 3. MAIN INTERFACE ---

if selected == "Intelligence":
    st.markdown("<br><h1 style='text-align: center; color: #ff4b4b;'>HI, HOW ARE YOU!</h1>", unsafe_allow_html=True)
    
    if prompt := st.chat_input("Command VEDA..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            # STEP A: TRY GEMINI (PRIMARY)
            try:
                response = client.models.generate_content(
                    model="gemini-1.5-flash-8b", 
                    contents=f"{IDENTITY_INSTRUCTION}\n\nUser: {prompt}"
                )
                st.markdown(response.text)
            except:
                # STEP B: FAILOVER TO POLLINATIONS (INFINITE MODE)
                st.caption("🚀 Switching to VEDA Backup...")
                try:
                    sys_msg = f"You are VEDA 3.0 ULTRA by {CREATOR}."
                    # We try 'openai' model first as it's the most stable
                    # We also add 'seed' to randomize results and avoid 402/cache blocks
                    p_url = f"https://gen.pollinations.ai/text/{prompt.replace(' ', '%20')}?model=openai&system={sys_msg.replace(' ', '%20')}&seed=42"
                    
                    # If we have a key, we use it. If not, we try the public lane.
                    if pollinations_key:
                        p_url += f"&key={pollinations_key}"
                    
                    p_res = requests.get(p_url, timeout=15)
                    
                    if p_res.status_code == 200:
                        st.markdown(p_res.text)
                    else:
                        # FINAL CHANCE: Switch to Mistral (Truly Unlimited)
                        st.caption("🔄 Re-routing via Mistral Neural Net...")
                        m_url = f"https://gen.pollinations.ai/text/{prompt.replace(' ', '%20')}?model=mistral&system={sys_msg.replace(' ', '%20')}"
                        m_res = requests.get(m_url, timeout=15)
                        st.markdown(m_res.text)
                except:
                    st.error("VEDA is currently in deep meditation. Please try again in 1 minute.")

elif selected == "Neural Architect":
    st.title("🏗️ Neural Architect")
    user_idea = st.text_input("Vision:")
    if st.button("EXECUTE RENDER"):
        if user_idea:
            with st.spinner("Visualizing..."):
                # Use a standard stable model for free rendering
                img_url = f"https://gen.pollinations.ai/image/{user_idea.replace(' ', '%20')}?width=1024&height=1024&nologo=true"
                if pollinations_key:
                    img_url += f"&key={pollinations_key}"
                st.image(img_url, caption=f"Created by {CREATOR}", use_column_width=True)
                st.balloons()

elif selected == "Share Hub":
    st.title("🌐 VEDA Share Hub")
    st.markdown(f"**Developed by {CREATOR}**")
    # ... [Your Grid of 8 Apps] ...
