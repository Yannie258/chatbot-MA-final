import os
from openai import OpenAI
from models.schemas import ChatResponse
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_response(user_message: str, strategy="plain") -> ChatResponse:
    if strategy == "markdown":
        prompt = f"""You are a helpful assistant. Format your reply using Markdown syntax. Question: {user_message}"""
        content_type = "markdown"

    elif strategy == "json":
        prompt = f"""Return a JSON object. Question: {user_message}"""
        content_type = "json"

    elif strategy == "card":
        prompt = f"""Reply in JSON with this format:\n{{"title": "...", "description": "...", "image_url": "..."}}"""
        content_type = "card"

    elif strategy == "carousel":
        prompt = f"""Reply in JSON as a list of cards like this:\n[{{"title": "...", "description": "...", "image_url": "..."}}]"""
        content_type = "carousel"

    elif strategy == "button":
        prompt = f"""Return a JSON object with 'text' and 'buttons' fields like this:\n{{"text": "...", "buttons": ["Option 1", "Option 2"]}}"""
        content_type = "button"

    elif strategy == "link":
        prompt = f"""Return a JSON object with clickable links like this:\n{{"text": "...", "links": [{{"label": "...", "url": "..."}}]}}"""
        content_type = "link"

    else:
        prompt = f"""You are a helpful assistant. Answer this question: {user_message}"""
        content_type = "text"

    # RAG context (if needed)
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    db = FAISS.load_local("vector_index", embeddings, allow_dangerous_deserialization=True)
    docs = db.similarity_search(user_message, k=3)
    context = "\n".join([doc.page_content for doc in docs])
    prompt = f"""Use the following context to answer:\n{context}\n\n{prompt}"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return ChatResponse(
        role="bot",
        content_type=content_type,
        content=response.choices[0].message.content
    )
