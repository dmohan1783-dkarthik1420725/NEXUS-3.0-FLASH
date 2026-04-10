import streamlit as st
from google import genai
from google.genai import types

# --- VEDA 3.0 ULTRA: SOVEREIGN CONFIGURATION ---
st.set_page_config(page_title="GenAI Sovereign Search", page_icon="🔱", layout="wide")

# Custom CSS for the VEDA/GenAI interface
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stTextInput>div>div>input { background-color: #262730; color: white; border: 1px solid #4a4a4a; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔱 GenAI: Intelligence & Global Search")
st.sidebar.info("Station: Hyderabad | Core: Gemini 2.0 Flash")

# 1. Initialize the Sovereign Client
# Replace the string below with your actual API Key
API_KEY = 'YOUR_API_KEY'
client = genai.Client(api_api_key=API_KEY)

# 2. Define the Search Engine Tool
search_tool = types.Tool(google_search=types.GoogleSearch())

# 3. Session State for Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. Command Input
if prompt := st.chat_input("Command GenAI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 5. Generate Response with GOOGLE SEARCH GROUNDING
    with st.chat_message("assistant"):
        with st.spinner("🔱 Infiltrating Global Search Mesh..."):
            try:
                response = client.models.generate_content(
                    model='gemini-2.0-flash',
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        tools=[search_tool],
                        system_instruction="You are GenAI, a search-integrated elite intelligence asset."
                    )
                )
                
                full_response = response.text
                st.markdown(full_response)
                
                # If the AI used Google Search, show the sources
                if response.candidates[0].grounding_metadata:
                    with st.expander("📡 Satellite Data Sources"):
                        st.write("Information verified via Google Search Grounding.")
                        # Link to search results
                        search_entry = response.candidates[0].grounding_metadata.search_entry_point
                        if search_entry:
                             st.html(search_entry.rendered_content)

            except Exception as e:
                st.error(f"🔱 Uplink Error: {e}")
                full_response = "Emergency: Secondary mesh failed to retrieve data."

    st.session_state.messages.append({"role": "assistant", "content": full_response})
