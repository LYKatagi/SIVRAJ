
from collections.abc import Callable
from typing import Any


Command = Callable[..., Any]


class CommandRegistry:
    """Registry responsável por armazenar os comandos disponíveis do SIVRAJ."""

    def __init__(self) -> None:
        self._commands: dict[str, Command] = {}

    def register(self, name: str, command: Command) -> None:
        """Registra um comando usando um nome único."""
        if not name:
            raise ValueError("Command name cannot be empty.")

        if name in self._commands:
            raise ValueError(f"Command already registered: {name}")

        self._commands[name] = command
        
    def get(self, name: str) -> Command | None:
        """Retorna um comando registrado ou None caso não exista."""
        return self._commands.get(name)

    def exists(self, name: str) -> bool:
        """Verifica se um comando está registrado."""
        return name in self._commands

    def unregister(self, name: str) -> None:
        """Remove um comando registrado."""
        self._commands.pop(name, None)

    def list_commands(self) -> list[str]:
        """Retorna os nomes dos comandos registrados."""
        return list(self._commands.keys())

    def clear(self) -> None:
        """Remove todos os comandos registrados."""
        self._commands.clear()

