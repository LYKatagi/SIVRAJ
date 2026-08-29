from __future__ import annotations

from typing import Any

from sivraj.ai.ollama import OllamaClient
from sivraj.ai.schema import Schema
from sivraj.core.recovery import RecoveryManager
from sivraj.core.router import CommandRouter
from sivraj.log.logger import get_logger


logger = get_logger(__name__)


class Orchestrator:
    """Coordena o pipeline principal do SIVRAJ."""

    def __init__(
        self,
        ollama: OllamaClient,
        router: CommandRouter,
        recovery: RecoveryManager | None = None,
    ) -> None:
        self.ollama = ollama
        self.router = router
        self.recovery = recovery or RecoveryManager()

    def process(self, prompt: str) -> dict[str, Any]:
        """Processa uma entrada através do pipeline completo."""

        logger.info("Processing input: %r", prompt)

        # Ollama
        logger.info("Calling Ollama")

        data = self.recovery.run(
            lambda: self.ollama.generate(prompt),
            name="ollama",
        )

        # Schema
        logger.info("Validating Ollama response")

        if not Schema.validate_data(data):
            logger.error(
                "Invalid SIVRAJ response from Ollama: %r",
                data,
            )

            raise ValueError("Ollama returned an invalid SIVRAJ response")

        logger.info("Ollama response validated successfully")

        # Conversation
        if data["cmd"] == "none":
            logger.info("Conversation response received")

            return {
                "success": True,
                "executed": False,
                "response": data["response"],
                "show": data["show"],
            }

        # Router → Command
        logger.info(
            "Routing command: %s",
            data["cmd"],
        )

        result = self.recovery.run(
            lambda: self.router.route(data),
            name=f"command:{data['cmd']}",
        )

        logger.info(
            "Command executed successfully: %s",
            data["cmd"],
        )

        return {
            "success": True,
            "executed": True,
            "response": data["response"],
            "result": result,
            "show": data["show"],
        }
