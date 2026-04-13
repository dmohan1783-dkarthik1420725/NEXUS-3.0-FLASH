import streamlit as st
import google.generativeai as genai
import random

# --- VEDA OS CORE CONFIG ---
st.set_page_config(page_title="VEDA 3.1 ULTRA", page_icon="🔱", layout="wide")

# --- NEURAL LINK (GEMINI) ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-pro')
else:
    st.error("🔱 SYSTEM ERROR: Neural Link API Key Missing.")

# --- SESSION SETUP ---
if 'step' not in st.session_state:
    st.session_state.step = 'details'

# --- SOVEREIGN UI ---
st.markdown("""
    <style>
    .stApp { background-color: #0a0a0a; color: #e0e0e0; }
    .title { text-align: center; color: #ff8c00; font-size: 60px; font-weight: bold; text-shadow: 2px 2px #000; }
    .module-card { background: #111; border: 1px solid #ff8c00; padding: 20px; border-radius: 15px; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='title'>VEDA 3.1 ULTRA</div>", unsafe_allow_html=True)

# --- PHASE 1: IDENTITY GATE ---
if st.session_state.step == 'details':
    with st.form("identity_gate"):
        st.subheader("🔱 Sovereign Identity Provisioning")
        col1, col2 = st.columns(2)
        with col1:
            fn = st.text_input("First Name")
            age = st.number_input("Age", min_value=1, value=18)
        with col2:
            ln = st.text_input("Last Name")
            parent = st.text_input("Parent Veda ID (If < 18)")
            
        if st.form_submit_button("ACTIVATE MESH"):
            if fn and ln:
                if age < 18 and not parent:
                    st.error("Guardian Handshake Required.")
                else:
                    st.session_state.id = f"{fn[0].lower()}{ln.lower()}{random.randint(1000,9999)}@veda.com"
                    st.session_state.user = f"{fn} {ln}"
                    st.session_state.step = 'active'
                    st.rerun()

# --- PHASE 2: SOVEREIGN COMMAND CENTER ---
elif st.session_state.step == 'active':
    st.sidebar.markdown(f"**ID:** {st.session_state.id}")
    st.sidebar.write(f"**Commander:** {st.session_state.user}")
    
    tab1, tab2, tab3 = st.tabs(["🧠 MEDHA (AI)", "🎵 SANGEET (Music)", "🎬 DRISHYAM (Video)"])

    # --- MEDHA: AI SEARCH ---
    with tab1:
        st.markdown("<div class='module-card'>", unsafe_allow_html=True)
        query = st.text_input("Command the Neural Mesh...", key="ai_q")
        if query:
            response = model.generate_content(query)
            st.info(f"🔱 VEDA: {response.text}")
        st.markdown("</div>", unsafe_allow_html=True)

    # --- SANGEET: MUSIC GENERATION ---
    with tab2:
        st.markdown("<div class='module-card'>", unsafe_allow_html=True)
        st.subheader("🎵 SANGEET Module")
        music_prompt = st.text_input("Describe the Veda Rhythm (e.g., Heavy Bass Phonk)...")
        if st.button("GENERATE TRACK"):
            st.write(f"🔱 SANGEET is composing: {music_prompt}...")
            st.warning("Note: Lyria 3 Integration is processing the audio frequencies.")
            # For now, it simulates the generation. Real audio requires the API hookup.
            st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3") 
        st.markdown("</div>", unsafe_allow_html=True)

    # --- DRISHYAM: VIDEO GENERATION ---
    with tab3:
        st.markdown("<div class='module-card'>", unsafe_allow_html=True)
        st.subheader("🎬 DRISHYAM Module")
        video_prompt = st.text_input("Describe the Visual Synthesis...")
        if st.button("SYNTHESIZE VIDEO"):
            st.write(f"🔱 DRISHYAM is rendering: {video_prompt}...")
            st.warning("Veo Model initializing visual corridors...")
            # Visual placeholder
            st.video("https://www.w3schools.com/html/mov_bbb.mp4")
        st.markdown("</div>", unsafe_allow_html=True)

    if st.sidebar.button("Logout"):
        st.session_state.step = 'details'
        st.rerun()
