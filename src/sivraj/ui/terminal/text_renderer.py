

"""Plain-text renderer for the SIVRAJ terminal UI."""

from __future__ import annotations

from typing import Any


class TextRenderer:
    """Render SIVRAJ responses as plain terminal text."""

    def render(self, result: Any) -> str:
        """Render a SIVRAJ result into a plain string.

        Args:
            result: Result returned by the SIVRAJ pipeline.

        Returns:
            A string suitable for printing in the terminal.
        """
        if result is None:
            return ""

        if isinstance(result, str):
            return result

        if isinstance(result, dict):
            response = result.get("response")

            if response is not None:
                return str(response)

            return str(result)

        return str(result)




