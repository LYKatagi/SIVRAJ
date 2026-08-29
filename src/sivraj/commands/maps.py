from typing import Any
from sivraj.commands.base import Command


class MapsCommand(Command):
    """Comando responsável por solicitações relacionadas a mapas."""

    name = "maps"

    def execute(self, command_data: dict[str, Any]) -> dict[str, Any]:
        """Executa o comando de mapas."""

        return {
            "success": True,
            "command": "maps",
            "show": command_data.get("show"),
            "message": "Solicitação de localização recebida.",
        }
