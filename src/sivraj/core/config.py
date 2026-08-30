
from pathlib import Path


# ============================================================
# Paths
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

SYSTEM_PROMPT_PATH = BASE_DIR / "prompt" / "system.txt"


# ============================================================
# AI
# ============================================================

OLLAMA_MODEL = "qwen2.5-coder:7b"


# ============================================================
# System Prompt
# ============================================================

if not SYSTEM_PROMPT_PATH.is_file():
    raise FileNotFoundError(
        f"System prompt not found: {SYSTEM_PROMPT_PATH}"
    )

SYSTEM_PROMPT = SYSTEM_PROMPT_PATH.read_text(
    encoding="utf-8"
)


# ============================================================
# SIVRAJ Response Schema
# ============================================================

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

