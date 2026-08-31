





"""SIVRAJ terminal renderer."""

from __future__ import annotations

from typing import Any

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.rule import Rule
from rich.text import Text

from sivraj.ui.terminal.rich_renderer import RichRenderer
from sivraj.ui.terminal.text_renderer import TextRenderer


class Renderer:
    """Render the SIVRAJ terminal interface."""

    def __init__(
        self,
        rich: bool = True,
        console: Console | None = None,
    ) -> None:
        self.rich_enabled = rich
        self.console = console or Console()

        self.text_renderer = TextRenderer()
        self.rich_renderer = RichRenderer(self.console)

    def start(self) -> None:
        """Display the application header."""
        if not self.rich_enabled:
            print("SIVRAJ")
            print("AI Personal Assistant")
            print("Digite 'exit' para sair.\n")
            return

        self.console.print()

        self.console.print(
            Panel(
                Text.assemble(
                    ("SIVRAJ", "bold cyan"),
                    "\n",
                    ("AI Personal Assistant", "dim"),
                ),
                border_style="cyan",
                padding=(1, 2),
            )
        )

        self.console.print(
            "[dim]Digite 'exit' para sair.[/dim]"
        )

        self.console.print(
            Rule(style="dim")
        )

    def input(self) -> str:
        """Read user input."""
        if not self.rich_enabled:
            return input("Você\n> ").strip()

        self.console.print(
            "\n[bold green]Você[/bold green]"
        )

        return self.console.input(
            "[green]>[/green] "
        ).strip()

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

    def render(self, result: Any) -> None:
        """Render a SIVRAJ result."""
        if result is None:
            return

        if not self.rich_enabled:
            output = self.text_renderer.render(result)

            if output:
                print(f"\nSIVRAJ\n{output}")

            return

        response = self._get_response(result)

        if response is None:
            return

        self.console.print()

        self.console.print(
            Panel(
                Markdown(str(response)),
                title="[bold cyan]SIVRAJ[/bold cyan]",
                title_align="left",
                border_style="cyan",
                padding=(1, 2),
            )
        )

        self.console.print()

    def render_error(self, error: Exception) -> None:
        """Render an application error."""
        if self.rich_enabled:
            self.console.print(
                Panel(
                    str(error),
                    title="[bold red]SIVRAJ • Error[/bold red]",
                    title_align="left",
                    border_style="red",
                    padding=(1, 2),
                )
            )
        else:
            print(f"SIVRAJ: Erro: {error}")

    def render_goodbye(self) -> None:
        """Render the exit message."""
        if self.rich_enabled:
            self.console.print(
                "\n[dim]SIVRAJ encerrado. Até mais![/dim]\n"
            )
        else:
            print("SIVRAJ: Até mais!")

    @staticmethod
    def _get_response(result: Any) -> str | None:
        """Extract the response from a command result."""
        if isinstance(result, dict):
            response = result.get("response")

            if response is not None:
                return str(response)

            return None

        return str(result)

