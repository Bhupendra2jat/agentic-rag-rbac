from fastapi import FastAPI
from pydantic import BaseModel
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document


def expand_query(query, llm):
    prompt = f"Expand this search query with 2-3 synonyms/related terms. Return ONLY the expanded query:\nQuery: {query}\nExpanded:"
    return llm.invoke(prompt)


app = FastAPI(title="Secure Agentic RAG API")

class QueryRequest(BaseModel):
    query: str
    role: str


embeddings = OllamaEmbeddings(model="llama3")
llm = Ollama(model="llama3")
db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

@app.post("/ask")
def ask_question(request: QueryRequest):
    try:
        valid_roles = ["junior", "executive", "director"]
        if request.role not in valid_roles:
            return {"status": "error", "message": f"Invalid role. Use: {valid_roles}"}

        role_hierarchy = {
            "junior": ["junior"],
            "executive": ["junior", "executive"],
            "director": ["junior", "executive", "director"]
        }
        allowed_roles = role_hierarchy.get(request.role, [])


        query = expand_query(request.query, llm)

        collection = db._collection
        results = collection.query(

            query_embeddings=[embeddings.embed_query(query)],
            n_results=5,
            where={"role": {"$in": allowed_roles}},
            include=["documents", "metadatas"]
        )
        docs = [Document(page_content=d, metadata=m) for d, m in zip(results["documents"][0], results["metadatas"][0])]
        context = "\n".join([doc.page_content for doc in docs])

        if not context:
            response = llm.invoke(request.query)
            return {"status": "success", "source": "general_knowledge", "answer": response}
        else:
            prompt = PromptTemplate(
                template="Context:\n{context}\nQuestion: {query}\nAnswer:",
                input_variables=["context", "query"]
            )
            response = llm.invoke(prompt.format(context=context, query=request.query))
            return {"status": "success", "source": "secure_documents", "answer": response}

    except Exception as e:
        return {"status": "error", "message": str(e)}
