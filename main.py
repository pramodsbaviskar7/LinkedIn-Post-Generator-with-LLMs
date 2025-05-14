import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post

# Options
length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Hinglish"]
tone_options = [
    "Informative", 
    "Inspirational", 
    "Celebratory", 
    "Promotional", 
    "Reflective", 
    "Conversational", 
    "Professional", 
    "Casual", 
    "Humorous", 
    "Friendly"
]

def main():
    st.title("🔧 LinkedIn Content Creator Tool")
    
    fs = FewShotPosts()
    tags = fs.get_tags()
    
    st.markdown("### 🧠 Choose a topic or enter your own")
    
    tag_input_method = st.radio(
        "How would you like to select the topic?",
        options=["Choose from suggestions", "Enter custom topic"],
        horizontal=True
    )
    
    if tag_input_method == "Choose from suggestions":
        selected_tag = st.selectbox("Select a predefined topic", options=tags)
    else:
        selected_tag = st.text_input("Enter your custom topic", placeholder="e.g., AI in Education")
    
    st.markdown("### 📐 Post Configuration")
    col1, col2 = st.columns(2)
    with col1:
        selected_length = st.selectbox("Length", options=length_options)
    with col2:
        selected_language = st.selectbox("Language", options=language_options)
    
    st.markdown("### 🧩 Optional Enhancements")
    
    # Tone selection (choose or enter)
    tone_enabled = st.checkbox("Choose tone & intent")
    if tone_enabled:
        tone_input_method = st.radio(
            "How would you like to set the tone?",
            options=["Choose from suggestions", "Enter your own tone"],
            horizontal=True
        )
        
        if tone_input_method == "Choose from suggestions":
            tone = st.selectbox("Select tone/intent", options=tone_options)
        else:
            tone = st.text_input("Enter your custom tone", placeholder="e.g., Friendly, Motivational, Bold")
    else:
        tone = None

    # Creativity control
    creativity_enabled = st.checkbox("Control creativity level")
    if creativity_enabled:
        creativity = st.slider("Creativity (0 = focused, 1 = creative)", 0.2, 1.0, 0.7)
    else:
        creativity = None

    # Hashtag enhancements
    hashtags_enabled = st.checkbox("Add or generate hashtags")
    if hashtags_enabled:
        hashtag_mode = st.radio("How would you like to handle hashtags?", ["Add manually", "Auto-generate"])
        if hashtag_mode == "Add manually":
            custom_hashtags = st.text_input("Enter hashtags (comma or space-separated)", placeholder="#AI #Leadership")
        else:
            custom_hashtags = "AUTO"
    else:
        custom_hashtags = None

    # Generate button
    if st.button("🚀 Generate Post"):
        if selected_tag.strip():
            post = generate_post(
                length=selected_length,
                language=selected_language,
                tag=selected_tag,
                tone=tone,
                creativity=creativity,
                hashtags=custom_hashtags
            )
            st.success("✅ Post generated successfully!")
            st.markdown("### 📝 Your LinkedIn Post")
            
            st.text_area(
                "Generated Post",
                value=post,
                height=300,
                help="Click and press Ctrl+A to select all, then Ctrl+C to copy",
                key="generated_post"
            )
        else:
            st.error("⚠️ Please provide a valid topic.")

if __name__ == "__main__":
    main()
