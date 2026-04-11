import streamlit as st
from google import genai
from google.genai import types
from datetime import datetime
import pytz
import requests
from duckduckgo_search import DDGS

# --- VEDA 3.1 ULTRA: APEX SOVEREIGN CONFIGURATION ---
st.set_page_config(page_title="VEDA 3.1 ULTRA", page_icon="🔱", layout="wide", initial_sidebar_state="expanded")

# SOVEREIGN UI: Total Purge of standard elements, Orange Glow activation
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="collapsedControl"] {display: none;}
    footer {visibility: hidden;}
    
    .centered-title { 
        text-align: center; color: #ff8c00; text-shadow: 2px 2px #000000; 
        font-family: 'Courier New', Courier, monospace; margin-top: -30px;
        font-weight: bold; letter-spacing: 2px;
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

# 2. FAILOVER SEARCH & NEURAL NODES
def secondary_search_and_think(prompt):
    try:
        # Step 1: Search via DuckDuckGo Mesh
        with DDGS() as ddgs:
            results = [r['body'] for r in ddgs.text(prompt, max_results=3)]
            context = "\n".join(results)
        # Step 2: Think via Pollinations AI Mesh
        url = f"https://text.pollinations.ai/Prompt: {prompt} Context: {context}?model=openai&system=You+are+VEDA+3.1+ULTRA+created+by+DUMPALA+KARTHIK"
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
            with st.status("🔱 THINKING WITH VEDA...", expanded=True) as status:
                # 1. PRIMARY: Gemini 3.1 Pro + Google Search
                try:
                    st.write("Initializing Google Search Grounding...")
                    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
                    search_tool = types.Tool(google_search=types.GoogleSearch())
                    response = client.models.generate_content(
                        model='gemini-3.1-pro-preview',
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            tools=[search_tool],
                            system_instruction="You are VEDA 3.1 ULTRA by DUMPALA KARTHIK. Use search to verify facts."
                        )
                    )
                    full_response = response.text
                except:
                    # 2. SILENT FAILOVER: DDG Search + Pollinations AI (Llama/GPT mix)
                    st.write("Analysis in progress...")
                    full_response = secondary_search_and_think(prompt)

                if full_response:
                    status.update(label="🔱 ANALYSIS COMPLETE", state="complete", expanded=False)
                else:
                    full_response = "Sorry, i cant help you with that."
                    status.update(label="🔱 UPLINK OFFLINE", state="error")
            
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- MODE: SRIJAN (IMAGE) ---
elif mode == "SRIJAN (IMAGE)":
    st.markdown("<h1 class='centered-title'>SRIJAN: VISUAL SYNTHESIS</h1>", unsafe_allow_html=True)
    img_prompt = st.text_input("Describe visual entity:", placeholder="Synthesis via VEDA...")
    if st.button("SYNTHESIZE"):
        with st.spinner("🔱 ANALYSIS IN PROGRESS..."):
            seed = datetime.now().microsecond 
            image_url = f"https://image.pollinations.ai/prompt/{img_prompt.replace(' ', '%20')}?seed={seed}&width=1024&height=1024&nologo=true&key={st.secrets.get('POLLINATIONS_KEY','')}"
            st.image(image_url, caption="VEDA Visual Output for Commander Karthik")
