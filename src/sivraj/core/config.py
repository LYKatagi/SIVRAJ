MODEL = "qwen2.5-coder:7b"


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

