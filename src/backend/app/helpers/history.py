MAX_TURNS = 3  # number of user turns to remember

def update_history(history, user_message, assistant_message):
    if history is None:
        history = []

    # append user message
    history.append({"role": "user", "content": user_message})

    # append assistant reply
    history.append({"role": "assistant", "content": assistant_message})

    # trim: keep only last MAX_TURNS user+assistant pairs
    return history[-MAX_TURNS*2:]
