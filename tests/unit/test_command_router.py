

from unittest.mock import Mock

import pytest

from sivraj.core.registry import CommandRegistry
from sivraj.core.router import CommandRouter


class TestCommandRouter:

    def create_router(self):
        registry = CommandRegistry()
        router = CommandRouter(registry)
        return registry, router

    def test_route_registered_command(self):
        registry, router = self.create_router()

        command = Mock()
        command.execute.return_value = {
            "success": True,
            "command": "example",
        }

        registry.register("example", command)

        data = {
            "cmd": "example",
            "response": "Testing.",
            "show": None,
        }

        result = router.route(data)

        assert result == {
            "success": True,
            "command": "example",
        }

        command.execute.assert_called_once_with(data)

    def test_route_unknown_command(self):
        _, router = self.create_router()

        data = {
            "cmd": "unknown",
            "response": "Testing.",
            "show": None,
        }

        with pytest.raises(
            ValueError,
            match="Unknown command: unknown",
        ):
            router.route(data)

    def test_route_requires_command_name(self):
        _, router = self.create_router()

        data = {
            "response": "Testing.",
            "show": None,
        }

        with pytest.raises(
            ValueError,
            match="Command data must contain 'cmd'",
        ):
            router.route(data)

    def test_command_receives_complete_data(self):
        registry, router = self.create_router()

        command = Mock()
        command.execute.return_value = None

        registry.register("capture", command)

        data = {
            "cmd": "capture",
            "response": "Hello.",
            "show": None,
        }

        router.route(data)

        command.execute.assert_called_once_with(data)

    def test_command_return_value_is_preserved(self):
        registry, router = self.create_router()

        expected_result = {
            "success": True,
            "command": "return",
            "message": "SIVRAJ executed successfully",
        }

        command = Mock()
        command.execute.return_value = expected_result

        registry.register("return", command)

        result = router.route({
            "cmd": "return",
            "response": "Testing.",
            "show": None,
        })

        assert result is expected_result
        command.execute.assert_called_once()

    def test_command_is_executed_exactly_once(self):
        registry, router = self.create_router()

        command = Mock()
        command.execute.return_value = {"success": True}

        registry.register("test", command)

        router.route({
            "cmd": "test",
            "response": "Testing.",
            "show": None,
        })

        command.execute.assert_called_once()

