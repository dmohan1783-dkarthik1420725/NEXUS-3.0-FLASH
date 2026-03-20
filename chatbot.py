import streamlit as st
from google import genai

# 1. Setup the new Client
try:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    # Testing the connection
    st.sidebar.success("NEXUS Brain Online ⚡")
except Exception as e:
    st.sidebar.error("NEXUS Brain Offline. Check Secrets.")

# 2. Main Chat Logic
if prompt := st.chat_input("Command NEXUS..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        # The new way to call Gemini
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=prompt
        )
        st.markdown(response.text)
