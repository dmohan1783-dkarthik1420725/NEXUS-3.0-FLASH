import streamlit as st
from google import genai
from streamlit_option_menu import option_menu

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="NEXUS Flash India", page_icon="⚡", layout="wide")
CREATOR = "Dumpala Karthik"

# --- 2. THE CONNECT LOGIC (BYOP System) ---
# This checks the URL for a Pollinations API Key
query_params = st.query_params
pollinations_key = query_params.get("api_key", None)

with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 80px; margin-bottom: 0;'>⚡</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>NEXUS FLASH INDIA</h3>", unsafe_allow_html=True)
    
    # The "Connect" Button Facility
    if not pollinations_key:
        st.warning("Neural Architect Offline")
        # Direct link to Pollinations Auth with your App URL
        auth_url = "https://enter.pollinations.ai/authorize?redirect_url=https://nexus-flash-india.streamlit.app"
        st.markdown(f'<a href="{auth_url}" target="_self"><button style="width:100%; background-color:#ff4b4b; color:white; border:none; padding:10px; border-radius:5px; cursor:pointer;">🔌 CONNECT POLLINATIONS</button></a>', unsafe_allow_html=True)
    else:
        st.success("Neural Architect Linked 🌸")
        st.info(f"Key Active: {pollinations_key[:8]}...")

    st.divider()
    selected = option_menu("Main Systems", ["Intelligence", "Neural Architect", "Share Hub"], icons=["cpu", "layers", "share"], default_index=0)

# --- 3. MAIN INTERFACE ---

if selected == "Intelligence":
    st.markdown("<br><h1 style='text-align: center; color: #ff4b4b; font-size: 60px;'>HI, HOW ARE YOU!</h1>", unsafe_allow_html=True)
    if prompt := st.chat_input("Command NEXUS..."):
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            try:
                client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
                response = client.models.generate_content(model="gemini-1.5-flash", contents=f"Creator: {CREATOR}\nUser: {prompt}")
                st.markdown(response.text)
            except: st.error("Check Google API Key.")

elif selected == "Neural Architect":
    st.title("🏗️ Neural Architect")
    if not pollinations_key:
        st.error("Please use the 'CONNECT' button in the sidebar to enable Image Generation.")
    else:
        design_prompt = st.text_input("Describe the visual:")
        if st.button("EXECUTE RENDER"):
            # Using the Key found in the URL to bypass rate limits
            image_url = f"https://image.pollinations.ai/prompt/{design_prompt.replace(' ', '%20')}?key={pollinations_key}&nologo=true"
            
            # THE GREEN BOX
            st.markdown(f"""
            <div style="border: 2px solid #28a745; padding: 20px; border-radius: 10px; background-color: rgba(40, 167, 69, 0.05); margin-bottom: 25px;">
                <p style="color: #28a745; font-family: monospace; font-weight: bold;">NEXUS_BYOP_LINK_ACTIVE:</p>
                <code style="color: #ffffff;">&lt;img src="{image_url}"&gt;</code>
            </div>
            """, unsafe_allow_html=True)
            st.image(image_url, caption=f"Render by {CREATOR}")
