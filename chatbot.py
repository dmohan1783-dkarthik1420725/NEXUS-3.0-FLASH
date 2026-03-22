# --- 📸 MULTIMEDIA INPUT AREA (Gemini Style) ---
    st.markdown("---")
    multi_cols = st.columns([1, 1, 1, 1, 6]) 
    
    with multi_cols[0]:
        cam_pop = st.popover("📷")
        cam_file = cam_pop.camera_input("Capture Vision")
    
    with multi_cols[1]:
        gal_pop = st.popover("🖼️")
        gal_file = gal_pop.file_uploader("Gallery", type=['png', 'jpg', 'jpeg'])

    with multi_cols[2]:
        file_pop = st.popover("📁")
        # Change 'uploaded_file' to 'doc_file' to avoid confusion
        doc_file = file_pop.file_uploader("Upload Files", type=['pdf', 'txt', 'docx'])

    with multi_cols[3]:
        if st.button("🎤"):
            st.toast("Voice synthesis initializing...")

    # --- 🛠️ THE FIX: Checking the variables correctly ---
    # We combine them so VEDA knows if ANY file was uploaded
    active_visual = cam_file or gal_file
    
    if active_visual:
        st.image(active_visual, caption="Visual Data Detected", width=200)

    if doc_file:
        st.success(f"📄 Document Attached: {doc_file.name}")

    # 📥 MAIN CHAT INPUT
    if prompt := st.chat_input("Command VEDA..."):
        add_to_memory("MEDHA", prompt)
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        # [Rest of your chat logic follows...]
