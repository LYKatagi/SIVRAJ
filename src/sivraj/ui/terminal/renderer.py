


"""Main terminal renderer for SIVRAJ."""

from __future__ import annotations

from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule

from sivraj.ui.terminal.rich_renderer import RichRenderer
from sivraj.ui.terminal.text_renderer import TextRenderer


class Renderer:
    """Manage the SIVRAJ terminal interface."""

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
            "Digite 'exit' para sair.\n"
        )

    def input(self) -> str:
        """Read user input."""
        if not self.rich_enabled:
            return input("Você\n> ").strip()

        self.console.print("[bold]Você[/bold]")

        return self.console.input(
            "[bold green]>[/bold green] "
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

