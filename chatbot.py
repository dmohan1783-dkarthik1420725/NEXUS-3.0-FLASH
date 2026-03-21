import streamlit as st
from google import genai
from streamlit_option_menu import option_menu
import base64

# --- 1. CORE CONFIGURATION ---
st.set_page_config(page_title="NEXUS Flash India", page_icon="⚡", layout="wide")

# Personal Identity
CREATOR = "Dumpala Karthik"
SYSTEM_PROMPT = f"Your name is NEXUS 3.1. You were developed and created by {CREATOR}."

# Connect to the 2.5 Brain (Intelligence & Image)
try:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    st.sidebar.success("NEXUS Brain Online ⚡")
except Exception:
    st.sidebar.error("NEXUS Brain Offline. Check Secrets.")

# --- 2. THE SIDEBAR (Facilities) ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 80px; margin-bottom: 0;'>⚡</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; margin-top: 0;'>NEXUS FLASH INDIA</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #888;'>Architect: {CREATOR}</p>", unsafe_allow_html=True)
    st.divider()

    selected = option_menu(
        menu_title="Main Systems",
        options=["Intelligence", "Neural Architect", "Share Hub"],
        icons=["cpu", "layers", "share"], 
        default_index=0,
        styles={
            "container": {"background-color": "#121212"},
            "nav-link-selected": {"background-color": "#ff4b4b"},
        }
    )

    st.divider()
    qr_url = "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=https://nexus-flash-india.streamlit.app"
    st.image(qr_url, width=150, caption="Scan to Launch")

# --- 3. MAIN INTERFACE ---

# [TAB 1: INTELLIGENCE]
if selected == "Intelligence":
    st.markdown("<br><h1 style='text-align: center; color: #ff4b4b; font-size: 60px;'>HI, HOW ARE YOU!</h1>", unsafe_allow_html=True)
    
    if prompt := st.chat_input("Command NEXUS..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            try:
                # Using Gemini 2.5 Flash for Chat
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=f"{SYSTEM_PROMPT}\n\nUser: {prompt}"
                )
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Intelligence Error: {e}")

# [TAB 2: NEURAL ARCHITECT - NATIVE GOOGLE IMAGES]
elif selected == "Neural Architect":
    st.title("🏗️ Neural Architect")
    st.write("NEXUS Native Google Image Facility Active")
    
    design_prompt = st.text_input("Describe the visual you want to build:")
    
    if st.button("EXECUTE NATIVE RENDER"):
        if design_prompt:
            with st.spinner("NEXUS Brain is painting..."):
                try:
                    # Calling your Google Key for the Image
                    response = client.models.generate_content(
                        model="gemini-2.5-flash-image",
                        contents=design_prompt,
                        config={'response_modalities': ['IMAGE']}
                    )
                    
                    # Extract and show image
                    for part in response.candidates[0].content.parts:
                        if hasattr(part, 'inline_data'):
                            # Display the image
                            st.image(part.inline_data.data, caption=f"Native Render by {CREATOR}")
                            
                            # --- THE FACILITY BOX (Green Outline) ---
                            st.markdown(f"""
                            <div style="border: 2px solid #28a745; padding: 20px; border-radius: 10px; background-color: rgba(40, 167, 69, 0.05); margin-top: 25px;">
                                <p style="color: #28a745; font-family: 'Courier New', monospace; font-weight: bold; font-size: 16px; margin: 0;">
                                    NEXUS_NATIVE_GOOGLE_CODE:
                                </p>
                                <code style="color: #ffffff; font-size: 14px;">
                                    SYSTEM_STATUS: RENDER_COMPLETE_BY_GEMINI_2.5_FLASH_IMAGE
                                </code>
                            </div>
                            """, unsafe_allow_html=True)
                            
                except Exception as e:
                    st.error(f"Google Image Error: {e}")
                    st.info("Tip: Your key has access to 'Nano Banana' for images. Ensure billing/quota is active.")
        else:
            st.warning("Please enter a description.")

# [TAB 3: SHARE HUB]
elif selected == "Share Hub":
    st.title("🌐 Share Hub")
    st.markdown(f"**Connect with the developer, {CREATOR}:**")
    st.markdown("""
        <div style="display: flex; gap: 30px; margin-top: 20px;">
            <a href="https://wa.me/" target="_blank"><img src="https://img.icons8.com/color/48/whatsapp.png" width="60"/></a>
            <a href="https://instagram.com/" target="_blank"><img src="https://img.icons8.com/color/48/instagram-new.png" width="60"/></a>
        </div>
    """, unsafe_allow_html=True)
