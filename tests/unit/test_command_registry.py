
import pytest

from sivraj.core.registry import CommandRegistry


def example_command():
    return "executed"


class TestCommandRegistry:
    def test_register_command(self):
        registry = CommandRegistry()

        registry.register("example", example_command)

        assert registry.exists("example") is True

    def test_get_command(self):
        registry = CommandRegistry()

        registry.register("example", example_command)

        assert registry.get("example") is example_command

    def test_get_unknown_command(self):
        registry = CommandRegistry()

        assert registry.get("unknown") is None

    def test_duplicate_command_is_rejected(self):
        registry = CommandRegistry()

        registry.register("example", example_command)

        with pytest.raises(ValueError):
            registry.register("example", example_command)

    def test_empty_command_name_is_rejected(self):
        registry = CommandRegistry()

        with pytest.raises(ValueError):
            registry.register("", example_command)

    def test_list_commands(self):
        registry = CommandRegistry()

        registry.register("maps", example_command)
        registry.register("open_app", example_command)

        assert registry.list_commands() == ["maps", "open_app"]

    def test_unregister_command(self):
        registry = CommandRegistry()

        registry.register("example", example_command)
        registry.unregister("example")

        assert registry.exists("example") is False

    def test_clear_registry(self):
        registry = CommandRegistry()

        registry.register("maps", example_command)
        registry.register("open_app", example_command)

        registry.clear()

        assert registry.list_commands() == []

