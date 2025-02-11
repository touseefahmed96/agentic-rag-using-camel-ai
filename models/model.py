from camel.agents import ChatAgent
from camel.configs import ChatGPTConfig
from camel.messages import BaseMessage
from camel.models import ModelFactory
from camel.types import ModelPlatformType, ModelType

from config.settings import MODEL_PLATFORM, MODEL_TYPE, SYSTEM_MESSAGE


def initialize_model():
    """
    Initializes the Chat Model and returns a ChatAgent instance.
    """
    model = ModelFactory.create(
        model_platform=ModelPlatformType[MODEL_PLATFORM],
        model_type=ModelType[MODEL_TYPE],
        model_config_dict=ChatGPTConfig().as_dict(),
    )

    chat_agent = ChatAgent(
        system_message=SYSTEM_MESSAGE,
        message_window_size=20,
        model=model,
    )

    return chat_agent


def update_agent_memory(chat_agent, knowledge: str):
    """
    Updates the ChatAgent memory with fetched knowledge.
    """
    knowledge_message = BaseMessage.make_user_message(
        role_name="User",
        content=f"Based on the following knowledge: {knowledge}",
    )
    chat_agent.update_memory(knowledge_message, "user")
