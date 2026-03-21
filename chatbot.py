import streamlit as st
import requests  # Added to talk to Pollinations Text API
from streamlit_option_menu import option_menu

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="NEXUS 3.0 ULTRA", page_icon="⚡", layout="wide")
CREATOR = "Dumpala Karthik"

# --- SMART KEY LOGIC ---
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

    st.divider()
    selected = option_menu("Main Systems", ["Intelligence", "Neural Architect", "Share Hub"], 
                          icons=["cpu", "layers", "share"], default_index=1)

# --- 3. MAIN INTERFACE ---

if selected == "Intelligence":
    st.info("Intelligence (Gemini) requires a Google API Key in Secrets. Use Neural Architect for Pollinations power.")

elif selected == "Neural Architect":
    st.title("🏗️ Neural Architect")
    if not pollinations_key:
        st.error("Please CONNECT in the sidebar first to use Pollinations.")
    else:
        user_idea = st.text_input("What should I build?", placeholder="e.g. Cyberpunk City")
        
        if st.button("EXECUTE RENDER"):
            with st.spinner("Pollinating Neural Pathways..."):
                try:
                    # 1. GENERATE THE HACKER CODE (Using Pollinations Text API)
                    # We ask Pollinations to act as a coder
                    text_prompt = f"Write 150 words of complex-looking, futuristic HTML and CSS code for a UI about {user_idea}. No talking, just code."
                    text_url = f"https://text.pollinations.ai/{text_prompt.replace(' ', '%20')}"
                    
                    text_response = requests.get(text_url)
                    matrix_text = text_response.text if text_response.status_code == 200 else "CODE_DECODING_ERROR"

                    # 2. GENERATE THE IMAGE (Using Pollinations Image API)
                    clean_idea = user_idea.replace(" ", "%20")
                    image_url = f"https://gen.pollinations.ai/image/{clean_idea}?width=1024&height=1024&nologo=true&key={pollinations_key}"
                    
                    # --- THE GREEN SCROLLING BOX ---
                    st.markdown(f"""
                    <div style="border: 2px solid #28a745; padding: 20px; border-radius: 10px; background-color: rgba(40, 167, 69, 0.05); height: 250px; overflow-y: scroll; margin-bottom: 20px;">
                        <p style="color: #28a745; font-family: monospace; font-weight: bold; margin-bottom: 5px;">NEXUS_POLLINATIONS_DECODED:</p>
                        <pre style="color: #28a745; font-size: 11px; white-space: pre-wrap; font-family: 'Courier New', monospace;">{matrix_text}</pre>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # 3. DISPLAY THE IMAGE
                    st.image(image_url, caption=f"Visual Render by {CREATOR}")
                
                except Exception as e:
                    st.error("Pollinations Connection Timed Out. Please try again.")

elif selected == "Share Hub":
    st.title("🌐 Share Hub")
    st.markdown(f"**NEXUS Network by {CREATOR}**")
    st.markdown("""
        <div style="display: flex; gap: 20px;">
            <a href="https://wa.me/" target="_blank">WhatsApp</a>
            <a href="https://instagram.com/" target="_blank">Instagram</a>
        </div>
    """, unsafe_allow_html=True)
