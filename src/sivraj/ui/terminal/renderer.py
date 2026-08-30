



"""Supreme terminal renderer for SIVRAJ.

The :class:`Renderer` is the public presentation facade used by the
application. It owns terminal input, UI state, status messages and delegates
actual response formatting to the specialised text and Rich renderers.
"""

from __future__ import annotations

import json
import msvcrt
from dataclasses import dataclass
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule

from sivraj.ui.terminal.rich_renderer import RichRenderer
from sivraj.ui.terminal.text_renderer import TextRenderer


@dataclass(slots=True)
class InputResult:
    """Represent one terminal input event."""

    prompt: str | None = None
    voice: bool = False


class Renderer:
    """Manage the complete SIVRAJ terminal interface.

    ``Renderer`` deliberately acts as a facade. The application only needs
    to know about this class; response-specific formatting remains isolated in
    :class:`RichRenderer` and :class:`TextRenderer`.
    """

    VOICE_KEY = "\x3c"  # F2 in the Windows console.
    EXIT_COMMANDS = frozenset({"exit", "quit"})

    def __init__(
        self,
        rich: bool = True,
        console: Console | None = None,
    ) -> None:
        self.rich_enabled = rich
        self.console = console or Console()

        self.text_renderer = TextRenderer()
        self.rich_renderer = RichRenderer(self.console)

        self._started = False
        self._thinking = False
        self._listening = False

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def start(self) -> None:
        """Display the SIVRAJ startup interface."""
        if self._started:
            return

        self._started = True

        if not self.rich_enabled:
            print("SIVRAJ")
            print("AI Personal Assistant")
            print("Digite 'exit' para sair.\n")
            return

        self.console.print(
            Panel(
                "[bold cyan]SIVRAJ[/bold cyan]\n"
                "[dim]AI Personal Assistant[/dim]",
                border_style="cyan",
                expand=True,
            )
        )

        self.console.print("Digite 'exit' para sair.")
        self.console.print("[dim]F2 para falar.[/dim]\n")

    # ------------------------------------------------------------------
    # Input
    # ------------------------------------------------------------------

    def input(self) -> InputResult:
        """Read text input or activate voice input with F2.

        The Rich mode uses ``msvcrt`` so function keys can be handled without
        requiring the user to press Enter. The plain renderer keeps standard
        ``input()`` semantics for compatibility.
        """
        if not self.rich_enabled:
            return InputResult(
                prompt=input("Você\n> ").strip()
            )

        self.console.print("[bold]Você[/bold]")
        self.console.print("[dim]F2 para falar[/dim]")

        self.console.print(
            "[bold green]>[/bold green] ",
            end="",
        )

        buffer: list[str] = []

        while True:
            key = msvcrt.getwch()

            # Function / extended key.
            if key in {"\x00", "\xe0"}:
                special_key = msvcrt.getwch()

                if special_key == self.VOICE_KEY:
                    self.console.print()

                    return InputResult(
                        voice=True
                    )

                continue

            # Enter.
            if key == "\r":
                self.console.print()

                return InputResult(
                    prompt="".join(buffer).strip()
                )

            # Backspace.
            if key == "\b":
                if buffer:
                    buffer.pop()

                    self.console.print(
                        "\b \b",
                        end="",
                    )

                continue

            # Escape cancels the current input.
            if key == "\x1b":
                self.console.print()

                return InputResult()

            # Printable character.
            if key.isprintable():
                buffer.append(key)

                self.console.print(
                    key,
                    end="",
                )

    # ------------------------------------------------------------------
    # Status / activity
    # ------------------------------------------------------------------

    def thinking(self) -> None:
        """Display the AI thinking state."""
        self._thinking = True

        self._status(
            "Thinking...",
            "dim",
        )

    def processing(self) -> None:
        """Display the command-processing state."""
        self._thinking = False

        self._status(
            "Processing...",
            "dim",
        )

    def listening(self) -> None:
        """Display the voice-listening state."""
        self._listening = True

        self._status(
            "🎙 Listening...",
            "bold magenta",
        )

    def ready(self) -> None:
        """Clear transient activity flags."""
        self._thinking = False
        self._listening = False

    def _status(
        self,
        message: str,
        style: str,
    ) -> None:
        """Render a status message."""
        if self.rich_enabled:
            self.console.print(
                f"[{style}]{message}[/{style}]"
            )
        else:
            print(message)

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def render(self, result: Any) -> None:
        """Render any result produced by the SIVRAJ pipeline."""
        self.ready()

        if result is None:
            return

        if self.rich_enabled:
            self.console.print(
                "\n[bold cyan]SIVRAJ[/bold cyan]"
            )

            self.rich_renderer.render(result)

            self.console.print()

            return

        output = self.text_renderer.render(result)

        if output:
            print(
                f"SIVRAJ\n{output}"
            )

    def render_error(
        self,
        error: Exception,
    ) -> None:
        """Render an application error without crashing the UI."""
        self.ready()

        message = (
            str(error)
            or error.__class__.__name__
        )

        if self.rich_enabled:
            self.console.print(
                Panel(
                    f"[bold red]{message}[/bold red]",
                    title="SIVRAJ — Error",
                    border_style="red",
                )
            )
        else:
            print(
                f"SIVRAJ: Erro: {message}"
            )

    def render_goodbye(self) -> None:
        """Render the application exit message."""
        self.ready()

        if self.rich_enabled:
            self.console.print(
                "\n[bold cyan]SIVRAJ[/bold cyan]"
            )

            self.console.print(
                "[dim]Até mais![/dim]"
            )
        else:
            print(
                "SIVRAJ: Até mais!"
            )

    def separator(self) -> None:
        """Render a visual separator."""
        if self.rich_enabled:
            self.console.print(
                Rule(style="dim")
            )
        else:
            print("-" * 60)

    # ------------------------------------------------------------------
    # Utility rendering helpers
    # ------------------------------------------------------------------

    def render_message(
        self,
        message: str,
        *,
        title: str | None = None,
    ) -> None:
        """Render a human-readable UI message."""
        if not message:
            return

        if self.rich_enabled:
            if title:
                self.console.print(
                    Panel(
                        message,
                        title=title,
                    )
                )
            else:
                self.console.print(message)
        else:
            print(message)

    def render_json(
        self,
        data: Any,
    ) -> None:
        """Render structured data as readable JSON for debugging."""
        try:
            serialized = json.dumps(
                data,
                ensure_ascii=False,
                indent=2,
                default=str,
            )
        except (TypeError, ValueError):
            serialized = str(data)

        if self.rich_enabled:
            self.console.print(
                Panel(
                    serialized,
                    title="Debug JSON",
                    border_style="yellow",
                )
            )
        else:
            print(serialized)

    def is_exit_command(
        self,
        prompt: str | None,
    ) -> bool:
        """Return whether a text prompt requests application shutdown."""
        if not prompt:
            return False

        return (
            prompt.strip().casefold()
            in self.EXIT_COMMANDS
        )

    # ------------------------------------------------------------------
    # State
    # ------------------------------------------------------------------

    @property
    def active(self) -> bool:
        """Whether the renderer has been started."""
        return self._started

    @property
    def busy(self) -> bool:
        """Whether the renderer is currently busy."""
        return (
            self._thinking
            or self._listening
        )