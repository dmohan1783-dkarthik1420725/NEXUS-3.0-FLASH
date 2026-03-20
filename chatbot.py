import streamlit as st
from google import genai
from openai import OpenAI
from streamlit_option_menu import option_menu

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="NEXUS Flash India", page_icon="⚡", layout="wide")

# Initialize Both Brains
try:
    # Google Brain (Intelligence)
    google_client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    # OpenAI Brain (Neural Architect / Pollutants)
    openai_client = OpenAI(api_key=st.secrets["POLLUTANTS_KEY"])
except Exception as e:
    st.error("NEXUS Brain Offline. Check Secrets for GOOGLE_API_KEY and POLLUTANTS_KEY.")

# --- 2. SIDEBAR (The Facilities) ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 80px; margin-bottom: 0;'>⚡</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; margin-top: 0;'>NEXUS FLASH INDIA</h3>", unsafe_allow_html=True)
    st.divider()

    selected = option_menu(
        menu_title="Main Systems",
        options=["Intelligence", "Neural Architect", "Share Hub"],
        icons=["cpu", "layers", "share"], 
        default_index=0,
        styles={
            "container": {"background-color": "#1e1e1e"},
            "nav-link-selected": {"background-color": "#ff4b4b"},
        }
    )

    st.divider()
    st.write("📲 **Scan to Launch**")
    qr_url = "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=https://nexus-flash-india.streamlit.app"
    st.image(qr_url, width=150)

# --- 3. MAIN INTERFACE ---

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
            # Using Google Gemini 1.5 Flash
            response = google_client.models.generate_content(model="gemini-1.5-flash", contents=prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

elif selected == "Neural Architect":
    st.title("🏗️ Neural Architect")
    st.info("Powered by Pollutants Engine (OpenAI)")
    
    arch_prompt = st.text_input("Describe a design (e.g., 'A blue futuristic button'):")
    
    if st.button("GENERATE ARCHITECTURE"):
        with st.spinner("Constructing..."):
            # Using OpenAI with your 'sk-...' key
            completion = openai_client.chat.completions.create(
                model="gpt-3.5-turbo", # Or gpt-4o
                messages=[{"role": "user", "content": f"Generate ONLY raw HTML/CSS code for: {arch_prompt}. No markdown, no text."}]
            )
            html_code = completion.choices[0].message.content
            st.components.v1.html(html_code, height=300, scrolling=True)
            st.code(html_code, language="html")

elif selected == "Share Hub":
    st.title("🌐 Share Hub")
    st.markdown("""
    <div style="display: flex; gap: 20px;">
        <a href="https://wa.me/"><img src="https://img.icons8.com/color/48/whatsapp.png" width="50"/></a>
        <a href="https://www.instagram.com"><img src="https://img.icons8.com/color/48/instagram-new.png" width="50"/></a>
    </div>
    """, unsafe_allow_html=True)
