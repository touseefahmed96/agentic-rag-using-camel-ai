# Agentic RAG Using CAMEL-AI

A Python-based conversational AI application that implements a knowledge-augmented chat system using the CAMEL-AI framework and Streamlit.

## Description

This application provides an interactive chat interface that utilizes the CAMEL-AI framework to deliver context-aware responses. It integrates web crawling for gathering knowledge from specified URLs and incorporates this information into the conversation context, allowing for dynamic knowledge updates.

## Features

- Web crawling using Firecrawl for knowledge acquisition
- Integration with OpenAI's GPT models (GPT-4o-mini)
- Persistent knowledge storage in markdown format
- Interactive chat interface powered by Streamlit
- Configurable message window size
- Customizable system messages
- Sidebar settings for URL-based knowledge retrieval

## Prerequisites

- Python 3.x
- CAMEL-AI framework
- Streamlit
- Firecrawl API key (for web crawling)
- OpenAI API access
- dotenv for managing environment variables

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/touseefahmed96/agentic-rag-using-camel-ai.git
    cd agentic-rag-using-camel-ai
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Create a `.env` file and add the required API keys:
    ```env
    FIRECRAWL_API_KEY=your_firecrawl_api_key
    OPENAI_API_KEY=your_openai_api_key
    ```

## Usage

1. Run the application:
    ```bash
    streamlit run app.py
    ```

2. The application will:
    - Allow users to input a URL in the sidebar
    - Crawl the specified URL for knowledge
    - Store the retrieved information in `local_data/sambanova_announcement.md`
    - Load the chat interface with preloaded knowledge

3. During the chat:
    - Type your messages in the chat input field
    - Press Enter to receive AI-generated responses
    - Type 'exit' to end the conversation

## Configuration

### The application can be configured by modifying:

- **Model type** (currently set to GPT-4o-mini)
- **System message** (default: "You are a helpful assistant.")
- **Message window size** (default: 20)
- **Knowledge source URL** (entered via sidebar)

## UI Enhancements

- The chat interface includes a visually enhanced layout with background colors for different roles (user, assistant).
- A loading animation is displayed while generating responses.
- Sidebar settings provide an intuitive way to update the knowledge source dynamically.
