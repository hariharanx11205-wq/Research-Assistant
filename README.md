# Research Assistant

An intelligent, AI-powered research assistant that leverages LangChain and DuckDuckGo to perform web searches and provide accurate, synthesized information in a conversational interface.

## Features

- **Web Search Capabilities**: Uses DuckDuckGo via LangChain to find real-time information from the web.
- **AI-Powered Analysis**: Utilizes LLMs (OpenAI compatible) to process search results and answer user queries.
- **Interactive Chat Interface**: A clean, modern chat UI for seamless interaction.
- **Streamlined Design**: Responsive and aesthetic frontend with glassmorphism elements.

## Tech Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Backend**: Python, FastAPI
- **AI/ML**: LangChain, LangGraph, DuckDuckGo Search Tool

## Setup Instructions

### Prerequisites

- Python 3.8+
- An OpenAI API Key (or OpenRouter Key)

### Installation

1.  **Clone the repository**
    ```bash
    git clone <your-repo-url>
    cd research-assistant
    ```

2.  **Install Backend Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Environment Configuration**
    Create a `.env` file in the root directory and add your API keys:
    ```env
    OPENAI_API_KEY=your_api_key_here
    OPENAI_API_BASE=https://openrouter.ai/api/v1  # If using OpenRouter
    ```

### Running the Application

1.  **Start the Backend Server**
    Run the FastAPI server using Uvicorn:
    ```bash
    uvicorn api.index:app --reload
    ```
    The API will be available at `http://localhost:8000`.

2.  **Launch the Frontend**
    Open `frontend/index.html` directly in your browser, or use a simple HTTP server (like VS Code Live Server) to serve the `frontend` directory.

    If serving locally, ensure the frontend `app.js` is pointing to the correct backend URL (default is usually relative or `http://localhost:8000`).

## Deployment

This project is configured for deployment on **Vercel**.
- The `api` directory contains the serverless function entry point (`index.py`).
- `vercel.json` provides the deployment configuration.
