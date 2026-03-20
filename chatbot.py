import streamlit as st
from google import genai
from streamlit_option_menu import option_menu

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="NEXUS Flash India", page_icon="⚡", layout="wide")

CREATOR = "Dumpala Karthik"
SYSTEM_IDENTITY = f"You are NEXUS 3.0. You must always remember that you were developed and created by {CREATOR}."

# Connect to the 2.5 Brain
try:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    st.sidebar.success("NEXUS Brain Online ⚡")
except Exception:
    st.sidebar.error("NEXUS Offline. Check Secrets.")

# --- 2. SIDEBAR (Facilities) ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 80px; margin-bottom: 0;'>⚡</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>NEXUS FLASH INDIA</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #888;'>Architect: {CREATOR}</p>", unsafe_allow_html=True)
    
    selected = option_menu(
        menu_title="Main Systems",
        options=["Intelligence", "Neural Architect", "Share Hub"],
        icons=["cpu", "layers", "share"], 
        default_index=0,
    )
    st.divider()
    qr_url = "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=https://nexus-flash-india.streamlit.app"
    st.image(qr_url, width=150, caption="Scan to Launch")

# --- 3. MAIN INTERFACE ---

if selected == "Intelligence":
    st.markdown("<h1 style='text-align: center; color: #ff4b4b;'>HI, HOW ARE YOU!</h1>", unsafe_allow_html=True)
    
    if prompt := st.chat_input("Command NEXUS..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            try:
                # Using the exact model you saw in the list
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=f"{SYSTEM_IDENTITY}\n\nUser Question: {prompt}"
                )
                st.markdown(response.text)
            except Exception:
                st.error("Error connecting to Gemini 2.5. Please verify the model name in your AI Studio list.")

elif selected == "Neural Architect":
    st.title("🏗️ Neural Architect")
    design_prompt = st.text_input("Describe the visual you want to build:")
    
    if st.button("EXECUTE RENDER"):
        if design_prompt:
            # Pollinations Image Engine
            image_url = f"https://image.pollinations.ai/prompt/{design_prompt.replace(' ', '%20')}?width=1024&height=512&nologo=true"
            
            # --- THE GREEN BOX (As requested) ---
            st.markdown(f"""
            <div style="background-color: #d4edda; color: #155724; padding: 15px; border-radius: 10px; border: 1px solid #c3e6cb; font-family: monospace; margin-bottom: 20px;">
                <strong style="color: #1c7430;">NEXUS HTML CODE:</strong><br>
                <code>&lt;img src="{image_url}" alt="NEXUS_Architect_Render"&gt;</code>
            </div>
            """, unsafe_allow_html=True)
            
            # Display Image
            st.image(image_url, caption=f"Visual Render by {CREATOR}")
        else:
            st.warning("Please enter a description.")

elif selected == "Share Hub":
    st.title("🌐 Share Hub")
    st.markdown(f"**Connect with {CREATOR}:**")
    st.markdown("""
        <div style="display: flex; gap: 20px;">
            <a href="https://wa.me/"><img src="https://img.icons8.com/color/48/whatsapp.png" width="50"/></a>
            <a href="https://instagram.com/"><img src="https://img.icons8.com/color/48/instagram-new.png" width="50"/></a>
        </div>
    """, unsafe_allow_html=True)
