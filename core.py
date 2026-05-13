from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from config import settings

def get_embeddings():
    """Shared initialization for Embeddings."""
    return OllamaEmbeddings(model=settings.ollama_model)

def get_llm():
    """Shared initialization for the Language Model."""
    return Ollama(model=settings.ollama_model)

def get_db():
    """Shared initialization for the Vector Database."""
    return Chroma(persist_directory=settings.chroma_persist_directory, embedding_function=get_embeddings())

def get_allowed_roles(role: str) -> list[str]:
    """Centralized RBAC logic to define accessible roles based on user role."""
    if role == "junior":
        return ["junior"]
    elif role == "executive":
        return ["junior", "executive"]
    elif role == "director":
        return ["junior", "executive", "director"]
    return []