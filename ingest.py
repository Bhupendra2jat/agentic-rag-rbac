import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.documents import Document


embeddings = OllamaEmbeddings(model="llama3")


documents = []
def load_docs_from_folder(folder_path, role):
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            if filename.endswith(".txt"):
                with open(os.path.join(folder_path, filename), "r", encoding="utf-8") as f:
                    documents.append(Document(page_content=f.read(), metadata={"role": role}))


load_docs_from_folder("./data/junior", "junior")
load_docs_from_folder("./data/executive", "executive")
load_docs_from_folder("./data/director", "director")


if documents:
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory="./chroma_db"
    )
    print(f"Ingested {len(documents)} documents with RBAC metadata!")
else:
    print("No .txt files found! Add documents to ./data/{role}/")
