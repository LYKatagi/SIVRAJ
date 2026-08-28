from ollama import chat

from sivraj.core.config import MODEL, SCHEMA


class OllamaClient:
    def generate(self, prompt: str, system: str | None = None) -> str:
        messages = []

        if system:
            messages.append({
                "role": "system",
                "content": system,
            })

        messages.append({
            "role": "user",
            "content": prompt,
        })

        response = chat(
            model=MODEL,
            messages=messages,
            format=SCHEMA,
            options={
                "temperature": 0,
            },
        )

        return response.message.content