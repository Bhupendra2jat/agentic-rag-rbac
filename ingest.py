import os
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from core import get_embeddings
from config import settings

# 1. Initialize local embeddings
embeddings = get_embeddings()

# Initialize text splitter for chunking
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    length_function=len,
    is_separator_regex=False,
)

# 2. Load Real Documents from Folders and Split into Chunks
documents = []

def load_docs_from_folder(folder_path, role):
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            if filename.endswith(".txt"):
                with open(os.path.join(folder_path, filename), "r", encoding="utf-8") as f:
                    content = f.read()
                    chunks = text_splitter.split_text(content)
                    for chunk in chunks:
                        documents.append(Document(page_content=chunk, metadata={"role": role}))

# Load junior, executive, and director text files
load_docs_from_folder("./data/junior", "junior")
load_docs_from_folder("./data/executive", "executive")
load_docs_from_folder("./data/director", "director")

# 3. Ingest into local ChromaDB
if documents:
    vectorstore = Chroma.from_documents(
        documents=documents, 
        embedding=embeddings, 
        persist_directory=settings.chroma_persist_directory
    )
    print(f"Successfully ingested {len(documents)} document chunks with RBAC!")
else:
    print("No .txt documents found! Please add text files to ./data folders.")