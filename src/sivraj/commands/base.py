from abc import ABC, abstractmethod
from typing import Any


class Command(ABC):
    """Base class for every SIVRAJ command."""

    name: str

    @abstractmethod
    def execute(self, **kwargs: Any) -> dict[str, Any]:
        """Execute the command and return its result."""
        raise NotImplementedError
