import streamlit as st
from google import genai
from streamlit_option_menu import option_menu

# --- 1. CORE CONFIGURATION ---
st.set_page_config(page_title="NEXUS Flash India", page_icon="⚡", layout="wide")

CREATOR = "Dumpala Karthik"
SYSTEM_PROMPT = f"Your name is NEXUS 3.1. You were developed and created by {CREATOR}."

# --- BYOP FACILITY: URL Key Detection ---
query_params = st.query_params
pollinations_key = query_params.get("api_key", None)

# Connect to Google Gemini (Intelligence)
try:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    st.sidebar.success("NEXUS Brain Online ⚡")
except Exception:
    st.sidebar.error("NEXUS Brain Offline. Check Secrets.")

# --- 2. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 80px; margin-bottom: 0;'>⚡</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; margin-top: 0;'>NEXUS FLASH INDIA</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #888;'>Architect: {CREATOR}</p>", unsafe_allow_html=True)
    st.divider()

    # THE FACILITY: BYOP CONNECT BUTTON (Added to your 100% correct base)
    if not pollinations_key:
        auth_url = "https://enter.pollinations.ai/authorize?redirect_url=https://nexus-flash-india.streamlit.app"
        st.markdown(f"""
            <button onclick="window.open('{auth_url}', '_blank')" style="
                width:100%; background-color:#ff4b4b; color:white; border:none; 
                padding:12px; border-radius:8px; font-weight:bold; cursor:pointer;">
                🔌 CONNECT POLLINATIONS
            </button>
            """, unsafe_allow_html=True)
    else:
        st.success("Neural Architect Linked 🌸")
        if st.button("🔌 DISCONNECT"):
            st.query_params.clear()
            st.rerun()

    st.divider()

    selected = option_menu(
        menu_title="Main Systems",
        options=["Intelligence", "Neural Architect", "Share Hub"],
        icons=["cpu", "layers", "share"], 
        default_index=0,
        styles={"nav-link-selected": {"background-color": "#ff4b4b"}}
    )

    st.divider()
    qr_url = "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=https://nexus-flash-india.streamlit.app"
    st.image(qr_url, width=150, caption="Scan to Launch")

# --- 3. MAIN INTERFACE ---

if selected == "Intelligence":
    st.markdown("<br><h1 style='text-align: center; color: #ff4b4b; font-size: 60px;'>HI, HOW ARE YOU!</h1>", unsafe_allow_html=True)
    
    if prompt := st.chat_input("Command NEXUS..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=f"{SYSTEM_PROMPT}\n\nUser: {prompt}"
                )
                st.markdown(response.text)
            except Exception:
                st.error("Intelligence is currently busy. Please try again in a moment.")

elif selected == "Neural Architect":
    st.title("🏗️ Neural Architect")
    
    if not pollinations_key:
        st.info("⚡ Please click the 'CONNECT' button in the sidebar to enable the Image Facility.")
    else:
        design_prompt = st.text_input("Describe the visual you want to build:")
        
        if st.button("EXECUTE RENDER"):
            if design_prompt:
                # Pollinations is used with your personal BYOP key
                image_url = f"https://image.pollinations.ai/prompt/{design_prompt.replace(' ', '%20')}?width=1024&height=512&nologo=true&seed=42&key={pollinations_key}"
                
                # --- THE FACILITY BOX (Green Outline) ---
                st.markdown(f"""
                <div style="border: 2px solid #28a745; padding: 20px; border-radius: 10px; background-color: rgba(40, 167, 69, 0.05); margin-bottom: 25px;">
                    <p style="color: #28a745; font-family: 'Courier New', monospace; font-weight: bold; font-size: 16px; margin: 0;">
                        NEXUS_SYSTEM_CODE_GENERATED:
                    </p>
                    <code style="color: #ffffff; font-size: 14px;">
                        &lt;img src="{image_url}" alt="NEXUS_Architect_Render"&gt;
                    </code>
                </div>
                """, unsafe_allow_html=True)
                
                # Display the Image
                st.image(image_url, caption=f"Visual Render by {CREATOR}")
            else:
                st.warning("Please enter a description.")

elif selected == "Share Hub":
    st.title("🌐 Share Hub")
    st.markdown("""
        <div style="display: flex; gap: 30px; margin-top: 20px;">
            <a href="https://wa.me/" target="_blank"><img src="https://img.icons8.com/color/48/whatsapp.png" width="60"/></a>
            <a href="https://instagram.com/" target="_blank"><img src="https://img.icons8.com/color/48/instagram-new.png" width="60"/></a>
        </div>
    """, unsafe_allow_html=True)
