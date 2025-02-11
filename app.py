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
firecrawl = Firecrawl(api_key=os.getenv("FIRECRAWL_API_KEY"))

# Fetch and store knowledge
knowledge = firecrawl.crawl(
    url="https://sambanova.ai/blog/qwen-2.5-32b-coder-available-on-sambanova-cloud"
)["data"][0]["markdown"]

os.makedirs("local_data", exist_ok=True)

with open("local_data/sambanova_announcement.md", "w") as f:
    f.write(knowledge)


# Define the model, here in this case we use gpt-4o-mini
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

# Streamlit UI
st.set_page_config(page_title="Chat Assistant", layout="wide")

st.sidebar.title("Chat Assistant Settings")
st.sidebar.markdown("Use this chatbot to interact based on preloaded knowledge.")
st.sidebar.write("\n")

st.title("🤖 Chat with AI")
st.markdown(
    "This chatbot is powered by GPT-4o-mini and preloaded with information from "
    "[SambaNova's blog post](https://sambanova.ai/blog/qwen-2.5-32b-coder-available-on-sambanova-cloud)."
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

    # Get AI response
    response = chat_agent.step(user_input)
    ai_response = response.msgs[0].content

    # Add AI response to history
    st.session_state["messages"].append({"role": "assistant", "content": ai_response})
    with st.chat_message("assistant"):
        st.markdown(ai_response)
