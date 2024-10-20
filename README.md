# **Chatbot Application**

## **Overview**

Welcome to the Chatbot Application repository! This project showcases a powerful chatbot built using **FastAPI** and **LangChain**. The chatbot provides an engaging user experience through a web interface, delivering informative responses powered by OpenAI's advanced language models. It also integrates with **Tavily's Search API** to enhance its search capabilities.

## **Key Features**

- **Natural Language Processing:** Employs LangChain for sophisticated natural language understanding and generation, ensuring a seamless conversation flow.
  
- **OpenAI Integration:** Utilizes OpenAI's language models for advanced conversational abilities, enabling the chatbot to respond intelligently to user queries.

- **Interactive Web Interface:** User-friendly web interface for smooth interaction with the chatbot, making it accessible to all users.

- **Docker Support:** Easily deployable using Docker containers, providing a consistent environment across different setups.

## **Installation and Configuration**

### Prerequisites

1. **Docker:** Ensure Docker is installed on your machine. You can download it from the [Docker website](https://www.docker.com/get-started).

### Configuration Steps

  Create a `.env` file based on the example provided:
  ```bash
  cp .env.example .env

Build and run
  
  docker compose up --build
