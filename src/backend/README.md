# Testing the Retrieval Module (FAISS Benchmark)

To verify that the Retrieval-Augmented Generation (RAG) indexing and retrieval pipeline works correctly, you can run the retrieval test script directly inside the backend environment.

## 1️⃣ Prerequisites

Ensure that the FAISS index has been generated and stored in:

app/vector_index/
├── index.faiss
└── index.pkl


Your .env file must contain a valid OPENAI_API_KEY.

## 2️⃣ Run the Retrieval Test

From the root of the backend (/app) directory, execute:
``` bash
cd /app
python3 services/test_retrieval.py
```

**💡 Important:**
Do not run the test from inside /app/services/,
because FAISS expects the vector_index directory to be found relative to the working directory (/app/vector_index).

## Running Inside Docker

If the backend runs in Docker, execute the following from your host machine:

```bash
# go to backend container
docker exec -it chatbot_ma_thesis-backend-1 bash

python3 services/test_retrieval.py
```

- You can find the container name using:
``` bash
docker ps
```
**Log Output:**

- A log file named retrieval_benchmark.log is automatically generated 
- This file contains detailed timing and similarity retrieval results that can be referenced in performance documentation or appendices.

### Run build_index:
If the backend runs in Docker, execute the following from your host machine:

```bash
# go to backend container
docker exec -it chatbot_ma_thesis-backend-1 bash
python3 scripts/build_index.py
```

- This command runs the indexing pipeline that processes all PDF documents inside the data/ directory.
- The console output will display the number of PDF files loaded, their total page count, and the total number of text chunks created