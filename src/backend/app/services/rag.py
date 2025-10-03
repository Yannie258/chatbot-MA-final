import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings

def _load_vector_db():
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    return FAISS.load_local("vector_index", embeddings, allow_dangerous_deserialization=True)

def retrieve_context(query: str, k: int = 5) -> str:
    """Retrieve relevant document chunks for user query"""
    vector_db = _load_vector_db()
    relevant_docs = vector_db.similarity_search(query, k=k)
    return [doc.page_content for doc in relevant_docs]
