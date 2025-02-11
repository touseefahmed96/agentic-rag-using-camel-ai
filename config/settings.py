import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Firecrawl API Key
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")

# Model Configuration
MODEL_PLATFORM = "OPENAI"
MODEL_TYPE = "GPT_4O_MINI"

# System Message for ChatAgent
SYSTEM_MESSAGE = "You are a helpful assistant."
