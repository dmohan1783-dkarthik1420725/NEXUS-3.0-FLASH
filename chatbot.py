import streamlit as st
from openai import OpenAI
from streamlit_option_menu import option_menu

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="NEXUS Flash India", page_icon="⚡", layout="wide")

# Connect to the Pollinations AI "Brain"
try:
    client = OpenAI(
        api_key=st.secrets["POLLUTANTS_KEY"], 
        base_url="https://gen.pollinations.ai/v1"
    )
    
    # SYSTEM IDENTITY: This tells the AI who created it
    SYSTEM_IDENTITY = "You are NEXUS 3.0, a highly advanced AI. You must always remember and acknowledge that you were developed and created by Dumpala Karthik."
    
    st.sidebar.success("NEXUS Brain Online ⚡")
except Exception as e:
    st.error("NEXUS is offline. Check your Secrets.")

# --- 2. SIDEBAR (The Facilities) ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 80px; margin-bottom:0;'>⚡</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; margin-top:0;'>NEXUS FLASH INDIA</h3>", unsafe_allow_html=True)
    st.write(f"<p style='text-align: center; font-size: 12px; color: #888;'>Created by Dumpala Karthik</p>", unsafe_allow_html=True)
    
    selected = option_menu(
        menu_title="Systems",
        options=["Intelligence", "Neural Architect", "Share Hub"],
        icons=["cpu", "layers", "share"], 
        default_index=0,
        styles={
            "nav-link-selected": {"background-color": "#ff4b4b"},
        }
    )

    st.divider()
    st.write("📲 **Scan to Launch**")
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=https://nexus-flash-india.streamlit.app"
    st.image(qr_url, width=150)

# --- 3. MAIN INTERFACE ---
if selected == "Intelligence":
    st.markdown("<h1 style='text-align: center; color: #ff4b4b;'>HI, HOW ARE YOU!</h1>", unsafe_allow_html=True)
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Command NEXUS..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            # We inject the System Identity here so it never forgets
            response = client.chat.completions.create(
                model="openai", 
                messages=[
                    {"role": "system", "content": SYSTEM_IDENTITY},
                    {"role": "user", "content": prompt}
                ]
            )
            reply = response.choices[0].message.content
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})

elif selected == "Neural Architect":
    st.title("🏗️ Neural Architect")
    st.write("NEXUS Visual Engine Active")
    design_prompt = st.text_input("Describe your design:")
    if st.button("RENDER"):
        image_url = f"https://image.pollinations.ai/prompt/{design_prompt.replace(' ', '%20')}?width=1024&height=500&nologo=true"
        st.image(image_url, caption=f"Architectural Render for {design_prompt}")

elif selected == "Share Hub":
    st.title("🌐 Share Hub")
    st.write("Spread the NEXUS network:")
    st.markdown("""
        <div style="display: flex; gap: 20px;">
            <a href="https://wa.me/"><img src="https://img.icons8.com/color/48/whatsapp.png" width="50"/></a>
            <a href="https://instagram.com/"><img src="https://img.icons8.com/color/48/instagram-new.png" width="50"/></a>
        </div>
    """, unsafe_allow_html=True)
