import logging
import os, json
import time
from openai import OpenAI
from models.chat_response import ChatResponse
from models.schemas import get_all_schemas
from services.rag import retrieve_context

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------------------------
# Dispatcher
# ---------------------------
def generate_response(user_message: str, strategy="plain", history=None) -> ChatResponse:
    
    logging.info(f"{'='*80}")
    logging.info(f"🔍 generate_response() CALLED")
    logging.info(f"  - user_message: {user_message[:100]}")
    logging.info(f"  - strategy: {strategy}")
    logging.info(f"  - history type: {type(history)}")
    logging.info(f"  - history is None: {history is None}")
    logging.info(f"  - history value: {history}")
    logging.info(f"{'='*80}\n")

    # Defensive check — handle pydantic model list
    if history and not isinstance(history[0], dict):
        history = [h.dict() for h in history]
        
    context = retrieve_context(user_message)
    
    start_time = time.time()
    
    if strategy == "plain":
        response = generate_response_plain(user_message, context, history)
    elif strategy == "function":
        response = generate_response_structured(user_message, context, history)
    else:
        raise ValueError(f"Unknown strategy: {strategy}")
    
    duration = time.time() - start_time
    logging.info(f"Response generated in {duration*1000:.2f}ms using {strategy} strategy")
    
    return response

# ---------------------------
# Version A – plain
# ---------------------------
def generate_response_plain(user_message: str, context: str, history = None) -> ChatResponse:
    messages = [{"role": "system", "content": "You are a helpful TU Chemnitz onboarding assistant."}]
    
    # Log history
    previous_context = ""
    if history:
        cleaned_history = []
        for msg in history:
            role = msg.get("role", "").lower().strip()
            content = msg.get("content", "")
            if isinstance(content, dict):
                content = str(content)
            if role in ("user", "assistant") and content:
                cleaned_history.append({"role": role, "content": content})
        if cleaned_history:
            cleaned_history = cleaned_history[-8:]  # keep last 8 turns
            messages.extend(cleaned_history)
            logging.info(f"✅ HISTORY ADDED TO MESSAGES: {len(cleaned_history)} messages")
        else:
            logging.info(f"⚠️ HISTORY EXISTS BUT EMPTY AFTER CLEANING")
    else:
        logging.info(f"⚠️ NO HISTORY TO ADD")

    previous_context = ""
    if history:
        for h in history[-4:]:  # include last 4 turns in text form
            role = h.get("role")
            content = h.get("content")
            if role == "user":
                previous_context += f"\nUser: {content}"
            elif role == "assistant":
                previous_context += f"\nAssistant: {content}"
    
    prompt = f"""
    You are TU Chemnitz Onboarding Assistant. 
    Your only purpose is to help international students with onboarding questions using the official TU Chemnitz context provided. 
    Use the following context to answer:
    {context}

    RESPONSE RULES:
    - Answer in English, clear and conversational
    - If context doesn't have the info, say so clearly
    - Match the user's tone (formal or casual)
    - Be concise and helpful

    FORMATTING RULES (FOLLOW EXACTLY):
    - Use ## for main section headings
    - Use bold (**text**) sparingly, only for emphasis within sentences
    - Separate paragraphs with SINGLE newline (\\n), never double (\\n\\n)
    - No blank lines anywhere in the response
    - Keep responses clear, concise, and scannable
    - End with a follow-up suggestion
    - No numbered lists unless specifically asked

    LINKS (IMPORTANT):
    - Format links as: [descriptive text](URL)
    - Always include the full URL with https:// 
    - If user needs a link to city services for example for residence registration (Anmeldung), provide this link: https://www.chemnitz.de/en/town-hall/office-service/citizen-service-centres
    - Alternative the link for city service and form:  https://www.chemnitz.de/en/rathaus/services-portal-and-forms
    - If user needs a link to course catalogue of TU Chemnitz, provide this link: https://www.tu-chemnitz.de/studierendenservice/zsb/studiengaenge/index.html.en

    Question: {user_message}
    """

    messages.append({
        "role": "user",
        "content": prompt
    })

    # Log what's being sent to OpenAI
    logging.info(f"\n📤 TOTAL MESSAGES SENT TO OPENAI: {len(messages)}")
    for i, msg in enumerate(messages, 1):
        logging.info(f"  [{i}] role={msg['role']}, content_length={len(msg['content'])} chars")
    logging.info(f"{'='*80}\n")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.2
    )

    msg_content = response.choices[0].message.content
    logging.info(f"RAW OpenAI content type={type(msg_content)} value={repr(msg_content)}")
    # Log history
    # 🔹 Update history with this turn
    updated_history = history.copy() if history else []
    updated_history.append({"role": "user", "content": user_message})
    updated_history.append({"role": "assistant", "content": msg_content})

    # ✅ Return full structured ChatResponse
    return ChatResponse(
        role="bot",
        content_type="text",
        content=msg_content,
        history=updated_history,
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


        FUNCTION SELECTION GUIDELINES:
            Choose the appropriate function based on the user's question:

            Use create_card when:
            - User asks "How to..." questions requiring step-by-step processes
            - Detailed explanations with procedures, requirements needed
            - Examples: "How do I register?", "What documents do I need?"

            Use create_buttons when:
            - User asks broad/vague questions needing clarification
            - Multiple topics available for selection (2-5 options)
            - Examples: "Tell me about housing", "I need help"

            Use create_carousel when:
            - User asks about multiple similar items for comparison
            - Questions about options, types, varieties
            - Examples: "What housing options?", "Show meal plans"
            - MANDATORY: Each carousel item MUST include action_url and action_label when relevant links exist

            Use create_link when:
            - Use `create_link` when providing one or more links (1–3).  
            - Always set `"type": "link"`.  
            - Include `"label"`, `"description"`, and an array `"links"` with objects containing `"label"` and `"url"`.
            - Use 'links' when specific resources/forms are needed (can be single or multiple related links).
            - Link examples:
                - Single: "Where is the application form?" → one link
                - Multiple: "I need enrollment documents" → application form, fee payment, document checklist
            - Include a helpful description encouraging further questions:
                - Example: "Here are the enrollment resources. Feel free to ask if you need help with specific forms or procedures."

            
        LINK REQUIREMENTS:
        - For carousels: Each item should have action_url and action_label when a relevant link exists
        - For cards: Include action_url and action_label for primary related resource
        - Use descriptive action labels:
          - SHOULD use:  "View Program Details", "Download Application", "Check Requirements"
          - NOT use: "Learn More", "Click Here", "Read More"
        - Prefer official TU Chemnitz pages over generic information
        - Always include the full URL with https:// 
        - If user needs a link to city services for example for residence registration (Anmeldung), provide this link: https://www.chemnitz.de/en/town-hall/office-service/citizen-service-centres
        - Alternative the link for city service and form:  https://www.chemnitz.de/en/rathaus/services-portal-and-forms
        - If user needs a link to course catalogue of TU Chemnitz, provide this link: https://www.tu-chemnitz.de/studierendenservice/zsb/studiengaenge/index.html.en

        
        GENERAL INSTRUCTIONS:
        - Always answer in English.
        - Use ONLY the given TU Chemnitz context. Do not invent or guess.
        - Descriptions must be at least 2–3 sentences long.
        - For cards: if steps or requirements exist, include at least 3 numbered items in the 'items' field and there is title (bold) for every item
        - Buttons must always have clear labels, not too long (max 4 words).
        - Carousels must contain at least 2 cards, each with its own title and description.
        - Every response must include a "follow_up_option" field.
        - The follow_up_option should be a short, friendly suggestion that keeps the conversation going.
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

    # normalize type for frontend ContentType enum
    resp_type = parsed_output.get("type", "text").lower()

    # Map schema type to FE ContentType
    type_map = {
        "card": "card",
        "button": "button",
        "carousel": "carousel",
        "link": "link"
    }

    return ChatResponse(
        role="bot",
        content_type=type_map.get(resp_type,'json'),
        content=parsed_output,
        history=history
    )

