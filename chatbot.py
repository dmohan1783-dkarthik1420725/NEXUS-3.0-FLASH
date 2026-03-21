import streamlit as st
from google import genai
from streamlit_option_menu import option_menu

# --- 1. CORE CONFIGURATION ---
st.set_page_config(page_title="NEXUS Flash India", page_icon="⚡", layout="wide")

CREATOR = "Dumpala Karthik"
SYSTEM_PROMPT = f"Your name is NEXUS 3.1. You were developed and created by {CREATOR}."

try:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
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
            response = client.models.generate_content(model="gemini-1.5-flash", contents=f"{SYSTEM_PROMPT}\n\nUser: {prompt}")
            st.markdown(response.text)

elif selected == "Neural Architect":
    st.title("🏗️ Neural Architect")
    design_prompt = st.text_input("Describe the visual you want to build:")
    
    if st.button("EXECUTE RENDER"):
        if design_prompt:
            with st.spinner("Generating Neural Code..."):
                # 1. Generate the 'Big' HTML text using Gemini (100-200 words of 'code')
                code_response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=f"Generate a very long, complex-looking HTML and CSS code block (about 150 words) for a professional UI component related to: {design_prompt}. Output ONLY the raw code."
                )
                fake_code = code_response.text

                # 2. Get the Pollinations Image
                image_url = f"https://image.pollinations.ai/prompt/{design_prompt.replace(' ', '%20')}?width=1024&height=512&nologo=true"
                
                # --- THE BIG GREEN MATRIX BOX ---
                st.markdown(f"""
                <div style="border: 2px solid #28a745; padding: 20px; border-radius: 10px; background-color: rgba(40, 167, 69, 0.05); height: 300px; overflow-y: scroll; margin-bottom: 25px;">
                    <p style="color: #28a745; font-family: 'Courier New', monospace; font-weight: bold; font-size: 16px; margin-bottom: 10px;">
                        NEXUS_NEURAL_STRUCTURE_DECODED:
                    </p>
                    <pre style="color: #28a745; font-size: 12px; white-space: pre-wrap; word-wrap: break-word;">
{fake_code}
                    </pre>
                </div>
                """, unsafe_allow_html=True)
                
                # 3. Final Image Display
                st.image(image_url, caption=f"Visual Render by {CREATOR}")
        else:
            st.warning("Enter a description first.")

elif selected == "Share Hub":
    st.title("🌐 Share Hub")
    st.markdown("""
        <div style="display: flex; gap: 30px; margin-top: 20px;">
            <a href="https://wa.me/" target="_blank"><img src="https://img.icons8.com/color/48/whatsapp.png" width="60"/></a>
            <a href="https://instagram.com/" target="_blank"><img src="https://img.icons8.com/color/48/instagram-new.png" width="60"/></a>
        </div>
    """, unsafe_allow_html=True)
