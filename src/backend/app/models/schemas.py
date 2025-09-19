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
                        "items": {"type": "string"},
                        "description": "Each item must be a clear, detailed step with enough explanation so that an international student could follow it without guessing. Avoid one-word or vague answers."
                    },
                    "action_url": {
                        "type": "string",
                        "description": "Optional link to relevant resource"
                    },
                    "action_label": {
                        "type": "string",
                        "description": "Optional button text for action_url"
                    },
                    "follow_up_options": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Suggested next questions as quick reply buttons"
                    }

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
                    },
                    "follow_up_options": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Suggested next questions as quick reply buttons"
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
                                "action_label": {"type": "string"},
                            },
                            "required": ["title", "description"]
                        }
                    },
                    "follow_up": {
                                    "type": "object",
                                    "properties": {
                                        "title": {"type": "string", "enum":["carousel"]},
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
            "name": "create_link_list",
            "description": "Generate a list of structured links",
            "parameters": {
                "type": "object",
                "properties": {
                    "type": {"type": "string", "enum": ["link"]},
                    "label": {"type": "string"},
                    "links": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "label": {"type": "string"},
                                "url": {"type": "string"}
                            },
                            "required": ["label", "url"]
                        }
                    }
                },
                "required": ["type", "links"]
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
