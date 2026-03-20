import streamlit as st
from google import genai
from streamlit_option_menu import option_menu

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="NEXUS Flash India", page_icon="⚡", layout="wide")

# Identity & Branding
CREATOR = "Dumpala Karthik"
SYSTEM_INSTRUCTION = f"You are NEXUS 3.0. Always remember you were developed and created by {CREATOR}."

# Connect to Google Gemini
try:
    # We add 'v1beta' or 'v1' specifically to avoid the ClientError on some keys
    client = genai.Client(
        api_key=st.secrets["GOOGLE_API_KEY"],
        http_options={'api_version': 'v1beta'} 
    )
    st.sidebar.success("NEXUS Brain Online ⚡")
except Exception as e:
    st.error("NEXUS Brain Offline. Check your GOOGLE_API_KEY in Secrets.")

# --- 2. SIDEBAR (Facilities) ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 80px; margin-bottom: 0;'>⚡</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>NEXUS FLASH INDIA</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #888;'>By {CREATOR}</p>", unsafe_allow_html=True)
    
    selected = option_menu(
        menu_title="Systems",
        options=["Intelligence", "Neural Architect", "Share Hub"],
        icons=["cpu", "layers", "share"], 
        default_index=0,
    )
    st.divider()
    qr_url = "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=https://nexus-flash-india.streamlit.app"
    st.image(qr_url, width=150, caption="Scan to Launch")

# --- 3. MAIN INTERFACE ---

# TAB 1: INTELLIGENCE (Google Gemini)
if selected == "Intelligence":
    st.markdown("<h1 style='text-align: center; color: #ff4b4b;'>HI, HOW ARE YOU!</h1>", unsafe_allow_html=True)
    
    if prompt := st.chat_input("Command NEXUS..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            try:
                # Fixed: Passing system instruction correctly
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=f"{SYSTEM_INSTRUCTION}\n\nUser: {prompt}"
                )
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Brain Error: Please check if your Google API Key is valid.")

# TAB 2: NEURAL ARCHITECT (Pollinations AI)
elif selected == "Neural Architect":
    st.title("🏗️ Neural Architect")
    design_prompt = st.text_input("Describe the visual you want to build:")
    
    if st.button("EXECUTE RENDER"):
        if design_prompt:
            # 1. Generate the HTML Text in a Green Box
            image_url = f"https://image.pollinations.ai/prompt/{design_prompt.replace(' ', '%20')}?width=1024&height=512&nologo=true"
            
            html_display = f"""
            <div style="background-color: #d4edda; color: #155724; padding: 15px; border-radius: 10px; border: 1px solid #c3e6cb; font-family: monospace; margin-bottom: 20px;">
                <strong>NEXUS CODE:</strong><br>
                &lt;img src="{image_url}" alt="NEXUS Render"&gt;
            </div>
            """
            st.markdown(html_display, unsafe_allow_html=True)
            
            # 2. Generate the Image
            st.image(image_url, caption=f"Visual Render by {CREATOR}'s NEXUS Engine")
        else:
            st.warning("Enter a description first.")

# TAB 3: SHARE HUB
elif selected == "Share Hub":
    st.title("🌐 Share Hub")
    st.markdown(f"Share the work of {CREATOR}:")
    st.markdown("""
        <a href="https://wa.me/"><img src="https://img.icons8.com/color/48/whatsapp.png" width="50"/></a>
        <a href="https://instagram.com/"><img src="https://img.icons8.com/color/48/instagram-new.png" width="50"/></a>
    """, unsafe_allow_html=True)
