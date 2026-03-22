# [TAB 3: VEDA HUB]
elif selected == "Veda (Hub)":
    st.markdown(ORANGE_TITLE, unsafe_allow_html=True)
    st.markdown('<div class="orange-title">VEDA NETWORK HUB</div>', unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #888;'>Architect: <b>{CREATOR}</b></p>", unsafe_allow_html=True)
    
    st.divider()
    
    # 📱 ACTUAL APP LINKS
    # You can change these URLs to your own profile links!
    apps = [
        ("WhatsApp", "whatsapp", "https://wa.me/"), # Add your number after the slash
        ("Instagram", "instagram-new", "https://instagram.com"), 
        ("YouTube", "youtube-play", "https://youtube.com"), 
        ("Facebook", "facebook-new", "https://facebook.com")
    ]
    
    # Create 4 columns for the icons
    cols = st.columns(4)
    
    for i, (name, icon, url) in enumerate(apps):
        with cols[i]:
            # This creates a clickable image that goes to the REAL site
            st.markdown(f"""
                <div style="text-align: center;">
                    <a href="{url}" target="_blank">
                        <img src="https://img.icons8.com/color/96/{icon}.png" width="80">
                    </a>
                    <p style="margin-top: 10px; font-weight: bold; color: white;">{name}</p>
                </div>
            """, unsafe_allow_html=True)
            
    st.divider()
    st.info("💡 Tip: Click the icons above to launch the official applications.")
