import time
import statistics
from langchain_community.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
import os

# Load the FAISS index
embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
db = FAISS.load_local("vector_index", embeddings, allow_dangerous_deserialization=True)

# Example queries (can add more from your dataset)
queries = [
    "How do I register my residence in Chemnitz?",
    "Where can I get my student ID card?",
    "What is the deadline for course registration?",
    "How do I open a bank account in Germany?",
    "Where can I eat on campus?"
]

timings = []

# Run each query multiple times
for query in queries:
    for _ in range(5):  # repeat to smooth out fluctuations
        start = time.time()
        _ = db.similarity_search(query, k=3)
        end = time.time()
        timings.append((end - start) * 1000)  # convert to ms

# Compute statistics
print(f"Queries run: {len(timings)}")
print(f"Average retrieval time: {statistics.mean(timings):.2f} ms")
print(f"Median retrieval time: {statistics.median(timings):.2f} ms")
print(f"Min retrieval time: {min(timings):.2f} ms")
print(f"Max retrieval time: {max(timings):.2f} ms")
# Run in docker: docker compose run --rm backend python scripts/test_benchmark_faiss.py
