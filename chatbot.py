import streamlit as st
from google import genai
from google.genai import types # Added for stricter configuration
from streamlit_option_menu import option_menu

# --- 1. CORE CONFIGURATION ---
st.set_page_config(page_title="NEXUS Flash India", page_icon="⚡", layout="wide")

CREATOR = "Dumpala Karthik"
SYSTEM_PROMPT = f"Your name is NEXUS 3.0. You were developed and created by {CREATOR}."

# STABLE CONNECTION SETUP
try:
    # Adding http_options forces the 'v1' stable API path
    client = genai.Client(
        api_key=st.secrets["GOOGLE_API_KEY"],
        http_options={'api_version': 'v1'}
    )
    st.sidebar.success("NEXUS Brain Online ⚡")
except Exception as e:
    st.sidebar.error("NEXUS Brain Offline.")

# --- 2. SIDEBAR (Facilities remain the same) ---
# ... [Keep your sidebar code here] ...

# --- 3. MAIN INTERFACE ---

if selected == "Intelligence":
    st.markdown("<br><h1 style='text-align: center; color: #ff4b4b; font-size: 60px;'>HI, HOW ARE YOU!</h1>", unsafe_allow_html=True)
    
    if prompt := st.chat_input("Command NEXUS..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            try:
                # Use a simplified content structure to avoid 'ClientError'
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=[f"{SYSTEM_PROMPT}", f"User: {prompt}"]
                )
                if response.text:
                    st.markdown(response.text)
                else:
                    st.error("NEXUS received an empty response. Try a different prompt.")
            except Exception as e:
                # This will now show you the REAL error instead of a generic message
                st.error(f"Connection Error: {str(e)}")
                st.info("Tip: Check if your API Key in Streamlit Secrets has any hidden spaces.")

# ... [Keep your Neural Architect and Share Hub code here] ...
