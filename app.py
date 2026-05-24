import streamlit as st
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document


def expand_query(query, llm):
    prompt = f"Expand this search query with 2-3 synonyms/related terms. Return ONLY the expanded query:\nQuery: {query}\nExpanded:"
    return llm.invoke(prompt)


st.set_page_config(
    page_title="Agentic RAG with RBAC",
    page_icon=None,
    layout="centered"
)

st.title("Agentic RAG with RBAC")
st.write("Production grade RAG with Role Based Access Control using local Llama3.")

role = st.selectbox("Select your role:", ["junior", "executive", "director"])

@st.cache_resource
def load_components():
    embeddings = OllamaEmbeddings(model="llama3")
    llm = Ollama(model="llama3")
    db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
    return embeddings, llm, db

embeddings, llm, db = load_components()
if "messages" not in st.session_state:
    st.session_state.messages = []
query = st.text_input("Ask a question about company data:")

if st.button("Search") and query:
    with st.spinner("Searching securely..."):
        role_hierarchy = {
            "junior": ["junior"],
            "executive": ["junior", "executive"],
            "director": ["junior", "executive", "director"]
        }
        allowed_roles = role_hierarchy.get(role, [])
        query = expand_query(query, llm)  

        #hybrid search 
        collection = db._collection
        query_embedding = embeddings.embed_query(query)
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=5,
            where={"role": {"$in": allowed_roles}},
            include=["documents", "metadatas"]
        )
        docs = [Document(page_content=d, metadata=m) for d, m in zip(results["documents"][0], results["metadatas"][0])]
        context = "\n".join([doc.page_content for doc in docs])



        if not context:
            st.warning("No internal docs found. Falling back to general AI knowledge...")
            response = llm.invoke(query)
            st.success("Response (General Knowledge)")
            st.write(response)
        else:
            prompt = PromptTemplate(
                template="Answer ONLY from this context:\n{context}\nQuestion: {query}\nAnswer:",
                input_variables=["context", "query"]
            )
            response = llm.invoke(prompt.format(context=context, query=query))
            st.success("Response (Secure Documents)")
            st.write(response)

            with st.expander("🔍 Retrieved Documents (Audit Log)"):
                for i, doc in enumerate(docs):
                    st.info(f"**Doc {i+1}** | Role: `{doc.metadata['role'].upper()}` | Content: {doc.page_content}")
