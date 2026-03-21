import streamlit as st
from google import genai
from streamlit_option_menu import option_menu

# --- 1. CORE CONFIGURATION ---
st.set_page_config(page_title="NEXUS Flash India", page_icon="⚡", layout="wide")

CREATOR = "Dumpala Karthik"
SYSTEM_PROMPT = f"Your name is NEXUS 3.1. You were developed and created by {CREATOR}."

# Check for Pollinations API Key in the URL (BYOP Facility)
query_params = st.query_params
pollinations_key = query_params.get("api_key", None)

# --- 2. THE SIDEBAR (Facilities & Connect) ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 80px; margin-bottom: 0;'>⚡</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; margin-top: 0;'>NEXUS FLASH INDIA</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #888;'>Architect: {CREATOR}</p>", unsafe_allow_html=True)
    st.divider()

    # THE FACILITY: CONNECT BUTTON (GitHub Fixed)
    if not pollinations_key:
        st.warning("Neural Architect Offline")
        auth_url = "https://enter.pollinations.ai/authorize?redirect_url=https://nexus-flash-india.streamlit.app"
        st.markdown(f"""
            <a href="{auth_url}" target="_blank">
                <button style="
                    width:100%; 
                    background-color:#ff4b4b; 
                    color:white; 
                    border:none; 
                    padding:12px; 
                    border-radius:8px; 
                    font-weight:bold;
                    cursor:pointer;
                    box-shadow: 0px 4px 10px rgba(255, 75, 75, 0.3);">
                    🔌 CONNECT POLLINATIONS
                </button>
            </a>
            """, unsafe_allow_html=True)
        st.caption("Login in the new tab to unlock images.")
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

# --- 3. MAIN INTERFACE ---

if selected == "Intelligence":
    st.markdown("<br><h1 style='text-align: center; color: #ff4b4b; font-size: 60px;'>HI, HOW ARE YOU!</h1>", unsafe_allow_html=True)
    
    if prompt := st.chat_input("Command NEXUS..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            try:
                # FIXED: Corrected client initialization
                client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=f"{SYSTEM_PROMPT}\n\nUser: {prompt}"
                )
                st.markdown(response.text)
            except Exception as e:
                st.error("Intelligence Error: Please check your Google API Key in Secrets.")

elif selected == "Neural Architect":
    st.title("🏗️ Neural Architect")
    
    if not pollinations_key:
        st.info("⚡ Please click the 'CONNECT' button in the sidebar to enable the Image Facility.")
    else:
        design_prompt = st.text_input("Describe the visual you want to build:")
        
        if st.button("EXECUTE RENDER"):
            if design_prompt:
                with st.spinner("Decoding Neural Structure..."):
                    try:
                        # FIXED: Corrected client and f-string syntax
                        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
                        code_query = f"Write 150 words of complex HTML/CSS code for: {design_prompt}"
                        code_res = client.models.generate_content(model="gemini-2.5-flash", contents=code_query)
                        matrix_text = code_res.text

                        # Get Image using the User's Connected Key
                        image_url = f"https://image.pollinations.ai/prompt/{design_prompt.replace(' ', '%20')}?key={pollinations_key}&nologo=true"
                        
                        # --- THE BIG GREEN MATRIX BOX ---
                        st.markdown(f"""
                        <div style="border: 2px solid #28a745; padding: 20px; border-radius: 10px; background-color: rgba(40, 167, 69, 0.05); height: 280px; overflow-y: scroll; margin-bottom: 25px;">
                            <p style="color: #28a745; font-family: monospace; font-weight: bold;">NEXUS_SYSTEM_CODE_DECODED:</p>
                            <pre style="color: #28a745; font-size: 12px; white-space: pre-wrap;">{matrix_text}</pre>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Display Image
                        st.image(image_url, caption=f"Visual Render by {CREATOR}")
                    except Exception as e:
                        st.error("Architect Error: Rendering sequence interrupted.")
            else:
                st.warning("Enter a description first.")

elif selected == "Share Hub":
    st.title("🌐 Share Hub")
    st.markdown(f"**NEXUS
