import streamlit as st

from models.model import initialize_model, update_agent_memory
from utils.fetch_knowledge import fetch_knowledge

# Load page settings
st.set_page_config(page_title="Chat Assistant", layout="wide")

# Apply custom styles
st.markdown(
    """
    <style>
        body {
            background-color: #f4f4f4;
        }
        .stChatMessage {
            border-radius: 10px;
            padding: 10px;
            margin: 5px 0;
        }
        .user {
            background-color: #d1e7dd;
        }
        .assistant {
            background-color: #f8d7da;
        }
        .loading {
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .dot {
            width: 10px;
            height: 10px;
            margin: 0 3px;
            background-color: #000;
            border-radius: 50%;
            animation: blink 1.5s infinite;
        }
        @keyframes blink {
            0% { opacity: 0.2; }
            50% { opacity: 1; }
            100% { opacity: 0.2; }
        }
    """,
    unsafe_allow_html=True,
)

# Sidebar
with open("templates/sidebar.md", "r") as sidebar_content:
    st.sidebar.markdown(sidebar_content.read())

# Allow user to input a custom URL
url = st.sidebar.text_input("Enter a URL to fetch knowledge:")

if url:
    try:
        knowledge = fetch_knowledge(url)
        chat_agent = initialize_model()
        update_agent_memory(chat_agent, knowledge)

        st.title("🤖 Chat with AI")
        st.markdown(
            "This chatbot is powered by GPT-4o-mini and preloaded with information from the given URL."
        )

        if "messages" not in st.session_state:
            st.session_state["messages"] = []

        # Display chat history
        for message in st.session_state["messages"]:
            with st.chat_message("user" if message["role"] == "user" else "assistant"):
                st.markdown(message["content"])

        # User input field
        user_input = st.chat_input("Type your message here...")
        if user_input:
            st.session_state["messages"].append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)

            # Show loading animation
            with st.spinner("Generating response..."):
                st.markdown(
                    "<div class='loading'><div class='dot'></div><div class='dot'></div><div class='dot'></div></div>",
                    unsafe_allow_html=True,
                )
                response = chat_agent.step(user_input)

            ai_response = response.msgs[0].content

            # Add AI response to history
            st.session_state["messages"].append(
                {"role": "assistant", "content": ai_response}
            )
            with st.chat_message("assistant"):
                st.markdown(ai_response)

    except Exception as e:
        st.sidebar.error(f"Error: {e}")
