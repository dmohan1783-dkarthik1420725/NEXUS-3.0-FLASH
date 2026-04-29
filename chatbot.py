import streamlit as st
from google import genai
import requests
from duckduckgo_search import DDGS
import random

# --- 1. SOVEREIGN UI ENGINE ---
st.set_page_config(page_title="VEDA 3.1 ULTRA", page_icon="🔱", layout="wide")

st.markdown("""
<style>
    .stApp {
        background-color: #0a0c10;
        background-image: 
            linear-gradient(rgba(255, 140, 0, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 140, 0, 0.05) 1px, transparent 1px);
        background-size: 60px 60px;
    }
    .hub-title { color: #ff8c00; font-size: 24px; font-family: 'Courier New', monospace; text-align: center; }
    .welcome-msg { color: #ff8c00; font-size: 36px; font-weight: bold; text-align: center; margin-bottom: 40px; }
    .stChatInput { border: 1px solid #ff8c00 !important; border-radius: 25px !important; }
</style>
""", unsafe_allow_html=True)

# --- 2. CORE LOGIC: GEMINI & POLLINATIONS ---
def generate_image(prompt):
    seed = random.randint(0, 999999)
    # Using Pollinations AI via Streamlit Secrets (if configured) or direct link
    image_url = f"https://pollinations.ai/p/{prompt.replace(' ', '_')}?seed={seed}&width=1024&height=1024&model=flux"
    return image_url

def veda_brain_router(prompt):
    model_id = "gemini-1.5-flash" if st.session_state.get("mode") == "FAST" else "gemini-1.5-pro"
    try:
        # Drawing Gemini API Key from Secrets
        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
        web_context = ""
        if st.session_state.get("mode") in ["PRO", "ULTRA"]:
            with DDGS() as ddgs:
                web_context = "\n".join([r['body'] for r in ddgs.text(prompt, max_results=3)])
        
        response = client.models.generate_content(
            model=model_id,
            contents=f"Identity: VEDA 3.1 ULTRA. Context: {web_context}\nUser: {prompt}"
        )
        return response.text
    except Exception as e:
        return f"🔱 NEURAL GAP: {str(e)}"

# --- 3. UI LAYOUT ---
if "messages" not in st.session_state: st.session_state.messages = []

# Medha Hub Display
if not st.session_state.messages:
    st.markdown('<p class="hub-title">VEDA 3.1 ULTRA</p>', unsafe_allow_html=True)
    st.markdown('<h1 class="welcome-msg">MEDHA HUB: WELCOME, COMMANDER.</h1>', unsafe_allow_html=True)

# Chat Interface
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Command the Ghost Mesh..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    
    with st.chat_message("assistant"):
        if "imagine" in prompt.lower() or "create image" in prompt.lower():
            img_url = generate_image(prompt)
            st.image(img_url, caption="🔱 VEDA VISUAL SYNTHESIS")
            st.session_state.messages.append({"role": "assistant", "content": f"Image generated for: {prompt}"})
        else:
            ans = veda_brain_router(prompt)
            st.markdown(f"🔱 {ans}")
            st.session_state.messages.append({"role": "assistant", "content": ans})