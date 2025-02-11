# Agentic RAG Using CAMEL-AI

A Python-based conversational AI application that implements a knowledge-augmented chat system using the CAMEL-AI framework.

## Description

This application creates a chat interface that leverages the CAMEL-AI framework to provide context-aware responses. It specifically uses web crawling to gather knowledge from specified URLs and incorporates this information into the conversation context.

## Features

- Web crawling using Firecrawl for knowledge gathering
- Integration with OpenAI's GPT models
- Persistent knowledge storage in markdown format
- Interactive chat interface
- Configurable message window size
- Customizable system messages

## Prerequisites

- Python 3.x
- CAMEL-AI framework
- OpenAI API access

## Installation

1. Clone the repository
2. Install the required dependencies:
    ```bash
    pip install -r requirments.txt
    ```

## Usage

1. Run the application:
    ```bash
    python app.py
    ```

2. The application will:
    - Crawl the specified URL for knowledge
    - Store the gathered information in local_data/sambanova_announcement.md
    - Start an interactive chat session

3. During the chat:
    - Type your messages and press Enter to receive responses
    - Type 'exit' to end the conversation

## Configuration

### The application can be configured by modifying:

- Model type (currently set to GPT-4O-MINI)
- System message
- Message window size (currently set to 20)
- Knowledge source URL