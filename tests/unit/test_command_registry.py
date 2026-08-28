

from typing import Any

import pytest

from sivraj.core.registry import CommandRegistry


def example_command(data: dict[str, Any]) -> dict[str, Any]:
    return {
        "success": True,
        "command": "example",
        "data": data,
    }


def another_command(data: dict[str, Any]) -> dict[str, Any]:
    return {
        "success": True,
        "command": "another",
    }


class TestCommandRegistry:

    def setup_method(self):
        self.registry = CommandRegistry()

    def test_register_command(self):
        self.registry.register("example", example_command)

        assert self.registry.get("example") is example_command

    def test_get_unknown_command_returns_none(self):
        assert self.registry.get("unknown") is None

    def test_exists_registered_command(self):
        self.registry.register("example", example_command)

        assert self.registry.exists("example") is True

    def test_exists_unknown_command(self):
        assert self.registry.exists("unknown") is False

    def test_register_multiple_commands(self):
        self.registry.register("example", example_command)
        self.registry.register("another", another_command)

        assert self.registry.get("example") is example_command
        assert self.registry.get("another") is another_command

    def test_list_commands(self):
        self.registry.register("example", example_command)
        self.registry.register("another", another_command)

        assert self.registry.list_commands() == [
            "example",
            "another",
        ]

    def test_unregister_command(self):
        self.registry.register("example", example_command)

        self.registry.unregister("example")

        assert self.registry.get("example") is None
        assert self.registry.exists("example") is False

    def test_unregister_unknown_command_does_not_fail(self):
        self.registry.unregister("unknown")

        assert self.registry.list_commands() == []

    def test_clear_registry(self):
        self.registry.register("example", example_command)
        self.registry.register("another", another_command)

        self.registry.clear()

        assert self.registry.list_commands() == []

    def test_empty_name_is_rejected(self):
        with pytest.raises(ValueError, match="Command name cannot be empty"):
            self.registry.register("", example_command)

    def test_duplicate_command_is_rejected(self):
        self.registry.register("example", example_command)

        with pytest.raises(
            ValueError,
            match="Command already registered: example",
        ):
            self.registry.register("example", another_command)

    def test_registered_callable_can_be_executed(self):
        self.registry.register("example", example_command)

        command = self.registry.get("example")

        result = command({
            "cmd": "example",
            "response": "Testing.",
            "show": None,
        })

        assert result["success"] is True
        assert result["command"] == "example"

