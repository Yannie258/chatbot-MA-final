MAX_TURNS = 10  # number of user turns to remember

import tiktoken

def trim_history(history, model="gpt-4o-mini", max_tokens=2000):
    """Trim history to fit within max_tokens by dropping oldest messages"""
    if not history:
        return []

    enc = tiktoken.encoding_for_model(model)

    total_tokens = 0
    trimmed = []

    # Walk backwards (keep newest first)
    for msg in reversed(history):
        msg_tokens = len(enc.encode(msg["content"]))
        if total_tokens + msg_tokens > max_tokens:
            break
        trimmed.insert(0, msg)  # preserve order
        total_tokens += msg_tokens

    return trimmed

MAX_TURNS = 5  # number of user turns to remember

def update_history(history, user_message, assistant_message, 
                   max_turns=MAX_TURNS, max_tokens=2000, model="gpt-4o-mini"):
    if history is None:
        history = []

    # Append new turn
    history.append({"role": "user", "content": user_message})
    history.append({"role": "assistant", "content": assistant_message})

    history = history[-max_turns*2:]
    # enforce token limit
    history = trim_history(history, model=model, max_tokens=max_tokens)

    return history
