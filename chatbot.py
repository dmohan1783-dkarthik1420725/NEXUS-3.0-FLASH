import streamlit as st
import requests
from streamlit_option_menu import option_menu

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="NEXUS 3.0 ULTRA", page_icon="⚡", layout="wide")
CREATOR = "Dumpala Karthik"

# --- SMART KEY LOGIC ---
# Detects key from URL after you click 'Connect'
pollinations_key = st.query_params.get("api_key", st.secrets.get("POLLINATIONS_KEY", ""))

# --- 2. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 80px; margin-bottom: 0;'>⚡</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>NEXUS 3.0 ULTRA</h3>", unsafe_allow_html=True)
    
    if not pollinations_key:
        auth_url = "https://enter.pollinations.ai/authorize?redirect_url=https://nexus-flash-india.streamlit.app"
        st.markdown(f"""
            <a href="{auth_url}" target="_blank">
                <button style="width:100%; background-color:#ff4b4b; color:white; border:none; padding:12px; border-radius:8px; cursor:pointer; font-weight:bold;">
                    🔌 CONNECT POLLINATIONS
                </button>
            </a>""", unsafe_allow_html=True)
    else:
        st.success("Architect Linked 🌸")
        st.caption(f"Key: {pollinations_key[:10]}...")

    st.divider()
    selected = option_menu("Main Systems", ["Intelligence", "Neural Architect", "Share Hub"], 
                          icons=["cpu", "layers", "share"], default_index=1)

# --- 3. MAIN INTERFACE ---

if selected == "Intelligence":
    st.info("Intelligence (Gemini) requires a Google API Key in Secrets. Please use the Neural Architect tab for now.")

elif selected == "Neural Architect":
    st.title("🏗️ Neural Architect")
    
    if not pollinations_key:
        st.error("Please click 'CONNECT POLLINATIONS' in the sidebar first!")
    else:
        user_idea = st.text_input("What should I build?", placeholder="e.g. Cyberpunk Space Station")
        
        if st.button("EXECUTE RENDER"):
            if user_idea:
                with st.spinner("Decoding Neural Pathways..."):
                    try:
                        # 1. GENERATE THE HACKER CODE (Using 2026 gen.pollinations.ai text endpoint)
                        # We use 'openai-fast' model for quick text generation
                        text_prompt = f"Write 150 words of complex-looking HTML/CSS code for a futuristic UI about {user_idea}. No preamble, just code."
                        text_api_url = f"https://gen.pollinations.ai/text/{text_prompt.replace(' ', '%20')}?model=openai-fast"
                        
                        text_res = requests.get(text_api_url, timeout=15)
                        matrix_text = text_res.text if text_res.status_code == 200 else "SYSTEM_DECODING_FAILURE"

                        # 2. GENERATE THE IMAGE (Using 2026 gen.pollinations.ai image endpoint)
                        clean_idea = user_idea.replace(" ", "%20")
                        # Adding seed and model=flux for the highest quality 2026 render
                        image_url = f"https://gen.pollinations.ai/image/{clean_idea}?width=1024&height=1024&nologo=true&model=flux&key={pollinations_key}"
                        
                        # --- THE GREEN SCROLLING BOX ---
                        st.markdown(f"""
                        <div style="border: 2px solid #28a745; padding: 20px; border-radius: 10px; background-color: rgba(40, 167, 69, 0.05); height: 280px; overflow-y: scroll; margin-bottom: 25px;">
                            <p style="color: #28a745; font-family: monospace; font-weight: bold; margin-bottom: 5px;">NEXUS_POLLINATIONS_DECODED:</p>
                            <pre style="color: #28a745; font-size: 11px; white-space: pre-wrap; font-family: 'Courier New', monospace;">{matrix_text}</pre>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # 3. DISPLAY THE IMAGE
                        st.image(image_url, caption=f"Visual Render by {CREATOR}")
                        
                    except Exception as e:
                        st.error(f"Architect Connection Lost. Please check your internet or try again.")
            else:
                st.warning("Please enter a description first!")

elif selected == "Share Hub":
    st.title("🌐 Share Hub")
    st.markdown(f"**NEXUS Network by {CREATOR}**")
    st.markdown("""
        <div style="display: flex; gap: 20px; margin-top: 10px;">
            <a href="https://wa.me/" target="_blank">WhatsApp</a> | 
            <a href="https://instagram.com/" target="_blank">Instagram</a>
        </div>
    """, unsafe_allow_html=True)
