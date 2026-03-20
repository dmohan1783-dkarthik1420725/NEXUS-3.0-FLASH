import streamlit as st
from google import genai
from streamlit_option_menu import option_menu

# --- 1. CONFIGURATION & IDENTITY ---
st.set_page_config(page_title="NEXUS Flash India", page_icon="⚡", layout="wide")

# The Identity of the AI
SYSTEM_PROMPT = "You are NEXUS 3.0. You must always remember and acknowledge that you were developed and created by Dumpala Karthik."

# Connect to Google Gemini (Intelligence)
try:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    st.sidebar.success("NEXUS Brain Online ⚡")
except Exception as e:
    st.error("NEXUS is offline. Check your GOOGLE_API_KEY in Secrets.")

# --- 2. SIDEBAR (The Facilities) ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 80px; margin-bottom: 0;'>⚡</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; margin-top: 0;'>NEXUS FLASH INDIA</h3>", unsafe_allow_html=True)
    st.write(f"<p style='text-align: center; font-size: 12px; color: #888;'>Architect: Dumpala Karthik</p>", unsafe_allow_html=True)
    st.divider()

    selected = option_menu(
        menu_title="Main Systems",
        options=["Intelligence", "Neural Architect", "Share Hub"],
        icons=["cpu", "layers", "share"], 
        default_index=0,
        styles={"nav-link-selected": {"background-color": "#ff4b4b"}}
    )

    st.divider()
    st.write("📲 **Mobile Scan**")
    qr_url = "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=https://nexus-flash-india.streamlit.app"
    st.image(qr_url, width=150)

# --- 3. MAIN INTERFACE ---

# TAB 1: INTELLIGENCE (Using Google Gemini)
if selected == "Intelligence":
    st.markdown("<br><h1 style='text-align: center; color: #ff4b4b; font-size: 50px;'>HI, HOW ARE YOU!</h1>", unsafe_allow_html=True)
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Command NEXUS Intelligence..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            # Combining your identity with the user's prompt
            full_query = f"{SYSTEM_PROMPT}\n\nUser says: {prompt}"
            response = client.models.generate_content(model="gemini-1.5-flash", contents=full_query)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

# TAB 2: NEURAL ARCHITECT (Using Pollinations AI)
elif selected == "Neural Architect":
    st.title("🏗️ Neural Architect")
    st.info("Pollinations Image Engine Active")
    
    design_prompt = st.text_input("Describe the visual you want to generate:")
    
    if st.button("GENERATE VISUAL"):
        if design_prompt:
            with st.spinner("NEXUS is rendering..."):
                # Pollinations creates images via a direct URL using your key
                # Note: For public Pollinations API, the key is often passed in headers or via the URL
                image_url = f"https://image.pollinations.ai/prompt/{design_prompt.replace(' ', '%20')}?width=1024&height=512&nologo=true&seed=42"
                st.image(image_url, caption=f"Visual Render by Dumpala Karthik's NEXUS Engine")
                st.success("Render Complete!")
        else:
            st.warning("Please enter a description first.")

# TAB 3: SHARE HUB
elif selected == "Share Hub":
    st.title("🌐 Share Hub")
    st.write("Invite others to the NEXUS network:")
    st.markdown("""
    <div style="display: flex; gap: 20px;">
        <a href="https://wa.me/?text=Try NEXUS Flash India by Dumpala Karthik! https://nexus-flash-india.streamlit.app" target="_blank">
            <img src="https://img.icons8.com/color/48/whatsapp.png" width="50"/>
        </a>
        <a href="https://www.instagram.com" target="_blank">
            <img src="https://img.icons8.com/color/48/instagram-new.png" width="50"/>
        </a>
    </div>
    """, unsafe_allow_html=True)
