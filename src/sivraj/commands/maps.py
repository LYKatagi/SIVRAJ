
from typing import Any

from sivraj.commands.base import Command


class MapsCommand(Command):
    """Command responsible for map and location requests."""

    name = "maps"

    def execute(self, **kwargs: Any) -> dict[str, Any]:
        """Execute the maps command."""

        return {
            "success": True,
            "command": self.name,
            "show": "location",
            "message": "Solicitação de localização recebida.",
        }

