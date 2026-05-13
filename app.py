import streamlit as st
from langchain.prompts import PromptTemplate
from core import get_llm, get_db, get_allowed_roles
from config import settings

# 1. Setup Streamlit UI
st.set_page_config(page_title="Secure RAG", page_icon="🛡️")
st.title("🛡️ Agentic RAG with RBAC")
st.write("Production-grade RAG with Role-Based Access Control using local Llama3.")

# 2. Select User Role (Simulating Authentication)
role = st.selectbox("Select your login role:", settings.valid_roles)

# 3. Initialize Embeddings, LLM, and VectorDB using Core logic
@st.cache_resource
def load_components():
    return get_llm(), get_db()

llm, db = load_components()

# 4. User Input
query = st.text_input("Ask a question about the company data:")

if st.button("Search") and query:
    with st.spinner("Searching securely..."):
        
        # 5. RBAC LOGIC: Use centralized allowed roles logic
        allowed_roles = get_allowed_roles(role)
        
        # Fetch documents matching the allowed roles using Chroma's $in operator
        results = db.similarity_search(
            query, 
            k=3, 
            filter={"role": {"$in": allowed_roles}}
        )
        
        context = "\n".join([doc.page_content for doc in results])
        
        if not context:
            # 6. AGENTIC FALLBACK
            st.warning("No internal documents found. Falling back to general AI knowledge... 🌐")
            fallback_response = llm.invoke(query)
            st.success("Response Generated (General Knowledge)!")
            st.write(fallback_response)
        else:
            # 7. Generate Answer via RAG
            prompt_template = "Answer the question based ONLY on the following context.\nContext:\n{context}\nQuestion: {query}\nAnswer:"
            prompt = PromptTemplate(template=prompt_template, input_variables=["context", "query"])
            final_prompt = prompt.format(context=context, query=query)
            
            response = llm.invoke(final_prompt)
            
            st.success("Response Generated!")
            st.write(response)
            
            # Audit Log for visibility
            with st.expander("🔍 View Retrieved Documents (Audit Log)"):
                for i, doc in enumerate(results):
                    st.info(f"Doc {i+1} | Classification: [{doc.metadata['role'].upper()}] | {doc.page_content}")
