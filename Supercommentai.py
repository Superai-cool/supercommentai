import streamlit as st
import openai

# Sidebar for OpenAI API Key
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="supercommentai_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

# App title
st.title("Supercomment.io")
st.caption("🚀 Generate concise, engaging, and human-like comments tailored to your needs")

# Initialize session state for storing messages
if "comments" not in st.session_state:
    st.session_state["comments"] = []

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

# Generate button
if st.button("Generate Comment"):
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    if not content or not content_type or not writer or not tone:
        st.error("Please fill in all fields before generating a comment.")
    else:
        try:
            # Set max_tokens for better control of output
            max_tokens = 300

            # Fine-tuned prompt for complete comments
            prompt = (
                f"Write a concise and {tone.lower()} comment for a {content_type} written by {writer}. "
                "The comment should be meaningful, engaging, and human-like. Acknowledge the post meaningfully, add value through a thoughtful insight or question. "
                f"Post Content: {content}\nComment:"
            )

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert at crafting complete, concise, and human-like comments."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.6
            )

            comment = response.choices[0].message.content.strip()

            # Ensure comments follow the specified ending rule
            if tone.lower() == "conversation starter style" and not comment.endswith("?"):
                comment = comment.rstrip(".") + "?"
            elif tone.lower() != "conversation starter style" and comment.endswith("?"):
                comment = comment.rstrip("?") + "."

            st.session_state["comments"].append({"role": "assistant", "content": comment})

            st.success("Generated Comment:")
            st.write(comment)
        except Exception as e:
            st.error(f"Error: {e}")

