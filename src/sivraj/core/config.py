OLLAMA_MODEL = "qwen2.5-coder:7b"

SYSTEM_PROMPT = """
You are SIVRAJ, an AI command interpreter.

Your job is to interpret the user's request and return ONLY a JSON object
following the SIVRAJ schema.

Available commands:
- maps
- open_app
- system
- none

Rules:

1. Normal conversation:
   - cmd must be "none"
   - show must be null

2. Showing the user's location:
   - cmd must be "maps"
   - show must be "location"

3. Opening an application:
   - cmd must be "open_app"
   - show must be null

4. System commands:
   - cmd must be "system"
   - show must be null

5. If no command is necessary:
   - cmd must be "none"
   - show must be null

6. Never invent commands.

7. The "show" field depends on the "cmd" field.

8. NEVER use "show": "location" when cmd is "none".

9. Return ONLY valid JSON.
10. Do not use Markdown.
11. Do not put the JSON inside ```json code blocks.
12. Do not add explanations before or after the JSON.

Expected structure:

{
    "cmd": "none",
    "response": "Your response here",
    "show": null
}
"""

SCHEMA = {
    "type": "object",

    "required": [
        "cmd",
        "response",
        "show",
    ],

    "properties": {
        "cmd": {
            "type": "string",
            "enum": [
                "maps",
                "open_app",
                "system",
                "none",
            ],
        },

        "response": {
            "type": "string",
        },

        "show": {
            "type": [
                "string",
                "null",
            ],
            "enum": [
                "location",
                None,
            ],
        },
    },

    "additionalProperties": False,

    "allOf": [
        {
            "if": {
                "properties": {
                    "cmd": {
                        "const": "maps",
                    },
                },
            },

            "then": {
                "properties": {
                    "show": {
                        "const": "location",
                    },
                },
            },
        },

        {
            "if": {
                "properties": {
                    "cmd": {
                        "enum": [
                            "open_app",
                            "system",
                            "none",
                        ],
                    },
                },
            },

            "then": {
                "properties": {
                    "show": {
                        "type": "null",
                    },
                },
            },
        },
    ],
}

