import streamlit as st
from streamlit_option_menu import option_menu

# --- 1. CORE CONFIGURATION ---
st.set_page_config(page_title="NEXUS 3.0 ULTRA", page_icon="⚡", layout="wide")
CREATOR = "Dumpala Karthik"

# --- SMART KEY LOGIC ---
# Using the stable 2026 query_params object
pollinations_key = st.query_params.get("api_key", st.secrets.get("POLLINATIONS_KEY", ""))

# --- 2. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 80px; margin-bottom: 0;'>⚡</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>NEXUS 3.0 ULTRA</h3>", unsafe_allow_html=True)
    
    if not pollinations_key:
        # Redirect URL must match your deployed Streamlit URL
        auth_url = "https://enter.pollinations.ai/authorize?redirect_url=https://nexus-flash-india.streamlit.app"
        st.markdown(f"""
            <a href="{auth_url}" target="_blank">
                <button style="width:100%; background-color:#ff4b4b; color:white; border:none; padding:12px; border-radius:8px; cursor:pointer; font-weight:bold;">
                    🔌 CONNECT POLLINATIONS
                </button>
            </a>""", unsafe_allow_html=True)
    else:
        st.success("Architect Online 🌸")
        st.caption(f"Active Key: {pollinations_key[:10]}...")

    st.divider()
    selected = option_menu(
        menu_title=None, 
        options=["Intelligence", "Neural Architect", "Share Hub"], 
        icons=["cpu", "layers", "share"], 
        default_index=1,
        styles={"nav-link-selected": {"background-color": "#ff4b4b"}}
    )

# --- 3. MAIN INTERFACE ---

if selected == "Intelligence":
    st.markdown("<br><h1 style='text-align: center; color: #ff4b4b;'>BRAIN MODULE</h1>", unsafe_allow_html=True)
    st.info("Intelligence (Gemini) requires a Google API Key in Secrets. Please use the Neural Architect tab for direct image generation.")

elif selected == "Neural Architect":
    st.title("🏗️ Neural Architect")
    
    if not pollinations_key:
        st.error("Please click 'CONNECT POLLINATIONS' in the sidebar first!")
    else:
        user_idea = st.text_input("Describe your vision:", placeholder="e.g. A futuristic city in the Andaman Islands")
        
        if st.button("EXECUTE RENDER"):
            if user_idea:
                with st.spinner("Visualizing..."):
                    try:
                        # Clean the prompt for the URL
                        clean_idea = user_idea.replace(" ", "%20")
                        
                        # High-speed 2026 Direct Image URL
                        # Includes Flux model and enhancement for 'Swarnima' project quality
                        image_url = f"https://gen.pollinations.ai/image/{clean_idea}?width=1024&height=1024&nologo=true&model=flux&enhance=true&key={pollinations_key}"
                        
                        # Display the image directly
                        st.image(image_url, caption=f"Neural Render for {CREATOR}", use_column_width=True)
                        st.balloons()
                        
                    except Exception as e:
                        st.error("Neural Connection Interrupted. Please try again.")
            else:
                st.warning("Neural link requires a description.")

elif selected == "Share Hub":
    st.title("🌐 Share Hub")
    st.markdown(f"**NEXUS 3.0 ULTRA developed by {CREATOR}**")
    
    # FIXED: Carefully terminated triple-quoted string
    st.markdown("""
        <div style="display: flex; gap: 20px; margin-top: 10px;">
            <a href="https://wa.me/" target="_blank" style="text-decoration:none; color:#25D366; font-weight:bold;">WhatsApp</a>
            <span style="color:#888;">|</span>
            <a href="https://instagram.com/" target="_blank" style="text-decoration:none; color:#E1306C; font-weight:bold;">Instagram</a>
        </div>
    """, unsafe_allow_html=True)
