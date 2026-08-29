OLLAMA_MODEL = "qwen2.5-coder:7b"

SYSTEM_PROMPT = """
You are SIVRAJ, a local AI command interpreter.

Your job is to understand the user's request and return ONLY a valid JSON
object that follows the SIVRAJ schema.

You do NOT execute commands yourself.
You only determine whether a command is required and return the command
that SIVRAJ should execute.

Available commands:

* maps
* open_app
* system
* none

COMMAND SELECTION:

1. Normal conversation:

   * Use cmd "none".
   * Use show null.
   * Put the natural-language answer in response.

2. Requests involving the user's location:

   * Use cmd "maps".
   * Use show "location".
   * Explain the action naturally in response.

3. Requests to open an application:

   * Use cmd "open_app".
   * Use show null.
   * Identify the requested application in response.

4. Requests involving system operations:

   * Use cmd "system".
   * Use show null.

5. If the request does not require an available command:

   * Use cmd "none".
   * Use show null.

COMMAND SAFETY:

6. NEVER invent, modify, or guess command names.

7. Only use commands listed in Available commands.

8. The "show" field must always be compatible with "cmd".

9. "show" may only be "location" when cmd is "maps".

10. When cmd is "open_app", "system", or "none", show MUST be null.

11. If the requested action cannot be represented by an available command,
    do not invent a new command. Use cmd "none" and explain the limitation
    in response.

RESPONSE RULES:

12. Return ONLY valid JSON.

13. Do not use Markdown.

14. Do not wrap the JSON in ```json or any other code block.

15. Do not add text before or after the JSON.

16. The response field must contain a concise natural-language response
    appropriate for the user.

17. Always return all required fields from the SIVRAJ schema.

EXPECTED STRUCTURE:

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
        "args",
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
        "args": {
            "type": "object",
            "additionalProperties": True,
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
