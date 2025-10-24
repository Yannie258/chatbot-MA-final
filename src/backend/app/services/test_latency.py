import sys, os, time, statistics

CURRENT_DIR = os.path.dirname(__file__)
APP_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(APP_DIR)

from chatbot.llm_client import generate_response

QUERIES = [
    "How can I apply to TU Chemnitz?",
    "Where can I register my residence in Chemnitz?",
    "What documents are required for enrollment?",
    "How can I get my student ID card?",
    "Where is the International Office located?",
    "How can I extend my visa in Chemnitz?",
    "How to find student accommodation near the campus?",
    "Who can help with health insurance for students?",
    "When is the residence registration deadline?",
    "How can I contact the Student Service Center?"
]

def benchmark(strategy="plain", log_file=None):
    latencies = []
    if log_file is None:
        log_file = f"chatbot_latency_{strategy}.log"

    with open(log_file, "w", encoding="utf-8") as f:
        for q in QUERIES:
            print(f"\n🔹 {q}")
            start = time.time()
            res = generate_response(q, strategy=strategy)
            elapsed = (time.time() - start) * 1000
            latencies.append(elapsed)
            f.write(f"Query: {q}\nLatency: {elapsed:.2f} ms\nResponse preview: {str(res.content)[:200]}\n\n")
            print(f" {strategy}: {elapsed:.2f} ms")

    mean, median = statistics.mean(latencies), statistics.median(latencies)
    print(f"\n{strategy.upper()} SUMMARY")
    print(f"Mean: {mean:.2f} ms | Median: {median:.2f} ms | Range: {min(latencies):.2f}-{max(latencies):.2f} ms")

if __name__ == "__main__":
    print(" Running 10 queries for both chatbot versions...")
    benchmark("plain")
    benchmark("function")
