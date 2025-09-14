import logging
import os, json
from openai import OpenAI
from models.chat_response import ChatResponse
from models.schemas import get_all_schemas
from services.rag import retrieve_context

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------------------------
# Dispatcher
# ---------------------------
def generate_response(user_message: str, strategy="plain") -> ChatResponse:
    context = retrieve_context(user_message)
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

    Answer in **plain natural text** only.
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

# Configure logging
logging.basicConfig(level=logging.INFO)
# ---------------------------
# Version B – structured
# ---------------------------
def generate_response_structured(user_message: str, context: str) -> ChatResponse:
    tools = get_all_schemas()  # load schemas

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a TU Chemnitz onboarding assistant. Use the best structured format (card, button, carousel, link)."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {user_message}"}
        ],
        tools=tools,
        tool_choice="auto",  # let model pick
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
        content_type=parsed_output.get("type", "json"),
        content=parsed_output
    )
