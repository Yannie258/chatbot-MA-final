def get_card_schema():
    return {
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
    }

def get_button_schema():
    return {
        "type": "function",
        "function": {
            "name": "create_buttons",
            "description": "Generate quick reply buttons with labels",
            "parameters": {
                "type": "object",
                "properties": {
                    "type": {"type": "string", "enum": ["button"]},
                    "title": {"type": "string"},
                    "options": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                },
                "required": ["type", "title", "options"]
            }
        }
    }

def get_carousel_schema():
    return {
        "type": "function",
        "function": {
            "name": "create_carousel",
            "description": "Generate a carousel with multiple cards",
            "parameters": {
                "type": "object",
                "properties": {
                    "type": {"type": "string", "enum": ["carousel"]},
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "title": {"type": "string"},
                                "description": {"type": "string"},
                                "action_url": {"type": "string"},
                                "action_label": {"type": "string"}
                            },
                            "required": ["title", "description"]
                        }
                    }
                },
                "required": ["type", "items"]
            }
        }
    }

def get_link_schema():
    return {
        "type": "function",
        "function": {
            "name": "create_link",
            "description": "Generate a structured link element",
            "parameters": {
                "type": "object",
                "properties": {
                    "type": {"type": "string", "enum": ["link"]},
                    "label": {"type": "string"},
                    "url": {"type": "string"}
                },
                "required": ["type", "label", "url"]
            }
        }
    }

def get_all_schemas():
    return [
        get_card_schema(),
        get_button_schema(),
        get_carousel_schema(),
        get_link_schema()
    ]
