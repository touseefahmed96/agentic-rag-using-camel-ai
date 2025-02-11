import os

import streamlit as st
from camel.agents import ChatAgent
from camel.configs import ChatGPTConfig
from camel.loaders import Firecrawl
from camel.messages import BaseMessage
from camel.models import ModelFactory
from camel.types import ModelPlatformType, ModelType
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Chat Assistant", layout="wide")

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

st.sidebar.title("Chat Assistant Settings")
st.sidebar.markdown("Use this chatbot to interact based on preloaded knowledge.")
st.sidebar.write("\n")

# Allow user to input a custom URL
url = st.sidebar.text_input(
    "Enter a URL to fetch knowledge:",
    # "https://sambanova.ai/blog/qwen-2.5-32b-coder-available-on-sambanova-cloud",
)

firecrawl = Firecrawl(api_key=os.getenv("FIRECRAWL_API_KEY"))

# Fetch and store knowledge
if url:
    knowledge = firecrawl.crawl(url=url)["data"][0]["markdown"]
    os.makedirs("local_data", exist_ok=True)
    with open("local_data/sambanova_announcement.md", "w", encoding="utf-8") as f:
        f.write(knowledge)

    # Define the model
    model = ModelFactory.create(
        model_platform=ModelPlatformType.OPENAI,
        model_type=ModelType.GPT_4O_MINI,
        model_config_dict=ChatGPTConfig().as_dict(),
    )

    # Create ChatAgent
    chat_agent = ChatAgent(
        system_message="You are a helpful assistant.",
        message_window_size=20,
        model=model,
    )

    # Update memory with knowledge
    knowledge_message = BaseMessage.make_user_message(
        role_name="User",
        content=f"Based on the following knowledge: {knowledge}",
    )
    chat_agent.update_memory(knowledge_message, "user")

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
        # Add user message to history
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
