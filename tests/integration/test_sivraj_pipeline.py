
from unittest.mock import patch

from sivraj.ai.ollama import OllamaClient
from sivraj.core.registry import CommandRegistry
from sivraj.core.router import CommandRouter


def test_complete_sivraj_pipeline():
    executed = {}

    def maps_command(data):
        executed.update(data)

        return {
            "success": True,
            "action": "maps",
        }

    registry = CommandRegistry()
    registry.register("maps", maps_command)

    router = CommandRouter(registry)

    ollama_response = {
        "cmd": "maps",
        "response": "Aqui está sua localização.",
        "show": "location",
    }

    with patch.object(
        OllamaClient,
        "generate",
        return_value=ollama_response,
    ):
        client = OllamaClient()

        command = client.generate("Mostre minha localização")

        result = router.route(command)

    assert result["success"] is True
    assert result["action"] == "maps"

    assert executed == ollama_response

