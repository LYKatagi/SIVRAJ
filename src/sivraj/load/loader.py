from __future__ import annotations

import importlib
import inspect
import pkgutil

from sivraj.commands.base import Command
from sivraj.core.registry import CommandRegistry


class CommandLoader:
    """Automatically discovers and registers SIVRAJ commands."""

    def __init__(self, registry: CommandRegistry) -> None:
        self.registry = registry

    def load(self) -> int:
        """Discover and register all available commands.

        Returns:
            Number of commands successfully loaded.
        """

        loaded = 0

        import sivraj.commands

        for module_info in pkgutil.iter_modules(sivraj.commands.__path__):
            module_name = module_info.name

            # Don't try to load the base command class itself.
            if module_name.startswith("_") or module_name == "base":
                continue

            module = importlib.import_module(f"sivraj.commands.{module_name}")

            for _, obj in inspect.getmembers(
                module,
                inspect.isclass,
            ):
                if (
                    issubclass(obj, Command)
                    and obj is not Command
                    and obj.__module__ == module.__name__
                ):
                    command = obj()

                    self.registry.register(
                        command.name,
                        command,
                    )

                    loaded += 1

        return loaded
