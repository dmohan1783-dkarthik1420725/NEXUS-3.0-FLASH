elif selected == "Neural Architect":
    st.title("🏗️ Neural Architect")
    design_prompt = st.text_input("Describe the visual you want to build:")
    
    if st.button("EXECUTE RENDER"):
        if design_prompt:
            # Pollinations Image Engine
            image_url = f"https://image.pollinations.ai/prompt/{design_prompt.replace(' ', '%20')}?width=1024&height=512&nologo=true"
            
            # --- THE COLORED OUTLINE BOX (Facility Fix) ---
            # 'border: 2px solid #28a745' creates the colored outline
            # 'color: #28a745' makes the text the same color
            st.markdown(f"""
            <div style="border: 2px solid #28a745; padding: 15px; border-radius: 5px; background-color: rgba(40, 167, 69, 0.1); margin-bottom: 20px;">
                <p style="color: #28a745; font-family: monospace; font-weight: bold; margin: 0;">
                    NEXUS_SYSTEM_CODE_GENERATED: <br>
                    <span style="color: #ffffff;">&lt;img src="{image_url}"&gt;</span>
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Generate the image below the box
            st.image(image_url, caption=f"Visual Render by {CREATOR}'s NEXUS Engine")
        else:
            st.warning("Please enter a description.")
