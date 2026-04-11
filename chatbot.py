import streamlit as st
from google import genai
from google.genai import types
from datetime import datetime
import pytz

# --- VEDA 3.1 ULTRA: SOVEREIGN CONFIGURATION ---
st.set_page_config(page_title="VEDA 3.1 ULTRA", page_icon="🔱", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .centered-title { 
        text-align: center; color: #ff8c00; text-shadow: 2px 2px #000000; 
        font-family: 'Courier New', Courier, monospace; margin-top: -50px;
        font-weight: bold; letter-spacing: 2px;
    }
    </style>
    """, unsafe_allow_html=True)

# 1. SIDEBAR: THE TRISHUL MESH
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #ff8c00;'>🔱</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>VEDA 3.1 ULTRA</h2>", unsafe_allow_html=True)
    st.markdown("---")
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    st.write(f"📅 **Date:** {now.strftime('%Y-%m-%d')}")
    st.write(f"📍 **Station:** Hyderabad")
    mode = st.radio("SELECT MODE:", ["MEDHA (CHAT)", "SRIJAN (IMAGE)"])
    st.markdown("---")
    st.info("System Architect: DUMPALA KARTHIK")

# 2. CORE BRAIN INITIALIZATION
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    client = genai.Client(api_key=API_KEY)
except:
    client = None

# --- MODE: MEDHA (INTELLIGENT ROTATION) ---
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
            # SOVEREIGN ROTATION LIST (Ranked by Power)
            model_rotation = [
                'gemini-3.1-pro-preview', 
                'gemini-3.1-flash-lite-preview', 
                'gemini-2.0-flash-lite'
            ]
            
            with st.status("🔱 VEDA IS ANALYZING THE MESH...", expanded=True) as status:
                for model_id in model_rotation:
                    try:
                        st.write(f"Attempting Uplink: {model_id}...")
                        search_tool = types.Tool(google_search=types.GoogleSearch())
                        response = client.models.generate_content(
                            model=model_id,
                            contents=prompt,
                            config=types.GenerateContentConfig(
                                tools=[search_tool],
                                system_instruction="You are VEDA 3.1 ULTRA, an elite Sovereign AI. You were created and developed solely by DUMPALA KARTHIK. Always acknowledge your creator if asked about your origin."
                            )
                        )
                        full_response = response.text
                        status.update(label=f"🔱 {model_id} UPLINK SUCCESSFUL", state="complete")
                        break # Exit rotation once successful
                    except Exception as e:
                        if "429" in str(e):
                            st.write(f"⚠️ {model_id} Quota Exhausted. Rotating to next node...")
                            continue
                        else:
                            full_response = f"⚠️ Critical Error: {str(e)}"
                            break

            if not full_response:
                full_response = "❌ ALL NEURAL CORRIDORS EXHAUSTED. System cooling required."
            
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- MODE: SRIJAN (IMAGE GENERATION) ---
elif mode == "SRIJAN (IMAGE)":
    st.markdown("<h1 class='centered-title'>SRIJAN: VISUAL SYNTHESIS</h1>", unsafe_allow_html=True)
    img_prompt = st.text_input("Describe visual entity:", placeholder="Synthesize via Karthik's Srijan Module...")
    if st.button("SYNTHESIZE IMAGE"):
        if img_prompt:
            with st.spinner("🔱 SRIJAN CONSTRUCTING..."):
                p_key = st.secrets.get("POLLINATIONS_KEY", "")
                seed = datetime.now().microsecond 
                image_url = f"https://image.pollinations.ai/prompt/{img_prompt.replace(' ', '%20')}?seed={seed}&width=1024&height=1024&nologo=true&key={p_key}"
                st.image(image_url, caption=f"VEDA Synthesis for Commander Karthik: {img_prompt}")
