import streamlit as st
import openai

# Set up OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# App title
st.title("Supercomment.io")
st.subheader("Generate complete, concise, and engaging comments effortlessly")

# Input fields
content = st.text_area("Content", placeholder="Enter the content here...")
content_type = st.selectbox("Content Type", ["LinkedIn Post", "Twitter Post", "Quora Post", "Google Review Post", "Zomato Review Post", "Custom"])
if content_type == "Custom":
    content_type = st.text_input("Custom Content Type", placeholder="Enter custom content type")

writer = st.selectbox("Who is Writing the Comment?", ["LinkedIn Profile Owner", "Quora Profile Owner", "Google Review Page Owner", "Restaurant Owner", "Custom"])
if writer == "Custom":
    writer = st.text_input("Custom Writer", placeholder="Enter custom writer")

tone = st.selectbox("Comment Tone", ["Formal", "Professional", "Sarcasm", "Positive", "Conversation Starter Style", "Funny", "Custom"])
if tone == "Custom":
    tone = st.text_input("Custom Tone", placeholder="Enter custom tone")

comment_length = st.selectbox("Comment Length", ["Short", "Long Note"])

# Generate button
if st.button("Generate Comment"):
    if not content or not content_type or not writer or not tone:
        st.error("Please fill in all fields before generating a comment.")
    else:
        try:
            # Set max_tokens based on length
            max_tokens = 100 if comment_length == "Short" else 200

            # Improved prompt for meaningful, complete comments
            prompt = (
                f"Write a {comment_length.lower()} and {tone.lower()} comment for a {content_type} written by {writer}. "
                "Make the comment meaningful, engaging, and complete, without exceeding the character limit. "
                "Ensure the comment is natural and human-like, with any hashtags or additional elements fully included."
                f"\nPo
