
import pytest

from sivraj.core.registry import CommandRegistry
from sivraj.core.router import CommandRouter


def example_command(data):
    return {
        "executed": True,
        "data": data,
    }


class TestCommandRouter:
    def test_route_registered_command(self):
        registry = CommandRegistry()
        registry.register("example", example_command)

        router = CommandRouter(registry)

        data = {
            "cmd": "example",
            "response": "Testing.",
            "show": None,
        }

        result = router.route(data)

        assert result["executed"] is True
        assert result["data"] == data

    def test_route_unknown_command(self):
        registry = CommandRegistry()
        router = CommandRouter(registry)

        data = {
            "cmd": "unknown",
            "response": "Testing.",
            "show": None,
        }

        with pytest.raises(ValueError, match="Unknown command"):
            router.route(data)

    def test_route_without_cmd(self):
        registry = CommandRegistry()
        router = CommandRouter(registry)

        data = {
            "response": "Testing.",
            "show": None,
        }

        with pytest.raises(ValueError, match="must contain 'cmd'"):
            router.route(data)

    def test_command_receives_complete_data(self):
        received_data = None

        def capture_command(data):
            nonlocal received_data
            received_data = data

        registry = CommandRegistry()
        registry.register("capture", capture_command)

        router = CommandRouter(registry)

        data = {
            "cmd": "capture",
            "response": "Hello.",
            "show": None,
        }

        router.route(data)

        assert received_data == data

    def test_command_return_value_is_preserved(self):
        def return_command(data):
            return "SIVRAJ executed successfully"

        registry = CommandRegistry()
        registry.register("return", return_command)

        router = CommandRouter(registry)

        result = router.route({
            "cmd": "return",
            "response": "Testing.",
            "show": None,
        })

        assert result == "SIVRAJ executed successfully"

