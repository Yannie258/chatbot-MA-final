import os, json
from openai import OpenAI
from models.schemas import ChatResponse
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------------------------
# Helpers
# ---------------------------
def _load_vector_db():
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    return FAISS.load_local("vector_index", embeddings, allow_dangerous_deserialization=True)

def _retrieve_context(query: str, k: int = 3) -> str:
    db = _load_vector_db()
    docs = db.similarity_search(query, k=k)
    return "\n".join([doc.page_content for doc in docs])

# ---------------------------
# Dispatcher
# ---------------------------
def generate_response(user_message: str, strategy="plain") -> ChatResponse:
    context = _retrieve_context(user_message)

    if strategy == "plain":
        return generate_response_plain(user_message, context)
    elif strategy == "function":
        return generate_response_structured(user_message, context)
    else:
        raise ValueError(f"Unknown strategy: {strategy}")

# ---------------------------
# Version A – plain
# ---------------------------
def generate_response_plain(user_message: str, context: str) -> ChatResponse:
    prompt = f"""
    You are a helpful student onboarding assistant at TU Chemnitz.
    Use the following context to answer:
    {context}

    Answer the question in **plain natural text** only.

    Style rules:
    - Be clear and concise
    - Use bold headlines
    - Bullet points for lists
    - End with a follow-up suggestion

    Question: {user_message}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return ChatResponse(
        role="bot",
        content_type="text",
        content=response.choices[0].message.content
    )

# ---------------------------
# Version B – structured
# ---------------------------
def generate_response_structured(user_message: str, context: str) -> ChatResponse:
    tools = [{
        "type": "function",
        "function": {
            "name": "create_card",
            "description": "Generate a structured onboarding info card",
            "parameters": {
                "type": "object",
                "properties": {
                    "type": {"type": "string", "enum": ["card"]},
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "action_url": {"type": "string"},
                    "action_label": {"type": "string"}
                },
                "required": ["type", "title", "description", "action_label"]
            }
        }
    }]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a TU Chemnitz onboarding assistant."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {user_message}"}
        ],
        tools=tools,
        tool_choice={"type": "function", "function": {"name": "create_card"}},
        temperature=0.2
    )

    tool_calls = response.choices[0].message.tool_calls
    if tool_calls:
        raw_output = tool_calls[0].function.arguments
        try:
            parsed_output = json.loads(raw_output)
        except json.JSONDecodeError:
            parsed_output = {"error": "Invalid JSON", "raw": raw_output}
    else:
        parsed_output = {"error": "No function call produced"}

    return ChatResponse(
        role="bot",
        content_type="json",
        content=parsed_output
    )
