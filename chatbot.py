import streamlit as st
from google import genai
from google.genai import types
import time

# --- VEDA 3.0 ULTRA: SOVEREIGN CONFIGURATION ---
st.set_page_config(page_title="VEDA 3.0 ULTRA", page_icon="🔱", layout="wide")

# Elite CSS for the Sovereign Interface
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stTextInput>div>div>input { background-color: #262730; color: white; border: 1px solid #4a4a4a; }
    h1 { color: #00d4ff; text-shadow: 2px 2px #000000; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔱 VEDA 3.0 ULTRA")
st.subheader("Sovereign AI developed by DUMPALA KARTHIK")

# 1. Initialize the Sovereign Client (FIXED TYPEERROR)
# Replace 'YOUR_API_KEY' with your actual key
API_KEY = 'YOUR_API_KEY'
client = genai.Client(api_key=API_KEY)

# 2. Define the Search & Intelligence Tools
search_tool = types.Tool(google_search=types.GoogleSearch())

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 3. Command Input
if prompt := st.chat_input("Input Command for VEDA..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 4. Generate Response with ANALYSIS status
    with st.chat_message("assistant"):
        # This creates the "Thinking/Analysis" status you requested
        with st.status("🔱 VEDA IS ANALYZING THE MESH...", expanded=True) as status:
            try:
                st.write("Intercepting global data packets...")
                response = client.models.generate_content(
                    model='gemini-2.0-flash',
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        tools=[search_tool],
                        system_instruction="You are VEDA 3.0 ULTRA, an elite AI asset created by Karthik Dumpala. Use search to provide real-time accuracy."
                    )
                )
                full_response = response.text
                st.write("Sovereign analysis complete.")
                status.update(label="🔱 ANALYSIS COMPLETE", state="complete", expanded=False)
            except Exception as e:
                st.error(f"Uplink Error: {e}")
                full_response = "Emergency: Secondary mesh failed."

        st.markdown(full_response)
        
        # Display Search Sources
        if response.candidates[0].grounding_metadata:
            with st.expander("📡 Satellite Search Grounding"):
                st.write("Data verified through real-time global search.")

    st.session_state.messages.append({"role": "assistant", "content": full_response})
