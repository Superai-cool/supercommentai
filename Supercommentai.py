import streamlit as st
import openai

# Set up OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# App title
st.title("Supercomment.io")
st.subheader("Generate complete, concise, and engaging comments tailored to your needs")

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
            max_tokens = 120 if comment_length == "Short" else 280

            # Enhanced prompt for highly engaging comments
            prompt = (
                f"Create a {comment_length.lower()} and {tone.lower()} comment for a {content_type} written by {writer}. "
                "Ensure the comment is meaningful, engaging, and adds value. Provide thoughtful feedback or insights. "
                f"The comment should fit within {max_tokens} characters and include hashtags if relevant. "
                f"Post Content: {content}\nComment:"
            )

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert at writing complete, concise, and human-like comments."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.5  # Lower temperature for more focused results
            )
            comment = response["choices"][0]["message"]["content"].strip()

            # Validate and finalize the comment
            if len(comment) > max_tokens:
                comment = comment[:max_tokens].rsplit(" ", 1)[0] + "..."

            st.success("Generated Comment:")
            st.write(comment)
        except Exception as e:
            st.error(f"Error: {e}")
