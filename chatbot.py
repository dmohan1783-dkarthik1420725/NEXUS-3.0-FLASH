import streamlit as st
from google import genai
import requests
import urllib.parse
from datetime import datetime
import pytz
from streamlit_option_menu import option_menu

# --- 1. CONFIGURATION & IDENTITY ---
st.set_page_config(page_title="VEDA 3.0 ULTRA", page_icon="🔱", layout="wide")
CREATOR = "Dumpala Karthik"

ist = pytz.timezone('Asia/Kolkata')
def get_now_time():
    return datetime.now(ist).strftime("%I:%M %p")

IDENTITY = f"Your name is VEDA 3.0 ULTRA. Created by {CREATOR}."

# --- 2. SESSION STATE ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- 3. THE REPAIR: DETAILED INITIALIZATION ---
client = None
api_status = "🔴 Offline"

# Check if key exists in secrets
if "GOOGLE_API_KEY" in st.secrets:
    try:
        # Initializing with the new SDK format
        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
        api_status = "🟢 Ready"
    except Exception as e:
        api_status = f"❌ Config Error: {str(e)}"

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown(f"### 🛰️ System Status: {api_status}")
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()
    
    st.divider()
    selected = option_menu(None, ["Medha (Chat)", "Srijan (Images)"], icons=["cpu", "layers"], default_index=0)

# --- 5. MAIN INTERFACE ---
if selected == "Medha (Chat)":
    st.title("🔱 VEDA 3.0 ULTRA")
    
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Command VEDA..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            answer = ""
            success = False
            
            # --- ENGINE 1: GEMINI (With Debugging) ---
            if client:
                try:
                    # Using the 8b flash model as per your previous config
                    res = client.models.generate_content(
                        model="gemini-1.5-flash-8b", 
                        contents=f"{IDENTITY}\n\nUser: {prompt}"
                    )
                    answer = res.text
                    success = True
                except Exception as e:
                    # This will show you EXACTLY why your new key isn't working
                    st.error(f"Gemini Engine Error: {str(e)}")
            
            # --- ENGINE 2: MISTRAL (Backup) ---
            if not success:
                try:
                    q_enc = urllib.parse.quote(prompt)
                    r = requests.get(f"https://text.pollinations.ai/{q_enc}?model=mistral", timeout=10)
                    if r.status_code == 200 and "Overload" not in r.text:
                        answer = r.text
                        success = True
                except: pass

            if not success:
                answer = "🔱 All neural links are currently unstable. Please check your API Key in Streamlit Secrets."

            st.markdown(answer)
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
