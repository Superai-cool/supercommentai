import streamlit as st
import openai

# Set up OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# App title
st.title("AI Comment Generator")
st.subheader("Generate concise and engaging comments tailored to your needs")

# Input fields
content = st.text_area("Content", placeholder="Enter the content here...", height=150)
content_type = st.selectbox("Content Type", ["LinkedIn Post", "Twitter Post", "Quora Post", "Google Review Post", "Zomato Review Post", "Custom"])
if content_type == "Custom":
    content_type = st.text_input("Custom Content Type", placeholder="Enter custom content type")

writer = st.selectbox("Who is Writing the Comment?", ["LinkedIn Profile Owner", "Quora Profile Owner", "Google Review Page Owner", "Restaurant Owner", "Custom"])
if writer == "Custom":
    writer = st.text_input("Custom Writer", placeholder="Enter custom writer")

tone = st.selectbox("Comment Tone", ["Formal", "Professional", "Sarcasm", "Positive", "Conversation Starter Style", "Funny", "Custom"])
if tone == "Custom":
    tone = st.text_input("Custom Tone", placeholder="Enter custom tone")

# Generate button
if st.button("Generate Comment"):
    if not content or not content_type or not writer or not tone:
        st.error("Please fill in all fields before generating a comment.")
    else:
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"Generate a {tone} comment for a {content_type} written by {writer}: {content}",
                max_tokens=100,
                temperature=0.7
            )
            comment = response.choices[0].text.strip()
            st.success("Generated Comment:")
            st.write(comment)
        except Exception as e:
            st.error(f"Error: {e}")
