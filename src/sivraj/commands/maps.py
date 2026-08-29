from typing import Any

from sivraj.commands.base import Command


class MapsCommand(Command):
    """Comando responsável por solicitações relacionadas a mapas."""

    name = "maps"

    def execute(self, **kwargs: Any) -> dict[str, Any]:
        """Executa o comando de mapas."""

        return {
            "success": True,
            "command": self.name,
            "show": "location",
            "message": "Solicitação de localização recebida.",
        }
