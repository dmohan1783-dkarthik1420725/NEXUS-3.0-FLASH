import streamlit as st
import requests
import random
from datetime import datetime

# --- VEDA 3.1 ULTRA: SONIC FREEDOM CONFIGURATION ---
st.set_page_config(page_title="VEDA 3.1 ULTRA", page_icon="🔱", layout="wide")

st.markdown("""
<style>
.main { background-color: #0e1117; color: #ffffff; }
.centered-title { 
    text-align: center; color: #ff8c00; text-shadow: 2px 2px #000000; 
    font-family: 'Courier New', Courier, monospace; margin-top: -30px;
    font-weight: bold; letter-spacing: 2px;
}
.wip-text {
    color: #ff8c00; font-family: 'Courier New', Courier, monospace;
    font-weight: bold; border: 1px solid #ff8c00; padding: 15px;
    text-align: center; border-radius: 5px; background: rgba(255, 140, 0, 0.1);
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# 1. SIDEBAR STATION
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #ff8c00;'>🔱</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>VEDA 3.1 ULTRA</h2>", unsafe_allow_html=True)
    st.markdown("---")
    mode = st.radio("SELECT MODE:", ["SANGEET (MUSIC MAKER)", "MEDHA (CHAT)", "SRIJAN (IMAGE)"])
    st.info("ARCHITECT: DUMPALA KARTHIK")

# --- MODE: SANGEET (FREE MUSIC MAKER) ---
if mode == "SANGEET (MUSIC MAKER)":
    st.markdown("<h1 class='centered-title'>SANGEET: SONIC ARCHITECT</h1>", unsafe_allow_html=True)
    
    # Free AI Music Input
    audio_prompt = st.text_input("Describe the music you want (e.g., 'Heavy Bass Phonk', 'Cyberpunk Synth', 'Indian Lo-fi'):")
    
    if st.button("MANIFEST SONIC MESH"):
        if audio_prompt:
            # WORK IN PROGRESS ALERT
            wip_placeholder = st.empty()
            wip_placeholder.markdown("<div class='wip-text'>🔱 WORK IN PROGRESS. PLEASE WAIT FOR 1-2 MINS...</div>", unsafe_allow_html=True)
            
            try:
                # Using the Free Pollinations Audio API
                # This generates a 30-60 second AI music track based on the prompt
                seed = random.randint(0, 1000000)
                audio_url = f"https://text.pollinations.ai/prompt/{audio_prompt.replace(' ', '%20')}?model=audio&seed={seed}"
                
                # Render the Audio Player
                st.audio(audio_url, format="audio/wav")
                st.success("🔱 Sangeet sequence complete.")
                
            except Exception as e:
                st.error("Neural Link Interrupted. Try again.")
            
            wip_placeholder.empty()
        else:
            st.warning("Please enter a sonic description.")

# --- MODE: MEDHA (CHAT) ---
elif mode == "MEDHA (CHAT)":
    st.markdown("<h1 class='centered-title'>MEDHA: INTELLIGENCE</h1>", unsafe_allow_html=True)
    if prompt := st.chat_input("Command Medha..."):
        # Simple free fallback chat logic
        url = f"https://text.pollinations.ai/{prompt}?model=openai"
        response = requests.get(url).text
        with st.chat_message("assistant"):
            st.markdown(response)

# --- MODE: SRIJAN (IMAGE) ---
elif mode == "SRIJAN (IMAGE)":
    st.markdown("<h1 class='centered-title'>SRIJAN: VISUAL FORGE</h1>", unsafe_allow_html=True)
    img_prompt = st.text_input("Describe visual:")
    if st.button("SYNTHESIZE"):
        img_url = f"https://image.pollinations.ai/prompt/{img_prompt.replace(' ', '%20')}?nologo=true"
        st.image(img_url)
