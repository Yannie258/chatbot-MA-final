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
        return generate_response_plain(user_message, context, history)
    elif strategy == "function":
        return generate_response_structured(user_message, context, history)
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
        - Always respond in structured JSON using the provided schemas.
        - Choose the schema that best fits the question:
            • Use "card" when the answer requires detailed explanation with steps and an action link.  
            • Use "button" (quick replies) when the user should select one option from 2–5 choices.  
            • Use "carousel" when multiple related items should be shown side by side (e.g., dorms, cafeterias).  
            • Use "link" when only a single resource is relevant.  

        GENERAL INSTRUCTIONS:
        - Always answer in English.
        - Use ONLY the given TU Chemnitz context. Do not invent or guess.
        - Descriptions must be at least 2–3 sentences long.
        - For cards: if steps or requirements exist, include at least 3 numbered items in the 'items' field. 
        - Buttons must always have clear labels, not too long (max 4 words).
        - Carousels must contain at least 2 cards, each with its own title and description.
        - Every response must include a "follow_up" field.
        - The follow_up should be a short, friendly suggestion that keeps the conversation going.
        - It must be context-specific (related to the topic in the card).
        - Avoid generic questions like "What information are you looking for?".
        - Example follow_up: 
            "Would you like me to also explain how to register your residence?",
            "Do you want me to show the deadlines for enrollment?",
            "Should I provide housing options too?"
        - If the question is vague or too broad, respond with buttons suggesting specific topics.
        - If no relevant info is found, return a fallback card:
          { "type": "card", "title": "Information Not Found", 
            "description": "I could not find this in the TU Chemnitz onboarding guide. Please visit TU Chemnitz website.", 
            "action_url": "https://www.tu-chemnitz.de", 
            "action_label": "Visit Website" }

        FOLLOW-UP RULES:
        - If follow-up is needed, provide specific options in the "follow_up_options" field as an array of strings
        - Options should be clear, 2–5 words each (max 4 items)
        - Avoid generic options like "yes" or "no"

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
