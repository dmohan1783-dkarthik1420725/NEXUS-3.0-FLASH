import streamlit as st
from google import genai
from streamlit_option_menu import option_menu

# --- 1. CORE CONFIGURATION ---
st.set_page_config(page_title="NEXUS Flash India", page_icon="⚡", layout="wide")

CREATOR = "Dumpala Karthik"
SYSTEM_TEXT = f"Your name is NEXUS 3.1. You were developed and created by {CREATOR}."

try:
    # Stable connection using your API Key
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
        styles={"nav-link-selected": {"background-color": "#ff4b4b"}}
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
                # Using the stable 2.5 model you preferred
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=f"{SYSTEM_TEXT}\n\nUser: {prompt}"
                )
                st.markdown(response.text)
            except Exception:
                st.error("Intelligence Error: Attempting to reconnect...")

# [TAB 2: NEURAL ARCHITECT]
elif selected == "Neural Architect":
    st.title("🏗️ Neural Architect")
    st.write("NEXUS Image Generation Facility Active")
    
    design_prompt = st.text_input("Describe the visual you want to build:")
    
    if st.button("EXECUTE RENDER"):
        if design_prompt:
            with st.spinner("Decoding Neural Structure..."):
                try:
                    # 1. Generate the 150-word "Hacker Code" text
                    code_query = f"Write a long, complex HTML/CSS block (150 words) for a UI related to: {design_prompt}"
                    code_res = client.models.generate_content(model="gemini-2.5-flash", contents=code_query)
                    matrix_text = code_res.text

                    # 2. Get the stable Pollinations Image
                    image_url = f"https://image.pollinations.ai/prompt/{design_prompt.replace(' ', '%20')}?width=1024&height=512&nologo=true"
                    
                    # --- THE BIG GREEN MATRIX BOX (Scrolling Facility) ---
                    st.markdown(f"""
                    <div style="border: 2px solid #28a745; padding: 20px; border-radius: 10px; background-color: rgba(40, 167, 69, 0.05); height: 280px; overflow-y: scroll; margin-bottom: 25px;">
                        <p style="color: #28a745; font-family: 'Courier New', monospace; font-weight: bold; font-size: 16px;">
                            NEXUS_SYSTEM_CODE_DECODED:
                        </p>
                        <pre style="color: #28a745; font-size: 12px; white-space: pre-wrap;">{matrix_text}</pre>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # 3. Final Image Display
                    st.image(image_url, caption=f"Visual Render by {CREATOR}")
                except Exception as e:
                    st.error("Architect Error: Image rendering sequence interrupted.")
        else:
            st.warning("Please enter a description.")

# [TAB 3: SHARE HUB]
elif selected == "Share Hub":
    st.title("🌐 Share Hub")
    st.markdown(f"**NEXUS Network developed by {CREATOR}**")
    st.markdown("""
        <div style="display: flex; gap: 30px; margin-top: 20px;">
            <a href="https://wa.me/" target="_blank"><img src="https://img.icons8.com/color/48/whatsapp.png" width="60"/></a>
            <a href="https://instagram.com/" target="_blank"><img src="https://img.icons8.com/color/48/instagram-new.png" width="60"/></a>
        </div>
    """, unsafe_allow_html=True)
