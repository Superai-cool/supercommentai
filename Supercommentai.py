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

comment_length = st.selectbox("Comment Length", ["Short", "Long"])

# Generate button
if st.button("Generate Comment"):
    if not content or not content_type or not writer or not tone or not comment_length:
        st.error("Please fill in all fields before generating a comment.")
    else:
        try:
            # Set maximum tokens based on comment length
            max_tokens = 60 if comment_length == "Short" else 200

            # Use ChatGPT model (gpt-3.5-turbo or gpt-4)
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an AI comment generator."},
                    {
                        "role": "user",
                        "content": f"Generate a {tone} comment for a {content_type} written by {writer} with a {comment_length.lower()} length: {content}"
                    }
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )

            comment = response["choices"][0]["message"]["content"].strip()
            st.success("Generated Comment:")
            st.write(comment)
        except Exception as e:
            st.error(f"Error: {e}")
