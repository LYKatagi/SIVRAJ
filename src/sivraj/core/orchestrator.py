
from typing import Any

from sivraj.ai.ollama import OllamaClient
from sivraj.ai.schema import Schema
from sivraj.core.router import CommandRouter


class Orchestrator:
    """Coordena o pipeline principal do SIVRAJ."""

    def __init__(
        self,
        ollama: OllamaClient,
        router: CommandRouter,
    ) -> None:
        self.ollama = ollama
        self.router = router

    def process(self, prompt: str) -> dict[str, Any]:
        """
        Processa uma entrada do usuário através da pipeline:

        Input → Ollama → Schema → Router → Command
        """

        if not isinstance(prompt, str):
            raise TypeError("Prompt must be a string.")

        if not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        # 1. IA interpreta a entrada
        response = self.ollama.generate(prompt)

        # 2. Valida a resposta da IA
        if not Schema.validate_data(response):
            raise ValueError(
                "Ollama returned an invalid SIVRAJ response."
            )

        # 3. Comandos que não precisam ser executados
        if response["cmd"] == "none":
            return {
                "success": True,
                "command": None,
                "show": response["show"],
                "message": response["response"],
            }

        # 4. Executa o comando através do Router
        result = self.router.route(response)

        # 5. Retorna o resultado final
        return result

