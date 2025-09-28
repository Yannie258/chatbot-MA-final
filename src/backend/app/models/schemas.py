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
                    "items": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "action_url": {"type": "string"},
                    "action_label": {"type": "string"},
                    "follow_up_options": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "options": {
                                "type": "array",
                                "items": {"type": "string"}
                            }
                        },
                        "required": ["title", "options"] 
                    }
                },
                "required": ["type", "title", "description"]
            }
        }
    }

def get_button_schema():
    return {
        "type": "function",
        "function": {
            "name": "create_buttons",
            "description": "Generate quick reply buttons for user selection",
            "parameters": {
                "type": "object",
                "properties": {
                    "type": {"type": "string", "enum": ["button"]},
                    "title": {"type": "string"},
                    "description": {
                        "type": "string",
                        "description": "Brief context or instruction"
                    },
                    "options": {
                        "type": "array",
                        "items": {"type": "string"},
                        "minItems": 2,
                        "maxItems": 5,
                        "description": "Clear, actionable button labels"
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
            "description": "Brief description or follow-up encouragement",
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
                                "action_label": {"type": "string"},
                                
                            },
                            "required": ["title", "description"]
                        },
                        "description": "At least 2 cards with distinct information"
                    },
                    "follow_up_options": {
                                    "type": "object",
                                    "properties": {
                                        "title": {"type": "string"},
                                        "options": {
                                            "type": "array",
                                            "items": {"type": "string"},
                                            "minItems": 2,
                                            "maxItems": 5
                                        }
                                    },
                                    "required": ["title", "options"]
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
            "description": "Generate a structured list of relevant links (max 3)",
            "parameters": {
                "type": "object",
                "properties": {
                    "type": {"type": "string", "enum": ["link","links"]},
                    "label": {"type": "string", "description": "Title for the link group (e.g., 'Enrollment Resources')"},
                    "description": {
                        "type": "string", 
                        "description": "Brief description encouraging further questions"
                    },
                    "links": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "label": {"type": "string"},
                                "url": {"type": "string"}
                            },
                            "required": ["label", "url"]
                        },
                        "minItems": 1,
                        "maxItems": 3
                    }
                },
                "required": ["type", "links", "link"]
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
