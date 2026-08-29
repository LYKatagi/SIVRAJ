import json
from typing import Any

import ollama

from sivraj.ai.schema import Schema
from sivraj.core.config import OLLAMA_MODEL, SYSTEM_PROMPT


class OllamaError(Exception):
    """Base exception for SIVRAJ Ollama errors."""


class OllamaConnectionError(OllamaError):
    """Raised when SIVRAJ cannot communicate with Ollama."""


class OllamaResponseError(OllamaError):
    """Raised when Ollama returns an invalid response."""


class OllamaClient:
    """Client responsible for communicating with the local Ollama server."""

    def __init__(
        self,
        model: str = OLLAMA_MODEL,
        client: ollama.Client | None = None,
    ) -> None:
        self.model = model
        self.client = client or ollama.Client()

    def generate(self, prompt: str) -> dict[str, Any]:
        """
        Send a user prompt to Ollama and return a validated SIVRAJ response.

        Raises:
            ValueError: If prompt is empty.
            OllamaConnectionError: If Ollama cannot be reached.
            OllamaResponseError: If the model returns invalid JSON or
                invalid SIVRAJ data.
        """

        if not isinstance(prompt, str):
            raise ValueError("Prompt must be a string.")

        prompt = prompt.strip()

        if not prompt:
            raise ValueError("Prompt cannot be empty.")

        try:
            response = self.client.chat(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT,
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                format="json",
                options={
                    "temperature": 0,
                },
            )

        except Exception as error:
            raise OllamaConnectionError(
                f"Failed to communicate with Ollama: {error}"
            ) from error

        raw_content = self._extract_content(response)

        data = self._parse_json(raw_content)

        if not Schema.validate_data(data):
            raise OllamaResponseError("Ollama returned an invalid SIVRAJ response")

        return data

    @staticmethod
    def _extract_content(response: Any) -> str:
        """Extract the assistant content from an Ollama response."""

        try:
            content = response["message"]["content"]
        except (KeyError, TypeError):
            try:
                content = response.message.content
            except AttributeError as error:
                raise OllamaResponseError(
                    "Ollama returned an unexpected response format."
                ) from error

        if not isinstance(content, str) or not content.strip():
            raise OllamaResponseError("Ollama returned an empty response.")

        return content.strip()

    @staticmethod
    def _parse_json(content: str) -> dict[str, Any]:
        """Parse the model response as JSON."""

        try:
            data = json.loads(content)
        except json.JSONDecodeError as error:
            raise OllamaResponseError("Ollama returned invalid JSON.") from error

        if not isinstance(data, dict):
            raise OllamaResponseError("Ollama response must be a JSON object.")

        return data
