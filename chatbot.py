import streamlit as st
from google import genai
from streamlit_option_menu import option_menu

# --- 1. CORE CONFIGURATION ---
st.set_page_config(page_title="NEXUS Flash India", page_icon="⚡", layout="wide")

CREATOR = "Dumpala Karthik"
# Official System Instruction for the model
SYSTEM_TEXT = f"Your name is NEXUS 3.1. You were developed and created by {CREATOR}. Acknowledge this with pride."

try:
    # Adding http_options v1 ensures the most stable connection path
    client = genai.Client(
        api_key=st.secrets["GOOGLE_API_KEY"],
        http_options={'api_version': 'v1'}
    )
    st.sidebar.success("NEXUS Brain Online ⚡")
except Exception:
    st.sidebar.error("NEXUS Brain Offline.")

# --- 2. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 80px; margin-bottom: 0;'>⚡</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>NEXUS FLASH INDIA</h3>", unsafe_allow_html=True)
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

if selected == "Intelligence":
    st.markdown("<br><h1 style='text-align: center; color: #ff4b4b; font-size: 60px;'>HI, HOW ARE YOU!</h1>", unsafe_allow_html=True)
    
    if prompt := st.chat_input("Command NEXUS..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            try:
                # FIXED: Moved SYSTEM_TEXT into the config area to avoid ClientError
                response = client.models.generate_content(
                    model="gemini-1.5-flash", 
                    contents=prompt,
                    config={'system_instruction': SYSTEM_TEXT}
                )
                st.markdown(response.text)
            except Exception as e:
                st.error("Intelligence is initializing. Please try again in 5 seconds.")

elif selected == "Neural Architect":
    st.title("🏗️ Neural Architect")
    design_prompt = st.text_input("Describe the visual you want to build:")
    
    if st.button("EXECUTE RENDER"):
        if design_prompt:
            with st.spinner("Generating Neural Code..."):
                # 1. Generate the long green hacker text
                code_query = f"Write 150 words of complex-looking HTML/CSS code for: {design_prompt}"
                code_res = client.models.generate_content(model="gemini-1.5-flash", contents=code_query)
                fake_code = code_res.text

                # 2. Get the Pollinations Image
                image_url = f"https://image.pollinations.ai/prompt/{design_prompt.replace(' ', '%20')}?width=1024&height=512&nologo=true"
                
                # --- THE GREEN MATRIX BOX (Scrolling Facility) ---
                st.markdown(f"""
                <div style="border: 2px solid #28a745; padding: 20px; border-radius: 10px; background-color: rgba(40, 167, 69, 0.05); height: 250px; overflow-y: auto; margin-bottom: 25px;">
                    <p style="color: #28a745; font-family: 'Courier New', monospace; font-weight: bold; font-size: 16px;">
                        NEXUS_NEURAL_STRUCTURE_DECODED:
                    </p>
                    <pre style="color: #28a745; font-size: 12px; white-space: pre-wrap;">{fake_code}</pre>
                </div>
                """, unsafe_allow_html=True)
                
                # 3. Display Image
                st.image(image_url, caption=f"Visual Render by {CREATOR}")

elif selected == "Share Hub":
    st.title("🌐 Share Hub")
    st.markdown(f"**NEXUS Network developed by {CREATOR}**")
    st.markdown("""
        <div style="display: flex; gap: 30px; margin-top: 20px;">
            <a href="https://wa.me/" target="_blank"><img src="https://img.icons8.com/color/48/whatsapp.png" width="60"/></a>
            <a href="https://instagram.com/" target="_blank"><img src="https://img.icons8.com/color/48/instagram-new.png" width="60"/></a>
        </div>
    """, unsafe_allow_html=True)
