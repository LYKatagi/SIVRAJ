
from typing import Any

from sivraj.core.registry import CommandRegistry


class CommandRouter:
    """Encaminha comandos para os handlers registrados."""

    def __init__(self, registry: CommandRegistry) -> None:
        self.registry = registry

    def route(self, command_data: dict[str, Any]) -> Any:
        """
        Executa o comando descrito em command_data.

        O campo 'cmd' determina qual comando será procurado
        no CommandRegistry.
        """
        command_name = command_data.get("cmd")

        if not command_name:
            raise ValueError("Command data must contain 'cmd'.")

        command = self.registry.get(command_name)

        if command is None:
            raise ValueError(f"Unknown command: {command_name}")

        return command.execute()

