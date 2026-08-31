





"""SIVRAJ terminal renderer."""

from __future__ import annotations

from typing import Any

from rich.align import Align
from rich.console import Console, Group
from rich.markdown import Markdown
from rich.panel import Panel
from rich.rule import Rule
from rich.status import Status
from rich.text import Text

from sivraj.ui.terminal.dolphin import dolphin
from sivraj.ui.terminal.rich_renderer import RichRenderer
from sivraj.ui.terminal.text_renderer import TextRenderer


class Renderer:
    """Render the SIVRAJ terminal interface."""

    TITLE = "SIVRAJ"
    SUBTITLE = "AI Personal Assistant"

    def __init__(
        self,
        rich: bool = True,
        console: Console | None = None,
    ) -> None:
        self.rich_enabled = rich
        self.console = console or Console()

        self.text_renderer = TextRenderer()
        self.rich_renderer = RichRenderer(self.console)

        self._status: Status | None = None

    # ------------------------------------------------------------------
    # Startup
    # ------------------------------------------------------------------

    def start(self) -> None:
        """Display the SIVRAJ startup screen."""
        if not self.rich_enabled:
            print(self.TITLE)
            print(self.SUBTITLE)
            print("Digite 'exit' para sair.\n")
            return

        self.console.clear()

        header = Text()
        header.append(self.TITLE, style="bold cyan")
        header.append("\n")
        header.append(self.SUBTITLE, style="dim")

        mascot = Text(
            dolphin,
            style="cyan",
        )

        startup = Group(
            Align.center(header),
            Text(""),
            Align.center(mascot),
            Text(""),
            Align.center(
                Text(
                    "Initializing SIVRAJ...",
                    style="dim",
                )
            ),
        )

        self.console.print(
            Panel(
                startup,
                border_style="cyan",
                padding=(1, 3),
            )
        )

        self.console.print()
        self.console.print(
            Text(
                "Digite 'exit' para sair.",
                style="dim",
            )
        )
        self.console.print(Rule(style="dim"))

    # ------------------------------------------------------------------
    # Input
    # ------------------------------------------------------------------

    def input(self) -> str:
        """Read user input."""
        if not self.rich_enabled:
            return input("Você\n> ").strip()

        self.console.print()

        self.console.print(
            Text(
                "Você",
                style="bold green",
            )
        )

        return self.console.input(
            "[bold green]>[/bold green] "
        ).strip()

    # ------------------------------------------------------------------
    # Processing states
    # ------------------------------------------------------------------

    def thinking(self) -> None:
        """Display the thinking state."""
        if not self.rich_enabled:
            print("Thinking...")
            return

        self._stop_status()

        self._status = Status(
            "Thinking...",
            spinner="dots",
            spinner_style="cyan",
        )

        self.console.print(self._status)

    def processing(self) -> None:
        """Display the processing state."""
        if not self.rich_enabled:
            print("Processing...")
            return

        self._stop_status()

        self._status = Status(
            "Processing...",
            spinner="dots",
            spinner_style="cyan",
        )

        self.console.print(self._status)

    def _stop_status(self) -> None:
        """Stop the active status indicator."""
        if self._status is not None:
            self._status.stop()
            self._status = None

    # ------------------------------------------------------------------
    # Output
    # ------------------------------------------------------------------

    def render(self, result: Any) -> None:
        """Render a SIVRAJ result."""
        self._stop_status()

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

        content = Markdown(str(response))

        self.console.print(
            Panel(
                content,
                title="[bold cyan]SIVRAJ[/bold cyan]",
                title_align="left",
                border_style="cyan",
                padding=(1, 2),
            )
        )

        self.console.print()

    # ------------------------------------------------------------------
    # Errors
    # ------------------------------------------------------------------

    def render_error(self, error: Exception) -> None:
        """Render an application error."""
        self._stop_status()

        if not self.rich_enabled:
            print(f"SIVRAJ: Erro: {error}")
            return

        error_text = Text(str(error))

        self.console.print()

        self.console.print(
            Panel(
                error_text,
                title="[bold red]Error[/bold red]",
                title_align="left",
                border_style="red",
                padding=(1, 2),
            )
        )

        self.console.print()

    # ------------------------------------------------------------------
    # Shutdown
    # ------------------------------------------------------------------

    def render_goodbye(self) -> None:
        """Render the exit message."""
        self._stop_status()

        if not self.rich_enabled:
            print("SIVRAJ: Até mais!")
            return

        self.console.print(
            Rule(style="dim")
        )

        self.console.print(
            Align.center(
                Text(
                    "SIVRAJ encerrado. Até mais!",
                    style="dim",
                )
            )
        )

        self.console.print()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _get_response(result: Any) -> str | None:
        """Extract the response from a SIVRAJ result."""
        if isinstance(result, dict):
            response = result.get("response")

            if response is not None:
                return str(response)

            return None

        return str(result)

