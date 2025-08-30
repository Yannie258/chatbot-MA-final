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
        prompt = f"""You are a helpful assistant. Reply with a JSON object like this:\n\n{{
            "title": "Card title",
            "description": "Description of the card",
            "image_url": "https://www.tu-chemnitz.de/tu/aktuelles/2025/1753698184-13054-0.jpg",
            "action_url": "https://www.tu-chemnitz.de/studiportal/",
            "action_label": "More Info"
            }}\n\n Only include 'image_url' if relevant. Answer the question using this format, without markdown or code formatting.\n\nQuestion: {user_message}"""
        content_type = "card"

    elif strategy == "carousel":
        prompt = f"""You are a helpful assistant. Based on the following context, reply in JSON as a list of cards. Each card should include a 'title', a 'description', and — if possible — an 'image_url' that is relevant to the topic. If the PDF context provides no image, you can use a placeholder or leave the 'image_url' empty.

        Format:
        [
        {{
            "title": "...",
            "description": "...",
            "image_url": "https://www.tu-chemnitz/.../image.jpg"  # or findout in pdf RAG or leave "https://www.tu-chemnitz.de/studierendenservice/images/Kopfbild_04.png" if no image is available
            "url": "https://example.com"
        }},
        ...
        ]

        Question: {user_message}
        """

        content_type = "carousel"

    elif strategy == "button":
        prompt = f"""Return a JSON object like this:
        {{
        "text": "your main response here",
        "buttons": ["Option 1", "Option 2", "Option 3"]
        }}
        User Question: {user_message}"""
        content_type = "button"

    elif strategy == "link":
        prompt = f"""Return a JSON object with clickable links like this and translate in english :\n{{"text": "...", "links": [{{"label": "...", "url": "..."}}]}}"""
        content_type = "link"

    elif strategy == "plain":
        prompt = f"""You are a helpful assistant. Answer this question: {user_message}"""
        content_type = "text"

    else:
        raise ValueError(f"Unknown strategy: {strategy}")

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
