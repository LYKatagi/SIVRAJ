
"""Rich renderer for the SIVRAJ terminal UI."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from rich.console import Console, RenderableType
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table


class RichRenderer:
    """Render SIVRAJ responses using Rich."""

    def __init__(self, console: Console | None = None) -> None:
        """Initialize the renderer.

        Args:
            console: Optional Rich console instance.
        """
        self.console = console or Console()

    def render(self, result: Any) -> None:
        """Render a SIVRAJ result.

        Args:
            result: Result returned by the SIVRAJ pipeline.
        """
        renderable = self.build(result)

        if renderable is not None:
            self.console.print(renderable)

    def build(self, result: Any) -> RenderableType | None:
        """Build a Rich renderable from a SIVRAJ result.

        Supported render types:

        - text
        - markdown
        - panel
        - table

        Args:
            result: Result returned by the SIVRAJ pipeline.

        Returns:
            A Rich renderable or None.
        """
        if result is None:
            return None

        if isinstance(result, str):
            return result

        if not isinstance(result, dict):
            return str(result)

        render = result.get("render")

        if render is None:
            return self._render_response(result)

        if isinstance(render, str):
            render_type = render
            render_data = result.get("data")
        elif isinstance(render, dict):
            render_type = render.get("type", "text")
            render_data = render.get("data")
        else:
            return self._render_response(result)

        handlers = {
            "text": self._text,
            "markdown": self._markdown,
            "panel": self._panel,
            "table": self._table,
        }

        handler = handlers.get(render_type)

        if handler is None:
            return self._render_response(result)

        return handler(result, render_data)

    def _render_response(self, result: dict[str, Any]) -> str | None:
        """Render the standard response field."""
        response = result.get("response")

        if response is None:
            return None

        return str(response)

    def _text(
        self,
        result: dict[str, Any],
        data: Any,
    ) -> str:
        """Render plain text."""
        if data is not None:
            return str(data)

        return str(result.get("response", ""))

    def _markdown(
        self,
        result: dict[str, Any],
        data: Any,
    ) -> Markdown:
        """Render Markdown."""
        content = data if data is not None else result.get("response", "")
        return Markdown(str(content))

    def _panel(
        self,
        result: dict[str, Any],
        data: Any,
    ) -> Panel:
        """Render a Rich panel."""
        content = data if data is not None else result.get("response", "")
        title = result.get("title")

        return Panel(
            str(content),
            title=str(title) if title is not None else None,
        )

    def _table(
        self,
        result: dict[str, Any],
        data: Any,
    ) -> Table | None:
        """Render a Rich table.

        Expected data format:

        {
            "columns": ["Name", "Value"],
            "rows": [
                ["CPU", "23%"],
                ["RAM", "64%"],
            ],
        }
        """
        table = Table(title=result.get("title"))

        if not isinstance(data, dict):
            return table

        columns = data.get("columns", [])
        rows = data.get("rows", [])

        if not isinstance(columns, Sequence) or isinstance(columns, str):
            return table

        for column in columns:
            table.add_column(str(column))

        if isinstance(rows, Sequence) and not isinstance(rows, str):
            for row in rows:
                if isinstance(row, Sequence) and not isinstance(row, str):
                    table.add_row(*(str(value) for value in row))


