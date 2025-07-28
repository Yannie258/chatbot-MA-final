import os
from openai import OpenAI
from models.schemas import ChatResponse
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_response(user_message: str) -> ChatResponse:
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    db = FAISS.load_local("vector_index", embeddings, allow_dangerous_deserialization=True)

    docs = db.similarity_search(user_message, k=3)
    context = "\n".join([doc.page_content for doc in docs])

    prompt = f"""You are a helpful assistant. Use the following context to answer:

Context:
{context}

User Question:
{user_message}

Reply using markdown if suitable."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return ChatResponse(
        role="bot",
        content_type="markdown",
        content=response.choices[0].message.content
    )
