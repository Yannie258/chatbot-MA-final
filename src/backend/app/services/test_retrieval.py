import os, time, statistics
from rag import retrieve_context

QUERIES = [
    "How to apply to TU Chemnitz?",
    "Where can I register my residence?",
    "How to get my student ID?",
    "Where is the International Office located?",
    "How can I extend my visa?"
]

def benchmark_retrieve_context(log_file="retrieval_benchmark.log"):
    latencies = []
    with open(log_file, "w", encoding="utf-8") as f:
        for q in QUERIES:
            start = time.time()
            results = retrieve_context(q, k=3)
            elapsed = (time.time() - start) * 1000  # milliseconds
            latencies.append(elapsed)
            
            f.write(f"🔎 Query: {q}\nLatency: {elapsed:.2f} ms\n")
            f.write(f"Top result: {results[0][:150]}...\n\n")
            print(f"{q} → {elapsed:.2f} ms")

    mean = statistics.mean(latencies)
    median = statistics.median(latencies)
    print(f"\nAverage latency: {mean:.2f} ms | Median: {median:.2f} ms")
    print(f"Range: {min(latencies):.2f}–{max(latencies):.2f} ms")

if __name__ == "__main__":
    benchmark_retrieve_context()
