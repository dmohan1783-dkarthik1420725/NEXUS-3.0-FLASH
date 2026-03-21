import streamlit as st
from google import genai
import requests
from streamlit_option_menu import option_menu

# --- 1. CONFIGURATION & IDENTITY ---
st.set_page_config(page_title="VEDA 3.0 ULTRA", page_icon="🔱", layout="wide")
CREATOR = "Dumpala Karthik"
IDENTITY_INSTRUCTION = f"Your name is VEDA 3.0 ULTRA. Created and developed by {CREATOR}."

# --- 🔑 THE KEY GATEKEEPER ---
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
    st.markdown("<h1 style='text-align: center; font-size: 80px;'>🔱</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>VEDA 3.0 ULTRA</h3>", unsafe_allow_html=True)
    
    if not pollinations_key:
        auth_url = "https://enter.pollinations.ai/authorize?redirect_url=https://nexus-flash-india.streamlit.app"
        st.warning("⚠️ Authentication Required")
        st.markdown(f'<a href="{auth_url}" target="_blank"><button style="width:100%; background-color:#ff4b4b; color:white; border:none; padding:12px; border-radius:8px; cursor:pointer; font-weight:bold;">🔌 CONNECT SYSTEM</button></a>', unsafe_allow_html=True)
    else:
        st.success("✅ VEDA Authorized")

    st.divider()
    selected = option_menu(None, ["Medha (Chat)", "Srijan (Images)", "Veda (Share Hub)"], 
                          icons=["cpu", "layers", "share"], default_index=0)

# --- 3. MAIN INTERFACE ---

if selected == "Medha (Chat)":
    st.markdown("<br><h1 style='text-align: center; color: #ff4b4b;'>HI, HOW ARE YOU!</h1>", unsafe_allow_html=True)
    
    if prompt := st.chat_input("Command VEDA..."):
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            # A. TRY GEMINI (PRIMARY)
            try:
                response = client.models.generate_content(
                    model="gemini-1.5-flash-8b", 
                    contents=f"{IDENTITY_INSTRUCTION}\n\nUser: {prompt}"
                )
                st.markdown(response.text)
            except:
                # B. FAILOVER TO POLLINATIONS (With 402 Bypass)
                if pollinations_key:
                    st.caption("🚀 Switching to VEDA Backup...")
                    try:
                        clean_prompt = prompt.replace(" ", "%20")
                        sys_msg = f"You are VEDA 3.0 ULTRA by {CREATOR}.".replace(" ", "%20")
                        
                        # Try the primary backup (OpenAI)
                        p_url = f"https://gen.pollinations.ai/text/{clean_prompt}?model=openai&system={sys_msg}&key={pollinations_key}"
                        p_res = requests.get(p_url, timeout=10)
                        
                        if p_res.status_code == 200:
                            st.markdown(p_res.text)
                        elif p_res.status_code == 402:
                            # 💡 SMART BYPASS: If 402 (Payment Required), switch to Mistral (Free)
                            st.caption("🔄 Quota full. Re-routing via Free Lane...")
                            m_url = f"https://gen.pollinations.ai/text/{clean_prompt}?model=mistral&system={sys_msg}&key={pollinations_key}"
                            m_res = requests.get(m_url, timeout=10)
                            st.markdown(m_res.text)
                        else:
                            st.error(f"Backup Busy ({p_res.status_code}).")
                    except:
                        st.error("System overload. Please try again.")
                else:
                    st.error("🔒 Please connect in the sidebar to use the Backup Brain.")

elif selected == "Srijan (Images)":
    st.title("🏗️ Srijan Image Architect")
    if not pollinations_key:
        st.warning("⚠️ Please connect in the sidebar first.")
    else:
        user_idea = st.text_input("Vision:")
        if st.button("RENDER"):
            if user_idea:
                with st.spinner("Srijan is creating..."):
                    # For images, we use a basic model if Flux gives a 402
                    img_url = f"https://gen.pollinations.ai/image/{user_idea.replace(' ', '%20')}?width=1024&height=1024&nologo=true&key={pollinations_key}"
                    st.image(img_url, caption=f"Created by {CREATOR}", use_column_width=True)
                    st.balloons()
