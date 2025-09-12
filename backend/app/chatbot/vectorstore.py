from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
import os

def load_vector_db():
    """Load FAISS vector index for runtime query processing"""
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    return FAISS.load_local("vector_index", embeddings, allow_dangerous_deserialization=True)

def retrieve_context(query: str, db: FAISS, k: int = 3):
    """Retrieve top-k relevant chunks for query"""
    relevant_docs = db.similarity_search(query, k=k)
    return "\n".join([doc.page_content for doc in relevant_docs])
