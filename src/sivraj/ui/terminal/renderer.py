




"""Supreme terminal renderer for SIVRAJ."""

from __future__ import annotations

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
    """Represent a terminal input event."""

    prompt: str | None = None
    voice: bool = False


class Renderer:
    """Manage the SIVRAJ terminal interface."""

    VOICE_KEY = "0"
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
            print("Digite 'exit' para sair.")
            print("F2 para falar.\n")
            return

        self.console.print(
            Panel(
                "[bold cyan]SIVRAJ[/bold cyan]\n"
                "[dim]AI Personal Assistant[/dim]",
                border_style="cyan",
                expand=True,
            )
        )

        self.console.print(
            "Digite 'exit' para sair."
        )

        self.console.print(
            "[dim]F2 para falar.[/dim]\n"
        )

    # ------------------------------------------------------------------
    # Input
    # ------------------------------------------------------------------

    def input(self) -> InputResult:
        """Read terminal input or activate voice mode."""

        if not self.rich_enabled:
            return InputResult(
                prompt=input("Você\n> ").strip()
            )

        self.console.print("[bold]Você[/bold]")
        self.console.print(
            "[dim]F2 para falar[/dim]"
        )

        self.console.print(
            "[bold green]>[/bold green] ",
            end="",
        )

        buffer: list[str] = []

        while True:
            key = msvcrt.getwch()

            # Extended/function key.
            if key in {"\x00", "\xe0"}:
                special_key = msvcrt.getwch()

                # F2
                if special_key == self.VOICE_KEY:
                    self.console.print()

                    return InputResult(
                        voice=True
                    )

                continue

            # Enter
            if key == "\r":
                self.console.print()

                return InputResult(
                    prompt="".join(buffer).strip()
                )

            # Backspace
            if key == "\b":
                if buffer:
                    buffer.pop()

                    self.console.print(
                        "\b \b",
                        end="",
                    )

                continue

            # Escape
            if key == "\x1b":
                self.console.print()

                return InputResult()

            # Printable character
            if key.isprintable():
                buffer.append(key)

                self.console.print(
                    key,
                    end="",
                )

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    def thinking(self) -> None:
        """Display the thinking state."""

        self._thinking = True

        if self.rich_enabled:
            self.console.print(
                "[dim]Thinking...[/dim]"
            )
        else:
            print("Thinking...")

    def processing(self) -> None:
        """Display the processing state."""

        self._thinking = False

        if self.rich_enabled:
            self.console.print(
                "[dim]Processing...[/dim]"
            )
        else:
            print("Processing...")

    def listening(self) -> None:
        """Display the voice recording state."""

        self._listening = True

        if self.rich_enabled:
            self.console.print(
                "[bold magenta]🎙 Gravando...[/bold magenta]"
            )
            self.console.print(
                "[dim]F2 para parar • ESC para cancelar[/dim]"
            )
        else:
            print("🎙 Gravando...")
            print("F2 para parar • ESC para cancelar")

    def ready(self) -> None:
        """Return the renderer to the idle state."""

        self._thinking = False
        self._listening = False

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def render(self, result: Any) -> None:
        """Render a SIVRAJ response."""

        self.ready()

        if result is None:
            return

        if not self.rich_enabled:
            output = self.text_renderer.render(result)

            if output:
                print(f"SIVRAJ\n{output}")

            return

        self.console.print(
            "\n[bold cyan]SIVRAJ[/bold cyan]"
        )

        self.rich_renderer.render(result)

        self.console.print()

    def render_error(
        self,
        error: Exception,
    ) -> None:
        """Render an application error."""

        self.ready()

        if self.rich_enabled:
            self.console.print(
                Panel(
                    f"[bold red]{error}[/bold red]",
                    title="SIVRAJ — Error",
                    border_style="red",
                )
            )
        else:
            print(
                f"SIVRAJ: Erro: {error}"
            )

    def render_goodbye(self) -> None:
        """Render the exit message."""

        self.ready()

        if self.rich_enabled:
            self.console.print(
                "\n[bold cyan]SIVRAJ[/bold cyan]"
            )
            self.console.print(
                "[dim]Até mais![/dim]"
            )
        else:
            print("SIVRAJ: Até mais!")

    def separator(self) -> None:
        """Render a separator."""

        if self.rich_enabled:
            self.console.print(
                Rule(style="dim")
            )
        else:
            print("-" * 60)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def render_message(
        self,
        message: str,
        *,
        title: str | None = None,
    ) -> None:
        """Render a human-readable message."""

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

    def is_exit_command(
        self,
        prompt: str | None,
    ) -> bool:
        """Check whether a prompt requests shutdown."""

        if not prompt:
            return False

        return (
            prompt.strip().casefold()
            in self.EXIT_COMMANDS
        )

    @property
    def active(self) -> bool:
        """Whether the renderer has started."""

        return self._started

    @property
    def busy(self) -> bool:
        """Whether the renderer is busy."""

        return (
            self._thinking
            or self._listening
        )

