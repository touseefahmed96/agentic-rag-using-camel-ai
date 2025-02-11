import os

from camel.loaders import Firecrawl

from config.settings import FIRECRAWL_API_KEY


def fetch_knowledge(url: str) -> str:
    """
    Fetch knowledge from a given URL using Firecrawl API.
    Stores the knowledge in a markdown file locally.
    """
    if not FIRECRAWL_API_KEY:
        raise ValueError("Firecrawl API Key is missing!")

    firecrawl = Firecrawl(api_key=FIRECRAWL_API_KEY)
    response = firecrawl.crawl(url=url)

    if not response["data"]:
        raise ValueError("Failed to fetch data from the URL.")

    knowledge = response["data"][0]["markdown"]

    os.makedirs("data/local_data", exist_ok=True)
    file_path = "data/local_data/knowledge.md"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(knowledge)

    return knowledge
