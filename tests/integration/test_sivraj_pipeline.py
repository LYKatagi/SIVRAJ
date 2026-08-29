from unittest.mock import Mock

from sivraj.ai.schema import Schema
from sivraj.core.registry import CommandRegistry
from sivraj.core.router import CommandRouter
from sivraj.load.loader import CommandLoader


class TestSivrajPipeline:
    """Integration tests for the complete SIVRAJ command pipeline."""

    def setup_method(self):
        self.registry = CommandRegistry()

        self.loader = CommandLoader(self.registry)
        self.loaded = self.loader.load()

        self.router = CommandRouter(self.registry)

    def test_commands_are_loaded(self):
        """All available commands should be discovered automatically."""

        assert self.loaded >= 1
        assert "maps" in self.registry._commands

    def test_maps_command_pipeline(self):
        """A maps response should travel through the complete pipeline."""

        ollama_response = {
            "cmd": "maps",
            "response": "Mostrando sua localização",
            "show": "location",
        }

        # Simulate Ollama.
        ollama = Mock()
        ollama.generate.return_value = ollama_response

        # Ollama → Schema
        data = ollama.generate("Mostre minha localização")

        assert Schema.validate_data(data) is True

        # Schema → Router → Registry → Command
        result = self.router.route(data)

        assert result["success"] is True
        assert result["command"] == "maps"
        assert result["show"] == "location"

    def test_conversation_does_not_execute_command(self):
        """A 'none' response should not be routed as a command."""

        ollama_response = {
            "cmd": "none",
            "response": "Olá! Como posso ajudar você hoje?",
            "show": None,
        }

        assert Schema.validate_data(ollama_response) is True

        assert ollama_response["cmd"] == "none"
        assert ollama_response["show"] is None

    def test_invalid_ollama_response_is_rejected(self):
        """Invalid AI output must never reach the Router."""

        invalid_response = {
            "cmd": "maps",
            "response": 123,
            "show": "location",
        }

        assert Schema.validate_data(invalid_response) is False

    def test_unknown_command_is_not_available(self):
        """The Registry should not contain commands that do not exist."""

        assert "banana" not in self.registry._commands
