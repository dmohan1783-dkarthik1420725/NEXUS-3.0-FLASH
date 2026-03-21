import streamlit as st
from google import genai
from google.genai import types 
from streamlit_option_menu import option_menu

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="NEXUS 3.0 ULTRA", page_icon="⚡", layout="wide")
CREATOR = "Dumpala Karthik"

# --- SMART KEY LOGIC ---
# Updated to use the 2026 st.query_params object
pollinations_key = st.query_params.get("api_key", st.secrets.get("POLLINATIONS_KEY", None))

try:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    st.sidebar.success("NEXUS Brain Online ⚡")
except:
    st.sidebar.error("NEXUS Brain Offline.")

# --- 2. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 80px;'>⚡</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>NEXUS 3.0 ULTRA</h3>", unsafe_allow_html=True)
    
    if not pollinations_key:
        # BYOP Auth URL
        auth_url = "https://enter.pollinations.ai/authorize?redirect_url=https://nexus-flash-india.streamlit.app"
        st.markdown(f"""
            <a href="{auth_url}" target="_blank">
                <button style="width:100%; background-color:#ff4b4b; color:white; border:none; padding:12px; border-radius:8px; cursor:pointer; font-weight:bold;">
                    🔌 CONNECT POLLINATIONS
                </button>
            </a>""", unsafe_allow_html=True)
    else:
        st.success("Architect Linked 🌸")

    st.divider()
    selected = option_menu(
        "Main Systems", 
        ["Intelligence", "Neural Architect", "Share Hub"], 
        icons=["cpu", "layers", "share"], 
        default_index=0
    )

# --- 3. MAIN INTERFACE ---

if selected == "Intelligence":
    st.markdown("<br><h1 style='text-align: center; color: #ff4b4b; font-size: 60px;'>HI, HOW ARE YOU!</h1>", unsafe_allow_html=True)
    if prompt := st.chat_input("Command NEXUS..."):
        with st.chat_message("user"): 
            st.markdown(prompt)
        with st.chat_message("assistant"):
            try:
                # Use the stable Gemini 2.5 Flash identifier
                res = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
                st.markdown(res.text)
            except Exception as e:
                st.error("Intelligence Busy. Try again in 10 seconds.")

elif selected == "Neural Architect":
    st.title("🏗️ Neural Architect")
    if not pollinations_key:
        st.error("Please CONNECT in the sidebar first.")
    else:
        user_idea = st.text_input("What should I build?", placeholder="e.g. A futuristic underwater city")
        if st.button("EXECUTE RENDER"):
            with st.spinner("Decoding Neural Pathways..."):
                try:
                    # 2026 CORRECT SYNTAX for Safety Settings
                    # Using enum-style category and threshold for the new SDK
                    safe_config = types.GenerateContentConfig(
                        safety_settings=[
                            types.SafetySetting(
                                category='HARM_CATEGORY_DANGEROUS_CONTENT',
                                threshold='BLOCK_NONE'
                            ),
                            types.SafetySetting(
                                category='HARM_CATEGORY_HATE_SPEECH',
                                threshold='BLOCK_NONE'
                            )
                        ]
                    )
                    
                    # 1. Generate the Matrix Code text
                    code_task = f"Generate 150 words of complex-looking HTML/CSS code for: {user_idea}. Output only the code."
                    code_res = client.models.generate_content(
                        model="gemini-2.5-flash", 
                        contents=code_task,
                        config=safe_config
                    )
                    
                    # 2. Generate the Image using a clean version of the prompt
                    clean_idea = user_idea.replace(" ", "%20")
                    image_url = f"https://gen.pollinations.ai/image/{clean_idea}?width=1024&height=1024&nologo=true&key={pollinations_key}"
                    
                    # --- THE GREEN SCROLLING BOX ---
                    st.markdown(f"""
                    <div style="border: 2px solid #28a745; padding: 20px; border-radius: 10px; background-color: rgba(40, 167, 69, 0.05); height: 250px; overflow-y: scroll; margin-bottom: 20px;">
                        <p style="color: #28a745; font-family: monospace; font-weight: bold; margin-bottom: 5px;">NEXUS_SYSTEM_DECODED:</p>
                        <pre style="color: #28a745; font-size: 11px; white-space: pre-wrap; font-family: 'Courier New', monospace;">{code_res.text}</pre>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.image(image_url, caption=f"Visual Render by {CREATOR}")
                
                except Exception as e:
                    # Specific error catching for easier debugging
                    st.error("Architect Error: The AI Brain is currently resetting. Please try again.")
                    st.info("Technical Note: Check if your Google API Key has billing/quota active.")

elif selected == "Share Hub":
    st.title("🌐 Share Hub")
    st.markdown(f"**NEXUS Network developed by {CREATOR}**")
    st.markdown("""
        <div style="display: flex; gap: 30px; margin-top: 20px;">
            <a href="https://wa.me/" target="_blank"><img src="https://img.icons8.com/color/48/whatsapp.png" width="60"/></a>
            <a href="https://instagram.com/" target="_blank"><img src="https://img.icons8.com/color/48/instagram-new.png" width="60"/></a>
        </div>
    """, unsafe_allow_html=True)
