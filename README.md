## **README**

### **Chatbot Application**

**Overview**

This repository contains the source code for a chatbot application built using FastAPI and LangChain. The chatbot is designed to interact with users through a web interface, providing informative and engaging responses powered by OpenAI's language models.

**Key Features**

  - **Natural Language Processing:** Utilizes LangChain for robust natural language understanding and generation.
  - **OpenAI Integration:** Leverages OpenAI's language models for advanced conversational capabilities.
  - **Web Interface:** Interactive web interface for user interaction.
  - **Docker Support:** Easily deployable using Docker containers for consistent environments.


**Installation**

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/chatbot.git](https://github.com/your-username/chatbot.git)
    ```
2.  **Build the Docker image:**
    ```bash
    docker build -t chatbot .
    ```
3.  **Run the Docker container:**
    ```bash
    docker run -p 8000:8000 --env OPENAI_API_KEY=your_openai_api_key chatbot
    ```

**Configuration**

  - **OpenAI API Key:** Set your OpenAI API key as the `OPENAI_API_KEY` environment variable when running the Docker container.

**Usage**

  - **Access the chatbot:** Open your web browser and navigate to `http://0.0.0.0:3000` (or the specified port).
  - **Interact with the chatbot:** Type your query into the chat interface and submit.
  - **Receive responses:** The chatbot will process your query using OpenAI's language models and provide a relevant response.

