import streamlit as st
from google import genai
from streamlit_option_menu import option_menu

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="NEXUS 3.0 ULTRA", page_icon="⚡", layout="wide")
CREATOR = "Dumpala Karthik"

# --- SMART KEY LOGIC ---
query_params = st.query_params
pollinations_key = query_params.get("api_key", st.secrets.get("POLLINATIONS_KEY", None))

try:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    st.sidebar.success("NEXUS Brain Online ⚡")
except:
    st.sidebar.error("NEXUS Brain Offline.")

# --- 2. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 80px;'>⚡</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>NEXUS 3.0 ULTRA</h3>", unsafe_allow_html=True)
    
    if not pollinations_key:
        auth_url = "https://enter.pollinations.ai/authorize?redirect_url=https://nexus-flash-india.streamlit.app"
        st.markdown(f'<a href="{auth_url}" target="_blank"><button style="width:100%; background-color:#ff4b4b; color:white; border:none; padding:12px; border-radius:8px; cursor:pointer;">🔌 CONNECT POLLINATIONS</button></a>', unsafe_allow_html=True)
    else:
        st.success("Architect Linked 🌸")

    st.divider()
    selected = option_menu("Main Systems", ["Intelligence", "Neural Architect", "Share Hub"], icons=["cpu", "layers", "share"], default_index=0)

# --- 3. MAIN INTERFACE ---

if selected == "Intelligence":
    st.markdown("<br><h1 style='text-align: center; color: #ff4b4b; font-size: 60px;'>HI, HOW ARE YOU!</h1>", unsafe_allow_html=True)
    if prompt := st.chat_input("Command NEXUS..."):
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            res = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
            st.markdown(res.text)

elif selected == "Neural Architect":
    st.title("🏗️ Neural Architect")
    if not pollinations_key:
        st.error("Please CONNECT in the sidebar first.")
    else:
        user_idea = st.text_input("What should I build?")
        if st.button("EXECUTE RENDER"):
            with st.spinner("Decoding..."):
                # 1. We ask Gemini for the "Matrix Code" ONLY (150 words)
                code_task = f"Generate 150 words of complex-looking HTML/CSS code for a futuristic UI about: {user_idea}. Output ONLY the code, no conversational text."
                code_res = client.models.generate_content(model="gemini-2.5-flash", contents=code_task)
                
                # 2. We use the CLEAN user_idea for the image, NOT the long code
                # New 2026 URL format: gen.pollinations.ai/image/
                clean_prompt = user_idea.replace(" ", "%20")
                image_url = f"https://gen.pollinations.ai/image/{clean_prompt}?width=1024&height=1024&nologo=true&key={pollinations_key}"
                
                # --- THE GREEN BOX ---
                st.markdown(f"""
                <div style="border: 2px solid #28a745; padding: 20px; border-radius: 10px; background-color: rgba(40, 167, 69, 0.05); height: 250px; overflow-y: scroll; margin-bottom: 20px;">
                    <p style="color: #28a745; font-family: monospace; font-weight: bold;">NEXUS_UI_DECODED:</p>
                    <pre style="color: #28a745; font-size: 11px; white-space: pre-wrap;">{code_res.text}</pre>
                </div>
                """, unsafe_allow_html=True)
                
                # 3. Display the actual image
                st.image(image_url, caption=f"Render by {CREATOR}")

elif selected == "Share Hub":
    st.title("🌐 Share Hub")
    st.markdown('<a href="https://wa.me/" target="_blank">WhatsApp</a> | <a href="https://instagram.com/" target="_blank">Instagram</a>', unsafe_allow_html=True)
