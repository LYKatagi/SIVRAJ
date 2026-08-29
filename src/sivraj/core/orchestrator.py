
from typing import Any

from sivraj.ai.schema import Schema
from sivraj.core.router import CommandRouter
from sivraj.log.logger import get_logger


class Orchestrator:
    """Coordena o pipeline principal do SIVRAJ."""

    def __init__(
        self,
        ollama: Any,
        router: CommandRouter,
        recovery: Any,
    ) -> None:
        self.ollama = ollama
        self.router = router
        self.recovery = recovery

    def process(self, prompt: str) -> dict[str, Any]:
        """Processa uma entrada através do pipeline completo."""
        logger = get_logger(__name__)
        logger.info("Processing input: %r", prompt)

        # Ollama
        logger.info("Calling Ollama")

        data = self.recovery.run(
            lambda: self.ollama.generate(prompt),
            name="ollama",
        )

        # Schema
        logger.info("Validating Ollama response")

        if not isinstance(data, dict):
            logger.error(
                "Ollama returned non-dict data: %r",
                data,
            )
            raise ValueError(
                "Ollama returned an invalid SIVRAJ response"
            )

        if not Schema.validate_data(data):
            logger.error(
                "Invalid SIVRAJ response from Ollama: %r",
                data,
            )
            raise ValueError(
                "Ollama returned an invalid SIVRAJ response"
            )

        command_name = data["cmd"]

        # Conversação normal não passa pelo Router.
        if command_name == "none":
            logger.info("No command required")

            return {
                "success": True,
                "command": "none",
                "response": data["response"],
                "show": data["show"],
            }

        # Command
        logger.info(
            "Routing command: %s",
            command_name,
        )

        result = self.router.route(data)

        logger.info(
            "Command %s executed successfully",
            command_name,
        )

        return result

