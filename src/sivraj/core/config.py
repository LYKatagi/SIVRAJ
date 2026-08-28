
SCHEMA = {
    "type": "object",
    "required": ["cmd", "response", "show"],
    "properties": {
        "cmd": {
            "type": "string",
            "enum": ["maps", "open_app", "system", "none"]
        },
        "response": {
            "type": "string"
        },
        "show": {
            "type": ["string", "null"],
            "enum": ["location", None]
        }
    },
    "additionalProperties": False
}