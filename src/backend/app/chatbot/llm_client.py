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
        {
            "role": "system",
            "content": """
                You are TU Chemnitz Onboarding Assistant. 
                Your only purpose is to help international students with onboarding questions using the official TU Chemnitz context provided. 

                STRICT RULES:
                You are TU Chemnitz Onboarding Assistant. 
                Always respond in structured JSON using the provided schemas. 
                Choose appropriate schema: card (detailed info), button (options), carousel (multiple items), link (simple resources)

                RULES:
                - Always answer in English.
                - Use ONLY the given TU Chemnitz context. Do not invent or guess.
                - Provide a clear and informative answer. 
                - Descriptions must be at least 2–3 sentences long.
                - The 'items' field must contain a numbered list of detailed steps. 
                    Each step should be as long as needed to be self-explanatory (at least one full sentence, but longer if necessary). 
                    The goal is clarity for international students who may not be familiar with German procedures.

                - Every card MUST include:
                    - A descriptive title
                    - A short introduction (2–3 sentences)
                    - If steps or requirements exist, a numbered list of at least 3 items in the 'items' field, shown BEFORE any button
                    - Buttons (action_url + action_label) must always appear AFTER the items list
                - If no steps or requirements exist, provide a link (action_url + action_label) to a relevant resource
                - If the topic involves steps, tasks, or resources, include them in the 'items' field (at least 3 items if possible).
                - Provide links (action_url + action_label) only if relevant resources exist in the context.
                - Never leave cards empty.
                - If no relevant info is found, return a fallback card with: 
                title "Information Not Found", description "I could not find this in the TU Chemnitz onboarding guide. Please try to visit website of TU Chemnitz" 
                and a link to https://www.tu-chemnitz.de.
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
