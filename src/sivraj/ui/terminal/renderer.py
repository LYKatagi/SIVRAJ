



"""Main terminal renderer for SIVRAJ."""

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
    """Represent terminal input."""

    prompt: str | None = None
    voice: bool = False


class Renderer:
    """Manage the SIVRAJ terminal interface."""

    def __init__(
        self,
        rich: bool = True,
        console: Console | None = None,
    ) -> None:
        self.rich_enabled = rich
        self.console = console or Console()
        self.VOICE_KEY = "\x3c"
        self.text_renderer = TextRenderer()
        self.rich_renderer = RichRenderer(self.console)

    def start(self) -> None:
        """Display the SIVRAJ interface."""
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

        self.console.print(
            "Digite 'exit' para sair."
        )
        self.console.print(
            "[dim]Ctrl+Space para falar.[/dim]\n"
        )

   

    


    def input(self) -> InputResult:
        """Read text input or activate voice input with F2."""
        if not self.rich_enabled:
            return InputResult(
                prompt=input("Você\n> ").strip()
            )

        self.console.print("[bold]Você[/bold]")
        self.console.print(
            "[dim]F2 para falar[/dim]"
        )

        buffer: list[str] = []

        self.console.print(
            "[bold green]>[/bold green] ",
            end="",
        )

        while True:
            key = msvcrt.getwch()

            # Special/function key.
            if key == "\x00" or key == "\xe0":
                special_key = msvcrt.getwch()

                # F2
                if special_key == self.VOICE_KEY:
                    self.console.print()

                    return InputResult(
                        prompt=None,
                        voice=True,
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



    def thinking(self) -> None:
        """Display the thinking state."""
        if self.rich_enabled:
            self.console.print(
                "[dim]Thinking...[/dim]"
            )
        else:
            print("Thinking...")

    def processing(self) -> None:
        """Display the processing state."""
        if self.rich_enabled:
            self.console.print(
                "[dim]Processing...[/dim]"
            )
        else:
            print("Processing...")

    def listening(self) -> None:
        """Display the voice listening state."""
        if self.rich_enabled:
            self.console.print(
                "[bold magenta]🎙 Listening...[/bold magenta]"
            )
        else:
            print("Listening...")

    def render(self, result: Any) -> None:
        """Render a SIVRAJ response."""
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

    def render_error(self, error: Exception) -> None:
        """Render an application error."""
        if self.rich_enabled:
            self.console.print(
                Panel(
                    f"[bold red]{error}[/bold red]",
                    title="SIVRAJ",
                    border_style="red",
                )
            )
        else:
            print(f"SIVRAJ: Erro: {error}")

    def render_goodbye(self) -> None:
        """Render the exit message."""
        if self.rich_enabled:
            self.console.print(
                "\n[dim]Até mais![/dim]"
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

