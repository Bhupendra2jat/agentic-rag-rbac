# Agentic RAG with RBAC

This project implements a secure, role-based Retrieval-Augmented Generation (RAG) system. It uses LangChain, ChromaDB, and local LLMs via Ollama to provide intelligent document querying while strictly enforcing access control based on user roles. 

The system features both a FastAPI backend and a Streamlit frontend, and includes an "agentic fallback" mechanism: if a user's query cannot be answered using the documents they have access to, the system falls back to the general knowledge of the underlying LLM.

## Project Structure & File Breakdown

*   **`api.py`**: A FastAPI application that exposes a `/ask` endpoint. It accepts a JSON payload containing a `query` and a `role`. It performs similarity search with RBAC filtering and returns the AI-generated answer.
*   **`app.py`**: A Streamlit interactive web application. It provides a UI to simulate user login (role selection), input queries, and view both the generated response and an audit log of the retrieved documents.
*   **`ingest.py`**: The data ingestion script. It reads text files from the `data/` directory, assigns role-based metadata according to the folder structure, generates embeddings, and stores them in a local ChromaDB vector store.
*   **`requirements.txt`**: Lists the Python dependencies required to run the project (e.g., `langchain`, `streamlit`, `fastapi`, `chromadb`).
*   **`chroma_db/`**: The local directory where the Chroma vector database is persisted.
*   **`data/`**: Contains the source documents organized by access level:
    *   `data/junior/`: Documents accessible to all employees (e.g., employee handbook).
    *   `data/executive/`: Confidential documents accessible only to executives and directors (e.g., financials).
    *   `data/director/`: Top-secret documents accessible only to directors (e.g., board secrets).

## Suggested Improvements

To make this project production-ready and further improve its architecture, consider the following enhancements:

### 1. Authentication & Security
*   **Real Authentication:** The current system relies on users self-reporting their role via a dropdown or API payload. Integrate a real identity provider (OAuth2, OIDC) or JWT-based authentication to securely verify user identities and extract their roles from claims.
*   **Secrets Management:** Ensure that sensitive documents in the `data/` folder are not committed to version control in a real-world scenario. Use secure cloud storage (like AWS S3) for document retrieval.

### 2. Architectural Refactoring
*   **Shared Core Module:** Both `app.py` and `api.py` duplicate the initialization logic for LLMs, Embeddings, and ChromaDB, as well as the RBAC and fallback logic. Extract this into a shared `core.py` or `services/` module to adhere to DRY (Don't Repeat Yourself) principles.
*   **Asynchronous Support:** The FastAPI endpoints and LangChain calls are currently synchronous. Upgrading to use LangChain's async methods (`ainvoke`) and async FastAPI endpoints (`async def`) will drastically improve concurrency and throughput under load.

### 3. Configuration Management
*   **Environment Variables:** Hardcoded values like model names (`llama3`), DB paths (`./chroma_db`), and even valid roles should be moved to a `.env` file and managed using `pydantic-settings` or `os.environ`. This allows deploying to different environments without code changes.

### 4. Dependency & Environment Management
*   **Version Pinning:** The `requirements.txt` file currently uses unpinned dependencies. Pinning exact versions (e.g., `fastapi==0.103.1`) or using a modern package manager like `Poetry` or `uv` will ensure reproducible builds and prevent unexpected breaking changes from upstream libraries.

### 5. Advanced RAG Features
*   **Prompt Engineering:** Improve the fallback prompt so the LLM explicitly states when it is relying on general knowledge versus internal documents.
*   **Chunking Strategy:** `ingest.py` currently loads entire documents as single chunks. Implementing a `RecursiveCharacterTextSplitter` will improve retrieval accuracy for larger documents.

## How to Run

1.  **Install Requirements:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Ensure Ollama is running:**
    Make sure you have Ollama installed and the `llama3` model pulled:
    ```bash
    ollama run llama3
    ```
3.  **Ingest Data:**
    ```bash
    python ingest.py
    ```
4.  **Start the API (Optional):**
    ```bash
    uvicorn api:app --reload
    ```
5.  **Start the Streamlit UI:**
    ```bash
    streamlit run app.py
    ```
