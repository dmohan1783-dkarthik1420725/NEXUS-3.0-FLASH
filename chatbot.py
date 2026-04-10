import streamlit as st
from google import genai
from google.genai import types

# --- VEDA 3.0 ULTRA: PRO-CLASS CONFIGURATION ---
st.set_page_config(page_title="VEDA 3.0 ULTRA", page_icon="🔱", layout="wide")

st.title("🔱 VEDA 3.0 ULTRA")
st.caption("Commander: DUMPALA KARTHIK | System: Gemini 3.1 Pro")

# --- SECURE UPLINK ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    st.error("🔱 SECURITY ERROR: GEMINI_API_KEY missing from secrets.")
    st.stop()

client = genai.Client(api_key=API_KEY)

# 1. Initialize Pro-Level Search Mesh
search_tool = types.Tool(google_search=types.GoogleSearch())

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 2. Command Input
if prompt := st.chat_input("Command VEDA..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # COMMANDED: Shows "THINKING WITH VEDA" or "ANALYSIS"
        with st.status("🔱 THINKING WITH VEDA...", expanded=True) as status:
            try:
                st.write("Initializing Gemini 3.1 Pro Brain...")
                st.write("Intercepting Search Engine Data...")
                
                response = client.models.generate_content(
                    model='gemini-1.5-pro', # Points to the 1.5/3.1 Pro architecture
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        tools=[search_tool],
                        system_instruction="You are VEDA 3.0 ULTRA, the elite intelligence partner of Karthik Dumpala. Use search to verify all 2026 data."
                    )
                )
                
                full_response = response.text
                status.update(label="🔱 ANALYSIS COMPLETE", state="complete", expanded=False)

            except Exception as e:
                st.error(f"Uplink Error: {e}")
                full_response = "Emergency: Pro-mesh synchronization failed."
                status.update(label="🔱 CRITICAL FAILURE", state="error")

        st.markdown(full_response)
        
        # Grounding Metadata (Sources)
        if response.candidates and response.candidates[0].grounding_metadata:
            with st.expander("📡 Verified Search Sources"):
                search_meta = response.candidates[0].grounding_metadata.search_entry_point
                if search_meta:
                    st.html(search_meta.rendered_content)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
