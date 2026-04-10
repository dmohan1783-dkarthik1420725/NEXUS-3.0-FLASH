import streamlit as st
from google import genai
from google.genai import types
from datetime import datetime
import pytz

# --- VEDA 3.0 ULTRA: SOVEREIGN CONFIGURATION ---
st.set_page_config(page_title="VEDA 3.0 ULTRA", page_icon="🔱", layout="wide")

# Elite CSS for UI centering, Sovereign Aesthetics, and ORANGE Text
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stTextInput>div>div>input { background-color: #262730; color: white; border: 1px solid #ff4b2b; }
    /* Centered Title with Orange Thermal Effect */
    .centered-title { 
        text-align: center; 
        color: #ff8c00; 
        text-shadow: 2px 2px #000000; 
        font-family: 'Courier New', Courier, monospace; 
        margin-top: -50px;
        font-weight: bold;
        letter-spacing: 2px;
    }
    </style>
    """, unsafe_allow_html=True)

# 1. SIDEBAR: THE TRISHUL MESH
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #ff8c00;'>🔱</h1>", unsafe_allow_html=True)
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
    # Key must be stored in Streamlit Cloud Secrets as GOOGLE_API_KEY
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    st.sidebar.error("❌ Key Uplink Failed")

# --- MODE: MEDHA (CHAT & SEARCH) ---
if mode == "MEDHA (CHAT)":
    # Centered Title in ORANGE
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
            
            with st.status("🔱 THINKING WITH VEDA...", expanded=True) as status:
                if client is None:
                    full_response = "❌ UPLINK FAILED: Check Secrets for GOOGLE_API_KEY."
                    status.update(label="🔱 SECURITY ERROR", state="error")
                else:
                    try:
                        st.write("Accessing 2026 Search Mesh...")
                        search_tool = types.Tool(google_search=types.GoogleSearch())
                        response = client.models.generate_content(
                            model='gemini-2.0-flash', 
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
            
            if response and response.candidates and response.candidates[0].grounding_metadata:
                with st.expander("📡 Verified Search Sources"):
                    search_meta = response.candidates[0].grounding_metadata.search_entry_point
                    if search_meta:
                        st.html(search_meta.rendered_content)

# --- MODE: SRIJAN (IMAGE GENERATION) ---
elif mode == "SRIJAN (IMAGE)":
    # Centered Title in ORANGE
    st.markdown("<h1 class='centered-title'>SRIJAN: VISUAL SYNTHESIS</h1>", unsafe_allow_html=True)
    
    img_prompt = st.text_input("Describe visual entity for synthesis:", placeholder="e.g., A cybernetic city in Hyderabad 2026...")
    
    if st.button("SYNTHESIZE IMAGE"):
        if img_prompt:
            with st.spinner("🔱 SRIJAN IS CONSTRUCTING VISUAL DATA..."):
                p_key = st.secrets.get("POLLINATIONS_KEY", "")
                seed = datetime.now().microsecond 
                image_url = f"https
