# Agentic RAG with RBAC: Project Preparation Guide

This document is designed to help you present this project effectively in a professional setting (e.g., in an interview, on your resume, or during a presentation) and outlines the key technical concepts you need to understand deeply.

---

## 1. What to Mention in Your Resume / Presentation

When discussing this project, highlight the *architectural decisions* and the *security features*, as these show maturity and production-readiness.

**Project Title Idea:** Secure Agentic Retrieval-Augmented Generation (RAG) System

**Key Bullet Points for Resume:**
*   **Role-Based Access Control (RBAC):** Designed and implemented a secure RAG architecture where document retrieval is strictly filtered by user authorization levels (e.g., Junior, Executive, Director) using vector database metadata filtering (`$in` operators in ChromaDB).
*   **Agentic Fallback Mechanism:** Engineered an intelligent fallback layer that prevents standard RAG failures; if no internal documents match the user's query and access level, the system automatically queries the foundational LLM's general knowledge.
*   **Asynchronous API Backend:** Built a high-concurrency RESTful API using **FastAPI** and **LangChain's asynchronous invocation methods (`ainvoke`, `asimilarity_search`)** to ensure high throughput under concurrent user load.
*   **Modular Architecture & Configuration Management:** Refactored the codebase to follow DRY principles by decoupling core logic (Embeddings, VectorDB, LLM) into a shared service module, and implemented environment-based configuration using `pydantic-settings`.
*   **Data Processing Pipeline:** Created an ingestion script utilizing LangChain's `RecursiveCharacterTextSplitter` to optimally chunk textual data, improving semantic search accuracy and managing LLM context window limits.
*   **Local AI Deployment:** Leveraged **Ollama** (`llama3`) for entirely local embedding generation and inference, ensuring maximum data privacy and zero external API costs.
*   **Interactive UI:** Developed a **Streamlit** frontend to demonstrate real-time, role-simulated queries alongside transparent audit logs displaying retrieved document classifications.

---

## 2. What to Study for This Particular Project

To confidently defend this project in a technical interview, you should study and deeply understand the following core concepts:

### A. RAG Architecture and Trade-offs
*   **How RAG works:** Understand the complete flow: Vectorization (Embeddings) -> Storage (Vector DB) -> Semantic Search (Cosine Similarity, etc.) -> Prompt Augmentation -> LLM Generation.
*   **Chunking Strategies:** Why did we use `RecursiveCharacterTextSplitter`? Be prepared to discuss how chunk size (e.g., 500 characters) and chunk overlap (e.g., 50 characters) affect retrieval accuracy and token limits.
*   **Embeddings:** What is an embedding? How does `OllamaEmbeddings` convert text into high-dimensional vectors?

### B. Security & Access Control (RBAC in Vector Databases)
*   **Metadata Filtering:** Understand how ChromaDB filters results *before* or *during* the similarity search (Post-filtering vs. Pre-filtering). In this project, we use metadata filters (`{"role": {"$in": allowed_roles}}`).
*   **Authentication (JWT/OAuth2):** Even though we simulated it, be ready to explain how you would implement real auth. *Study how JSON Web Tokens (JWT) work, how a frontend passes them in an Authorization header, and how FastAPI's `Depends` decodes them to extract claims (like user roles).*

### C. Backend Engineering (FastAPI & Async Python)
*   **Asynchronous Programming (`async`/`await`):** Why did we make the FastAPI endpoints asynchronous? Understand the Global Interpreter Lock (GIL) in Python and how async I/O helps with network/database bound tasks (like calling an LLM or querying a database) without blocking the main thread.
*   **Dependency Injection in FastAPI:** Understand how `Depends()` works in FastAPI (e.g., for validating the token/role on every request).
*   **Pydantic & Settings Management:** How does `pydantic-settings` load environment variables? Why is this a best practice for Twelve-Factor Apps?

### D. The "Agentic" Aspect
*   **Agentic Workflows:** In this project, the "Agentic Fallback" is a simple conditional check (if context is empty -> use general knowledge). Be prepared to discuss how you could make it *more* agentic. For example, using LangChain Agents with tools (e.g., a "Database Search Tool" and a "Web Search Tool") where the LLM *decides* which tool to use.

### E. Database Specifics
*   **ChromaDB vs. Alternatives:** Why use ChromaDB? (It's local, SQLite-based, great for prototyping). What would you use in production? (Study alternatives like Pinecone, PgVector, Qdrant, or Milvus and their pros/cons).