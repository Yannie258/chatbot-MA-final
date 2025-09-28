import os
import glob
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

def build_index(data_dir="data", index_path="vector_index"):
    documents = []
    for pdf_path in glob.glob(os.path.join(data_dir, "*.pdf")):
        loader = PyMuPDFLoader(pdf_path)
        docs = loader.load()
        documents.extend(docs)
        print(f"Loaded {pdf_path} with {len(docs)} pages")

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    db = FAISS.from_documents(chunks, embeddings)

    db.save_local(index_path)
    print(f"Index saved at {index_path} with {len(chunks)} chunks")

if __name__ == "__main__":
    build_index()
