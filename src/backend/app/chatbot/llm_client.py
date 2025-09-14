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
def generate_response(user_message: str, strategy="plain", history=None) -> ChatResponse:
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
def generate_response_plain(user_message: str, context: str, history = None) -> ChatResponse:
    messages = [{"role": "system", "content": "You are a helpful TU Chemnitz onboarding assistant."}]
    prompt = f"""
    You are a helpful student onboarding assistant at TU Chemnitz.
    Use the following context to answer:
    {context}

    Answer in **plain natural text** only.
    - in English
    - Be clear and concise
    - Use bold headlines
    - Bullet points for lists
    - End with a follow-up suggestion

    Question: {user_message}
    """
    if history:
        messages.extend(history)   # keep conversation memory

    messages.append({
        "role": "user",
        "content": prompt
    })

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
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
def generate_response_structured(user_message: str, context: str, history=None) -> ChatResponse:
    tools = get_all_schemas()  # load schemas
    messages = [
        {"role": "system", "content": """
            You are a TU Chemnitz onboarding assistant.
            Always respond in structured JSON using the provided schemas.
            - Answer in English.
            - Use the context to answer the question.  
            - If the answer contains multiple steps, tasks, or recommendations, use the 'items' field in cards as a bullet list.
            - The 'description' should be a short summary (1–2 sentences), not the full content.
            - Use 'items' for detailed lists of steps or options.
            - Include an 'action_url' and 'action_label' only if there is a relevant official resource (avoid irrelevant buttons).
            - Do not leave cards empty; always provide informative content.
            """
        }

    ]

    if history:
        messages.extend(history)   # keep conversation memory

    # Add the new user query with context
    messages.append({
        "role": "user",
        "content": f"Context:\n{context}\n\nQuestion: {user_message}"
    })

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools,
        tool_choice="auto",  # let model pick schema
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
