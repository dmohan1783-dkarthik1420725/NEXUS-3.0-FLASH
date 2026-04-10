import streamlit as st
from google import genai
from google.genai import types
from datetime import datetime
import pytz

# --- VEDA 3.0 ULTRA: SOVEREIGN CONFIGURATION ---
st.set_page_config(page_title="VEDA 3.0 ULTRA", page_icon="🔱", layout="wide")

# Elite CSS for UI centering and Sovereign Aesthetics
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stTextInput>div>div>input { background-color: #262730; color: white; border: 1px solid #00d4ff; }
    .centered-title { text-align: center; color: #00d4ff; text-shadow: 2px 2px #000000; font-family: 'Courier New', Courier, monospace; }
    </style>
    """, unsafe_allow_html=True)

# 1. SIDEBAR: THE TRISHUL MESH
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #00d4ff;'>🔱</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>VEDA 3.0 ULTRA</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Live Telemetry
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    st.write(f"📅 **Date:** {now.strftime('%Y-%m-%d')}")
    st.write(f"⌚ **Time:** {now.strftime('%H:%M:%S')} IST")
    st.write("📍 **Station:** Hyderabad")
    st.markdown("---")
    
    # Mode Selection
    mode = st.radio("SELECT MODE:", ["MEDHA (CHAT)", "SRIJAN (IMAGE)"])
    st.markdown("---")
    st.caption("Developed by DUMPALA KARTHIK")

# 2. CORE BRAIN INITIALIZATION
client = None
try:
    if "GEMINI_API_KEY" in st.secrets:
        API_KEY = st.secrets["GEMINI_API_KEY"]
        client = genai.Client(api_key=API_KEY)
except Exception:
    client = None

# --- MODE: MEDHA (CHAT & SEARCH) ---
if mode == "MEDHA (CHAT)":
    # Centered Title as Commanded
    st.markdown("<h1 class='centered-title'>VEDA: INTELLIGENCE HUB</h1>", unsafe_allow_html=True)
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Command Medha..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = None
            full_response = ""
            
            with st.status("🔱 VEDA IS ANALYZING THE MESH...", expanded=True) as status:
                if client is None:
                    full_response = "❌ UPLINK FAILED: API Key missing in Streamlit Secrets. Access denied."
                    status.update(label="🔱 SECURITY ERROR", state="error")
                else:
                    try:
                        search_tool = types.Tool(google_search=types.GoogleSearch())
                        response = client.models.generate_content(
                            model='gemini-1.5-pro',
                            contents=prompt,
                            config=types.GenerateContentConfig(tools=[search_tool])
                        )
                        full_response = response.text
                        status.update(label="🔱 ANALYSIS COMPLETE", state="complete", expanded=False)
                    except Exception as e:
                        full_response = f"⚠️ Uplink Error: {str(e)}"
                        status.update(label="🔱 MESH ERROR", state="error")
            
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
            # Safe Grounding Check to prevent NameError
            if response and hasattr(response, 'candidates') and response.candidates[0].grounding_metadata:
                with st.expander("📡 Verified Search Sources"):
                    search_meta = response.candidates[0].grounding_metadata.search_entry_point
                    if search_meta:
                        st.html(search_meta.rendered_content)

# --- MODE: SRIJAN (IMAGE GENERATION via POLLINATIONS) ---
elif mode == "SRIJAN (IMAGE)":
    st.markdown("<h1 class='centered-title'>SRIJAN: VISUAL SYNTHESIS</h1>", unsafe_allow_html=True)
    
    img_prompt = st.text_input("Describe visual entity for synthesis:", placeholder="e.g., A cybernetic Trishul in deep space...")
    
    if st.button("SYNTHESIZE IMAGE"):
        if img_prompt:
            with st.spinner("🔱 SRIJAN IS CONSTRUCTING VISUAL DATA..."):
                seed = datetime.now().microsecond 
                image_url = f"https://image.pollinations.ai/prompt/{img_prompt.replace(' ', '%20')}?seed={seed}&width=1024&height=1024&nologo=true"
                st.image(image_url, caption=f"VEDA Synthesis: {img_prompt}", use_container_width=True)
                st.success("🔱 Visual Reconstruction Complete.")
