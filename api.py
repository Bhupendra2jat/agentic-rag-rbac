from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from langchain.prompts import PromptTemplate
from core import get_llm, get_db, get_allowed_roles
from config import settings

app = FastAPI(title="Secure Agentic RAG API")

class QueryRequest(BaseModel):
    query: str
    role: str # In a real app, this role would be extracted securely from a JWT token

async def get_current_user_role(request: QueryRequest):
    """
    Simulated Authentication Dependency.
    In a production application, this dependency would decode a JWT token from 
    the Authorization header and verify the user's role securely.
    """
    if request.role not in settings.valid_roles:
        raise HTTPException(status_code=403, detail=f"Invalid or missing role. Must be one of: {settings.valid_roles}")
    return request.role

@app.post("/ask")
async def ask_question(request: QueryRequest, role: str = Depends(get_current_user_role)):
    try:
        allowed_roles = get_allowed_roles(role)
        db = get_db()
        llm = get_llm()

        # Asynchronous similarity search for improved throughput
        results = await db.asimilarity_search(request.query, k=2, filter={"role": {"$in": allowed_roles}})
        context = "\n".join([doc.page_content for doc in results])

        if not context:
            # Agentic Fallback with asynchronous invocation
            response = await llm.ainvoke(request.query)
            return {"status": "success", "source": "general_knowledge", "answer": response}
        else:
            # Standard RAG with asynchronous invocation
            prompt = PromptTemplate(template="Context:\n{context}\nQuestion: {query}\nAnswer:", input_variables=["context", "query"])
            response = await llm.ainvoke(prompt.format(context=context, query=request.query))
            return {"status": "success", "source": "secure_documents", "answer": response}
            
    except Exception as e:
        return {"status": "error", "message": str(e)}