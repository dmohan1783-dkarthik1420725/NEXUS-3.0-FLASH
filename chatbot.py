import streamlit as st
from google import genai
from google.genai import types
from datetime import datetime
import pytz
from duckduckgo_search import DDGS # Sovereign Backup Mesh

# --- VEDA 3.0 ULTRA: SOVEREIGN CONFIGURATION ---
st.set_page_config(page_title="VEDA 3.0 ULTRA", page_icon="🔱", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stTextInput>div>div>input { background-color: #262730; color: white; border: 1px solid #ff4b2b; }
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
    st.markdown("<h2 style='text-align: center;'>VEDA 3.0 ULTRA</h2>", unsafe_allow_html=True)
    st.markdown("---")
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    st.write(f"📅 **Date:** {now.strftime('%Y-%m-%d')}")
    st.write(f"⌚ **Time:** {now.strftime('%H:%M:%S')} IST")
    st.write("📍 **Station:** Hyderabad")
    mode = st.radio("SELECT MODE:", ["MEDHA (CHAT)", "SRIJAN (IMAGE)"])
    st.caption("Developed by DUMPALA KARTHIK")

# 2. CORE BRAIN INITIALIZATION
client = None
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    client = genai.Client(api_key=API_KEY)
except:
    client = None

# --- MODE: MEDHA (CHAT & SEARCH) ---
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
            response = None
            full_response = ""
            
            with st.status("🔱 THINKING WITH VEDA...", expanded=True) as status:
                try:
                    st.write("Checking Primary Orbital Mesh...")
                    search_tool = types.Tool(google_search=types.GoogleSearch())
                    response = client.models.generate_content(
                        model='gemini-2.0-flash', 
                        contents=prompt,
                        config=types.GenerateContentConfig(tools=[search_tool])
                    )
                    full_response = response.text
                    status.update(label="🔱 PRIMARY UPLINK SUCCESSFUL", state="complete", expanded=False)
                
                except Exception as e:
                    if "429" in str(e):
                        st.write("⚠️ Quota Exhausted. Switching to Secondary Search Mesh...")
                        # FAILOVER TO DUCKDUCKGO
                        try:
                            with DDGS() as ddgs:
                                results = [r['body'] for r in ddgs.text(prompt, max_results=3)]
                                context = "\n".join(results)
                                # Try to generate without search tool to save quota
                                response = client.models.generate_content(
                                    model='gemini-2.0-flash',
                                    contents=f"Context: {context}\n\nUser Question: {prompt}\n\nAnalyze using the provided context."
                                )
                                full_response = response.text
                                status.update(label="🔱 SECONDARY MESH ACTIVE", state="complete", expanded=False)
                        except:
                            full_response = "❌ ALL MESHES EXHAUSTED. Retry in 60 seconds."
                            status.update(label="🔱 UPLINK OFFLINE", state="error")
                    else:
                        full_response = f"⚠️ Error: {str(e)}"
                        status.update(label="🔱 MESH ERROR", state="error")
            
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- MODE: SRIJAN (IMAGE GENERATION) ---
elif mode == "SRIJAN (IMAGE)":
    st.markdown("<h1 class='centered-title'>SRIJAN: VISUAL SYNTHESIS</h1>", unsafe_allow_html=True)
    img_prompt = st.text_input("Describe visual entity:", placeholder="e.g., A cybernetic Trishul...")
    if st.button("SYNTHESIZE IMAGE"):
        if img_prompt:
            with st.spinner("🔱 SRIJAN ANALYIZING..."):
                p_key = st.secrets.get("POLLINATIONS_KEY", "")
                seed = datetime.now().microsecond 
                image_url = f"https://image.pollinations.ai/prompt/{img_prompt.replace(' ', '%20')}?seed={seed}&width=1024&height=1024&nologo=true&key={p_key}"
                st.image(image_url, caption=f"VEDA Synthesis: {img_prompt}", use_container_width=True)
