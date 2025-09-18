import os
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

def test_query(query, index_path="vector_index"):
    # Load embeddings + FAISS index
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    db = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)

    # Search top 3 chunks
    docs = db.similarity_search(query, k=3)

    print(f"\n🔎 Query: {query}\n")
    for i, doc in enumerate(docs, start=1):
        print(f"--- Result {i} ---")
        print(doc.page_content[:500])  # print first 500 chars
        print(f"[Source: {doc.metadata}]\n")

if __name__ == "__main__":
    test_query("How to apply to TU Chemnitz?")
    test_query("Where can I register my residence?")
