# Agentic RAG with RBAC

A secure Retrieval-Augmented Generation (RAG) system built using local LLaMA3, LangChain, ChromaDB, FastAPI, and Streamlit.  
This project focuses on improving retrieval quality while enforcing secure document access using Role-Based Access Control (RBAC).

---

# Overview

Traditional RAG systems usually retrieve documents without considering user permissions or retrieval quality optimizations.  
This project was built to simulate a more production-oriented AI system where:

- users can only access documents allowed for their role
- retrieval quality is improved using query expansion and retrieval tuning
- the system falls back to general LLM knowledge when no internal documents are found

The application uses local LLaMA3 through Ollama, making the system fully local and API-independent.

---

# What is RAG?

RAG (Retrieval-Augmented Generation) is an AI architecture where:

1. Relevant documents are retrieved from a knowledge base
2. Retrieved context is sent to an LLM
3. The LLM generates answers grounded in those documents

Instead of relying only on pretrained knowledge, the model answers using real-time retrieved information.

---

# What is Agentic RAG?

Agentic RAG extends traditional RAG systems by adding decision-making behavior.

In this project:
- if relevant secure documents exist → answer using RAG
- if no relevant documents are found → fallback to general LLM reasoning

This creates a more adaptive and reliable AI workflow instead of failing silently.

---

# RBAC (Role-Based Access Control)

The system implements hierarchical RBAC:

- Junior → access to junior documents
- Executive → access to junior + executive documents
- Director → access to all documents

Access control is enforced at the retrieval layer using metadata filtering in ChromaDB.

This prevents unauthorized document retrieval before context reaches the LLM.

---

# Features

- Secure multi-document RAG pipeline
- Hierarchical RBAC enforcement
- Local LLaMA3 inference using Ollama
- Query expansion for improved retrieval
- Retrieval tuning using top-k retrieval
- Metadata-aware vector search using ChromaDB
- FastAPI backend APIs
- Streamlit frontend UI
- Agentic fallback mechanism
- Audit logging for retrieved documents

---

# Tech Stack

## AI / LLM
- LLaMA3
- Ollama
- LangChain

## Backend
- FastAPI
- REST APIs

## Retrieval
- ChromaDB
- Vector embeddings
- Semantic search

## Frontend
- Streamlit

## Language
- Python

---

# Project Structure

```bash
rag_rbac_system/
│
├── app.py              # Streamlit frontend
├── api.py              # FastAPI backend
├── ingest.py           # Document ingestion pipeline
├── chroma_db/          # Persistent vector database
├── data/
│   ├── junior/
│   ├── executive/
│   └── director/
