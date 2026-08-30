
"""Main renderer for the SIVRAJ terminal UI."""

from __future__ import annotations

from typing import Any

from sivraj.ui.terminal.rich_renderer import RichRenderer
from sivraj.ui.terminal.text_renderer import TextRenderer


class Renderer:
    """Dispatch SIVRAJ results to the appropriate renderer."""

    def __init__(self, rich: bool = True) -> None:
        """Initialize the renderer.

        Args:
            rich: Whether to use Rich rendering.
        """
        self.rich_enabled = rich

        self.text_renderer = TextRenderer()
        self.rich_renderer = RichRenderer()

    def render(self, result: Any) -> None:
        """Render a SIVRAJ result.

        Args:
            result: Result returned by the SIVRAJ pipeline.
        """
        if self.rich_enabled:
            self.rich_renderer.render(result)
        else:
            output = self.text_renderer.render(result)

            if output:
                print(output)

    def render_text(self, result: Any) -> str:
        """Always render a result as plain text.

        Args:
            result: Result returned by the SIVRAJ pipeline.

        Returns:
            Plain-text representation of the result.
        """
        return self.text_renderer.render(result)

    def render_rich(self, result: Any) -> None:
        """Always render a result using Rich.

        Args:
            result: Result returned by the SIVRAJ pipeline.
        """
        self.rich_renderer.render(result)



