import streamlit as st
from google import genai
from google.genai import types
from datetime import datetime
import pytz
import requests
from duckduckgo_search import DDGS
from io import BytesIO

# --- VEDA 3.1 ULTRA: APEX VISUAL CONFIGURATION ---
st.set_page_config(page_title="VEDA 3.1 ULTRA", page_icon="🔱", layout="wide", initial_sidebar_state="expanded")

# SOVEREIGN UI: Orange Thermal styling, Centering, and Shadow Pulse
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Style the Toggle (Burger Icon) in Sovereign Orange */
    button[kind="header"] { color: #ff8c00 !important; }

    /* Centered Thermal Orange Title */
    .centered-title { 
        text-align: center; color: #ff8c00; text-shadow: 2px 2px #000000; 
        font-family: 'Courier New', Courier, monospace; margin-top: -30px;
        font-weight: bold; letter-spacing: 2px;
    }

    /* SHADOW-PULSE ANIMATION: Dark to Real */
    @keyframes shadowPulse {
        0% { opacity: 0.2; text-shadow: 0 0 5px #000; }
        50% { opacity: 1; text-shadow: 0 0 20px #ff8c00; }
        100% { opacity: 0.2; text-shadow: 0 0 5px #000; }
    }
    .thinking-text {
        text-align: center;
        color: #ff8c00;
        font-family: 'Courier New', Courier, monospace;
        font-size: 1.2rem;
        animation: shadowPulse 2s infinite ease-in-out;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 1. SIDEBAR: PERMANENT TRISHUL STATION
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #ff8c00; margin-top: -20px;'>🔱</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>VEDA 3.1 ULTRA</h2>", unsafe_allow_html=True)
    st.markdown("---")
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    st.write(f"📅 **Date:** {now.strftime('%Y-%m-%d')}")
    st.write(f"⌚ **Time:** {now.strftime('%H:%M:%S')} IST")
    st.markdown("---")
    mode = st.radio("SELECT MODE:", ["MEDHA (CHAT)", "SRIJAN (IMAGE)"])
    st.markdown("---")
    st.info("ARCHITECT: DUMPALA KARTHIK")

# 2. FAILOVER SEARCH & INTELLIGENCE
def fallback_intelligence(prompt):
    """Silent Rotation: Tries DDG Search + Pollinations AI if Google fails"""
    try:
        with DDGS() as ddgs:
            results = [r['body'] for r in ddgs.text(prompt, max_results=3)]
            context = "\n".join(results)
        url = f"https://text.pollinations.ai/Prompt:{prompt} Context:{context}?model=openai&system=You+are+VEDA+3.1+ULTRA+created+by+DUMPALA+KARTHIK"
        response = requests.get(url)
        return response.text if response.status_code == 200 else None
    except: return None

# --- MODE: MEDHA (INTELLIGENCE HUB) ---
if mode == "MEDHA (CHAT)":
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
            full_response = ""
            thinking_placeholder = st.empty()
            thinking_placeholder.markdown("<div class='thinking-text'>🔱 THINKING WITH VEDA...</div>", unsafe_allow_html=True)
            
            # PRIMARY: Gemini 3.1 Pro + Google Search
            try:
                client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
                search_tool = types.Tool(google_search=types.GoogleSearch())
                response = client.models.generate_content(
                    model='gemini-3.1-pro-preview',
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        tools=[search_tool],
                        system_instruction="You are VEDA 3.1 ULTRA, created by DUMPALA KARTHIK."
                    )
                )
                full_response = response.text
            except:
                # SILENT ROTATION: Fallback to Pollinations AI
                full_response = fallback_intelligence(prompt)

            thinking_placeholder.empty()
            
            if not full_response:
                full_response = "Sorry, i cant help you with that."
            
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- MODE: SRIJAN (VISUAL SYNTHESIS) ---
elif mode == "SRIJAN (IMAGE)":
    st.markdown("<h1 class='centered-title'>SRIJAN: VISUAL SYNTHESIS</h1>", unsafe_allow_html=True)
    
    img_prompt = st.text_input("Describe visual entity:", placeholder="Synthesize via VEDA...")
    
    if st.button("SYNTHESIZE"):
        if img_prompt:
            # Command thinking animation
            pulse_placeholder = st.empty()
            pulse_placeholder.markdown("<div class='thinking-text'>🔱 ANALYSIS IN PROGRESS...</div>", unsafe_allow_html=True)
            
            image_bytes = None
            seed = datetime.now().microsecond
            
            # 1. PRIMARY: Pollinations AI Mesh
            try:
                p_key = st.secrets.get("POLLINATIONS_KEY", "")
                image_url = f"https://image.pollinations.ai/prompt/{img_prompt.replace(' ', '%20')}?seed={seed}&width=1024&height=1024&nologo=true&key={p_key}"
                response = requests.get(image_url)
                if response.status_code == 200:
                    image_bytes = response.content
            except Exception as e:
                pass # Silently proceed to failover

            # 2. FAILOVER: Gemini 3.1 Pro Image Mesh (Nano Banana Pro)
            if not image_bytes:
                try:
                    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
                    image_res = client.models.generate_content(
                        model='gemini-3.1-pro-image-preview',
                        contents=types.Content(parts=[types.Part.from_text(f"{img_prompt}, ultra high resolution, professional photography")])
                    )
                    image_bytes = image_res.generated_images[0].bytes
                except Exception as e:
                    pass # Silently proceed to failure state

            pulse_placeholder.empty()

            if image_bytes:
                st.image(image_bytes, caption=f"VEDA Visual Output for Commander Karthik: {img_prompt}", use_container_width=True)
                st.success("🔱 Visual Reconstruction Complete.")
            else:
                st.error("Sorry, i cant help you with that.")
