
import json

from ollama import chat

from sivraj.ai.schema import Schema
from sivraj.core.config import MODEL, SCHEMA


class OllamaClient:
    def __init__(self, model: str = MODEL) -> None:
        self.model = model

    def generate(self, prompt: str) -> dict:
        response = chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            format=SCHEMA,
            options={
                "temperature": 0,
            },
        )

        data = json.loads(response.message.content)

        if not Schema.validate_data(data):
            raise ValueError("Ollama returned an invalid SIVRAJ response")

        return data

