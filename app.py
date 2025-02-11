import os

from camel.agents import ChatAgent
from camel.configs import ChatGPTConfig
from camel.loaders import Firecrawl
from camel.messages import BaseMessage
from camel.models import ModelFactory
from camel.types import ModelPlatformType, ModelType
from dotenv import load_dotenv

load_dotenv()
firecrawl = Firecrawl(api_key=os.getenv("FIRECRAWL_API_KEY"))

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

chat_agent = ChatAgent(
    system_message="You are a helpful assistant.",
    message_window_size=20,
    model=model,
)

knowledge_message = BaseMessage.make_user_message(
    role_name="User",
    content=f"Based on the following knowledge: {knowledge}",
)

chat_agent.update_memory(knowledge_message, "user")

print("Start Chatting! Type 'exit' to end the conversation.")
while True:
    user_input = input("User: ")
    if user_input.lower() == "exit":
        print("Exiting the conversation.")
        break
    response = chat_agent.step(user_input)
    print(f"Assistant: {response.msgs[0].content}")
