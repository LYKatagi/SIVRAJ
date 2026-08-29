from typing import Any

from sivraj.core.registry import CommandRegistry


class CommandRouter:
    """Responsável por encaminhar respostas da IA para os comandos."""

    def __init__(self, registry: CommandRegistry) -> None:
        self.registry = registry

    def route(self, command_data: dict[str, Any]) -> Any:
        """Executa o comando descrito em command_data."""

        command_name = command_data.get("cmd")

        if not command_name:
            raise ValueError("Command data must contain 'cmd'.")

        command = self.registry.get(command_name)

        if command is None:
            raise ValueError(f"Unknown command: {command_name}")

        args = command_data.get("args", {})

        if not isinstance(args, dict):
            raise ValueError("Command 'args' must be an object.")

        return command.execute(**args)
